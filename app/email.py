# from typing import List
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import EmailStr, BaseModel
# from .config import settings
# from jinja2 import Environment, select_autoescape, PackageLoader
# import ssl


# # Initialize Jinja2 environment for email templates
# env = Environment(
#     loader=PackageLoader('app', 'templates'),
#     autoescape=select_autoescape(['html', 'xml'])
# )


# class EmailSchema(BaseModel):
#     email: List[EmailStr]


# class GmailConfig:
#     """Gmail-specific configuration settings"""
#     SMTP_HOST = "smtp.gmail.com"
#     SMTP_PORT = 587  # Gmail's TLS port
    
#     @staticmethod
#     def get_connection_config(settings) -> ConnectionConfig:
#         """
#         Creates a ConnectionConfig object with Gmail-specific settings
        
#         Note: For Gmail, you need to:
#         1. Enable 2-Step Verification
#         2. Generate an App Password
#         """
#         return ConnectionConfig(
#             MAIL_USERNAME=settings.EMAIL_USERNAME,
#             MAIL_PASSWORD=settings.EMAIL_PASSWORD,  # Use App Password here
#             MAIL_FROM=settings.EMAIL_FROM,
#             MAIL_PORT=GmailConfig.SMTP_PORT,
#             MAIL_SERVER=GmailConfig.SMTP_HOST,
#             MAIL_STARTTLS=True,  # Required for Gmail
#             MAIL_SSL_TLS=False,  # Don't use SSL
#             USE_CREDENTIALS=True,
#             VALIDATE_CERTS=True,
#             TEMPLATE_FOLDER='app/templates',  # Optional: specify template folder
#             SSL_CONTEXT=ssl.create_default_context()  # Use default SSL context
#         )


# class Email:
#     def __init__(self, user: dict, url: str, email: List[EmailStr]):
#         self.name = user['name']
#         self.sender = 'HackAI'
#         self.email = email
#         self.url = url
#         self.gmail_config = GmailConfig.get_connection_config(settings)

#     async def sendMail(self, subject: str, template: str):
#         """
#         Sends an email using Gmail SMTP
        
#         Args:
#             subject: Email subject
#             template: Name of the HTML template file (without .html extension)
#         """
#         try:
#             # Get and render the HTML template
#             template = env.get_template(f'{template}.html')
#             html = template.render(
#                 url=self.url,
#                 first_name=self.name,
#                 subject=subject
#             )

#             # Create message
#             message = MessageSchema(
#                 subject=subject,
#                 recipients=self.email,
#                 body=html,
#                 subtype="html"
#             )

#             # Initialize FastMail with Gmail config
#             fm = FastMail(self.gmail_config)
            
#             # Send the email
#             await fm.send_message(message)
            
#             return True
            
#         except Exception as e:
#             print(f"Error sending email: {str(e)}")
#             raise e

#     async def sendVerificationCode(self):
#         """Sends a verification code email"""
#         await self.sendMail('Your verification code (Valid for 10min)', 'verification')










from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from .config import settings
from jinja2 import Environment, select_autoescape, PackageLoader


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, user: dict, url: str, email: List[EmailStr]):
        self.name = user['name']
        self.sender = 'HackAI <marufintern@gmail.com>'
        self.email = email
        self.url = url
        pass

    async def sendMail(self, subject, template):
        # Define the config
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USERNAME,
            MAIL_PASSWORD=settings.EMAIL_PASSWORD,
            MAIL_FROM=settings.EMAIL_FROM,
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            url=self.url,
            first_name=self.name,
            subject=subject
        )

        # Define the message options
        message = MessageSchema(
            subject=subject,
            recipients=self.email,
            body=html,
            subtype="html"
        )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

    async def sendVerificationCode(self):
        await self.sendMail('Your verification code (Valid for 10min)', 'verification')
