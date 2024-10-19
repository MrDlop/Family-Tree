# Описание проекта
Программа для отображения семейного древа и хранения его
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
Отображение ближайшего дерева
### Class PersonDialog
наследник QDialog
Отображение Person
### Class PersonDialogEdit
наследник QDialog
Изменение информации о Person
### Class Person
класс наследник DeclarativeBase (sqlalchemy) - для работы с информацией о человеке

Fields: columns db

Methods: getters, setter, getAge, getPhoto???
### Class Connect 
наследник DeclarativeBase (sqlalchemy) - для работы со связями между Person
### Class view
Класс реализующий графический интерфейс основной
### Class person_view
Дополнительное окно, для отображения информации о человеке
## Data base

### persons:

ID|Name|Data of birsday|Data of Dead(None)|Info(maybe some columns)|Sex|Maybe photo???

### connect:

ID|ID|type
