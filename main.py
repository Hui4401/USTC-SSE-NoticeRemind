import requests
from bs4 import BeautifulSoup
import datetime
from smtplib import SMTP
from email.mime.text import MIMEText

import config


BASE_URL = 'http://mis.sse.ustc.edu.cn'
VALID_URL = BASE_URL + '/ValidateCode.aspx?ValidateCodeType=1&0.011150883024061309'
SSE_URL = BASE_URL + '/default.aspx'
HOME_PAGE = BASE_URL + '/homepage/StuHome.aspx'


# 计算验证码数字之和
def calculate_code(codes):
    res = 0
    for code in codes:
        res += int(code)
    return res


def sendmail(title, author, time, content):
    msg = MIMEText(content, 'html')
    msg['subject'] = title + ' ' + author + ' ' + time
    msg["from"] = 'NoticeReminder'
    msg["to"] = ','.join(config.SMTP_RECIVER)
    with SMTP(config.SMTP_HOST, config.SMTP_PORT) as smtp:
        smtp.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        smtp.sendmail(config.SMTP_SENDER, config.SMTP_RECIVER, msg.as_string())


# 解析公告列表，每个公告形式：(标题，发布人，时间，详细链接)
def parse_notice(html):
    notices = []
    soup = BeautifulSoup(html, 'lxml')
    notice_nodes = soup.find(id="global_LeftPanel_UpRightPanel_ContentPanel2_ContentPanel3_content").find_all('tr')
    for node in notice_nodes:
        title = node.find_all('td')[0].text
        author = node.find_all('td')[1].text
        time = node.find_all('td')[2].text
        link = BASE_URL + node.find_all('td')[0].a['href']
        notices.append((title, author, time, link))
    return notices


def main():
    year  = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day   = datetime.datetime.now().day
    cur_date = str(year) + "-" + str(month) + "-" + str(day)
    with requests.Session() as s:
        res = s.get(VALID_URL)
        codes = res.cookies['CheckCode']
        code = calculate_code(codes)
        data = {
            '__EVENTTARGET' : 'winLogin$sfLogin$ContentPanel1$btnLogin',
            'winLogin$sfLogin$txtUserLoginID' : config.USERNAME,
            'winLogin$sfLogin$txtPassword' : config.PASSWORD,
            'winLogin$sfLogin$txtValidate' : code,
        }
        s.post(SSE_URL, data=data)
        res = s.get(HOME_PAGE)
        notices = parse_notice(res.text)
        for notice in notices:
            if notice[2] == cur_date:
                res = s.get(notice[3])
                content = res.text
                sendmail(notice[0], notice[1], notice[2], content)


if __name__ == '__main__':
    main()