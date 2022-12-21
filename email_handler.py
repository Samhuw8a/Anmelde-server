import smtplib
import ssl
from errors import Error
from   email.mime.text import MIMEText
from   email.mime.multipart import MIMEMultipart

class Email_server():
    def __init__(self,port:int, server:str, pswrd:str) -> None:
        self.port:int   = port
        self.server:str = server
        self.pswrd:str  = pswrd
        self.sender:str = "no_reply@ksrminecraft.ch"
        self.subject:str = "Deine Registration bei KSRMinecraft"
        self.message:str = "Hello_world"

    def load_from_template(self,file_name:str)->None:
        with open(file_name,"r") as f:
            self.message = f.read().strip()

    def send(self,mail:str)->None:
        self.message = self.message.replace("{mail}",mail)
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = mail
        msg["Subject"] = self.subject
        msg.attach(MIMEText(self.message,"plain","utf-8"))
        text = msg.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
            server.login(self.sender, self.pswrd)
            server.sendmail(self.sender, mail, text)
    
def main()->None:
    serv=Email_server(465,"cap.ssl.hosttech.eu","**************")
    serv.load_from_template("template/test_mail.txt")
    serv.send("samuel.huwiler@gmx.ch")

if __name__=="__main__":
    main()
