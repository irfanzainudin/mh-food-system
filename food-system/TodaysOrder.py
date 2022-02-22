# This code's strength:
# - automated

# This code's weakness:
# - cannot support multiple menus in one day

from datetime import datetime
import gspread

# dev or production?
debug = True

service_account = gspread.service_account()
sheet = service_account.open("MALAYSIA HALL DINNER SEM 2/21")
worksheet = sheet.worksheets()[0]  # get the latest worksheet


def what_day_is_today(day):
    if day == 0:
        return "Monday"
    elif day == 1:
        return "Tuesday"
    elif day == 2:
        return "Wednesday"
    elif day == 3:
        return "Thursday"
    elif day == 4:
        return "Friday"
    elif day == 5:
        return "Saturday"
    else:
        return "Sunday"


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


# 0 == Monday
# 1 == Tuesday
# 2 == Wednesday
# 3 == Thursday
# 4 == Friday
day = datetime.today().weekday()
### DEV/TESTING ###
if debug:
    day_count = 2
    print("Salam Abg Sam", "\n")
    print("Menu hari ni:")
    print(todays_menu(day_count), "\n")
    i = 1
    for cell in worksheet.get("B11:I41"):
        if cell[day_count]:
            if int(cell[day_count]) > 1:
                letter = 65
                for count in range(int(cell[day_count])):
                    print(str(i) + ".", cell[0].capitalize(), chr(letter))
                    letter += 1
                    i += 1
            else:
                print(str(i) + ".", cell[0].capitalize())
                i += 1
    print("\n", f"Total {i - 1} pax hari ni. Thank you Abg Sam!")
### PRODUCTION ###
else:
    if day >= 0 and day < 5:  # no orders on weekends
        print("Salam Abg Sam", "\n")
        print("Menu hari ni:")
        print(todays_menu(day), "\n")
        i = 1
        for cell in worksheet.get("B11:I41"):  # DO NOT CHANGE THE CELLS' VALUES
            if cell[day_count(day)]:
                if int(cell[day_count(day)]) > 1:
                    letter = 65
                    for count in range(int(cell[day_count(day)])):
                        print(str(i) + ".", cell[0].capitalize(), chr(letter))
                        letter += 1
                        i += 1
                else:
                    print(str(i) + ".", cell[0].capitalize())
                    i += 1
        print("\n", f"Total {i - 1} pax hari ni. Thank you Abg Sam!")
