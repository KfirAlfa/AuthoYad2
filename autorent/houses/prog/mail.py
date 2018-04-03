import smtplib
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



MY_EMAIL = "yad2fuak@gmail.com"
PASSWORD = "fuckyad2"
MAILING_LIST = ["kfir.alf@gmail.com", "Razlotan12@gmail.com", "lior3122@gmail.com", ""]

class AddSender(object):
    def __init__(self):
        self._server = smtplib.SMTP("smtp.gmail.com:587")
        self._server.ehlo()
        self._server.starttls()
        self._server.login(MY_EMAIL, PASSWORD)

    def send_new_adds(self, adds):
        msg = MIMEMultipart()
        msg["Subject"] = u"New apt {time}".format(time=time.ctime(time.time()))

        adds = u"\n".join([unicode(add) for add in adds])

        body = MIMEText(adds.encode("utf-8"), "plain", "utf-8")
        msg.attach(body)
        #self._server.sendmail(MY_EMAIL, MAILING_LIST, msg.as_string())



