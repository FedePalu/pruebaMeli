import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class UsuarioService:
    
    def __init__(self, remitente, password):
        self.remitente = remitente
        self.password = password

    def enviarCorreo(self, destinatario, asunto, body):
        try:
            mimemsg = MIMEMultipart()
            mimemsg['From'] = self.remitente
            mimemsg['To'] = destinatario
            mimemsg['Subject'] = asunto
            mimemsg.attach(MIMEText(body, 'plain'))
            connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
            connection.starttls()
            connection.login(self.remitente,self.password)
            connection.send_message(mimemsg)
            connection.quit()
            print("El mensaje se ha enviado con exito")
        except:
            print("Ha habido un error al enviar el mensaje")