# Тимербаев Эмиль Б05-408
# Описание проекта
Программа для отображения семейного древа и хранения его
# Используемые библиотеки
SqlAlchemy
PyQt5
# Поддерживаемые версии Python
Python 3.12
# Реализуемый функционал
Графический интерфейс реализуемый с помощью PyQt5

Основное окно - окно отображающее ближайшее дерево (родители, дети, супруги)

Окна с информацией о человеке с возможностью перемещения по его родственникам. В окне отображается основная информация о человеке и его ближайшие родственники

Также функция изменения данных/добавления человека в семейное древо

Работа с базами данных с помощью SQLAlchemy

Для изменения/добавления сущности будет обращения к базе данных через SQLAlchemy
# Архитектура
## Код
### Class MainWindow 
наследник QMainWindow
Приветственное окно
### Class TreeDialog
наследник QDialog
Отображение ближайшего дерева (родители/супруги/дети)

person_root: Human - текущий корень дерева

def start(self) - функция обработки нажатия на листья

Если нажат текущий корень открывается окно PersonDialog, для просмотра информации о человеке

Если нажат другой лист, дерево "переподвешивается" (def __render(self))
### Class PersonDialog
наследник QDialog

Отображение Person (первый столбец информация, второй родственники, по которым можно переходить)

def edit(self) обработка нажатия на кнопку edit, при нажатии на которыю создаётся EditPersonDialog, после чего вызывается def __render(self)
### Class EditPersonDialog
наследник QDialog

Изменение информации о Person
### Class Person
класс наследник DeclarativeBase (sqlalchemy) - для работы с информацией о человеке

Fields: columns db
### Class ConnectPerson
класс наследник DeclarativeBase (sqlalchemy) - для работы с информацией о связями между людьми

Fields: columns db
### Class Human
Класс по работе с Person и ConnectPerson

Имеются геттеры и сетеры

 def __meta_info(self, meta_info: dict[str, str]) -> str - преобразует dict в str, для хранения в БД
 
 def get_info(self) -> dict[str, str] - преобразует str из БД в dict
 
 def __add_member_connection(self, member: Self, type_con: str) -> None - функция для создания связей между людьми (от нее зависят более понятные функции add_mother, add_child, ...) (_Возможно удаление других функций и оставление только add_member_connection_)
 
 def __delete_member(self, member: Self, type_con) -> None - удаление связей между людьми

def get_family(self) -> dict[str, Self] - получение текущего дерева
### Class Connect 
наследник DeclarativeBase (sqlalchemy) - для работы со связями между Person
## Data base

### persons:

ID|Name|Data of birsday|Data of Dead(None)|Info(maybe some columns)|Sex|Maybe photo???

### connect:

ID|ID|type
