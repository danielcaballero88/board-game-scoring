import threading

from django.core.mail import send_mail


def send_email_async(
    subject: str, message: str, from_email: str, recipient_list: list[str]
) -> threading.Thread:
    def send():
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

    thread = threading.Thread(target=send)
    thread.start()
    return thread
