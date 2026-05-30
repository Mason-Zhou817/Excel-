# 自动发送邮件报表

这是一个把 Excel 报表自动发送给客户或团队的 Python 项目。它可以把前面项目生成的 `.xlsx` 报表作为附件，生成邮件预览，或者在配置 SMTP 后真正发送邮件。

默认模式只生成 `.eml` 邮件预览，不会真的发送。只有加上 `--send` 并配置 SMTP 后，才会连接邮箱服务器。

## 客户问题

很多客户不只需要生成报表，还希望每天或每周自动收到报表，例如：

- 每周一把销售 Excel 发给老板。
- 每天早上把天气或运营报表发给团队。
- API 同步完成后自动通知客户。
- 数据采集完成后把结果发给指定邮箱。

这个项目把“生成文件”后面的交付动作也自动化，接单价值比单纯生成 Excel 更高。

## 这个工具做什么

- 读取一个已有报表文件作为附件。
- 生成包含标题、正文和附件的邮件。
- 默认保存 `.eml` 预览文件，方便检查邮件内容。
- 支持从 `email_settings.env` 读取 SMTP 配置。
- 支持通过 `--send` 真正发送邮件。
- 真实邮箱密码不进入 GitHub，只提交示例配置。

## 项目结构

```text
projects/04_email_report_sender/
|-- input/
|   `-- email_settings.example.env
|-- output/
|   |-- .gitkeep
|   `-- email_preview.eml
|-- PORTFOLIO_CASE_STUDY.md
`-- README.md
```

核心脚本：

```text
freelance_starter/email_report_sender.py
```

测试文件：

```text
tests/test_email_report_sender.py
```

## 快速运行：生成邮件预览

在项目根目录运行：

```powershell
cd D:\工作\python-freelance-starter
.\.venv\Scripts\Activate.ps1
python -m freelance_starter.email_report_sender
```

默认会把天气 API 项目的报表作为附件：

```text
projects/03_api_report_tool/output/weather_report.xlsx
```

并生成邮件预览：

```text
projects/04_email_report_sender/output/email_preview.eml
```

## 指定自己的附件

```powershell
python -m freelance_starter.email_report_sender `
  --attachment "D:\工作\python-freelance-starter\projects\02_public_data_collector\output\hn_stories_report.xlsx" `
  --subject "Weekly public data report" `
  --preview-output "D:\工作\python-freelance-starter\projects\04_email_report_sender\output\email_preview.eml"
```

## 配置真实发送

先复制示例配置：

```powershell
Copy-Item `
  projects\04_email_report_sender\input\email_settings.example.env `
  projects\04_email_report_sender\input\email_settings.env
```

然后编辑：

```text
projects/04_email_report_sender/input/email_settings.env
```

填写真实 SMTP 信息：

```text
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=reports@example.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

EMAIL_FROM=reports@example.com
EMAIL_TO=client@example.com
```

注意：很多邮箱需要使用“应用专用密码”或“授权码”，不是网页登录密码。

发送邮件：

```powershell
python -m freelance_starter.email_report_sender --send
```

## 安全边界

- 不把真实密码、授权码、客户邮箱提交到 GitHub。
- `email_settings.env` 已经被 `.gitignore` 忽略。
- 仓库只提交 `email_settings.example.env`。
- 第一次测试先用预览模式，确认附件和正文没问题后再发送。

## 验证

运行这个项目的测试：

```powershell
pytest tests/test_email_report_sender.py
```

运行全部项目测试：

```powershell
pytest
```

## 用到的技能

- Python 命令行工具：`argparse`
- 邮件构造：`email.message.EmailMessage`
- SMTP 发送：`smtplib`
- 附件处理：`mimetypes`、二进制文件读取
- 配置管理：环境变量和 `.env` 风格配置文件
- 安全习惯：示例配置与真实密钥分离
- 自动化测试：用假的 SMTP 对象验证发送流程

## 可接单改造方向

- 把 Excel 报表生成和邮件发送串成一条命令。
- 增加多个附件。
- 增加 HTML 邮件正文。
- 加入日志文件，记录每次发送时间和收件人。
- 配合 Windows 任务计划程序做每日/每周定时发送。
- 改造成企业微信、钉钉、Slack、Telegram 通知。
