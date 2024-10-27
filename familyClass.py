from typing_extensions import Self, Dict, List

from data import db_session
from data.person import Person
from data.connect_person import ConnectPerson

db_session.global_init("db.bd")

session = db_session.create_session()


class Human:
    person: Person
    flag: bool

    def __init__(self, id: int | None = None) -> None:
        """
        :param id: id person in database
        """
        self.flag = id is not None
        if self.flag:
            self.person = session.query(Person).filter(Person.id == id).one()
        else:
            self.person = Person()

    def update(self) -> None:
        """
        Function update data of person
        :return:
        """
        if self.flag:
            self.person = session.query(Person).filter(Person.id == self.person.id).one()
        else:
            self.flag = True
            session.add(self.person)
            session.commit()

    def set_name(self, name: str) -> None:
        self.person.name = name
        session.commit()

    def get_name(self):
        return self.person.name

    def get_id(self) -> int:
        return self.person.id

    def set_data_of_birthday(self, data_of_birthday: str) -> None:
        self.person.data_of_birthday = data_of_birthday
        session.commit()

    def get_data_of_birthday(self) -> str:
        return self.person.data_of_birthday

    def set_data_of_dead(self, data_of_dead: str | None) -> None:
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
        if self.person.info == "" or self.person.info is None:
            return dict()
        return {i.split(':')[0]: i.split(':')[1] for i in self.person.info.split("#")}

    def __meta_info(self, meta_info: dict[str, str]) -> str:
        return '#'.join([':'.join([i, meta_info[i]]) for i in meta_info])

    def add_info(self, info: list[str, str]) -> None:
        meta_info = self.get_info()
        meta_info[info[0]] = info[1]
        self.person.info += self.__meta_info(meta_info)
        session.commit()

    def set_info(self, info: dict[str, str]) -> None:
        self.person.info = self.__meta_info(info)
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

    def change_member_connection(self, member: Self | None, type_con: str) -> None:
        if self.person.id is not None:
            member_con_0 = session.query(ConnectPerson).filter(
                ConnectPerson.id_first == self.person.id).filter(ConnectPerson.type == type_con).all()
            if len(member_con_0) == 0:
                member_con_0 = None
            else:
                member_con_0 = member_con_0[0]
        else:
            member_con_0 = None
        if member_con_0 is None:
            if member is not None:
                con = ConnectPerson()
                con.id_first = self.person.id
                con.id_second = member.person.id
                con.type = type_con
                session.add(con)
        else:
            if member is not None:
                member_con_0.id_second = member.person.id
            else:
                session.delete(member_con_0)
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

    def get_all_humans(self) -> list[Self]:
        list_humans = list()
        for i in session.query(Person).all():
            list_humans.append(Human(i.id))
        return list_humans

    def __eq__(self, other):
        return self.person.id == other.person.id


if __name__ == '__main__':
    Human(0)
