from typing import NoReturn, Any, Callable
from abc import ABC, abstractmethod

from .app_logging import logger


class View(ABC):
    __master: Any

    def __init__(self, master: Any):
        self.master = master

    @property
    def master(self) -> Any:
        return self.__master

    @master.setter
    def master(self, master: Any) -> NoReturn:
        self.__master = master

    @abstractmethod
    def switch(self, view: Any) -> NoReturn:
        pass

    @abstractmethod
    def run(self) -> bool:
        pass


@logger
class Application(View):
    __apps: dict

    def __init__(self, master: Any):
        super().__init__(master)
        self.apps = APPLICATIONS
        self.apps['Выход'] = self.__class__

    @property
    def apps(self) -> dict:
        return self.__apps

    @apps.setter
    def apps(self, apps: dict) -> NoReturn:
        self.__apps = apps

    def switch(self, view: Any) -> NoReturn:
        self.master.slave = view

    def run(self) -> bool:
        aps = {pos: app for pos, app in enumerate(APPLICATIONS, 1)}
        print('Выберите приложение:', '\n'.join([f'{pos}) {app}' for pos, app in aps.items()]), sep='\n')

        while True:
            try:
                choice = int(input('>>> '))
            except Exception as ex:
                print(f'Для выбора укажите номер варианта (Ошибка: {ex})')
            else:
                app = self.apps[aps[choice]]
                if app == self.__class__:
                    return False
                self.switch(app)
                return True


@logger
class ComplexCalcView(View):

    def __init__(self, master: Any):
        super().__init__(master)

    @staticmethod
    def __intro() -> str:
        return """
        Добро пожаловать в калькулятор комплексных чисел!

        Правила работы с калькулятором:

        - комплексное должно иметь вид "X±Yj",
        где X и Y - действительные числа, а j - обозначение мнимой части;

        - допускается ввод только действительной части (X), либо только мнимой части (Yj);

        - ввод операндов осуществляется по одному за раз;

        - доступные операции над комплексными числами:
            1) сложение, символ операции - '+';
            2) вычитание, символ операции - '-';
            3) умножение, символ операции - '*';
            4) деление, символ операции - '/'.

        - для выбора операции необходимо ввести символ операции; 
        """

    @staticmethod
    def __is_valid_operation(operation: str) -> bool:
        if len(operation) == 1 and operation in '+-*/':
            return True
        return False

    @staticmethod
    def __input_exception(user_input: str, type_exc: str, example: str) -> NoReturn:
        print(f'Ошибка ввода {type_exc}, пример: {example}, вы ввели: {user_input}')

    @staticmethod
    def __is_complex(value: str) -> bool:
        try:
            complex(value)
        except Exception:
            return False
        else:
            return True

    @staticmethod
    def __input() -> str:
        return input('>>> ')

    def __continue(self) -> bool:
        print('Продолжить работу?\n(Y - for Yes, AnyKey - for No)')
        if (choice := self.__input()) and choice.upper() in "YES":
            return True
        return False

    def __operation_input(self,
                          intro: str,
                          validation: Callable[[str], bool],
                          ex_out: Callable[[str, str, str], NoReturn],
                          type_exc: str, example: str) -> str:
        print(intro)
        user_input = self.__input()
        while not validation(user_input):
            ex_out(user_input, type_exc, example)
            user_input = self.__input()
        return user_input

    def switch(self, view: Any) -> NoReturn:
        self.master.slave = view

    def run(self) -> bool:
        print(self.__intro())
        while self.__continue():
            request = dict(
                left=self.__operation_input('Введите левый операнд:',
                                            self.__is_complex,
                                            self.__input_exception,
                                            'комплексного числа',
                                            '"1+2j", "2-1j", "2", "1j"'),

                operation=self.__operation_input("Выберите операцию: '+', '-', '*', '/'",
                                                 self.__is_valid_operation,
                                                 self.__input_exception,
                                                 'комплексного числа',
                                                 '"1+2j", "2-1j", "2", "1j"'),

                right=self.__operation_input('Введите правый операнд:',
                                             self.__is_complex,
                                             self.__input_exception,
                                             'комплексного числа', '"1+2j", "2-1j", "2", "1j"')

            )
            self.master.post(request)
            pretty_text = "{left}{operation}{right}".format(**request)
            print(pretty_text + "={result}".format(request, **self.master.get()))

        self.switch(Application)
        return True


APPLICATIONS: dict = {
    'Калькулятор комплексных чисел': ComplexCalcView
}