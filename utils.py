import os
import re
import csv
from dotenv import load_dotenv

# Loading Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class IDs:
    server = 1182668463496499240
    test_channel = 1198395844391604419
    verify_channel = 1198749464068894771
    param = 531398388516651029
    arnold = 762015770728202243
    rupkatha = 1187052225441316916


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

    check_presence = CheckPresence("./sep-23.csv")
    print(check_presence("21f1000019@ds.study.iitm.ac.in"))
    print(check_presence("22f3000797@ds.study.iitm.ac.in"))
    print(check_presence("Me"))





