# Python 自动化接单作品集

这是一个面向接单展示的 Python 自动化作品集。它包含 5 个可运行项目，覆盖 Excel 报表自动化、公开数据采集、API 报表生成、邮件发送和 SQLite 信息管理系统，目标是把重复的表格整理、数据同步、报表分发和基础数据管理流程变成可复用的小工具。

我可以提供的服务方向：

- 批量清洗 CSV/Excel，并生成汇总报表。
- 调用公开 API 或客户授权 API，整理成 Excel。
- 按关键词采集允许访问的公开数据，并输出结构化表格。
- 把生成好的报表作为邮件附件自动发送给指定人员。
- 把 Excel/CSV 资料升级成可查询、可统计、可导出的轻量数据库工具。
- 为重复办公流程制作简单、可运行、可交付的 Python 自动化脚本。

## 作品列表

| 作品 | 解决的问题 | 输出成果 | 案例文案 |
| --- | --- | --- | --- |
| Excel 自动化报表 | 合并销售表、清洗重复订单、按品类/月度汇总 | `sales_report.xlsx` | [查看案例](projects/01_excel_report_automation/PORTFOLIO_CASE_STUDY.md) |
| 公开数据采集工具 | 按关键词收集公开讨论数据，整理标题、链接和热度 | `hn_stories_report.xlsx` | [查看案例](projects/02_public_data_collector/PORTFOLIO_CASE_STUDY.md) |
| 天气 API 报表小工具 | 调用公开天气 API，生成多个城市的天气报表 | `weather_report.xlsx` | [查看案例](projects/03_api_report_tool/PORTFOLIO_CASE_STUDY.md) |
| 自动发送邮件报表 | 把 Excel 报表作为附件生成邮件预览或发送 | `email_preview.eml` | [查看案例](projects/04_email_report_sender/PORTFOLIO_CASE_STUDY.md) |
| 学生信息管理系统 | 把学生资料保存到 SQLite，支持查询、筛选、统计和导出 | `students_export.csv` | [查看案例](projects/05_student_manager/PORTFOLIO_CASE_STUDY.md) |

## 项目亮点

- **可运行**：每个项目都有命令行入口，可以直接生成示例输出。
- **可交付**：每个项目都有输入样例、输出文件、README 和作品集文案。
- **有测试**：使用 `pytest` 验证核心逻辑，避免只做一次性脚本。
- **有容错**：API 类项目包含超时重试和失败记录。
- **有数据质量报告**：Excel 项目会输出异常日期、非法数量和重复订单记录。
- **有安全边界**：邮件项目只提交示例配置，真实密码和授权码不进入仓库。

## 技术栈

- Python
- pandas
- openpyxl
- requests
- smtplib / EmailMessage
- sqlite3
- pytest
- CSV / Excel / JSON / SQLite / SMTP

## 快速开始

```powershell
cd D:\工作\python-freelance-starter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest
```

## 运行示例

Excel 自动化报表：

```powershell
python -m freelance_starter.excel_report
```

公开数据采集报表：

```powershell
python -m freelance_starter.hn_collector
```

天气 API 报表：

```powershell
python -m freelance_starter.open_meteo_report
```

邮件报表预览：

```powershell
python -m freelance_starter.email_report_sender
```

学生信息管理系统：

```powershell
python -m freelance_starter.student_manager import-csv
python -m freelance_starter.student_manager list
python -m freelance_starter.student_manager stats
```

## 目录结构

```text
freelance_starter/
|-- excel_report.py
|-- hn_collector.py
|-- open_meteo_report.py
|-- email_report_sender.py
`-- student_manager.py

projects/
|-- 01_excel_report_automation/
|-- 02_public_data_collector/
|-- 03_api_report_tool/
|-- 04_email_report_sender/
`-- 05_student_manager/

tests/
|-- test_excel_report.py
|-- test_hn_collector.py
|-- test_open_meteo_report.py
`-- test_email_report_sender.py
```

## 接单定位

不要只说“我会 Python”。更清楚的表达是：

> 我可以把你的 Excel、CSV、公开数据或第三方 API 数据自动整理成可复用报表，并按需自动发送给指定人员，减少手工复制、清洗、统计和邮件分发。

适合承接的第一批小项目：

- Excel/CSV 批量清洗和汇总。
- 销售、库存、订单、运营日报自动生成。
- 公开 API 数据同步到 Excel。
- 公开关键词数据收集和整理。
- Excel 报表自动邮件发送。
- 学生、会员、客户等小型信息管理和 CSV 导入导出。

## 合规与安全

- 不采集登录后数据、付费墙内容、验证码保护内容或客户未授权数据。
- 不把真实 API Key、邮箱密码、授权码提交到 GitHub。
- 示例数据用于作品集展示，不包含真实客户隐私。
- 正式客户项目开始前，先确认数据来源、字段范围、运行频率和交付格式。

## 学习与展示建议

1. 跑通 5 个项目，确认都能生成输出文件。
2. 为每个项目截图：输入文件、运行命令、输出报表。
3. 给每个项目录 1 分钟演示视频。
4. 把 `PORTFOLIO_CASE_STUDY.md` 的文案改成自己的表达。
5. 用 `docs/proposal_templates.md` 里的模板去投小单。
