

from celery import shared_task
from django.core.mail import send_mail
from .models import CustomUser

@shared_task
def send_password_reset_email(email, reset_link):
    send_mail(
        subject="Password Reset Request",
        message=f"Click the link below to reset your password:\n\n{reset_link}",
        from_email="konul.bairamovaa@gmail.com",
        recipient_list=[email],
    )

@shared_task
def send_user_count_to_admin():
    user_count = CustomUser.objects.count()
    send_mail(
        subject='Number of users',
        message=f'The current number of users in the system is {user_count}.',
        from_email='konul.bairamovaa@gmail.com',  # Sender email
        recipient_list=['konul.bairamovaa@gmail.com'],  # Admin email
        fail_silently=False, # Django will raise an exception, and we will be notified of the error.
    )
