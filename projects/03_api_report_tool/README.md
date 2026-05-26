# 天气 API 报表小工具

这是一个面向门店运营、物流、出行、活动策划等场景的 API 自动报表项目。它读取城市配置，调用 Open-Meteo 免费公开天气 API，把多个城市的实时天气和未来 3 天预报整理成 Excel 报表。

这个项目的重点不是天气本身，而是练习真实接单中很常见的流程：读取配置、调用第三方 API、处理 JSON、容错重试、整理成 Excel。

## 客户问题

客户可能每天都需要查看多个城市或门店所在地的天气，例如：

- 连锁门店需要关注不同城市温度和降雨。
- 活动团队需要提前查看未来几天天气。
- 物流或外勤团队需要把公开天气数据整理成日报。
- 运营负责人希望每天收到一份固定格式的 Excel。

如果手工打开网页查每个城市，再复制到表格里，既重复又容易漏。这个工具把流程变成一条命令。

## 这个工具做什么

- 读取 `input/cities.json` 中配置的城市名称、纬度、经度。
- 调用 Open-Meteo Forecast API。
- 获取当前温度、湿度、风速。
- 获取未来 3 天最高温、最低温、降水量。
- API 超时或失败时自动重试。
- 某个城市失败时，不中断整个报表，而是把失败原因写入 `api_errors`。
- 输出带多个工作表和基础格式的 Excel 报表。

## 项目结构

```text
projects/03_api_report_tool/
├─ input/
│  └─ cities.json
├─ output/
│  └─ weather_report.xlsx
├─ PORTFOLIO_CASE_STUDY.md
└─ README.md
```

核心脚本在：

```text
freelance_starter/open_meteo_report.py
```

测试在：

```text
tests/test_open_meteo_report.py
```

## 输入配置

`input/cities.json` 示例：

```json
[
  {
    "name": "Shanghai",
    "latitude": 31.2304,
    "longitude": 121.4737
  },
  {
    "name": "Beijing",
    "latitude": 39.9042,
    "longitude": 116.4074
  }
]
```

每个城市必须包含：

- `name`
- `latitude`
- `longitude`

## 输出成果

默认输出：

```text
output/weather_report.xlsx
```

Excel 文件包含 4 个工作表：

- `report_summary`：报表运行摘要，包括配置城市数、成功城市数、失败城市数。
- `current_weather`：每个城市的当前温度、湿度、风速。
- `daily_forecast`：每个城市未来 3 天的最高温、最低温、降水量。
- `api_errors`：API 请求失败的城市和失败原因。

## 快速运行

在项目根目录运行：

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.open_meteo_report
```

成功后终端会显示类似结果：

```text
Weather report created for 3/3 city/cities: ...\output\weather_report.xlsx
```

## 自定义输入输出

可以指定自己的城市配置和输出位置：

```powershell
python -m freelance_starter.open_meteo_report `
  --cities "D:\客户资料\cities.json" `
  --output "D:\客户资料\weather_report.xlsx"
```

也可以调整 API 超时和重试次数：

```powershell
python -m freelance_starter.open_meteo_report --timeout 30 --retries 3
```

## 验证

运行天气项目测试：

```powershell
pytest tests/test_open_meteo_report.py
```

也可以运行全部项目测试：

```powershell
pytest
```

## 用到的技能

- Python 命令行工具开发：`argparse`
- API 请求：`requests`
- JSON 配置读取：`json`
- 数据整理：`pandas`
- Excel 输出和格式处理：`openpyxl`
- 异常处理：超时、重试、失败记录
- 自动化测试：模拟 API 成功、临时失败、持续失败

## 作品集展示建议

建议准备 4 个展示素材：

- `cities.json` 配置截图。
- 终端运行成功截图。
- `weather_report.xlsx` 中 `report_summary` 和 `daily_forecast` 截图。
- 测试通过截图。

可以直接复制的作品集文案放在：

```text
PORTFOLIO_CASE_STUDY.md
```

## 可接单改造方向

- 换成客户真实 API，例如 CRM、ERP、Notion、Airtable、Shopify、OpenWeather。
- 增加 API key 配置和 `.env` 管理。
- 增加日志文件，记录每次同步结果。
- 自动发送 Excel 到邮箱或企业微信。
- 加入定时任务，每天早上自动生成报表。
- 把 Excel 输出改成数据库、网页接口或仪表盘。
