from django.core.mail import send_mail

from time import sleep
from celery import shared_task


@shared_task
def notify_customers(message):
    print('Sending 10k emails..')
    print(message)
    # sleep(20)

    # for i in range(10):
    # print('i', i)
    send_mail('Email Test', 'This is a dummy message of Django',
              'gauravsomani52750@gmail.com', ['jonnyroy789@gmail.com'],
              fail_silently=False)
    print('Emails were sent successfully!')
