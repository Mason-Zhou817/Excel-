# 作品 2：公开数据采集工具

## 客户场景

客户想跟踪某些关键词在公开站点上的讨论，例如竞品、技术趋势、行业词。这个工具调用 Hacker News 的公开搜索 API，导出结构化数据，避免手动搜索和复制。

## 运行方式

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.hn_collector --keyword python --keyword automation
```

也可以直接读取 `input/keywords.txt`：

```powershell
python -m freelance_starter.hn_collector
```

默认输出 `output/hn_stories.csv`。

## 合规边界

- 只采集公开 API 或允许访问的公开页面。
- 不绕过登录、验证码、付费墙、反爬限制。
- 不采集私人信息或敏感账号数据。

## 可接单改造

- 换成客户指定的公开 API。
- 增加字段筛选、定时运行、去重、邮件推送。
- 输出 Excel、CSV、Google Sheets 或数据库。

## 可写在作品集里的描述

我做了一个关键词数据采集工具，输入关键词后自动调用公开 API，整理标题、链接、作者、评论数等字段，并导出为 CSV/Excel，适合竞品监控和内容选题收集。
