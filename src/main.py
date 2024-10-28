import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QLineEdit, QRadioButton, QLabel, QGridLayout

from sqlalchemy.exc import NoResultFound

from family_class import Human


class MainWindow(QMainWindow):
    root: Human

    def __init__(self):
        """
        Initialization function (basic QT + create/connect to db)
        """
        super().__init__()

        try:
            root = Human(1)
        except NoResultFound:
            root = Human()
            root.person.id = 1
            root.update()

        self.setWindowTitle("My App")
        self.root = root
        button = QPushButton("Start")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self):
        """
        method for start main dialog
        :return:
        """
        dlg = TreeDialog(person_root=self.root, parent=self)
        dlg.exec()


class TreeDialog(QDialog):
    person_root: Human
    layout: QGridLayout
    person_root: Human
    button_box: QDialogButtonBox

    def __init__(self, person_root: Human, parent: QDialog = None) -> None:
        """
        Initialization function (basic QT)
        :param person_root: root of the person tree
        :param parent:
        """
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.person_root = person_root
        self.__render()

    def __render(self, is_created: bool = False) -> None:
        """
        Update layout with current root
        :param is_created: False if first creating and True is not single
        :return:
        """
        if is_created:
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().deleteLater()
        self.setWindowTitle(self.person_root.get_name())

        cancel_button = QDialogButtonBox.Cancel
        columns = 0
        family = self.person_root.get_family()
        for member in family:
            if 'child' in member:
                columns += 1
        columns = max(columns, 3)
        posR = columns // 2

        if 'mother' in family:
            self.__add_member("mother", family["mother"], posR - 1, 0)

        if 'father' in family:
            self.__add_member("father", family["father"], posR + 1, 0)

        self.__add_member("self", self.person_root, posR, 1)

        if 'spouse' in family:
            self.__add_member("spouse", family["spouse"], posR + 1, 1)
        idx = -1
        for member in family:
            if 'child' in member:
                self.__add_member(member, family[member], idx := idx + 1, 2)

        add_human_button = QPushButton("Добавить человека")
        add_human_button.clicked.connect(self.__add_human)

        self.button_box = QDialogButtonBox(cancel_button)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box, 3, columns + 1)
        self.layout.addWidget(add_human_button, 3, columns)
        self.update()

    def start(self) -> None:
        """
        Move root or open information window
        :return:
        """
        if self.sender().objectName() == 'self':
            dlg = PersonDialog(self.person_root, self)
            if not dlg.exec():
                self.__render(True)
        else:
            self.person_root = self.person_root.get_family()[self.sender().objectName()]
            self.__render(True)

    def __add_member(self, name: str, obj_member: Human, pos_x: int, pos_y: int) -> None:
        """
        Method move the member to Grid
        :param name:
        :param obj_member:
        :param pos_x:
        :param pos_y:
        :return:
        """
        but_member = QPushButton(obj_member.get_name())
        but_member.setObjectName(name)
        but_member.clicked.connect(self.start)
        self.layout.addWidget(but_member, pos_x, pos_y)

    def __add_human(self) -> None:
        """
        create dialog for create people
        :return:
        """
        dlg = EditPersonDialog(None, self)
        dlg.exec()


class PersonDialog(QDialog):
    person: Human
    layout: QGridLayout
    buttonBox: QDialogButtonBox

    def __init__(self, person: Human, parent: QDialog = None) -> None:
        """
        Initialize the person dialog
        :param person:
        :param parent:
        """
        super().__init__(parent)
        person.update()
        self.person = person

        self.layout = QGridLayout(self)
        self.setWindowTitle(person.get_name())
        self.__render()

    def edit(self) -> None:
        """
        Method starting edit person dialog
        :return:
        """
        dlg = EditPersonDialog(self.person, self)
        if not dlg.exec():
            self.person.update()
            self.__render(True)

    def __render(self, is_created: bool = False) -> None:
        """
        Method update person view
        :param is_created: Is layout created
        :return:
        """
        if is_created:
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().deleteLater()
        button_cancel = QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(button_cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        name_0 = QLabel('Имя:')
        name = QLabel(self.person.get_name())
        data_of_birthday_0 = QLabel('Дата рождения:')
        data_of_birthday = QLabel(self.person.get_data_of_birthday())
        gender_0 = QLabel('Пол:')
        gender = QLabel(self.person.get_gender())
        info_label = dict()

        idx = -1
        label_2 = QLabel('Информация')
        self.layout.addWidget(label_2, idx := idx + 1, 0)
        self.layout.addWidget(name, idx := idx + 1, 1)
        self.layout.addWidget(name_0, idx, 0)
        self.layout.addWidget(data_of_birthday, idx := idx + 1, 1)
        self.layout.addWidget(data_of_birthday_0, idx, 0)
        self.layout.addWidget(gender, idx := idx + 1, 1)
        self.layout.addWidget(gender_0, idx, 0)
        if self.person.get_dead():
            data_of_death_0 = QLabel('Дата смерти:')
            data_of_death = QLabel(self.person.get_data_of_dead())
            self.layout.addWidget(data_of_death, idx := idx + 1, 1)
            self.layout.addWidget(data_of_death_0, idx, 0)
        other_information = self.person.get_info()
        for i in other_information:
            info = QLabel(other_information[i])
            info_0 = QLabel(i)
            info_label[i] = info
            self.layout.addWidget(info, idx := idx + 1, 1)
            self.layout.addWidget(info_0, idx, 0)
        idx_family = -1
        label_1 = QLabel('Родственники')
        self.layout.addWidget(label_1, idx_family := idx_family + 1, 2)
        family = self.person.get_family()
        for i in family:
            label_0 = QPushButton(i)
            label_0.clicked.connect(self.clicked)
            self.layout.addWidget(label_0, idx_family := idx_family + 1, 2)
        editButton = QPushButton('Edit')
        editButton.clicked.connect(self.edit)
        self.layout.addWidget(editButton, max(idx, idx_family) + 1, 1)
        self.layout.addWidget(self.buttonBox, max(idx, idx_family) + 1, 2)
        self.update()

    def clicked(self) -> None:
        """
        Button clicked (start new Person Dialog)
        :return:
        """
        dlg = PersonDialog(self.person.get_family()[self.sender().text()], self)
        dlg.exec()


class EditPersonDialog(QDialog):
    label: QGridLayout
    information: dict[str, (QLineEdit, QLineEdit)]
    rb_dead: QRadioButton
    gender: QLineEdit | QLineEdit
    data_of_dead: QLineEdit | QLineEdit
    data_of_birthday: QLineEdit | QLineEdit
    name: QLineEdit
    person: Human
    list_humans: list[Human]
    list_childs: list[QComboBox] = list()
    information_unique_key: str = "0"
    childs: int = 0
    idx: int = -1
    idx_family: int = -1
    button_box: QDialogButtonBox
    save_button: QPushButton
    add_child_button: QPushButton
    add_spouse_button: QPushButton
    add_info_button: QPushButton

    def __init__(self, person: Human | None, parent=None) -> None:
        """
        Initialize the edit person dialog
        :param person:
        :param parent:
        """
        super().__init__(parent)

        if person is not None:
            person.update()
            self.person = person
        else:
            self.person = Human()

        self.list_humans = self.person.get_all_humans()
        self.setWindowTitle((self.person.get_name() if self.person.get_name() is not None else "New person"))
        self.__render()

    def __render(self) -> None:
        """
        Render layout
        :return:
        """
        q_button_cancel = QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(q_button_cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.label = QGridLayout()

        idx = -1
        label_2 = QLabel('Информация')
        self.label.addWidget(label_2, idx := idx + 1, 0)

        name_label = QLabel('Имя:')
        self.name = QLineEdit(self.person.get_name())
        self.label.addWidget(self.name, idx := idx + 1, 1)
        self.label.addWidget(name_label, idx, 0)

        data_of_birthday_label = QLabel('Дата рождения:')
        self.data_of_birthday = QLineEdit(self.person.get_data_of_birthday())
        self.label.addWidget(self.data_of_birthday, idx := idx + 1, 1)
        self.label.addWidget(data_of_birthday_label, idx, 0)

        gender_label = QLabel('Пол:')
        self.gender = QLineEdit(self.person.get_gender())
        self.label.addWidget(self.gender, idx := idx + 1, 1)
        self.label.addWidget(gender_label, idx, 0)

        rb_dead_label = QLabel("Дата смерти (on/off)")
        self.rb_dead = QRadioButton()
        data_of_dead_label = QLabel('Дата смерти:')
        if self.person.get_data_of_dead() is None:
            self.data_of_dead = QLineEdit()
        else:
            self.data_of_dead = QLineEdit(self.person.get_data_of_dead())
        self.label.addWidget(self.rb_dead, idx := idx + 1, 1)
        self.label.addWidget(rb_dead_label, idx, 0)
        self.label.addWidget(self.data_of_dead, idx := idx + 1, 1)
        self.label.addWidget(data_of_dead_label, idx, 0)

        other_information = self.person.get_info()
        self.information = dict()
        for i in other_information:
            info_description = QLineEdit(other_information[i])
            info_information = QLineEdit(i)
            self.information[i] = (info_description, info_information)
            info_button = QPushButton()
            info_button.setObjectName(i)
            info_button.setText('Удалить')
            info_button.clicked.connect(self.delete_info)
            self.label.addWidget(info_description, idx := idx + 1, 1)
            self.label.addWidget(info_button, idx, 2)
            self.label.addWidget(info_information, idx, 0)

        idx_family = -1
        label_1 = QLabel('Родственники')
        self.label.addWidget(label_1, idx_family := idx_family + 1, 3)

        family = self.person.get_family()
        self.name_list_humans = [i.get_name() for i in self.list_humans] + [""]

        label_mother = QLabel('Мать')
        self.cb_mother = QComboBox(self)
        self.cb_mother.setGeometry(200, 150, 120, 30)
        self.cb_mother.addItems(self.name_list_humans)
        if 'mother' in family.keys():
            self.cb_mother.setCurrentIndex(self.list_humans.index(family['mother']))
        else:
            self.cb_mother.setCurrentIndex(len(self.list_humans))
        self.label.addWidget(label_mother, idx_family := idx_family + 1, 3)
        self.label.addWidget(self.cb_mother, idx_family, 4)

        label_father = QLabel('Отец')
        self.cb_father = QComboBox(self)
        self.cb_father.setGeometry(200, 150, 120, 30)
        self.cb_father.addItems(self.name_list_humans)
        if 'father' in family.keys():
            self.cb_father.setCurrentIndex(self.list_humans.index(family['father']))
        else:
            self.cb_father.setCurrentIndex(len(self.list_humans))
        self.label.addWidget(label_father, idx_family := idx_family + 1, 3)
        self.label.addWidget(self.cb_father, idx_family, 4)

        label_spouse = QLabel('Супруг(-а)')
        self.cb_spouse = QComboBox(self)
        self.cb_spouse.setGeometry(200, 150, 120, 30)
        self.cb_spouse.addItems(self.name_list_humans)
        if 'spouse' in family.keys():
            self.cb_spouse.setCurrentIndex(self.list_humans.index(family['spouse']))
        else:
            self.cb_spouse.setCurrentIndex(len(self.list_humans))
        self.label.addWidget(label_spouse, idx_family := idx_family + 1, 3)
        self.label.addWidget(self.cb_spouse, idx_family, 4)

        for i in family:
            if 'child' in i:
                label_child = QLabel('Ребёнок')
                cb_child = QComboBox(self)
                cb_child.setObjectName(i)
                cb_child.setGeometry(200, 150, 120, 30)
                cb_child.addItems(self.name_list_humans)
                cb_child.setCurrentIndex(self.list_humans.index(family[i]))
                self.label.addWidget(label_child, idx_family := idx_family + 1, 3)
                self.label.addWidget(cb_child, idx_family, 4)
                self.childs += 1

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save)
        self.add_child_button = QPushButton('Добавить ребёнка')
        self.add_child_button.clicked.connect(self.add_child)
        self.add_spouse_button = QPushButton('Добавить супруга')
        self.add_spouse_button.clicked.connect(self.add_spouse)
        self.add_info_button = QPushButton('Добавить информацию')
        self.add_info_button.clicked.connect(self.add_information)

        self.label.addWidget(self.add_child_button, max(idx, idx_family) + 1, 3)
        # self.label.addWidget(self.addSpouseButton, max(idx, idx_family) + 1, 4)
        self.label.addWidget(self.add_info_button, max(idx, idx_family) + 1, 0)
        self.label.addWidget(self.save_button, max(idx, idx_family) + 2, 1)
        self.label.addWidget(self.button_box, max(idx, idx_family) + 2, 2)
        self.setLayout(self.label)
        self.idx = idx
        self.idx_family = idx_family

    def save(self) -> None:
        """
        Update database
        :return:
        """
        self.list_humans += [None]
        self.person.set_name(self.name.text())

        self.person.set_gender(self.gender.text())

        self.person.set_data_of_birthday(self.data_of_birthday.text())

        if self.rb_dead.isChecked():
            self.person.set_data_of_dead(self.data_of_dead.text())
        else:
            self.person.set_data_of_dead(None)

        info = dict()
        for i in self.information:
            info[self.information[i][0].text()] = self.information[i][1].text()
        self.person.set_info(info)
        self.person.update()
        self.person.change_member_connection(self.list_humans[self.cb_mother.currentIndex()], 'mother')
        self.person.change_member_connection(self.list_humans[self.cb_father.currentIndex()], 'father')
        self.person.change_member_connection(self.list_humans[self.cb_spouse.currentIndex()], 'spouse')
        for i in self.list_childs:
            self.person.change_member_connection(self.list_humans[i.currentIndex()], i.objectName())

        self.person.update()
        self.close()

    def add_child(self) -> None:
        label_child = QLabel('Ребёнок')
        cb_child = QComboBox(self)
        cb_child.setObjectName(f"child_{self.childs}")
        cb_child.setGeometry(200, 150, 120, 30)
        cb_child.addItems(self.name_list_humans)
        cb_child.setCurrentIndex(len(self.list_humans))
        self.list_childs.append(cb_child)
        self.idx_family += 1
        self.label.addWidget(label_child, self.idx_family, 3)
        self.label.addWidget(cb_child, self.idx_family, 4)
        self.childs += 1

        self.label.addWidget(self.add_child_button, max(self.idx, self.idx_family) + 1, 3)
        # self.label.addWidget(self.addSpouseButton, max(self.idx, self.idx_family) + 1, 4)
        self.label.addWidget(self.add_info_button, max(self.idx, self.idx_family) + 1, 0)
        self.label.addWidget(self.save_button, max(self.idx, self.idx_family) + 2, 1)
        self.label.addWidget(self.button_box, max(self.idx, self.idx_family) + 2, 2)

    def add_spouse(self) -> None:
        pass

    def delete_info(self) -> None:
        """
        Delete information
        :return:
        """
        info_description, info_information = self.information[self.sender().objectName()]
        del self.information[self.sender().objectName()]

        info_description.setEnabled(False)
        info_information.setEnabled(False)
        self.sender().setText('Удалено')
        self.sender().setEnabled(False)

    def add_information(self) -> None:
        """
        Add new information
        :return:
        """
        info_description = QLineEdit()
        info_information = QLineEdit()
        while self.information_unique_key in self.information.keys():
            self.information_unique_key = str(int(self.information_unique_key) + 1)
        self.information[self.information_unique_key] = (info_description, info_information)
        info_button = QPushButton()
        info_button.setObjectName(self.information_unique_key)
        info_button.setText('Удалить')
        info_button.clicked.connect(self.delete_info)
        self.idx += 1
        self.label.addWidget(info_description, self.idx, 1)
        self.label.addWidget(info_button, self.idx, 2)
        self.label.addWidget(info_information, self.idx, 0)

        self.label.addWidget(self.add_child_button, max(self.idx, self.idx_family) + 1, 3)
        # self.label.addWidget(self.addSpouseButton, max(self.idx, self.idx_family) + 1, 4)
        self.label.addWidget(self.add_info_button, max(self.idx, self.idx_family) + 1, 0)
        self.label.addWidget(self.save_button, max(self.idx, self.idx_family) + 2, 1)
        self.label.addWidget(self.button_box, max(self.idx, self.idx_family) + 2, 2)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
