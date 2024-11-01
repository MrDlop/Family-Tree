import os
import unittest

from data.person import Person

os.remove("db.bd")
from family_class import Human


class TestFamilyClass(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.person = Human()
        self.person.update()
        self.person2 = Human()
        self.person2.update()

    def test_set_name(self):
        self.assertEqual(self.person.get_name(), None)
        self.person.set_name("<NAME>")
        self.person.update()
        self.assertEqual(self.person.get_name(), "<NAME>")

    def test_id_first(self):
        self.assertEqual(self.person.get_id(), 1)

    def test_id_none(self):
        temp = Human()
        self.assertEqual(temp.get_id(), None)

    def test_find_person(self):
        find = Human(1)
        self.assertEqual(find, self.person)

    def test_data_of_birthday(self):
        self.assertEqual(self.person.get_data_of_birthday(), None)
        self.person.set_data_of_birthday("1.0.1")
        self.person.update()
        self.assertEqual(self.person.get_data_of_birthday(), "1.0.1")

    def test_gender(self):
        self.assertEqual(self.person.get_gender(), None)
        self.person.set_gender("male")
        self.person.update()
        self.assertEqual(self.person.get_gender(), "male")

    def test_dead(self):
        self.assertEqual(self.person.get_dead(), False)
        self.assertEqual(self.person.get_data_of_dead(), None)
        self.person.set_data_of_dead("1.0.1")
        self.person.update()
        self.assertEqual(self.person.get_dead(), True)
        self.assertEqual(self.person.get_data_of_dead(), "1.0.1")

    def test_info(self):
        self.assertEqual(self.person.get_info(), {})
        self.person.add_info(["name", "John"])
        self.person.update()
        self.assertEqual(self.person.get_info(), {'name': 'John'})
        self.person.set_info({'name': 'Logan'})
        self.person.update()
        self.assertEqual(self.person.get_info(), {'name': 'Logan'})
        self.person.del_info('name')
        self.person.update()
        self.assertEqual(self.person.get_info(), {})

    def test_connection(self):
        person1 = Human(1)
        person2 = Human(2)
        person1.change_member_connection(person2, 'father')
        person2.change_member_connection(person1, 'mother')
        person1.update()
        person2.update()
        self.assertEqual(person1.get_family(), {'father': person2})


if __name__ == '__main__':
    unittest.main()
