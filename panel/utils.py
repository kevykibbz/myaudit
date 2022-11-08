from django.http import BadHeaderError
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .tokens import create_token
from django.conf import settings
import threading
from django.contrib.auth.models import User
from django.contrib.sessions .models import Session
from django.utils import timezone
from installation.models import SiteModel
from django.core.cache import cache
from smtplib import SMTPException


#get current writers
def get_current_writers():
    active_sessions=Session.objects.filter(expire_date__gte=timezone.now())
    users_id_list=[]
    for session in active_sessions:
        data=session.get_decoded()
        users_id_list.append(data.get('_auth_user_id',None))
    return User.objects.filter(id__in=users_id_list,extendedauthuser__category='writer')

#get current customers
def get_current_customers():
    active_sessions=Session.objects.filter(expire_date__gte=timezone.now())
    users_id_list=[]
    for session in active_sessions:
        data=session.get_decoded()
        users_id_list.append(data.get('_auth_user_id',None))
    return User.objects.filter(id__in=users_id_list,extendedauthuser__category='customer')

#get current users
def get_current_users():
    active_sessions=Session.objects.filter(expire_date__gte=timezone.now())
    users_id_list=[]
    for session in active_sessions:
        data=session.get_decoded()
        users_id_list.append(data.get('_auth_user_id',None))
    return User.objects.filter(id__in=users_id_list)

#threads
class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    def run(self):
        try:
            self.email.send()
        except SMTPException as e:
            print('error sending mail'+e)
        except BadHeaderError:
            print('Invalid header found')
        except:
            print('Error sending mail')


#send email
def send_email(subject,email,message,template):
    mail_subject=subject
    html_content=render_to_string(template,message)
    text_content=strip_tags(html_content)
    to_email=email
    email=EmailMultiAlternatives(mail_subject,text_content,settings.EMAIL_HOST_USER,[to_email])
    email.attach_alternative(html_content,'text/html')
    EmailThread(email).start()

#site constants
def getSiteData():
    if SiteModel.objects.count() > 0:
        obj=SiteModel.objects.values()[0]
        return obj


#social links
def sociallinks():
    return {
                    "facebook":
                                {
                                "username":"kevy.kibbz",
                                "link":"https://web.facebook.com/kevy.kibbz/"
                                },
                    "twitter":
                                {
                                "username":"Kevin36285655",
                                "link":"https://twitter.com/Kevin36285655"
                                },
                    "instagram":
                                {
                                "username":"kevviey",
                                "link":"ttps://www.instagram.com/kevviey/"
                                },
                    "github":
                                {
                                "username":"kevin",
                                "link":"https://github.com"
                                },
                    "whatsapp":
                                {
                                "username":"kevin",
                                "link":"https://wa.link/r9fxm4"
                                },
                    "linkedin":
                                {
                                "username":"chill-cash-260aba206",
                                "link":"https://www.linkedin.com/in/chill-cash-260aba206/"
                                },
                    "youtube":
                                {
                                "username":"kevin kibebe",
                                "link":"https://youtube.com"
                                },
                    }