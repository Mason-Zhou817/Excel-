# 作品 3：API 报表小工具

## 客户场景

客户有多个门店或城市，需要从第三方 API 拉取数据，整理成每日可读报表。这个样例使用 Open-Meteo 免费公开 API，不需要 API key。

## 运行方式

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.open_meteo_report
```

默认读取 `input/cities.json`，输出 `output/weather_report.xlsx`，包含：

- `current_weather`
- `daily_forecast`

## 可接单改造

- 换成客户的 CRM、ERP、Notion、Airtable、Shopify、OpenWeather 等 API。
- 增加 API key 配置、失败重试、日志和增量同步。
- 把 Excel 输出改成数据库、网页接口或定时邮件。

## 可写在作品集里的描述

我做了一个 API 报表工具，可以批量调用公开 API，把多个城市的实时数据和未来 3 天数据整理成 Excel 报表。这个结构可以改造成客户系统的数据同步和自动报表任务。
