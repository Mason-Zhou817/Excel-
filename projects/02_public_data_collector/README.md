# 公开数据采集工具

这是一个面向内容选题、行业趋势观察和公开讨论监控的 Python 数据采集项目。它根据关键词调用 Hacker News 的公开搜索 API，把结果整理成带汇总和明细的 Excel 报表。

这个项目练习的是接单里常见的工作流程：客户提供关注关键词，你从允许访问的数据源取得结构化数据，再输出业务人员能继续筛选和阅读的表格。

## 客户问题

客户可能想持续关注某些公开话题，例如：

- 某个技术方向在社区里有没有新的讨论。
- 与产品或行业相关的公开文章线索。
- 可用于内容选题的标题、链接和讨论热度。
- 多个关键词的搜索结果汇总与比较。

手动逐个搜索、复制链接和整理热度字段很耗时。这个工具把它变成可重复运行的报表流程。

## 这个工具做什么

- 从 `input/keywords.txt` 读取需要监控的关键词。
- 也支持在命令行临时传入关键词。
- 调用 Hacker News Algolia Search 公开 API。
- 整理标题、来源网站、链接、作者、积分、评论数和发布时间。
- 请求失败或超时时自动重试。
- 某个关键词失败时，将失败记录写进报表，不中断其他关键词采集。
- 生成 Excel 报表，并在关键词汇总页添加柱状图。

## 合规边界

- 只使用公开 API 或网站明确允许访问的公开数据。
- 不绕过登录、验证码、付费墙或反爬限制。
- 不采集私人信息、敏感账号数据或客户未授权的数据。
- 用于正式客户项目时，应确认目标数据源的使用条款和交付范围。

## 项目结构

```text
projects/02_public_data_collector/
|-- input/
|   `-- keywords.txt
|-- output/
|   |-- hn_stories.csv
|   `-- hn_stories_report.xlsx
|-- PORTFOLIO_CASE_STUDY.md
`-- README.md
```

核心脚本：

```text
freelance_starter/hn_collector.py
```

测试文件：

```text
tests/test_hn_collector.py
```

## 输入配置

默认关键词文件 `input/keywords.txt`：

```text
python
automation
data pipeline
```

你可以把它改成客户需要观察的公开主题，每行填写一个关键词。

## 输出成果

默认输出：

```text
output/hn_stories_report.xlsx
```

Excel 文件包含 3 个工作表：

- `keyword_summary`：每个关键词采集到的文章数、总积分、总评论数，并带柱状图。
- `stories`：文章明细，包括标题、来源网站、链接、作者和讨论数据。
- `api_errors`：请求失败的关键词和失败原因。

一次成功演示中，工具使用 3 个关键词、每个关键词获取 10 条公开结果，共输出 30 行明细。由于来源是实时公开搜索，实际标题和热度会随着时间变化。

## 快速运行

在项目根目录运行：

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.hn_collector
```

成功后会看到类似输出：

```text
Collected 30 rows for 3 keyword(s), failed=0: ...\output\hn_stories_report.xlsx
```

## 临时输入关键词

不修改配置文件，也可以直接搜索新的关键词：

```powershell
python -m freelance_starter.hn_collector `
  --keyword "python automation" `
  --keyword "data reporting" `
  --limit 10
```

## 自定义输出与网络设置

```powershell
python -m freelance_starter.hn_collector `
  --output "D:\客户资料\public_topics_report.xlsx" `
  --timeout 30 `
  --retries 3
```

如果输出文件以 `.csv` 结尾，程序会只导出文章明细表。

## 验证

运行这个项目的测试：

```powershell
pytest tests/test_hn_collector.py
```

运行全部项目测试：

```powershell
pytest
```

## 用到的技能

- Python 命令行工具：`argparse`
- 公开 API 调用：`requests`
- 表格数据整理：`pandas`
- Excel 输出、表格格式和图表：`openpyxl`
- 网络异常处理：超时、重试、失败记录
- 数据字段处理：关键词、链接域名、热度指标
- 自动化测试：模拟成功请求和失败请求

## 作品集展示建议

建议准备这些截图：

- `keywords.txt` 中的关键词配置。
- 命令行执行成功结果。
- `keyword_summary` 页和图表。
- `stories` 明细页中的标题、链接和评论数。

可以直接发布的案例文案放在：

```text
PORTFOLIO_CASE_STUDY.md
```

## 可接单改造方向

- 换成客户指定且允许访问的公开 API。
- 增加日期范围、最低热度、来源域名等筛选条件。
- 定时运行并自动邮件发送报表。
- 将输出改为 Google Sheets、数据库或轻量网页看板。
- 进一步做关键词趋势对比和定期增量采集。
