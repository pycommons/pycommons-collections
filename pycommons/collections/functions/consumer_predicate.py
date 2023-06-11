from abc import ABC
from typing import TypeVar, Callable, Type, Generic

from pycommons.base.function import Predicate, Consumer

_T = TypeVar("_T")
_E = TypeVar("_E", Exception, RuntimeError)


class ConsumerRaisesPredicate(Predicate[_T], Consumer[_T], Generic[_T], ABC):

    @classmethod
    def of(cls, consumer: Callable[[_T], None]) -> Consumer[_T]:
        class BasicConsumerRaisesPredicate(ConsumerRaisesPredicate[_T]):
            def accept(self, value: _T) -> None:
                consumer(value)

        return BasicConsumerRaisesPredicate()

    def __init__(self, exception: Type[_E] = Exception):
        self._expected_exception: _E = exception

    def test(self, value: _T) -> bool:
        try:
            self.accept(value)
            return False
        except self._expected_exception:
            return True
        except:
            return False


class ConsumerDoesNotRaisePredicate(Predicate[_T], Consumer[_T], Generic[_T], ABC):

    @classmethod
    def of(cls, consumer: Callable[[_T], None]) -> Consumer[_T]:
        class BasicConsumerDoesNotRaisesPredicate(ConsumerDoesNotRaisePredicate[_T]):
            def accept(self, value: _T) -> None:
                consumer(value)

        return BasicConsumerDoesNotRaisesPredicate()

    def test(self, value: _T) -> bool:
        try:
            self.accept(value)
            return True
        except Exception:
            return False
