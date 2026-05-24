# 作品 1：销售 Excel 自动化报表

这是一个面向小商家、运营团队和销售团队的 Python 自动化报表项目。它把多个销售 CSV/Excel 文件合并在一起，自动清洗重复订单和异常数据，然后生成可以直接交付的 Excel 汇总报表。

## 客户问题

客户每周或每月都会收到多个销售明细表，原本需要手工完成这些重复工作：

- 把多个文件复制到一个总表。
- 删除重复订单和无效数据。
- 按商品品类统计销量和收入。
- 整理成老板或客户能看的 Excel 报表。

这个项目把上面的流程变成一条命令，适合包装成“Excel 报表自动化”“销售数据清洗”“月度经营报表生成”等接单服务。

## 这个工具做什么

- 批量读取 `input` 文件夹里的 `.csv`、`.xlsx`、`.xls` 文件。
- 统一字段名，清理订单号、客户名、商品名等文本字段。
- 自动过滤无效日期、空订单号、非正数数量和异常价格。
- 按 `order_id` 去重，保留最新出现的订单记录。
- 计算每条订单收入：`quantity * unit_price`。
- 生成按品类汇总和按月份汇总的数据表。
- 输出带多个工作表和柱状图的 Excel 报表。

## 项目结构

```text
projects/01_excel_report_automation/
├─ input/
│  ├─ sales_q1.csv
│  └─ sales_q2.csv
├─ output/
│  ├─ category_summary.csv
│  └─ sales_report.xlsx
├─ PORTFOLIO_CASE_STUDY.md
└─ README.md
```

核心脚本在：

```text
freelance_starter/excel_report.py
```

测试在：

```text
tests/test_excel_report.py
```

## 输入样例

当前样例输入是两个季度销售文件：

- `input/sales_q1.csv`
- `input/sales_q2.csv`

需要包含这些字段：

```text
order_id,date,customer,product,category,region,salesperson,quantity,unit_price
```

## 输出成果

运行后会生成：

- `output/sales_report.xlsx`
- `output/category_summary.csv`

Excel 文件包含 3 个工作表：

- `cleaned_orders`：清洗后的订单明细。
- `summary_by_category`：按品类汇总销量和收入，并带柱状图。
- `monthly_trend`：按月份汇总订单数、销量和收入。

当前样例数据的处理结果：

| 指标 | 数值 |
| --- | ---: |
| 原始行数 | 12 |
| 清洗后订单数 | 11 |
| 去重订单数 | 1 |
| 汇总品类数 | 3 |

品类收入汇总：

| 品类 | 销量 | 收入 |
| --- | ---: | ---: |
| Electronics | 34 | 609.50 |
| Office | 76 | 606.00 |
| Home | 33 | 348.80 |

## 快速运行

在项目根目录运行：

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.excel_report
```

成功后终端会显示类似结果：

```text
Report created: ...\output\sales_report.xlsx | source rows=12 clean rows=11 categories=3
```

## 自定义输入输出

如果客户给了自己的文件夹，可以这样指定路径：

```powershell
python -m freelance_starter.excel_report `
  --input-dir "D:\客户资料\sales_input" `
  --output "D:\客户资料\sales_report.xlsx" `
  --summary-csv "D:\客户资料\category_summary.csv"
```

## 验证

运行第一个项目相关测试：

```powershell
pytest tests/test_excel_report.py
```

也可以运行全部项目测试：

```powershell
pytest
```

## 用到的技能

- Python 命令行工具开发：`argparse`
- 表格数据处理：`pandas`
- Excel 文件生成和图表：`openpyxl`
- 数据清洗：字段标准化、缺失值过滤、重复订单处理
- 自动化交付：固定输入目录、固定输出文件、可配置路径
- 基础测试：用 `pytest` 验证清洗和汇总逻辑

## 作品集展示建议

发布这个项目时，建议准备 4 个展示素材：

- 输入文件截图：展示两个原始 CSV。
- 终端运行截图：展示一条命令生成报表。
- 输出 Excel 截图：展示 `summary_by_category` 和柱状图。
- 代码仓库截图：展示 README、脚本和测试文件结构。

可以直接复制的作品集文案放在：

```text
PORTFOLIO_CASE_STUDY.md
```

## 可接单改造方向

- 把样例字段换成客户真实字段。
- 增加地区、渠道、销售员、SKU 等统计维度。
- 增加固定 Excel 模板、公司 logo 和品牌配色。
- 自动把报表发送到邮箱或企业微信。
- 打包成 `.exe`，让不会 Python 的客户双击运行。
- 加入定时任务，每天或每周自动生成报表。
