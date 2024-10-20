import sys

from PyQt5.QtWidgets import *
from familyClass import Human


class MainWindow(QMainWindow):
    def __init__(self, root):
        super().__init__()

        self.setWindowTitle("My App")
        self.root = root
        button = QPushButton("Start")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self):
        dlg = TreeDialog(person_root=self.root, parent=self)
        dlg.exec()


class TreeDialog(QDialog):
    person_root: Human

    def __init__(self, person_root: Human, parent: QDialog = None) -> None:
        super().__init__(parent)
        self.person_root = person_root
        self.__render()

    def start(self) -> None:
        if self.sender().objectName() == 'self':
            dlg = PersonDialog(self.person_root, self)
            dlg.exec()
        else:
            self.person_root = self.person_root.get_family()[self.sender().objectName()]
            self.__render()

    def __addMember(self, name: str, obj_member: Human, pos_x: int, pos_y: int) -> None:
        but_member = QPushButton(obj_member.get_name())
        but_member.setObjectName(name)
        but_member.clicked.connect(self.start)
        self.layout.addWidget(but_member, pos_x, pos_y)

    def __render(self) -> None:
        self.layout = QGridLayout()

        self.setWindowTitle(self.person_root.get_name())

        QBtn = QDialogButtonBox.Cancel
        columns = 0
        family = self.person_root.get_family()
        for member in family:
            if 'child' in member:
                columns += 1
        columns = max(columns, 3)
        posR = columns // 2

        if 'mother' in family:
            self.__addMember("mother", family["mother"], posR - 1, 0)

        if 'father' in family:
            self.__addMember("father", family["father"], posR + 1, 0)

        self.__addMember("self", self.person_root, posR, 1)

        if 'spouse' in family:
            self.__addMember("spouse", family["spouse"], posR + 1, 1)
        idx = -1
        for member in family:
            if 'child' in member:
                self.__addMember(member, family[member], idx := idx + 1, 2)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox, 3, columns)
        self.setLayout(self.layout)
        self.update()


class PersonDialog(QDialog):
    person: Human

    def __init__(self, person: Human, parent: QDialog = None) -> None:
        super().__init__(parent)

        person.update()
        self.person = person

        self.setWindowTitle(person.get_name())
        self.__render()

    def edit(self):
        dlg = EditPersonDialog(self.person, self)
        if not dlg.exec():
            self.person.update()
            self.__render()
            self.update()

    def __render(self):
        QBtn = QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()
        name_0 = QLabel('Имя:')
        name = QLabel(self.person.get_name())
        data_of_birthday_0 = QLabel('Дата рождения:')
        data_of_birthday = QLabel(self.person.get_data_of_birthday())
        gender_0 = QLabel('Пол:')
        gender = QLabel(self.person.get_gender())
        info_label = dict()

        idx = -1
        label_2 = QLabel('Информация')
        layout.addWidget(label_2, idx := idx + 1, 0)
        layout.addWidget(name, idx := idx + 1, 1)
        layout.addWidget(name_0, idx, 0)
        layout.addWidget(data_of_birthday, idx := idx + 1, 1)
        layout.addWidget(data_of_birthday_0, idx, 0)
        layout.addWidget(gender, idx := idx + 1, 1)
        layout.addWidget(gender_0, idx, 0)
        if self.person.get_dead():
            data_of_death_0 = QLabel('Дата смерти:')
            data_of_death = QLabel(self.person.get_data_of_dead())
            layout.addWidget(data_of_death, idx := idx + 1, 1)
            layout.addWidget(data_of_death_0, idx, 0)
        other_information = self.person.get_info()
        for i in other_information:
            info = QLabel(other_information[i])
            info_0 = QLabel(i)
            info_label[i] = info
            layout.addWidget(info, idx := idx + 1, 1)
            layout.addWidget(info_0, idx, 0)
        idx_family = -1
        label_1 = QLabel('Родственники')
        layout.addWidget(label_1, idx_family := idx_family + 1, 2)
        family = self.person.get_family()
        for i in family:
            label_0 = QPushButton(i)
            label_0.clicked.connect(self.clicked)
            layout.addWidget(label_0, idx_family := idx_family + 1, 2)
        editButton = QPushButton('Edit')
        editButton.clicked.connect(self.edit)
        layout.addWidget(editButton, max(idx, idx_family) + 1, 1)
        layout.addWidget(self.buttonBox, max(idx, idx_family) + 1, 2)
        self.setLayout(layout)

    def clicked(self):
        a = self.sender()
        dlg = PersonDialog(self.person.get_family()[a.text()], self)
        dlg.exec()


class EditPersonDialog(QDialog):
    person: Human

    def __init__(self, person: Human, parent=None):
        super().__init__(parent)

        person.update()
        self.person = person

        self.setWindowTitle(person.get_name())
        self.render_()

    def render_(self):
        QBtn = QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()
        name_0 = QLabel('Имя:')
        name = QLineEdit(self.person.get_name())
        data_of_birthday_0 = QLabel('Дата рождения:')
        data_of_birthday = QLineEdit(self.person.get_data_of_birthday())
        gender_0 = QLabel('Пол:')
        gender = QLineEdit(self.person.get_gender())
        dead = QRadioButton()
        dead_0 = QLabel("Дата смерти (on/off)")
        data_of_dead_0 = QLabel('Дата смерти:')
        if self.person.get_data_of_dead() is None:
            data_of_dead = QLineEdit()
        else:
            data_of_dead = QLineEdit(self.person.get_data_of_dead())
        info_label = dict()

        idx = -1
        label_2 = QLabel('Информация')
        layout.addWidget(label_2, idx := idx + 1, 0)
        layout.addWidget(name, idx := idx + 1, 1)
        layout.addWidget(name_0, idx, 0)
        layout.addWidget(data_of_birthday, idx := idx + 1, 1)
        layout.addWidget(data_of_birthday_0, idx, 0)
        layout.addWidget(gender, idx := idx + 1, 1)
        layout.addWidget(gender_0, idx, 0)
        layout.addWidget(dead, idx := idx + 1, 1)
        layout.addWidget(dead_0, idx, 0)
        layout.addWidget(data_of_dead, idx := idx + 1, 1)
        layout.addWidget(data_of_dead_0, idx, 0)
        if self.person.get_dead():
            data_of_death_0 = QLabel('Дата смерти:')
            data_of_death = QLineEdit(self.person.get_data_of_dead())
            layout.addWidget(data_of_death, idx := idx + 1, 1)
            layout.addWidget(data_of_death_0, idx, 0)
        other_information = self.person.get_info()
        for i in other_information:
            info = QLabel(other_information[i])
            info_0 = QLabel(i)
            info_label[i] = info
            layout.addWidget(info, idx := idx + 1, 1)
            layout.addWidget(info_0, idx, 0)
        idx_family = -1
        label_1 = QLabel('Родственники')
        layout.addWidget(label_1, idx_family := idx_family + 1, 3)
        family = self.person.get_family()
        for i in family:
            label_0 = QPushButton(i)
            label_0.clicked.connect(self.clicked)
            layout.addWidget(label_0, idx_family := idx_family + 1, 3)
        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.save)
        addMemberButton = QPushButton('Add relative')
        addMemberButton.clicked.connect(self.addRelative)
        addInfoButton = QPushButton('Add information')
        addInfoButton.clicked.connect(self.addInformation)

        layout.addWidget(addMemberButton, max(idx, idx_family) + 1, 3)
        layout.addWidget(addInfoButton, max(idx, idx_family) + 1, 0)
        layout.addWidget(saveButton, max(idx, idx_family) + 2, 1)
        layout.addWidget(self.buttonBox, max(idx, idx_family) + 2, 2)
        self.setLayout(layout)

    def save(self):
        a = self.sender()
        dlg = PersonDialog(self.person.get_family()[a.text()], self)
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

    def addRelative(self):
        pass

    def addInformation(self):
        pass


root = Human(1)
app = QApplication(sys.argv)
window = MainWindow(root)
window.show()
app.exec()
