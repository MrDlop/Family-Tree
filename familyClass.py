from typing_extensions import Self, Dict, List

from data import db_session
from data.person import Person
from data.connect_person import ConnectPerson

db_session.global_init("db.bd")

session = db_session.create_session()


class Human:
    person: Person

    def __init__(self, id: int) -> None:
        """
        :param id: id person in database
        """
        self.person = session.query(Person).filter(Person.id == id).one()

    def update(self) -> None:
        """
        Function update data of person
        :return:
        """
        self.person = session.query(Person).filter(Person.id == self.person.id).one()

    def set_name(self, name: str) -> None:
        self.person.name = name
        session.commit()

    def get_name(self):
        return self.person.name

    def set_data_of_birthday(self, data_of_birthday: str) -> None:
        self.person.data_of_birthday = data_of_birthday
        session.commit()

    def get_data_of_birthday(self) -> str:
        return self.person.data_of_birthday

    def set_data_of_dead(self, data_of_dead: str) -> None:
        self.person.data_of_dead = data_of_dead
        session.commit()

    def get_dead(self) -> bool:
        return not (self.person.data_of_dead is None)

    def get_data_of_dead(self) -> str:
        return self.person.data_of_dead

    def set_gender(self, gender: str) -> None:
        self.person.gender = gender
        session.commit()

    def get_gender(self) -> str:
        return self.person.gender

    def get_info(self) -> dict[str, str]:
        if self.person.info is None:
            return dict()
        return {i.split(':')[0]: i.split(':')[1] for i in self.person.info.split("#")}

    def __meta_info(self, meta_info: dict[str, str]) -> str:
        return '#'.join([':'.join([i, meta_info[i]]) for i in meta_info])

    def set_info(self, info: list[str, str]) -> None:
        meta_info = self.get_info()
        meta_info[info[0]] = info[1]
        self.person.info += self.__meta_info(meta_info)
        session.commit()

    def del_info(self, info_tag: str) -> None:
        meta_info = self.get_info()
        if info_tag in meta_info:
            del meta_info[info_tag]
        self.person.name = self.__meta_info(meta_info)
        session.commit()

    def __add_member_connection(self, member: Self, type_con: str) -> None:
        member_con = ConnectPerson()
        member_con.name = type_con
        member_con.id_second = member.person.id
        member_con.id_first = self.person.id
        session.add(member_con)
        session.commit()

    def add_mother(self, mother: Self) -> None:
        self.__add_member_connection(mother, 'mother')

    def add_father(self, father: Self) -> None:
        self.__add_member_connection(father, 'father')

    def add_child(self, child: Self) -> None:
        self.__add_member_connection(child, 'child')

    def add_spouse(self, spouse: Self) -> None:
        self.__add_member_connection(spouse, 'spouse')

    def add_love(self, love):
        self.__add_member_connection(love, 'love')

    def __delete_member(self, member: Self, type_con) -> None:
        member_con = ConnectPerson()
        member_con.name = type_con
        member_con.id_second = member.person.id
        member_con.id_first = self.person.id
        session.delete(member_con)
        session.commit()

    def delete_mother(self, mother):
        self.__delete_member(mother, 'mother')

    def delete_father(self, father):
        self.__delete_member(father, 'father')

    def delete_child(self, child):
        self.__delete_member(child, 'child')

    def delete_spouse(self, spouse):
        self.__delete_member(spouse, 'spouse')

    def delete_love(self, love):
        self.__delete_member(love, 'love')

    def get_family(self) -> dict[str, Self]:
        family = dict()
        child_idx = 0
        for member in session.query(ConnectPerson).filter(ConnectPerson.id_first == self.person.id).all():
            if member.type == 'child':
                family[member.type + "_" + str(child_idx)] = Human(member.id_second)
            else:
                family[member.type] = Human(member.id_second)
        return family


if __name__ == '__main__':
    person1 = Person()
    person1.name = "Тимербаев Эмиль"
    person1.data_of_birthday = "11.12.2006"
    person1.gender = "Муж"
    session.add(person1)

    person2 = Person()
    person2.name = "Тимербаев Эльвир"
    person2.data_of_birthday = "24.02.1982"
    person2.gender = "Муж"
    session.add(person2)

    person3 = Person()
    person3.name = "Тимербаева Татьяна"
    person3.data_of_birthday = "12.07.1982"
    person3.gender = "Жен"
    session.add(person3)

    person4 = Person()
    person4.name = "Тимербаева Элина"
    person4.data_of_birthday = "08.04.2002"
    person4.gender = "Жен"
    session.add(person4)

    person5 = Person()
    person5.name = "Тимербаев Роман"
    person5.data_of_birthday = "18.05.2013"
    person5.gender = "Муж"
    session.add(person5)
