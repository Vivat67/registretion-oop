"""Модуль реализует хранение пользователей в текстовом файле
 их авторизацию и регистрацию.
"""

from typing import Union

FILENAME = 'log.txt'
REGISTER = 1
AUTHORIZED = 2


class UserBase:
    """Клас реализует хранение пользователей в текстовом файле,
      запись пользователей в файл, проверяет наличии их в файле.
    """

    def __init__(self):
        self.filename = FILENAME

    def create_file(self):
        """Создает пустой текстовый файл"""
        with open(self.filename, 'w+', encoding='utf-8'):
            pass

    def read_file(self) -> str:
        """
        Открывает файл.

        Args:
            filename: файл с базой пользователей
        Returns:
            f.readlines(): функция, предоставляющая
            в строковом виде информацию о пользователях
        """
        with open(self.filename, encoding='utf-8') as f:
            return f.readlines()

    def write_file(self, login: Union[str, int], password: Union[str, int]):
        """
        Добавляет нового пользователя.

        Производим запись о новом пользователе в файл,
        через ';' заносятся логин и пароль,
        при удачном добавлении пользователя,
        в консоль выводится:
        'Данные успешно записаны!'

        Args:
            login: имя пользователя (логин)
            password: пароль пользователя (пароль)
        """
        with open(self.filename, 'a+', encoding='utf-8') as f:
            f.write(''.join([login, ';', password, '\n']))
            print('Данные успешно записаны!')

    def check_login(self, login: Union[str, int]) -> bool:
        """
        Проверяет наличие логина в базе.

        Функция проверяет является введенный логин оригинальным,
        если нет то сообщает об этом пользователю и предлагает
        придумать другой логин, либо авторизоваться.

        Args:
            login: имя пользователя (логин)
        Returns:
            False: логин является оригиналным
            True: логин уже существует
        """
        for line in self.read_file():
            log_file_read = line.split(';')[0]
            if login == log_file_read:
                print('Такое имя пользователя уже существует')
                print('Придумайте другой логин, либо авторизуйтесь')
                return True
        return False


class AccountManager:
    """Класс реализует взаимодействие с пользователем,
      позволяет совершить авторизацию и регистрацию.
    """
    def __init__(self):
        self.user = UserBase()

    def log_pass_input(self) -> Union[str, int]:
        """
        Просит ввести имя пользователя и пароль.

        Выводит в консоль предложение ввести имя пользователя и пароль,
        проверяет логин и пароль на валидность, если проверка пройдена-
        возвращает логин и пароль.

        Returns:
            login: логин
            password: пароль
        """
        login = input('Введите имя пользователя: ')
        password = input('Введите пароль: ')
        assert 3 < len(login) < 21, 'Имя пользователя слишком короткое!'
        assert 4 < len(password) < 33, 'Пароль слишком короткий!'
        return login, password

    def log_pass_verification(
            self, login: Union[str, int], password: Union[str, int]):
        """
        Верификация пользователя.

        Сверяет логин и пароль пользователя с базой данных.
        Если введенные данные верны- сообщает об успехе.
        Если пароль не верен просит повторить ввод.
        Если логин и пароль не верны сообщает,
        что такой пользовает отсутствует.

        Args:
            login: имя пользователя (логин)
            password: пароль
        """
        for line in self.user.read_file():
            log_file_read = line.split(';')[0]
            pass_file_read = line.rstrip('\n').split(';')[1]

            if login == log_file_read and password == pass_file_read:
                print('Авторизация успешна!')
                break

            elif login == log_file_read and password != pass_file_read:
                print('Введен неверный пароль! Повторите попытку!')
                break
        else:
            print('В базе данных такой пользователь не найден!')
            print('Вы переведены в главное меню')

    def account_register(
            self, login: Union[str, int], password: Union[str, int]):
        """
        Ргистрация аккаунта.

        Проверяет, что пользователя нет в базе.
        Если такого пользователя не существует-
        записывает в файл данные пользователя,
        его логин и пароль.

        Args:
            login: логин
            password: пароль
        """
        if self.user.check_login(login):
            return
        self.user.write_file(login, password)

    def choice_command(self, command: int):
        """
        Менеджер команд.

        Дает пользователю выбор действия: авторизация, регистрация, выход.
        Просит пользователя ввести данные: логин, пароль для автоизации или
        регистрации.

        Args:
            command: команда(регистрация, авторизация)
        """
        try:
            login, password = self.log_pass_input()
        except AssertionError as error:
            print(str(error))
            return
        if command == REGISTER:
            self.account_register(login, password)
        elif command == AUTHORIZED:
            self.log_pass_verification(login, password)


def main():
    account_manager = AccountManager()
    account_manager.user.create_file()
    print('Добро пожаловать!')
    print('Хотите зарегистрироваться или авторизоваться?')
    while True:
        try:
            print('Введите:')
            print('1 для регистрации')
            print('2 для авторизации')
            print('3 выход')
            command = int(input('Введите цифру: '))
            if command not in [1, 2, 3]:
                raise ValueError
            if command == 3:
                break
            account_manager.choice_command(command)
        except ValueError:
            print('Ошибка ввода данных!')


if __name__ == '__main__':
    main()
