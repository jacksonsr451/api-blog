import inspect
from typing import Any, Callable, Dict, Type, TypeVar

T = TypeVar('T')

class DependencyContainer:
    def __init__(self):
        self._registrations: Dict[Type, Callable[[], Any]] = {}

    def register(self, abstraction: Type[T], implementation: Callable[[], T]):
        self._registrations[abstraction] = implementation

    def resolve(self, abstraction: Type[T]) -> T:
        if abstraction not in self._registrations:
            raise ValueError(f'Nenhuma implementação registrada para {abstraction}')
        return self._registrations[abstraction]()

    def resolve_all(self, obj: Any) -> None:
        if inspect.isclass(obj):
            for param in inspect.signature(obj.__init__).parameters.values():
                param_annotation = param.annotation
                if param_annotation != param.empty and param_annotation != None:
                    setattr(obj, param.name, self.resolve(param_annotation))
        elif callable(obj):
            signature = inspect.signature(obj)
            for param in signature.parameters.values():
                param_annotation = param.annotation
                if param_annotation != param.empty:
                    param_value = self.resolve(param_annotation)
                    obj.__dict__[param.name] = param_value


container = DependencyContainer()