import inspect
from typing import Any, Callable, Dict, Type, TypeVar
from fastapi import Request

T = TypeVar("T")


class DependencyContainer:
    def __init__(self):
        self._registrations: Dict[Type, Callable[[], Any]] = {}

    def register(self, abstraction: Type[T], implementation: Callable[[], T]):
        """
        Registra uma implementação para uma abstração no container.
        """
        self._registrations[abstraction] = implementation

    def resolve(self, abstraction: Type[T]) -> T:
        """
        Resolve a dependência registrada para a abstração fornecida.
        """
        if abstraction in self._registrations:
            return self._registrations[abstraction]()
        return None

    def resolve_all(self, obj: Any) -> None:
        """
        Resolve todas as dependências necessárias para uma classe ou função.
        """
        if inspect.isclass(obj):
            for param in inspect.signature(obj.__init__).parameters.values():
                if param.annotation != param.empty and param.annotation != Request:
                    resolved_value = self.resolve(param.annotation)
                    if resolved_value is not None:
                        setattr(obj, param.name, resolved_value)
        elif callable(obj):
            signature = inspect.signature(obj)
            for param in signature.parameters.values():
                if param.annotation != param.empty and param.annotation != Request:
                    param_value = self.resolve(param.annotation)
                    if param_value is not None:
                        obj.__dict__[param.name] = param_value
