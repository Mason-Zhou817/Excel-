from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from freelance_starter.paths import ensure_parent, project_path


DEFAULT_DB = project_path("projects", "05_student_manager", "output", "students.db")
STUDENT_COLUMNS = [
    "student_id",
    "name",
    "age",
    "gender",
    "major",
    "phone",
    "email",
    "enrollment_year",
    "status",
]


@dataclass(frozen=True)
class Student:
    student_id: str
    name: str
    age: int
    gender: str
    major: str
    phone: str = ""
    email: str = ""
    enrollment_year: int | None = None
    status: str = "active"


class StudentStore:
    def __init__(self, db_path: Path = DEFAULT_DB) -> None:
        self.db_path = db_path
        ensure_parent(db_path)
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.init_db()

    def close(self) -> None:
        self.connection.close()

    def init_db(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                gender TEXT NOT NULL,
                major TEXT NOT NULL,
                phone TEXT DEFAULT '',
                email TEXT DEFAULT '',
                enrollment_year INTEGER,
                status TEXT DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def add_student(self, student: Student, *, upsert: bool = False) -> None:
        validate_student(student)
        now = timestamp()
        if upsert:
            self.connection.execute(
                """
                INSERT INTO students (
                    student_id, name, age, gender, major, phone, email,
                    enrollment_year, status, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                    name = excluded.name,
                    age = excluded.age,
                    gender = excluded.gender,
                    major = excluded.major,
                    phone = excluded.phone,
                    email = excluded.email,
                    enrollment_year = excluded.enrollment_year,
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                student_values(student, now, now),
            )
        else:
            self.connection.execute(
                """
                INSERT INTO students (
                    student_id, name, age, gender, major, phone, email,
                    enrollment_year, status, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                student_values(student, now, now),
            )
        self.connection.commit()

    def update_student(self, student_id: str, fields: dict[str, Any]) -> bool:
        allowed = set(STUDENT_COLUMNS) - {"student_id"}
        updates = {key: value for key, value in fields.items() if key in allowed and value is not None}
        if not updates:
            return False
        updates["updated_at"] = timestamp()
        assignments = ", ".join(f"{key} = ?" for key in updates)
        values = list(updates.values()) + [student_id]
        cursor = self.connection.execute(
            f"UPDATE students SET {assignments} WHERE student_id = ?",
            values,
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_student(self, student_id: str) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def find_student(self, student_id: str) -> dict[str, Any] | None:
        cursor = self.connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def list_students(
        self,
        *,
        search: str | None = None,
        major: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        clauses: list[str] = []
        values: list[Any] = []
        if search:
            clauses.append("(student_id LIKE ? OR name LIKE ? OR phone LIKE ? OR email LIKE ?)")
            pattern = f"%{search}%"
            values.extend([pattern, pattern, pattern, pattern])
        if major:
            clauses.append("major = ?")
            values.append(major)
        if status:
            clauses.append("status = ?")
            values.append(status)

        sql = "SELECT * FROM students"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY student_id"
        cursor = self.connection.execute(sql, values)
        return [dict(row) for row in cursor.fetchall()]

    def stats_by_major(self) -> list[dict[str, Any]]:
        cursor = self.connection.execute(
            """
            SELECT major, COUNT(*) AS students, ROUND(AVG(age), 1) AS avg_age
            FROM students
            GROUP BY major
            ORDER BY students DESC, major
            """
        )
        return [dict(row) for row in cursor.fetchall()]

    def import_csv(self, path: Path, *, upsert: bool = True) -> int:
        count = 0
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            for item in csv.DictReader(file):
                self.add_student(student_from_mapping(item), upsert=upsert)
                count += 1
        return count

    def export_csv(self, path: Path) -> int:
        rows = self.list_students()
        ensure_parent(path)
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[*STUDENT_COLUMNS, "created_at", "updated_at"],
                extrasaction="ignore",
            )
            writer.writeheader()
            writer.writerows(rows)
        return len(rows)


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def student_values(student: Student, created_at: str, updated_at: str) -> tuple[Any, ...]:
    return (
        student.student_id,
        student.name,
        student.age,
        student.gender,
        student.major,
        student.phone,
        student.email,
        student.enrollment_year,
        student.status,
        created_at,
        updated_at,
    )


def parse_optional_int(value: Any) -> int | None:
    if value is None or str(value).strip() == "":
        return None
    return int(value)


def student_from_mapping(item: dict[str, Any]) -> Student:
    return Student(
        student_id=str(item.get("student_id", "")).strip(),
        name=str(item.get("name", "")).strip(),
        age=int(item.get("age", 0)),
        gender=str(item.get("gender", "")).strip(),
        major=str(item.get("major", "")).strip(),
        phone=str(item.get("phone", "") or "").strip(),
        email=str(item.get("email", "") or "").strip(),
        enrollment_year=parse_optional_int(item.get("enrollment_year")),
        status=str(item.get("status", "active") or "active").strip(),
    )


def validate_student(student: Student) -> None:
    if not student.student_id:
        raise ValueError("student_id is required.")
    if not student.name:
        raise ValueError("name is required.")
    if student.age <= 0:
        raise ValueError("age must be a positive integer.")
    if not student.gender:
        raise ValueError("gender is required.")
    if not student.major:
        raise ValueError("major is required.")


def seed_demo_data(store: StudentStore) -> int:
    students = [
        Student("2026001", "Mason", 18, "male", "AI Engineering", "18800000001", "mason@example.com", 2026),
        Student("2026002", "Alice", 19, "female", "Computer Science", "18800000002", "alice@example.com", 2026),
        Student("2026003", "Bob", 20, "male", "Data Science", "18800000003", "bob@example.com", 2025),
        Student("2026004", "Cindy", 18, "female", "AI Engineering", "18800000004", "cindy@example.com", 2026),
    ]
    for student in students:
        store.add_student(student, upsert=True)
    return len(students)


def print_table(rows: list[dict[str, Any]], columns: list[str]) -> None:
    if not rows:
        print("No records.")
        return
    widths = {
        column: max(len(column), *(len(str(row.get(column, ""))) for row in rows))
        for column in columns
    }
    print(" | ".join(column.ljust(widths[column]) for column in columns))
    print("-+-".join("-" * widths[column] for column in columns))
    for row in rows:
        print(" | ".join(str(row.get(column, "")).ljust(widths[column]) for column in columns))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SQLite student information management tool.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init")
    subparsers.add_parser("demo")
    subparsers.add_parser("stats")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--search")
    list_parser.add_argument("--major")
    list_parser.add_argument("--status")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--student-id", required=True)
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--age", type=int, required=True)
    add_parser.add_argument("--gender", required=True)
    add_parser.add_argument("--major", required=True)
    add_parser.add_argument("--phone", default="")
    add_parser.add_argument("--email", default="")
    add_parser.add_argument("--enrollment-year", type=int)
    add_parser.add_argument("--status", default="active")
    add_parser.add_argument("--upsert", action="store_true")

    export_parser = subparsers.add_parser("export-csv")
    export_parser.add_argument(
        "--output",
        type=Path,
        default=project_path("projects", "05_student_manager", "output", "students_export.csv"),
    )

    import_parser = subparsers.add_parser("import-csv")
    import_parser.add_argument(
        "--file",
        type=Path,
        default=project_path("projects", "05_student_manager", "input", "students.csv"),
    )
    import_parser.add_argument("--no-upsert", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    store = StudentStore(args.db)
    try:
        if args.command == "init":
            print(f"Database ready: {args.db}")
        elif args.command == "demo":
            print(f"Demo students inserted or updated: {seed_demo_data(store)}")
        elif args.command == "list":
            rows = store.list_students(search=args.search, major=args.major, status=args.status)
            print_table(rows, ["student_id", "name", "age", "gender", "major", "phone", "status"])
        elif args.command == "add":
            student = Student(
                args.student_id,
                args.name,
                args.age,
                args.gender,
                args.major,
                args.phone,
                args.email,
                args.enrollment_year,
                args.status,
            )
            store.add_student(student, upsert=args.upsert)
            print(f"Student saved: {student.student_id}")
        elif args.command == "import-csv":
            count = store.import_csv(args.file, upsert=not args.no_upsert)
            print(f"Imported CSV records: {count}")
        elif args.command == "export-csv":
            count = store.export_csv(args.output)
            print(f"Exported records: {count} -> {args.output}")
        elif args.command == "stats":
            print_table(store.stats_by_major(), ["major", "students", "avg_age"])
    except (sqlite3.IntegrityError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    finally:
        store.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
