from interfaces.interfaces.abstract_controller_interface import (
    AbstractControllerInterface,
)


class PostControllerInterface(AbstractControllerInterface):
    def __init__(self, service):
        self._service = service
