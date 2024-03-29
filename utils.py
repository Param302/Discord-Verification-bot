import os
import re
import csv
import ssl
import json
import smtplib
from random import randint
from dotenv import load_dotenv
from email.message import EmailMessage

# Loading Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PSWD = os.getenv("ACC_PSWD")
EMAIL_ID = os.getenv("ACC_EMAIL")

def extract_ids(path):
    with open(path, "r") as f:
        return json.load(f)[0]

ids = extract_ids("./ids.json")
# IDs = namedtuple("IDs", ids.keys())(**ids)
IDs = type("IDs", (), ids)


class EmailParser:
    __pattern = re.compile(r'^(21|22|23|24|25)(f|ds|dp)[1-3]\d{6}@(ds|es)\.study\.iitm\.ac\.in$')
        
    def __call__(self, email) -> bool:
        return bool(self.__pattern.match(email))


class CheckPresence:
    def __init__(self, data: str):
        self.data = self._read_data(data)
    
    def _read_data(self, data: str):
        with open(data, 'r') as f:
            return tuple(csv.DictReader(f))

    def __call__(self, email: str) -> dict | None:
        for row in self.data:
            if email == row["Email"]:
                return row
        return None
    

class EmailVerifier:
    from_email = EMAIL_ID
    subject = "Verification Code for Pichavaram House Discord Server"

    def __init__(self):
        ...
    
    def _generate_code(self) -> str:
        return randint(100000, 999999)
    
    def _create_template(self, code:int) -> str:
        em = EmailMessage()
        em["Subject"] = self.subject
        em["From"] = self.from_email
        em.set_content(f"Your verification code is {code}")
        return em
    
    def _send_email(self, template: EmailMessage, to_email: str):
        template["To"] = to_email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.from_email, PSWD)
            server.sendmail(self.from_email, to_email, template.as_string())

    def __call__(self, to_email: str) -> int:
        code = self._generate_code()
        template = self._create_template(code)
        self._send_email(template, to_email)
        return code
