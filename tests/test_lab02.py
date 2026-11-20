"""Контрольні тести ЛР №2 (тільки стандартна бібліотека)."""

import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from student_manager.lab02.analytics import (
    average_grade,
    average_values,
    create_record,
    find_best_student,
    group_statistics,
    make_grade_filter,
    process_pipeline,
    sort_records,
)
from student_manager.lab02.benchmark import export_csv, generate_records, run_benchmark
from student_manager.lab02.data import FIELDS, load_students
from student_manager.lab02.decorators import measure_time
from student_manager.lab02.processors import (
    OperationHistory,
    count_by_group,
    create_index,
    filter_by_group,
    filter_items,
    find_indexed,
    find_linear,
    group_by_group_and_band,
    group_students,
    unique_groups,
)


class TestLab02Data(unittest.TestCase):
    def setUp(self) -> None:
        self.records = load_students()

    def test_load_from_lab01(self) -> None:
        self.assertEqual(len(self.records), 6)
        self.assertEqual(self.records[0]["name"], "Піхоцький Павло")

    def test_tuple_fields(self) -> None:
        self.assertEqual(FIELDS, ("id", "name", "group", "grade"))

    def test_unique_groups(self) -> None:
        self.assertEqual(unique_groups(self.records), {"ФеП-31", "ФеП-32"})

    def test_create_index(self) -> None:
        index = create_index(self.records)
        self.assertEqual(index[4]["name"], "Бондар Марія")

    def test_reject_duplicate_index(self) -> None:
        with self.assertRaises(ValueError):
            create_index(self.records + [self.records[0]])

    def test_filter_by_group(self) -> None:
        self.assertEqual(len(filter_by_group(self.records, "феп-31")), 4)

    def test_universal_filter(self) -> None:
        self.assertEqual(len(filter_items(self.records, lambda row: row["grade"] >= 90)), 3)

    def test_defaultdict_grouping(self) -> None:
        grouped = group_students(self.records)
        self.assertEqual([len(grouped["ФеП-31"]), len(grouped["ФеП-32"])], [4, 2])

    def test_counter(self) -> None:
        counts = count_by_group(self.records)
        self.assertEqual(dict(counts), {"ФеП-31": 4, "ФеП-32": 2})

    def test_nested_grouping(self) -> None:
        grouped = group_by_group_and_band(self.records)
        self.assertEqual(len(grouped["ФеП-31"]["90–100"]), 2)
        self.assertEqual(len(grouped["ФеП-32"]["90–100"]), 1)

    def test_linear_and_indexed(self) -> None:
        self.assertEqual(find_linear(self.records, 6), find_indexed(create_index(self.records), 6))

    def test_not_found(self) -> None:
        self.assertIsNone(find_linear(self.records, 900))
        self.assertIsNone(find_indexed(create_index(self.records), 900))

    def test_average_grade(self) -> None:
        with redirect_stdout(io.StringIO()):
            value = average_grade(self.records)
        self.assertAlmostEqual(value, 88.25)

    def test_empty_average(self) -> None:
        with redirect_stdout(io.StringIO()):
            self.assertEqual(average_grade([]), 0.0)

    def test_args_average(self) -> None:
        self.assertEqual(average_values(75, 80, 92, 96), 85.75)
        self.assertEqual(average_values(), 0.0)

    def test_kwargs_record(self) -> None:
        row = create_record(id=7, name=" Новак Тарас ", group="ФеП-33", grade=87)
        self.assertEqual(row["name"], "Новак Тарас")
        self.assertEqual(row["grade"], 87.0)

    def test_kwargs_invalid_record(self) -> None:
        with self.assertRaises(ValueError):
            create_record(id=7, name="", group="ФеП-33", grade=87)
        with self.assertRaises(ValueError):
            create_record(id=7, name="А Б", group="ФеП-33", grade=float("nan"))
        with self.assertRaises(ValueError):
            create_record(id=7, name="А Б", group="ФеП-33", grade=101)
        with self.assertRaises(ValueError):
            create_record(id=7, name="А Б", group="ФеП-33")

    def test_sorting(self) -> None:
        sorted_rows = sort_records(self.records, field="grade")
        self.assertEqual(sorted_rows[0]["name"], "Бондар Марія")
        self.assertEqual(self.records[0]["id"], 1)

    def test_sort_unknown_field(self) -> None:
        with self.assertRaises(ValueError):
            sort_records(self.records, field="unknown")

    def test_best(self) -> None:
        self.assertEqual(find_best_student(self.records)["id"], 4)
        self.assertIsNone(find_best_student([]))

    def test_closure(self) -> None:
        predicate = make_grade_filter(90)
        self.assertEqual(sum(predicate(row) for row in self.records), 3)
        with self.assertRaises(ValueError):
            make_grade_filter(-1)

    def test_group_stats(self) -> None:
        result = group_statistics(self.records)
        self.assertEqual(result["ФеП-31"][0], 4)
        self.assertAlmostEqual(result["ФеП-31"][1], 87.625)

    def test_pipeline(self) -> None:
        result = process_pipeline(self.records, minimum=85, group="ФеП-31")
        self.assertEqual([row["id"] for row in result], [1, 6, 2])

    def test_deque(self) -> None:
        history = OperationHistory(2)
        for word in ("a", "b", "c"):
            history.add(word)
        self.assertEqual(history.recent(), ("b", "c"))
        with self.assertRaises(ValueError):
            OperationHistory(0)

    def test_decorator_preserves_name(self) -> None:
        @measure_time("Демонстрація")
        def square(value: int) -> int:
            return value * value

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.assertEqual(square(3), 9)
        self.assertIn("Демонстрація", buffer.getvalue())
        self.assertEqual(square.__name__, "square")

    def test_generate_records(self) -> None:
        rows = generate_records(20)
        self.assertEqual(len(rows), 20)
        self.assertEqual(rows[-1]["id"], 20)
        with self.assertRaises(ValueError):
            generate_records(0)

    def test_small_benchmark_and_csv(self) -> None:
        rows = run_benchmark((50,))
        self.assertEqual(len(rows), 1)
        self.assertGreaterEqual(rows[0].list_us, 0)
        self.assertGreaterEqual(rows[0].index_build_ms, 0)
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "benchmark.csv"
            export_csv(rows, filename)
            with filename.open(encoding="utf-8-sig", newline="") as stream:
                csv_rows = list(csv.DictReader(stream))
            self.assertEqual(csv_rows[0]["records"], "50")


if __name__ == "__main__":
    unittest.main()
