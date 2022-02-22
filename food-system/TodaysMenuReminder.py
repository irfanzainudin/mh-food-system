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

day = datetime.today().weekday()
if day == 0:
    print(worksheet.acell("C6").value)
elif day == 1:
    print(worksheet.acell("D6").value)
elif day == 2:
    print(worksheet.acell("E6").value)
elif day == 3:
    print(worksheet.acell("F6").value)
elif day == 4:
    print(worksheet.acell("G6").value)
