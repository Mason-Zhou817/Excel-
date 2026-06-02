from __future__ import annotations

from pathlib import Path

from freelance_starter.student_manager import Student, StudentStore


def test_student_store_add_list_stats_and_export(tmp_path: Path) -> None:
    db_path = tmp_path / "students.db"
    export_path = tmp_path / "students.csv"
    store = StudentStore(db_path)

    try:
        store.add_student(
            Student(
                "2026001",
                "Mason",
                18,
                "male",
                "AI Engineering",
                "18800000001",
            )
        )
        store.add_student(
            Student(
                "2026002",
                "Alice",
                19,
                "female",
                "Computer Science",
                "18800000002",
            )
        )

        rows = store.list_students(search="Mason")
        stats = store.stats_by_major()
        exported = store.export_csv(export_path)

        assert rows[0]["student_id"] == "2026001"
        assert {row["major"] for row in stats} == {"AI Engineering", "Computer Science"}
        assert exported == 2
        assert export_path.exists()
    finally:
        store.close()
