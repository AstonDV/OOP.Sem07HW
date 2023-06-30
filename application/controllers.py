from typing import NoReturn, NewType, Any, Union
from abc import ABC, abstractmethod

from .app_logging import logger

import json

JSON = NewType('Json', Union[str, dict])


class AbcController(ABC):
    __master: Any
    __slave: Any

    def __init__(self, master, slave):
        self.master = master
        self.slave = slave

    @property
    def master(self) -> Any:
        return self.__master

    @master.setter
    def master(self, master: Any):
        self.__master = master

    @property
    def slave(self) -> Any:
        return self.__slave

    @slave.setter
    def slave(self, slave: Any):
        self.__slave = slave

    @abstractmethod
    def post(self, request: JSON) -> JSON:
        pass

    @abstractmethod
    def get(self) -> JSON:
        pass


@logger
class ModelController(AbcController):
    def __init__(self, master, slave):
        super().__init__(master, slave)

    def post(self, request: JSON) -> JSON:
        try:
            self.slave = self.slave(**json.loads(request))
        except Exception as ex:
            return JSON(json.dumps(dict(response=400, exeption=str(ex))))
        else:
            return JSON(json.dumps(dict(response=200)))

    def get(self) -> JSON:
        try:
            result = self.slave.get()
        except Exception as ex:
            return JSON(json.dumps(dict(response=400, exeption=str(ex))))
        else:
            return JSON(json.dumps(dict(response=200, result=str(result))))


@logger
class ViewController(AbcController):
    def __init__(self, master, slave):
        super().__init__(master, slave)

    def run_view(self) -> NoReturn:
        while self.slave(self).run():
            pass

    def post(self, request: JSON) -> JSON:
        return JSON(self.master.post(json.dumps(request)))

    def get(self) -> JSON:
        return JSON(json.loads(self.master.get()))


@logger
class Controller(AbcController):
    def __init__(self, view: Any, model: Any):
        super().__init__(ViewController(self, view), ModelController(self, model))

    def post(self, request: JSON) -> JSON:
        return self.slave.post(request)

    def get(self) -> JSON:
        return self.slave.get()