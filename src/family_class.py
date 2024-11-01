from typing_extensions import Self

from data import db_session
from data.person import Person
from data.connect_person import ConnectPerson

db_session.global_init("db.bd")

session = db_session.create_session()


class Human:
    person: Person
    flag: bool

    def __init__(self, id_human: int | None = None) -> None:
        """
        :param id_human: id person in database
        :return: None
        """
        self.flag = id_human is not None
        if self.flag:
            self.person = session.query(Person).filter(Person.id == id_human).one()
        else:
            self.person = Person()

    def update(self) -> None:
        """
        Function update data of person
        :return: None
        """
        if self.flag:
            self.person = session.query(Person).filter(Person.id == self.person.id).one()
        else:
            self.flag = True
            session.add(self.person)
            session.commit()

    def set_name(self, name: str) -> None:
        """
        Setter
        :param name: name of human
        :return:
        """
        self.person.name = name
        session.commit()

    def get_name(self) -> str:
        """
        Getter
        :return: name
        """
        return self.person.name

    def get_id(self) -> int:
        """
        Getter
        :return: id
        """
        return self.person.id

    def set_data_of_birthday(self, data_of_birthday: str) -> None:
        """
        Setter
        :param data_of_birthday:
        :return:
        """
        self.person.data_of_birthday = data_of_birthday
        session.commit()

    def get_data_of_birthday(self) -> str:
        """
        Getter
        :return: data of birthday
        """
        return self.person.data_of_birthday

    def set_data_of_dead(self, data_of_dead: str | None) -> None:
        """
        Setter
        :param data_of_dead: if data of dead is None - person life
        :return:
        """
        self.person.data_of_dead = data_of_dead
        session.commit()

    def get_dead(self) -> bool:
        """
        Getter
        :return: boolean flag view life people
        """
        return not (self.person.data_of_dead is None)

    def get_data_of_dead(self) -> str:
        """
        Getter
        :return: data of dead
        """
        return self.person.data_of_dead

    def set_gender(self, gender: str) -> None:
        """
        Setter
        :param gender:
        :return:
        """
        self.person.gender = gender
        session.commit()

    def get_gender(self) -> str:
        """
        Getter
        :return: gender of person
        """
        return self.person.gender

    def get_info(self) -> dict[str, str]:
        """
        Getter
        :return: Info how dict ("type information": "text information")
        """
        if self.person.info == "" or self.person.info is None:
            return dict()
        return {i.split(':')[0]: i.split(':')[1] for i in self.person.info.split("#")}

    @staticmethod
    def __meta_info(meta_info: dict[str, str]) -> str:
        """
        :param meta_info: dict ("type information": "text information")
        :return: info how read database
        """
        return '#'.join([':'.join([i, meta_info[i]]) for i in meta_info])

    def add_info(self, info: list[str]) -> None:
        """
        Setter
        :param info: ("type information", "text information")
        :return:
        """
        meta_info = self.get_info()
        meta_info[info[0]] = info[1]
        self.person.info += self.__meta_info(meta_info)
        session.commit()

    def set_info(self, info: dict[str, str]) -> None:
        """
        :param info: ("type information": "text information")
        :return:
        """
        self.person.info = self.__meta_info(info)
        session.commit()

    def del_info(self, info_tag: str) -> None:
        """
        :param info_tag: type information
        :return:
        """
        meta_info = self.get_info()
        if info_tag in meta_info:
            del meta_info[info_tag]
        self.person.info = self.__meta_info(meta_info)
        session.commit()

    def change_member_connection(self, member: Self | None, type_con: str) -> None:
        """
        :param member: Member from database
        :param type_con: Type connection (connection don't commutativity)
        :return:
        """
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

    def get_family(self) -> dict[str, Self]:
        """
        :return: all family members
        """
        family = dict()
        child_idx = 0
        for member in session.query(ConnectPerson).filter(ConnectPerson.id_first == self.person.id).all():
            if member.type == 'child':
                family[member.type + "_" + str(child_idx)] = Human(member.id_second)
            else:
                family[member.type] = Human(member.id_second)
        return family

    @staticmethod
    def get_all_humans() -> list[Self]:
        """
        :return: all human from database
        """
        list_humans = list()
        for person in session.query(Person).all():
            list_humans.append(Human(person.id))
        return list_humans

    def __eq__(self, other: Self) -> bool:
        """
        :param other:
        :return:
        """
        return self.person.id == other.person.id
