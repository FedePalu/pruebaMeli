import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class UsuarioService:
    
    def __init__(self, remitente, password):
        self.connection = smtplib.SMTP(host='smtp.gmail.com', port=587)  
        self.remitente = remitente
        self.password = password

    def mailCambioVisibilidad(self, file):
        asunto = "Visibilidad de su archivo %s" % file['title']
        body = "Se ha cambiado la visibilidad de su archivo con nombre: %s a Privado por causa de seguridad." % file['title']
        mimemsg = MIMEMultipart()
        mimemsg['From'] = self.remitente
        mimemsg['To'] = file['owners'][0]['emailAddress']
        mimemsg['Subject'] = asunto
        mimemsg.attach(MIMEText(body, 'plain'))
        return mimemsg

    def enviarCorreoCambioDeVisibilidad(self, file):
        try:
            mail = self.mailCambioVisibilidad(file)
            self.connection.starttls()
            self.connection.login(self.remitente,self.password)
            self.connection.send_message(mail)
            self.connection.quit()
        except:
            # Me importa que falle?
            None