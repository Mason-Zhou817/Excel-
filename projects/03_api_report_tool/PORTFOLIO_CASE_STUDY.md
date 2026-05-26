# 作品集案例：天气 API 自动报表

## 一句话介绍

我做了一个 Python API 报表工具，可以批量调用公开天气 API，把多个城市的实时天气和未来 3 天预报整理成 Excel 报表，并记录 API 请求失败的城市。

## 客户场景

一个运营团队需要每天查看多个城市的天气情况，用来安排门店运营、活动计划或外勤工作。原本负责人需要手动打开网页查询每个城市，再复制到 Excel。这个流程重复、耗时，而且网络或 API 失败时很难追踪。

## 我的解决方案

我用 Python 做了一个命令行工具，客户只需要维护一个 `cities.json` 城市配置文件，然后运行一条命令，就可以自动生成 Excel 天气报表。

自动化流程：

1. 读取城市名称、纬度、经度。
2. 调用 Open-Meteo 天气 API。
3. 获取当前温度、湿度、风速。
4. 获取未来 3 天最高温、最低温、降水量。
5. API 超时或失败时自动重试。
6. 把成功数据和失败记录一起写入 Excel。

## 交付内容

- 可运行的 Python 脚本。
- 示例城市配置：`cities.json`。
- 示例输出报表：`weather_report.xlsx`。
- 项目 README 和运行说明。
- 自动化测试，覆盖成功、重试、失败记录。

## 报表内容

Excel 报表包含 4 个工作表：

- `report_summary`：运行摘要。
- `current_weather`：城市当前天气。
- `daily_forecast`：未来 3 天预报。
- `api_errors`：失败城市和失败原因。

## 演示命令

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.open_meteo_report
```

## 可以直接发布的作品集文案

我做了一个“天气 API 自动报表”项目，用 Python 批量调用公开天气 API，并把多个城市的实时天气和未来 3 天预报整理成 Excel 报表。工具支持从 JSON 配置读取城市列表，自动处理 API 返回的 JSON 数据，生成包含运行摘要、当前天气、天气预报和错误记录的工作簿。

这个项目模拟的是客户常见的 API 数据同步需求：把第三方系统或公开接口中的数据定时拉取下来，整理成业务人员能直接查看的 Excel。项目可以继续改造成 CRM 数据同步、库存 API 报表、订单 API 报表、Notion/Airtable 自动导出等服务。

技术点：Python、requests、JSON、pandas、openpyxl、Excel 自动化、API 重试、错误记录、pytest 测试。

## 1 分钟演示视频脚本

1. 打开 `cities.json`，展示城市配置。
2. 在终端运行 `python -m freelance_starter.open_meteo_report`。
3. 展示终端输出：成功城市数和报表路径。
4. 打开 `weather_report.xlsx`，展示 `report_summary`、`current_weather`、`daily_forecast`。
5. 说明：这个结构可以替换成客户自己的 API，自动生成每日业务报表。

## 接单时可以怎么说

您好，我可以帮您把第三方 API 或业务系统里的数据自动整理成 Excel 报表。比如每天自动拉取门店、订单、库存、天气、CRM 或 Notion/Airtable 数据，清洗后生成固定格式的报表。如果 API 临时失败，也可以记录失败原因，方便排查和补跑。

## 下一步可升级

- 增加 `.env` API key 配置。
- 增加日志文件和同步时间。
- 自动发送邮件。
- 加入定时任务。
- 做成双击运行的小工具。
