# This code's strength:
# - automated

# This code's weakness:
# - cannot support multiple menus in one day

from datetime import datetime
import gspread
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env

# dev or production?
# dev == True
# production == False
debug = True

service_account = gspread.service_account()
sheet = service_account.open("MALAYSIA HALL DINNER SEM 2/21")
worksheet = sheet.worksheets()[0]  # get the latest worksheet


def day_count(day):
    return day + 1


def todays_menu(day):
    if day == 0:
        return worksheet.acell("C6").value
    elif day == 1:
        return worksheet.acell("D6").value
    elif day == 2:
        return worksheet.acell("E6").value
    elif day == 3:
        return worksheet.acell("F6").value
    elif day == 4:
        return worksheet.acell("G6").value


client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_API_KEY"))
day = datetime.today().weekday()

### DEV/TESTING ###
if debug:
    day_count = 3
    body = ""
    body = body + "Salam Abg Sam\n\nMenu hari ni:\n" + todays_menu(day_count) + "\n\n"
    i = 1
    for cell in worksheet.get("B11:I41"):
        if len(cell) > day_count and cell[day_count]:
            pack_count = int(cell[day_count][0])
            if pack_count > 1:
                letter = 65
                for count in range(int(cell[day_count])):
                    body = (
                        body
                        + str(i)
                        + ". "
                        + cell[0].capitalize()
                        + " "
                        + chr(letter)
                        + "\n"
                    )
                    letter += 1
                    i += 1
            else:
                body = body + str(i) + ". " + cell[0].capitalize() + "\n"
                i += 1
    body = body + "\n\n" + f"Total {i - 1} pax hari ni. Thank you Abg Sam!"
    message = client.messages.create(
        messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
        body=body,
        to=os.getenv("FOOD_DIRECTOR_PHONE_NUMBER"),
    )
### PRODUCTION ###
else:
    # 0 == Monday
    # 1 == Tuesday
    # 2 == Wednesday
    # 3 == Thursday
    # 4 == Friday
    if day >= 0 and day < 5:  # no orders on weekends
        body = ""
        body = body + "Salam Abg Sam\n\nMenu hari ni:\n" + todays_menu(day) + "\n\n"
        i = 1
        for cell in worksheet.get("B11:I41"):  # DO NOT CHANGE THE CELLS' VALUES
            if len(cell) > day_count(day) and cell[day_count(day)]:
                pack_count = int(cell[day_count(day)][0])
                if pack_count > 1:
                    letter = 65
                    for count in range(int(cell[day_count(day)])):
                        body = (
                            body
                            + str(i)
                            + ". "
                            + cell[0].capitalize()
                            + " "
                            + chr(letter)
                            + "\n"
                        )
                        letter += 1
                        i += 1
                else:
                    body = body + str(i) + ". " + cell[0].capitalize() + "\n"
                    i += 1
        body = body + "\n\n" + f"Total {i - 1} pax hari ni. Thank you Abg Sam!"
        message = client.messages.create(
            messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
            body=body,
            to=os.getenv("FOOD_DIRECTOR_PHONE_NUMBER"),
        )
