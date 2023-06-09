from typing import TypeVar, List, Optional, Iterable, Generic, Union

_T = TypeVar("_T")


class OrderedSet(set, Generic[_T]):

    def __init__(self, iterable: Optional[Iterable[_T]] = None):
        super().__init__(iterable)
        self._order: List[_T] = list()

        _copy_set = set()
        for _set_item in iter(iterable):
            if _set_item not in _copy_set:
                self._order.append(_set_item)
                _copy_set.add(_set_item)

    def add(self, element: _T) -> None:
        if element not in self:
            self._order.append(element)

        super().add(element)

    def discard(self, element: _T) -> None:
        if element in self:
            self._order.remove(element)

    def __iter__(self):
        return iter(self._order)

    def __getitem__(self, item: Union[int, slice]):
        if isinstance(item, slice):
            return OrderedSet(self._order[item])
        return self._order[item]
