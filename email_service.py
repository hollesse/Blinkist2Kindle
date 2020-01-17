import json
import logging
import smtplib
import ssl
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List

from book_converter import Format


@dataclass
class Sender:
    name: str
    email: str
    username: str
    password: str
    smtp_server: str
    smtp_port: int


@dataclass
class Receiver:
    name: str
    email: str
    format: Format


class SenderFactory:

    @staticmethod
    def sender(configfile_name: str) -> Sender:

        with open(configfile_name) as configfile:
            sender_config = json.load(configfile)['email']['sender']
        return Sender(name=sender_config['name'],
                      email=sender_config['email'],
                      username=sender_config['username'],
                      password=sender_config['password'],
                      smtp_server=sender_config['smtp_server'],
                      smtp_port=sender_config['smtp_port'])


class ReceiverFactory:

    @staticmethod
    def receivers(configfile_name: str) -> List[Receiver]:

        with open(configfile_name) as configfile:
            receiver_config = json.load(configfile)['email']['receivers']
        receivers = list()
        for receiver in receiver_config:
            receivers.append(Receiver(name=receiver['name'],
                                      email=receiver['email'],
                                      format=Format(receiver['format'])))
        return receivers


class EmailService:
    SMTP_PORT = 25
    SMTP_PORT_TLS = 587
    SMTP_PORT_SSL = 465

    def __init__(self, sender: Sender):
        self.sender = sender
        logging.debug('Connecting to SMTP Server...')
        self.server = smtplib.SMTP(self.sender.smtp_server, self.sender.smtp_port)
        logging.info('Connected to SMTP Server')
        try:
            context = ssl.create_default_context()
            self.server.starttls(context=context)
            logging.info('TLS started')

            self.server.login(self.sender.username, self.sender.password)
            logging.info('logged in at SMTP Server')
        except Exception as e:
            logging.error(f'Oh no! Something bad happened!n{e}')

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info('Closing the server...')
        self.server.quit()

    def send_email(self, receivers, subject, body, attachment_filename):
        for receiver in receivers:
            logging.debug("Sending the email...")
            msg = MIMEMultipart()
            msg['To'] = formataddr((receiver.name, receiver.email))
            msg['From'] = formataddr((self.sender.name, self.sender.email))
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            try:
                with open(attachment_filename, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)

                attachment_filename_without_path = attachment_filename.split('/')[-1]
                part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {attachment_filename_without_path}",
                )
                msg.attach(part)
            except Exception as e:
                logging.error(f"Oh no! We didn't found the attachment!n{e}")
                break

            try:
                self.server.sendmail(self.sender.email, receiver.email, msg.as_string())
                logging.info('Email to "' + receiver.email + '" sent!')
            except Exception as e:
                logging.error(f'Oh no! Something bad happened!n{e}')
                break
