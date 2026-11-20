"""Автоматичні перевірки бізнес-логіки без зовнішніх бібліотек."""

import unittest

from student_manager.models import Student
from student_manager.services import (
    DuplicateStudentError,
    add_student,
    calculate_group_average,
    filter_by_group,
    find_best_student,
    find_students,
    group_statistics,
    sort_students,
)


class TestStudentModel(unittest.TestCase):
    def test_full_name_and_trim(self) -> None:
        student = Student(" Павло ", " Піхоцький ", " ФеП-31 ", 90)
        self.assertEqual(student.full_name, "Павло Піхоцький")
        self.assertEqual(student.group, "ФеП-31")

    def test_empty_first_name_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            Student(" ", "Піхоцький", "ФеП-31", 88)

    def test_grade_below_zero_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            Student("Павло", "Піхоцький", "ФеП-31", -1)

    def test_grade_above_hundred_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            Student("Павло", "Піхоцький", "ФеП-31", 101)

    def test_nan_grade_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            Student("Павло", "Піхоцький", "ФеП-31", float("nan"))


class TestStudentServices(unittest.TestCase):
    def setUp(self) -> None:
        self.students = [
            Student("Павло", "Піхоцький", "ФеП-31", 92),
            Student("Іван", "Мельник", "ФеП-31", 78),
            Student("Марія", "Бондар", "ФеП-32", 95),
        ]

    def test_filter_by_group(self) -> None:
        self.assertEqual(len(filter_by_group(self.students, "феп-31")), 2)

    def test_calculate_group_average(self) -> None:
        group = filter_by_group(self.students, "ФеП-31")
        self.assertEqual(calculate_group_average(group), 85.0)

    def test_empty_average(self) -> None:
        self.assertEqual(calculate_group_average([]), 0.0)

    def test_find_best_student(self) -> None:
        self.assertEqual(find_best_student(self.students), self.students[2])

    def test_best_student_empty(self) -> None:
        self.assertIsNone(find_best_student([]))

    def test_find_students_by_fragment(self) -> None:
        self.assertEqual(find_students(self.students, "пІХ"), [self.students[0]])

    def test_find_students_no_query(self) -> None:
        self.assertEqual(find_students(self.students, "   "), [])

    def test_sort_students_by_grade(self) -> None:
        sorted_students = sort_students(self.students, by="grade", descending=True)
        self.assertEqual([s.average_grade for s in sorted_students], [95.0, 92.0, 78.0])
        self.assertEqual(self.students[0].average_grade, 92.0)

    def test_sort_students_invalid_key(self) -> None:
        with self.assertRaises(ValueError):
            sort_students(self.students, by="unknown")  # type: ignore[arg-type]

    def test_add_student(self) -> None:
        add_student(self.students, Student("Олена", "Коваль", "ФеП-31", 89))
        self.assertEqual(len(self.students), 4)

    def test_duplicate_student(self) -> None:
        with self.assertRaises(DuplicateStudentError):
            add_student(self.students, Student("павло", "піхоцький", "феп-31", 82))

    def test_group_statistics(self) -> None:
        result = group_statistics(self.students)
        self.assertEqual(result["ФеП-31"], (2, 85.0))
        self.assertEqual(result["ФеП-32"], (1, 95.0))


if __name__ == "__main__":
    unittest.main()
