from bs4 import BeautifulSoup
import email
from email import parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.message import MIMEMessage
import poplib
import smtplib
import time

from rate_results import get_email_result
# pip install BeautifulSoup4

def get_message_info(message):
    message_info = parser.Parser().parsestr("\n".join(message))
    sender = message_info['From']
    subj = message_info['Subject']
    msg_id = message_info["Message-ID"]
    return  msg_id, sender, subj

def covert_html_to_text(message):
    soup = BeautifulSoup(message)
    return soup.get_text()

def get_message_text(message):
    for idx, item in enumerate(message):
        if type(item) == str:
            if item.startswith('<div'):
                first_div_idx = idx
                break

    item = message[first_div_idx]
    div_open = item.count('<div')
    div_close = item.count('</div>')
    text_message = item
    for i, item in enumerate(message[idx+1:]):
        if type(item) == str:
            if div_open == div_close:
                break
            div_open += item.count('<div')
            div_close += item.count('</div>')
            text_message += item
    
    return text_message

class EmailHandler:
    pop_conn = None
    mail_server = None
    emails_answered = 0

    def record_answered_mails(self):
        with open("last_answered_email.txt", 'w') as out:
            out.write(str(self.emails_answered))

    def load_answered_mails(self):
        try:
            with open("last_answered_email.txt", 'r') as in_file:
                self.emails_answered = eval(in_file.read())
        except Exception:
            self.emails_answered = 0

    def connect(self):
        while True:
            try:
                user_name = 'git_helper@yahoo.com'
                password = '123456aBc'
                print 'checking mail'
                pop_conn = poplib.POP3_SSL('pop.mail.yahoo.com')
                print "pop3 Connection made"
                pop_conn.user(user_name)
                pop_conn.pass_(password)
                MAIL_SERVER = 'smtp.mail.yahoo.com'
                mail_server = smtplib.SMTP(MAIL_SERVER, 587)
                mail_server.starttls()
                mail_server.login(user_name, password)
                print 'smtp Connection made'
                break
            except Exception as e: # handshake error, try till succede
                time.sleep(10)
        self.pop_conn = pop_conn
        self.mail_server = mail_server


    def check_mail(self):
        self.connect()
       
        self.load_answered_mails()
        while True:
            try:
                numMessages = len(self.pop_conn.list()[1])
                should_record = self.emails_answered < numMessages
                for i in range(self.emails_answered, numMessages):
                    try:
                        msg = self.pop_conn.retr(i+1)[1] # new statement
                        msg_text = get_message_text(msg)
                        msg_text = covert_html_to_text(msg_text)
                        msg_response = get_email_result(msg_text)
                        msg_id, sender, subj = get_message_info(msg)
                        self.send_mail(msg_id, sender, subj, msg_response)
                    except Exception: # email can't be parsed or sent, still mark it as answered
                        print "error replying msg: %s" % msg_id
                self.emails_answered = numMessages
                if should_record:
                    print 'recording messages'
                    self.record_answered_mails()
                time.sleep(60)
            except Exception as e: # inactivity timeout, connect again
                print e
                self.connect()

        self.pop_conn.quit()


    def send_mail(self, msg_id, to_address, subj, text):
        print 'sending mail to %s' % to_address
        FROM_ADDRESS = 'git_helper@yahoo.com'

        new = MIMEMultipart("mixed")
        body = MIMEMultipart("alternative")
        body.attach( MIMEText("reply body text", "plain") )
        body.attach( MIMEText(text, "html") )
        new.attach(body)

        new["Message-ID"] = email.utils.make_msgid()
        new["In-Reply-To"] = msg_id
        new["References"] = msg_id
        new["Subject"] = "Re: "+subj
        new["To"] = to_address
        new["From"] = FROM_ADDRESS
        self.mail_server.sendmail(new['from'], [new['to']], new.as_string())
        print 'mail sent'

mail_checker = EmailHandler()
mail_checker.check_mail()