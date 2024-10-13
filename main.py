class Node(object):
    parents = []
    children = []
    spouse = []
    gender = ''
    name = dict()
    data_of_birthday = ''
    death = False
    data_of_death = ''
    other_information = dict()

    def __init__(self, **kwargs):
        pass

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def add_parent(self, parent):
        parent.add_child(self)

    def set_data_of_birthday(self, data_of_birthday):
        self.data_of_birthday = data_of_birthday

    def set_gender(self, gender):
        self.gender = gender

    def set_name(self, name):
        self.name = name

    def set_spouse(self, spouse):
        self.spouse.append(spouse)
        spouse.set_spouse(self)

    def replace_dead(self):
        self.death = not self.death





