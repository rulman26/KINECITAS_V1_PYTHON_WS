import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
class Conecction():
    def __init__(self):
        KEY = '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'
        self.sg = SendGridAPIClient(KEY)

    def sendMail(self,to,subject,message):
        try:
            message = Mail(
                from_email='no-reply@kinecitas.com',
                to_emails= to,
                subject= subject,
                html_content= message)
            response = self.sg.send(message)
            result = { 
                'status_code' : response.status_code,
                'body' : response.body ,
                'headers' : response.headers}
            return { 'status' : True , 'data' : result }
        except Exception as e:
            print("Error Correo ", e.message)
            return { 'status' : False , 'data' : e.message}