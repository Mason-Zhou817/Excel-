# 作品 5：SQLite 学生信息管理系统

这是一个小型信息管理系统项目，用 SQLite 保存学生资料，支持导入、查询、筛选、统计和导出。它适合展示 CRUD、数据库、CSV 导入导出和命令行工具开发能力。

## 这个工具做什么

- 初始化 SQLite 数据库。
- 从 `input/students.csv` 导入学生信息。
- 支持按姓名、学号、手机号、邮箱模糊搜索。
- 支持按专业和状态筛选。
- 支持添加单个学生。
- 支持按专业统计人数和平均年龄。
- 支持把所有学生导出成 CSV。

## 项目结构

```text
projects/05_student_manager/
├─ input/
│  └─ students.csv
├─ output/
│  ├─ students.db
│  └─ students_export.csv
└─ README.md
```

核心脚本在：

```text
freelance_starter/student_manager.py
```

## 快速运行

在项目根目录运行：

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.student_manager init
python -m freelance_starter.student_manager import-csv
python -m freelance_starter.student_manager list
python -m freelance_starter.student_manager stats
python -m freelance_starter.student_manager export-csv
```

## 添加学生

```powershell
python -m freelance_starter.student_manager add `
  --student-id 2026005 `
  --name David `
  --age 19 `
  --gender male `
  --major "Data Science" `
  --phone 18800000005
```

## 可接单改造方向

- 把 CSV 导入换成 Excel 导入。
- 增加 Flask 或 Streamlit 页面。
- 增加登录、权限和操作日志。
- 增加班级、课程、成绩、缴费等模块。
- 导出固定模板的 Excel 报表。
