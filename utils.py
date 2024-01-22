import os
import re
import csv
import ssl
import smtplib
from random import randint
from dotenv import load_dotenv
from email.message import EmailMessage


# Loading Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PSWD = os.getenv("ACC_PSWD")


class IDs:
    server = 1182668463496499240
    test_channel = 1198395844391604419
    verify_channel = 1198756336977068112
    param = 531398388516651029
    arnold = 762015770728202243
    rupkatha = 1187052225441316916
    verified_iitm_role = ...
    group_no_role = ...
    group_leader_role = ...
    pichavaram_role = ...


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
    from_email = "pichavaram-webad@ds.study.iitm.ac.in"
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

class TrackEmail:
    def __init__(self, email:str):
        self.email = email
        self.gen_code = None
        self.user_code = None
    


if __name__ == "__main__":
    # parse_email = EmailParser()
    # print("Valid cases")
    # print(parse_email("23f3000042@es.study.iitm.ac.in"))
    # print(parse_email("21f2000518@ds.study.iitm.ac.in"))
    # print(parse_email("23dp2000028@ds.study.iitm.ac.in"))
    # print(parse_email("23ds2000028@ds.study.iitm.ac.in"))
    # print(parse_email("21f1000004@ds.study.iitm.ac.in"))
    # print(parse_email("23f1234567@ds.study.iitm.ac.in"))
    # print("Invalid cases")
    # print(parse_email("Hello"))
    # print(parse_email("26f1000004@ds.study.iitm.ac.in"))
    # print(parse_email("23df1000004@ds.study.iitm.ac.in"))
    # print(parse_email("22f12345678@ds.study.iitm.ac.in"))
    # print(parse_email("22f1234567@ess.study.iitm.ac.in"))
    # print(parse_email("22f1234567@ds.iitm.ac.in"))
    # print(parse_email("22f123457@study.iitm.ac.in"))
    # print(parse_email("25f4000004@ds.study.iitm.ac.in"))
    # print(parse_email("25f0000004@ds.study.iitm.ac.in"))

    # check_presence = CheckPresence("./sep-23.csv")
    # print(check_presence("21f1000019@ds.study.iitm.ac.in"))
    # print(check_presence("22f3000797@ds.study.iitm.ac.in"))
    # print(check_presence("Me"))

    # verifyemail = EmailVerifier()
    # print(verifyemail._generate_code())
    # print(verifyemail._create_template(123456))
    # print("Arnold", verifyemail("pichavaram-sec@ds.study.iitm.ac.in"))
    # print("Rupkatha", verifyemail("pichavaram-ds@ds.study.iitm.ac.in"))

    tracker = TrackEmail("Hello@gmail.com")
    print(tracker.email)
    print(tracker.verified)
    tracker.gen_code = 12345
    tracker.user_code = 12345
    print(tracker)
    tracker.email_verified()
    if tracker.code_gen == tracker.user_code:
        print("Verified")
        del tracker

    print("After verifying", tracker)





