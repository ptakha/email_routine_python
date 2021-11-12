"""
Routine for using smtplib with gmail
Either
1. Create test account
2. Go to Google Cloud Platorm via this account
3. Create new project
4. Create Oauth consent screen, add to testing users this account
5. Create client credentials for desktop app
6. Update all cerificates for python2
6. Using this repo https://github.com/google/gmail-oauth2-tools and client
credentials create access token for every hour you will need new
7. Using access token create oauth authentication string
Or
1. Create test account
2. Turn on two-factor authentication
3. Generate password for app
4. Use it for login
"""
import imapclient
import os
import smtplib
import ssl

def secure_gmail_smtp(auth_string):
    """Creates secure connection to smtp.gmail.com, using XOAUTH2 protocol"""
    default_context=ssl.create_default_context()
    smtp_conn = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_conn.starttls(context=default_context)
    smtp_conn.ehlo()
    smtp_conn.docmd('AUTH', 'XOAUTH2 '+auth_string)
    return smtp_conn

def gmail_smtp(login, password):
    """Creates connection to smtp.gmail.com, using 2FA and application password"""
    default_context=ssl.create_default_context()
    smtp_conn=smtplib.SMTP("smtp.gmail.com", 587)
    smtp_conn.starttls(context=default_context)
    smtp_conn.ehlo()
    smtp_conn.login(login, password)
    return smtp_conn

def gmail_imap(login, password):
    default_context = ssl.create_default_context()
    rcv_conn = imapclient.IMAP4_TLS("imap.gmail.com", 993, default_context)
    rcv_conn.login(login, password)
    rcv_conn.select('INBOX', readonly=True)
    return rcv_conn

