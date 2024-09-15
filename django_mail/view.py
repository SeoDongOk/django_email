# views.py

from django.core.mail import send_mail
from django.http import HttpResponse
from .getData import getData

def send_gmail(request):
    joblist=getData()
    joblist_html = joblist.to_html(index=False)  
    subject = '잡코리아 산업기능요원 이메일'
    message = joblist_html
    recipient_list = ['hcan1445@gmail.com']  # 받는 사람 이메일 주소
    from_email = 'hcan1445@gmail.com'

    try:
        send_mail(subject, message, from_email, recipient_list,fail_silently=False,html_message=joblist_html)
        return HttpResponse('Email sent successfully')
    except Exception as e:
        return HttpResponse(f'Error sending email: {str(e)}')
