from abc import ABC
from typing import TypeVar, Iterable, Generic, Tuple, Optional

from pycommons.base.container import IntegerContainer
from pycommons.base.function import Predicate
from pycommons.base.function.predicate import PassingPredicate, FailingPredicate
from pycommons.base.utils import ObjectUtils

_T = TypeVar("_T")


class DecoratedPredicate(Predicate[_T], Generic[_T], ABC):
    def __init__(
        self, predicates: Iterable[Predicate[_T]], empty_predicate: Optional[Predicate[_T]]
    ):
        self._predicates = []

        for predicate in predicates:
            ObjectUtils.require_not_none(predicate)
            self._predicates.append(predicate)

        if len(self._predicates) == 0 and empty_predicate:
            self._predicates.append(empty_predicate)

    def get_predicates(self) -> Tuple[Predicate[_T], ...]:
        return tuple(self._predicates)


class AllPredicate(DecoratedPredicate[_T], Generic[_T]):
    """
    A Predicate that returns True if all the predicates that it is decorating is True.
    If the decorated predicate list is empty, the predicate returns True
    """

    def __init__(self, predicates: Iterable[Predicate[_T]]):
        super().__init__(predicates, PassingPredicate())

    def test(self, value: _T) -> bool:
        """
        Test a value. Returns True if all the predicates return True. This is a short-circuiting
        operation, i.e. returns False if any one of the predicate returns False and does not
        perform a test on all the predicates in the list.
        Args:
            value: Value to be tested.

        Returns:
            True if all the predicates returns True
        """
        for predicate in self._predicates:
            if not predicate.test(value):
                return False
        return True


class AnyPredicate(DecoratedPredicate[_T], Generic[_T]):
    """
    A Predicate that returns True if all the predicates that it is decorating is True.
    If the decorated predicate list is empty, the predicate returns False
    """

    def __init__(self, predicates: Iterable[Predicate[_T]]):
        super().__init__(predicates, FailingPredicate())

    def test(self, value: _T) -> bool:
        """
        Test a value. Returns True if any of the predicates return True. This is a short-circuiting
        operation, i.e. returns True if any one of the predicate returns True and does not
        perform a test on all the predicates in the list.
        Args:
            value: Value to be tested.

        Returns:
            True if any the predicates returns True
        """
        for predicate in self._predicates:
            if predicate.test(value):
                return True
        return False


class NeitherPredicate(DecoratedPredicate[_T], Generic[_T]):
    """
    A Predicate that returns True if neither of the predicates that it is decorating is True.
    If the decorated predicate list is empty, the predicate returns True
    """

    def __init__(self, predicates: Iterable[Predicate[_T]]):
        super().__init__(predicates, FailingPredicate())

    def test(self, value: _T) -> bool:
        """
        Test a value. Returns True if neither of the predicates return True.
        This is a short-circuiting operation, i.e. returns False if any one
        of the predicate returns True and does not perform a test on all
        the predicates in the list.
        Args:
            value: Value to be tested.

        Returns:
            True if neither the predicates returns True
        """
        for predicate in self._predicates:
            if predicate.test(value):
                return False
        return True


class ExactCountPredicate(DecoratedPredicate[_T], Generic[_T]):
    def test(self, value: _T) -> bool:
        if self._decorated:
            return self._decorated.test(value)

        count: IntegerContainer = IntegerContainer()
        for predicate in self._predicates:
            if predicate.test(value):
                count.increment()

                if count.get() > self._expected_count:
                    return False

        return count.get() == self._expected_count

    def get_predicates(self) -> Tuple[Predicate[_T], ...]:
        if self._decorated:
            return self._decorated.get_predicates()
        return super().get_predicates()

    def __init__(self, predicates: Iterable[Predicate[_T]], count: int):
        super().__init__(predicates, None)

        if count > len(self._predicates):
            raise ValueError("count is greater than the number of decorated predicates")

        self._decorated: Optional[DecoratedPredicate[_T]] = None
        self._expected_count = count
        if count == 0:
            self._decorated = NeitherPredicate(self._predicates)
        elif count == len(self._predicates) or count < 0:
            self._decorated = AllPredicate(self._predicates)
            self._expected_count = len(self._predicates)


class ExactOnePredicate(ExactCountPredicate[_T], Generic[_T]):
    def __init__(self, predicates: Iterable[Predicate[_T]]):
        super().__init__(predicates, 1)


class AndPredicate(DecoratedPredicate[_T], Generic[_T]):
    def __init__(self, predicate1: Predicate[_T], predicate2: Predicate[_T]):
        super().__init__((predicate1, predicate2), None)

    def test(self, value: _T) -> bool:
        return self._predicates[0].test(value) and self._predicates[1].test(value)


class OrPredicate(DecoratedPredicate[_T], Generic[_T]):
    def __init__(self, predicate1: Predicate[_T], predicate2: Predicate[_T]):
        super().__init__((predicate1, predicate2), None)

    def test(self, value: _T) -> bool:
        return self._predicates[0].test(value) and self._predicates[1].test(value)


class NotPredicate(DecoratedPredicate[_T], Generic[_T]):
    def __init__(self, predicate: Predicate[_T]):
        super().__init__((predicate,), None)

    def test(self, value: _T) -> bool:
        return not self._predicates[0].test(value)


class ValuedPredicate(Predicate[_T], Generic[_T], ABC):
    def __init__(self, value: _T):
        self._value: _T = value


class IdentityPredicate(ValuedPredicate[_T], Generic[_T]):
    def test(self, value: _T) -> bool:
        return value is self._value


class EqualsPredicate(ValuedPredicate[_T], Generic[_T]):
    def test(self, value: _T) -> bool:
        return value == self._value


class NotEqualsPredicate(ValuedPredicate[_T], Generic[_T]):
    def test(self, value: _T) -> bool:
        return value != self._value


NonePredicate = IdentityPredicate(None)
NoneIsTruePredicate = NonePredicate
NoneIsFalsePredicate = NotPredicate(NonePredicate)


class IterableValuedPredicate(Predicate[_T], Generic[_T], ABC):
    def __init__(self, iterable: Iterable[_T]):
        self._value_iterable: Iterable[_T] = iterable


class InPredicate(IterableValuedPredicate[_T], Generic[_T]):
    def test(self, value: _T) -> bool:
        return value in self._value_iterable


class NotInPredicate(Predicate[_T], Generic[_T]):
    def __init__(self, value: Iterable[_T]):
        self._value_iterable: Iterable[_T] = value

    def test(self, value: _T) -> bool:
        return value not in self._value_iterable
