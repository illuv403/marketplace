import smtplib

import email_creds

def send_email(email_to, products):
    email = email_creds.email
    password = email_creds.password

    body = 'Thank You for ordering from us! Here are the products you ordered:\n'
    for product in products:
        body += f'{product.name}\n'

    message = 'Subject: Thank You for your order!\n'
    message += f'From: {email}\n'
    message += f'To: {email_to}\n'
    message += f'\n{body}'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email, password)
        server.sendmail(email, email_to, message)
        server.close()
        print('Email sent successfully!')
    except Exception as e:
        print(f'An error occurred while sending the email: {e}')
