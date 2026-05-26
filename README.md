# Python 接单作品集 Starter

这个文件夹把“Python 自动化 + 数据处理 + 简单 API 集成”的接单计划落成了 3 个可运行作品。你可以先用它练手，再把截图、输出文件和演示视频放到 Upwork、Fiverr、程序员客栈、电鸭、猪八戒等平台的个人资料里。

## 快速开始

```powershell
cd D:\工作\python-freelance-starter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest
```

## 3 个作品

1. **Excel 自动化报表**
   - 合并多个销售表，清洗重复/脏数据，生成 Excel 报表和图表。
   - 作品集案例：`projects/01_excel_report_automation/PORTFOLIO_CASE_STUDY.md`
   - 运行：
     ```powershell
     python -m freelance_starter.excel_report
     ```

2. **公开数据采集工具**
   - 输入关键词，调用 Hacker News 公开搜索 API，导出结构化 CSV/Excel。
   - 作品集案例：`projects/02_public_data_collector/PORTFOLIO_CASE_STUDY.md`
   - 运行：
     ```powershell
     python -m freelance_starter.hn_collector --keyword python --keyword automation
     ```

3. **API 报表小工具**
   - 调用 Open-Meteo 公开天气 API，把多个城市的实时天气和 3 天预报整理成 Excel。
   - 作品集案例：`projects/03_api_report_tool/PORTFOLIO_CASE_STUDY.md`
   - 运行：
     ```powershell
     python -m freelance_starter.open_meteo_report
     ```

## 建议学习顺序

1. 先跑通 3 个项目，确认能生成输出文件。
2. 打开每个项目的 README，按“可接单改造”清单改成自己的版本。
3. 给每个项目录 1 分钟视频：输入、运行、输出、客户能省什么时间。
4. 用 `docs/proposal_templates.md` 里的模板去投小单。
5. 每次接触客户都先用 `docs/client_intake_checklist.md` 确认边界。

## 第一阶段服务定位

不要写“我会 Python”。改成：

> 我可以把你的 Excel、网页公开数据或第三方系统数据自动整理成可复用报表，减少手工复制、清洗和重复统计。

第一批单子优先选 1-3 天内能完成的小项目：Excel 自动化、CSV 清洗、公开 API 数据同步、简单报表生成。
