from enum import Enum

TOKEN = "626563305:AAEQBLLDERFUD2TgIRxwWK8uCtA7ONhAEFc"

db_file = "database.vdb"

class States(Enum):
    S_START = "0"  # Начало нового диалога
    MAIN_SELECT = "1"  # Первое меню
    SELECT_WEATHER = "2"  # Выбор погоды
    SELECT_RULES = "3"  # Выбор маршрута поезда

GREETINGS = [
    "хай",
    "дороу",
    "привет",
    "дарова",
    "алё",
]

TRAINS = [
    "поезд",
    "колеса",
    "электон",
    "электричка",
]

MINSK = [
    "на минск"
]

MOLO = [
    "на молодечно"
]