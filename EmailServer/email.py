from django.core.mail import send_mail,EmailMessage
from django.template.loader import get_template

class Mail:
    def __init__(self, subject,body,mail_sender,mail_receiver):
        self.subject=subject
        self.body=body
        self.mail_sender=mail_sender
        self.mail_receiver=mail_receiver

    def send(self):
        try:
            send_mail(self.subject,self.body,self.mail_sender,[self.mail_receiver],fail_silently=False)
        except Exception as e:
            print(e)

    def invoice_send(self,filename,client_name):
        try:
            obj={
                'client_name':client_name,
                'subject':self.subject,
                'body':self.body
            }
            message = get_template("mail_template.html").render(obj)
            email=EmailMessage(self.subject,message,self.mail_sender,[self.mail_receiver])
            email.content_subtype = "html"  
            email.attach_file(f'media/{filename}')
            email.send()
        except Exception as e:
            print(e)

    def mailWithTemplate(self,client_name):
        try:
            obj={
                'client_name':client_name,
                'subject':self.subject,
                'body':self.body
            }
            message = get_template("mail_template.html").render(obj)
             
            mail=EmailMessage(
                subject=self.subject,
                body=message,
                from_email=self.mail_sender,
                to=[self.mail_receiver]
            )
            mail.content_subtype="html"
            mail.send()
        except Exception as e:
            print(e)
