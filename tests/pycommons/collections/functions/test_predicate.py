from unittest import TestCase

from pycommons.base.function.predicate import PassingPredicate, Predicate, FailingPredicate

from pycommons.collections.functions.predicate import (
    AllPredicate,
    AnyPredicate,
    NeitherPredicate,
    DecoratedPredicate,
    ExactCountPredicate, ExactOnePredicate,
)


class TestAllPredicate(TestCase):
    def test_passing_predicate(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = PassingPredicate()
        predicate3: Predicate[int] = PassingPredicate()
        predicate4: Predicate[int] = PassingPredicate()

        all_predicate: DecoratedPredicate[int] = AllPredicate(
            (predicate1, predicate2, predicate3, predicate4)
        )

        self.assertTrue(all_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), all_predicate.get_predicates()
        )

    def test_failing_predicate(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = PassingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = PassingPredicate()

        all_predicate: DecoratedPredicate[int] = AllPredicate(
            (predicate1, predicate2, predicate3, predicate4)
        )

        self.assertFalse(all_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), all_predicate.get_predicates()
        )

    def test_predicate_when_empty(self):
        all_predicate: DecoratedPredicate[int] = AllPredicate(())
        self.assertTrue(all_predicate.test(1))


class TestAnyPredicate(TestCase):
    def test_passing_predicate(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        any_predicate: DecoratedPredicate[int] = AnyPredicate(
            (predicate1, predicate2, predicate3, predicate4)
        )

        self.assertTrue(any_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), any_predicate.get_predicates()
        )

    def test_failing_predicate(self):
        predicate1: Predicate[int] = FailingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        any_predicate: DecoratedPredicate[int] = AnyPredicate(
            (predicate1, predicate2, predicate3, predicate4)
        )

        self.assertFalse(any_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), any_predicate.get_predicates()
        )

    def test_predicate_when_empty(self):
        all_predicate: DecoratedPredicate[int] = AnyPredicate(())
        self.assertFalse(all_predicate.test(1))


class TestNeitherPredicate(TestCase):
    def test_passing_predicate(self):
        predicate1: Predicate[int] = FailingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        neither_predicate: DecoratedPredicate[int] = NeitherPredicate(
            (predicate1, predicate2, predicate3, predicate4)
        )

        self.assertTrue(neither_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), neither_predicate.get_predicates()
        )

    def test_failing_predicate(self):
        predicate1: Predicate[int] = FailingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = PassingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        neither_predicate: DecoratedPredicate[int] = NeitherPredicate(
            (predicate1, predicate2, predicate3, predicate4)
        )

        self.assertFalse(neither_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), neither_predicate.get_predicates()
        )

    def test_predicate_when_empty(self):
        neither_predicate: DecoratedPredicate[int] = NeitherPredicate(())
        self.assertTrue(neither_predicate.test(1))


class TestExactCountPredicate(TestCase):

    def test_initialization_when_count_greater_than_number_of_predicates(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = PassingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()
        with self.assertRaises(ValueError):
            ExactCountPredicate(
                (predicate1, predicate2, predicate3, predicate4), 8
            )

    def test_passing_predicate(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = PassingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactCountPredicate(
            (predicate1, predicate2, predicate3, predicate4), 2
        )

        self.assertIsNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertTrue(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )

    def test_failing_predicate_when_count_exceeds_expected_count(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = PassingPredicate()
        predicate3: Predicate[int] = PassingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactCountPredicate(
            (predicate1, predicate2, predicate3, predicate4), 2
        )

        self.assertIsNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertFalse(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )

    def test_failing_predicate_when_count_is_less_than_expected_count(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactCountPredicate(
            (predicate1, predicate2, predicate3, predicate4), 2
        )

        self.assertIsNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertFalse(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )

    def test_passing_predicate_when_count_is_same_as_the_length_of_list(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = PassingPredicate()
        predicate3: Predicate[int] = PassingPredicate()
        predicate4: Predicate[int] = PassingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactCountPredicate(
            (predicate1, predicate2, predicate3, predicate4), 4
        )

        self.assertIsNotNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertEqual(AllPredicate, type(exact_count_predicate._decorated))  # pylint: disable=W0212
        self.assertTrue(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )

    def test_failing_predicate_when_count_is_same_as_the_length_of_list(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = PassingPredicate()
        predicate3: Predicate[int] = PassingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactCountPredicate(
            (predicate1, predicate2, predicate3, predicate4), 4
        )

        self.assertIsNotNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertEqual(AllPredicate, type(exact_count_predicate._decorated))  # pylint: disable=W0212
        self.assertFalse(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )

    def test_passing_predicate_when_count_is_zero(self):
        predicate1: Predicate[int] = FailingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactCountPredicate(
            (predicate1, predicate2, predicate3, predicate4), 0
        )

        self.assertIsNotNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertEqual(NeitherPredicate, type(exact_count_predicate._decorated))  # pylint: disable=W0212
        self.assertTrue(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )

    def test_failing_predicate_when_count_is_zero(self):
        predicate1: Predicate[int] = FailingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = PassingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactCountPredicate(
            (predicate1, predicate2, predicate3, predicate4), 0
        )

        self.assertIsNotNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertEqual(NeitherPredicate, type(exact_count_predicate._decorated))  # pylint: disable=W0212
        self.assertFalse(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )


class TestExactOnePredicate(TestCase):

    def test_passing_predicate(self):
        predicate1: Predicate[int] = PassingPredicate()
        predicate2: Predicate[int] = FailingPredicate()
        predicate3: Predicate[int] = FailingPredicate()
        predicate4: Predicate[int] = FailingPredicate()

        exact_count_predicate: ExactCountPredicate[int] = ExactOnePredicate(
            (predicate1, predicate2, predicate3, predicate4),
        )

        self.assertEqual(1, exact_count_predicate._expected_count)  # pylint: disable=W0212
        self.assertIsNone(exact_count_predicate._decorated)  # pylint: disable=W0212
        self.assertTrue(exact_count_predicate.test(1))
        self.assertTupleEqual(
            (predicate1, predicate2, predicate3, predicate4), exact_count_predicate.get_predicates()
        )
