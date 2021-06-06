# USTC-SSE-Notice-Remind
中科大软件学院信息化平台通知提醒，该脚本可以登录信息化平台查询当日公告、通知并发送到指定接收邮箱，配合服务器定时任务使用，避免错过重要通知

## Install

```bash
git clone https://github.com/Hui4401/USTC-SSE-NoticeRemind.git
```

## Usage

首先确保系统已有 Python3.8+ 环境并安装第三方包 requests、beautifulsoup4、lxml

然后修改 config.py 中的配置信息，设置自己的信息化平台账号、smtp账号、接收邮箱等

执行 main.py 即可查询当日公告，可部署到云服务器设置每日定时任务来进行自动化提醒，定时任务见 Crontab

## License

[GPLv3](LICENSE) © Hui4401