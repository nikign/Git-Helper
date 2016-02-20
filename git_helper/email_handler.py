from email import parser
from email.mime.text import MIMEText
import poplib
import smtplib


def get_message_info(message):
    message_info = parser.Parser().parsestr("\n".join(message))
    sender = message_info['From']
    subj = message_info['Subject']
    return sender, subj
    

def get_text_message(message):
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
    
    return text_message, sender, subj


def check_mail():
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

    numMessages = len(pop_conn.list()[1])    
    for i in range(numMessages):
        msg = pop_conn.retr(i+1)[1] # new statement
        msg_text = get_text_message(msg)
        sender, subj = get_message_info(msg)
        send_mail(mail_server, sender, subj, msg_text)

    pop_conn.quit()


def send_mail(server, to_address, subj, text):
    print 'sending mail to %s' % to_address
    TO_ADDRESS = to_address
    FROM_ADDRESS = 'git_helper@yahoo.com'
    REPLY_TO_ADDRESS = to_address
    msg = MIMEText(text)
    msg['to'] = TO_ADDRESS
    msg['from'] = FROM_ADDRESS
    msg['subject'] = subj
    msg.add_header('reply-to', REPLY_TO_ADDRESS)
    server.sendmail(msg['from'], [msg['to']], msg.as_string())
    print 'mail sent'


check_mail()