import smtplib
from flask import session
import email_creds  # Contains the sender email and password


def send_email(email_to, products):
    """
    Sends an order confirmation email to the specified recipient.

    This function composes a simple plaintext email that includes a thank-you
    message and a list of the ordered products. It sends the email using Gmail's
    SMTP server over SSL.
    """

    # Fetch sender credentials from the external module
    email = email_creds.email
    password = email_creds.password
    cart = session['cart']
    total = session['total']

    # Compose the email body with the product list
    body = 'Thank You for ordering from us! Here are the products you ordered:\n'
    for product in products:
        body += f'{product.name} in quantity of {cart[str(product.id)]}\n'

    body += f'\nYour total order amount is ${total:.2f}.'
    body += '\nPlease visit our website to see the products we have in stock.'
    body += '\nHave a great day!'

    # Construct the full email message
    message = 'Subject: Thank You for your order!\n'
    message += f'From: {email}\n'
    message += f'To: {email_to}\n'
    message += f'\n{body}'

    try:
        # Connect securely to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()  # Identify ourselves to the server
        server.login(email, password)  # Log in with the sender's credentials
        server.sendmail(email, email_to, message)  # Send the message
        server.close()  # Terminate the SMTP session
        print('Email sent successfully!')
    except Exception as e:
        # Print any error that occurs during the process
        print(f'An error occurred while sending the email: {e}')
