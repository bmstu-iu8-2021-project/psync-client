import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import random
from data_processing import constants


def send_mail(mail, theme, text, code_flag=False):
    code = ''
    if code_flag:
        code = str(random.randint(10000, 99999))
        text = text % code

    msg = MIMEMultipart()
    msg['From'] = constants.EMAIL
    msg['To'] = mail
    mailsender = smtplib.SMTP('smtp.mail.ru', 587)
    mailsender.starttls()
    mailsender.login(constants.EMAIL, constants.PASSWORD)
    mail_body_html = '<html><head><body>' + text + '</body></head></html>'
    msg = MIMEText(mail_body_html, 'html', 'utf-8')
    msg['Subject'] = Header(theme, 'utf-8')
    mailsender.sendmail(constants.EMAIL, mail, msg.as_string())
    mailsender.quit()
    return code
