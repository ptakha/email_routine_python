"""
Routine for using smtplib with gmail
1. Create test account
2. Go to Google Cloud Platorm via this account
3. Create new project
4. Create Oauth consent screen, add to testing users this account
5. Create client credentials for desktop app
6. Update all cerificates for python2
6. Using this repo https://github.com/google/gmail-oauth2-tools and client
credentials create access token for every hour you will need new
7. Using access token create oauth authenfication string
"""
import os
import smtplib
import ssl

def secure_gmail_smtp(auth_string, def_context):
    """Creates secure connection to smtp.gmail.com, using auth_string"""
    smtp_conn = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_conn.starttls(context=def_context)
    smtp_conn.ehlo()
    smtp_conn.docmd('AUTH', 'XOAUTH2 '+auth_string)
    return smtp_conn

def gmail_smtp(login, password, def_context):
    """Creates connection to smtp.gmail.com, you need to authorise using this
    account for unsafe applications"""
    smtp_conn=smtplib.SMTP("smtp.gmail.com", 587)
    smtp_conn.starttls(context=def_context)
    smtp_conn.ehlo()
    smtp_conn.login(login, password)
    return smtp_conn

def send_mail_gmail(conn, from_addr, rcpn_addr, msg):
    """Just sends mail from created connection"""
    conn.sendmail(from_addr, rcpn_addr, msg)


if __name__=="__main__":
    default_context=ssl.create_default_context()
    auth = os.environ.get('AUTH_STRING')
    conn = secure_gmail_smtp(auth, default_context)
    message="""\
            Subject: Hello there
            
            General Kenobi"""
    from_addr="some.testing.example@gmail.com"
    to_addr="some.testing.example@gmail.com"
    conn.sendmail(from_addr, to_addr, message)
    conn.quit()
