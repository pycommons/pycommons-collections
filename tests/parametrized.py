import dataclasses
import functools
from typing import Any, Optional, List


@dataclasses.dataclass
class TestData:
    data: Any
    expected: Any

    message: Optional[str] = None

    def get_message(self):
        return (
            f"{self.message if self.message else 'TestCase'} "
            f"(data={self.data}, expected={self.expected})"
        )


def cases(testcases: List[TestData]):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(self):
            for case in testcases:
                with self.subTest(case.get_message()):
                    f(self, case)

        return wrapped

    return decorator
