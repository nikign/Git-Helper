from bs4 import BeautifulSoup
import email
from email import parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.message import MIMEMessage
import poplib
import smtplib
import time

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from  rate_results import get_email_result

SURVEY_LINK = 'http://goo.gl/forms/5MU1QUJNou'
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
    email_record_file = 'git_email_helper/last_answered_email.txt'

    def record_answered_mails(self):
        with open(self.email_record_file, 'w') as out:
            out.write(str(self.emails_answered))

    def load_answered_mails(self):
        try:
            with open(self.email_record_file, 'r') as in_file:
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
                mail_server.ehlo()

                mail_server.starttls()
                mail_server.login(user_name, password)
                print 'smtp Connection made'
                break
            except Exception as e: # handshake error, try till succede
                time.sleep(10)
        self.pop_conn = pop_conn
        self.mail_server = mail_server

    def create_mail_body(self, question, answer, link_to_page, link_to_survey):
        mail_body = ('Hi,<br> This question and its top answer seem close to your problem.<br>'+\
            'Question:<br>%s<br> Top Answer:<br>%s<br> You can view the complete conversation in this link:<br>%s<br>'+\
            ' To help us improve this tool, please take a minute to complete this survey:<br>'+\
            '%s<br> Thanks,<br>The Git_Helper Team') %(str(question), str(answer), link_to_page, link_to_survey)
        return mail_body

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
                        question, answer, link = get_email_result(msg_text)
                        answer = answer[0]['html_text']
                        question = question['html_text']
                        msg_response = self.create_mail_body(question, answer, link, SURVEY_LINK)
                        msg_id, sender, subj = get_message_info(msg)
                        self.send_mail(msg_id, sender, subj, msg_response)
                    except Exception as e: # email can't be parsed or sent, still mark it as answered
                        print e
                        print "error replying msg:" #% msg_id
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

        new = MIMEMultipart("alternative")
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