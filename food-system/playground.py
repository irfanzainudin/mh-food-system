# playground to test code

import gspread
from datetime import datetime

# GLOBALS
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
MENU_ROW = "2"

# CONNECTION SETUP
service_account = gspread.service_account()
sheet = service_account.open("MALAYSIA HALL DINNER SEM 2/21")
worksheet = sheet.worksheets()[0]  # get the latest worksheet


# MAIN FUNCTION
menu_count_for_each_day = {}
MONDAYS_COLUMN_NUMBER = worksheet.find("Monday").col
prev_day = "Monday"  # because Monday is the first ordering day
prev_col = MONDAYS_COLUMN_NUMBER
for day in WEEKDAYS:
    if day == "Monday":
        result = worksheet.find(day)
        prev_day = day
        prev_col = result.col
    elif day == "Friday":
        result = worksheet.find(day)
        menu_count_for_each_day[prev_day] = result.col - prev_col
        prev_day = day
        prev_col = result.col
    else:  # Tuesday, Wednesday, Thursday
        result = worksheet.find(day)
        menu_count_for_each_day[prev_day] = result.col - prev_col
        prev_day = day
        prev_col = result.col
result = worksheet.find(prev_day)
last_col = worksheet.find("TOTAL $").col
menu_count_for_each_day[prev_day] = last_col - prev_col


for menu in worksheet.row_values(MENU_ROW):
    print(menu)
