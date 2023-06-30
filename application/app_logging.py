from typing import NoReturn, Any

import logging


def new_log(obj_name, method):

    def log(*args, **kwargs):
        logging.info(f'Начало работы метода {obj_name}.{method.__name__}({args}{kwargs})')
        result = method(*args, **kwargs)
        logging.info(f'Метода {obj_name}.{method.__name__} закончил работу, начало возврата результата {str(result)}')
        return result

    return log


def logger(cls):

    class Logger:

        def __init__(self, *args, **kwargs):
            self.object = cls(*args, **kwargs)
            logging.info(f'Инициализирован экземпляр {self.get_object_name()}')

        def __getattribute__(self, s):
            try:
                x = super().__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            attr = self._obj.__getattribute__(s)
            if isinstance(attr, type(self.__init__)):
                return new_log(self.get_object_name(), attr)
            else:
                return attr

        @property
        def object(self) -> Any:
            return self._obj

        @object.setter
        def object(self, obj: Any) -> NoReturn:
            self._obj = obj

        def get_object_name(self) -> str:
            return f'{self.object.__class__.__name__}'

    logging.basicConfig(level=logging.INFO, filename="logs.log", format="%(asctime)s %(levelname)s -> %(message)s")

    return Logger