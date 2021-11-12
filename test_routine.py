"""Tests for email_routine"""

import datetime
from email.message import EmailMessage
from email_routine import secure_gmail_smtp, gmail_smtp, gmail_imap
import imapclient
import os
import pytest
import ssl
import time

def msg_test(now):
    """Creating test message"""
    msg = EmailMessage()
    msg['Subject']="Deploy key for project from "+now
    msg.set_content("Never gonna give you up")
    return msg


@pytest.fixture
def enviroment():
    """Pulling variables from enviroment"""
    enviroment_dict = {'login_oauth':os.environ.get('login_oauth'),
                       'oauth_string':os.environ.get('oauth_string'),
                       'login_pass':os.environ.get('login_pass'),
                       'some_password':os.environ.get('some_password'),
                       'another_password':os.environ.get('another_password')}
    return enviroment_dict


@pytest.mark.skip(reason="problems with OAuth")
def test_oauth_connection(enviroment):
    """ehlo of oauth connection"""
    conn = secure_gmail_smtp(enviroment['oauth_string'])
    conn.ehlo()#sometimes server's first response is code 334
    response = conn.ehlo()
    conn.quit()
    assert response[0]==250

def test_connection(enviroment):
    """ehlo of ordinary connection"""
    conn = gmail_smtp(enviroment['login_pass'], enviroment['another_password'])
    response = conn.ehlo()
    conn.quit()
    assert response[0]==250

@pytest.mark.skip(reason="problems with OAuth")
def test_sending_mail_via_oauth_connection(enviroment):
    """sending mail with oauth connection"""
    now = datetime.datetime.now()
    msg = msg_test(str(now))
    from_addr = enviroment['login_oauth']
    to_addr = enviroment['login_pass']
    conn = secure_gmail_smtp(enviroment['oauth_string'])
    conn.sendmail(from_addr, to_addr, msg.as_string())
    conn.quit()
    rcv_conn = gmail_imap(to_addr, enviroment['another_password'])
    results = rcv_conn.search(None, 'SUBJECT '+str(now.time()))
    rcv_conn.logout()
    list_of_mail=[int(x) for x in results[1][0].decode('utf8').split()]
    assert len(list_of_mail)!=0

def test_sending_mail(enviroment):
    """sending mail with ordinary connection """
    now = datetime.datetime.now()
    msg = msg_test(str(now))
    from_addr = enviroment['login_pass']
    to_addr = enviroment['login_oauth']
    conn = gmail_smtp(enviroment['login_pass'],
                      enviroment['another_password'])
    conn.sendmail(from_addr, to_addr, msg.as_string())
    conn.quit()
    time.sleep(2)
    rcv_conn=gmail_imap(to_addr, enviroment['some_password'])
    results = rcv_conn.search(None, 'SUBJECT '+str(now.time()))
    print(results)
    print(str(now.time()))
    rcv_conn.logout()
    list_of_mail=[int(x) for x in results[1][0].decode('utf8').split()]
    assert len(list_of_mail)!=0
