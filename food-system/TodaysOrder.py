# This code's strength:
# - automated
# - supports multiple menus in one day

# This code's weakness:
# 1. [NOT ROBUST]
#   - changes to the template of
#   the Google Spreadsheet WILL and SHALL
#   break the code

# IMPROVEMENTS:
# 1. To be more precise in terms of finding menu items

from datetime import datetime
import gspread
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env

###########
# GLOBALS #
###########

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
MENU_ROW = "2"
TOTAL_HALL_RESIDENTS = 31

####################
# CONNECTION SETUP #
####################

service_account = gspread.service_account()
sheet = service_account.open("MALAYSIA HALL DINNER SEM 2/21")
worksheet = sheet.worksheets()[0]  # get the latest worksheet

worksheet_cells = worksheet.get_all_cells()
worksheet_values = worksheet.get()

# print(worksheet_cells)
# print(worksheet_values)

#######################
# AUXILIARY FUNCTIONS #
#######################


def int_to_day(number):
    if number == 0:
        return "Monday"
    elif number == 1:
        return "Tuesday"
    elif number == 2:
        return "Wednesday"
    elif number == 3:
        return "Thursday"
    else:
        return "Friday"


def day_count(day):
    return day + 1


def calculate_menu_count_for_each_day():
    menu_count_for_each_day = {}

    MONDAYS_COLUMN_NUMBER = find_in_worksheet_values("Monday")[1]
    prev_day = "Monday"  # because Monday is the first ordering day
    prev_col = MONDAYS_COLUMN_NUMBER
    for day in WEEKDAYS:
        # day_position[0] == row number
        # day_position[1] == col number
        day_position = find_in_worksheet_values(day)
        if day == "Monday":
            result = find_in_worksheet_cells(day_position[0], day_position[1])
            prev_day = day
            prev_col = result.col
        elif day == "Friday":
            result = find_in_worksheet_cells(day_position[0], day_position[1])
            menu_count_for_each_day[prev_day] = result.col - prev_col
            prev_day = day
            prev_col = result.col
        else:
            result = find_in_worksheet_cells(day_position[0], day_position[1])
            menu_count_for_each_day[prev_day] = result.col - prev_col
            prev_day = day
            prev_col = result.col
    prev_day_pos = find_in_worksheet_values(prev_day)
    result = find_in_worksheet_cells(prev_day_pos[0], prev_day_pos[1])
    last_col = find_in_worksheet_values("TOTAL $")[1]
    menu_count_for_each_day[prev_day] = last_col - prev_col

    return menu_count_for_each_day


def todays_menu(day, menu_count):
    todays_menu = []
    today = int_to_day(day)
    col_number = find_in_worksheet_values(today)[1]
    for i in range(menu_count[today]):
        menu = find_in_worksheet_cells(MENU_ROW, col_number).value
        todays_menu.append(menu)
        col_number += 1

    return todays_menu


def find_in_worksheet_cells(row, col):
    row = int(row)
    col = int(col)
    position = (31 * (row - 1)) + (col - 1)
    return worksheet_cells[position]


def find_in_worksheet_values(needle):
    for i, haystack in enumerate(worksheet_values, start=1):
        if len(haystack) > 0:
            for j, stack in enumerate(haystack, start=1):
                if stack == needle:
                    return i, j


#################
# MAIN FUNCTION #
#################


def todays_order():
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_API_KEY"))
    # day = datetime.today().weekday()
    day = 2

    if day >= 0 and day < 5:  # no orders on weekends
        menu_count = calculate_menu_count_for_each_day()
        body = ""
        body = body + "Salam Abg Sam\n\nMenu hari ni:\n"
        today = int_to_day(day)
        todays_cell_position = find_in_worksheet_values(today)
        row_number = todays_cell_position[0]
        col_number = todays_cell_position[1]
        # find the starting row and col number
        DISTANCE_BETWEEN_TODAYS_CELL_AND_FIRST_ORDER_OF_THE_DAY = 2
        starting_row = (
            row_number + DISTANCE_BETWEEN_TODAYS_CELL_AND_FIRST_ORDER_OF_THE_DAY
        )
        starting_col = col_number
        # traverse to the TOTAL_HALL_RESIDENTS-th row
        # and menu_count[today]-th column after
        # the starting row and column respectively
        who_ordered_what = {}
        how_many_have_a_resident_ordered = {}
        for menu in range(menu_count[today]):
            residents_who_ordered = []
            menu_items = todays_menu(day, menu_count)[menu]
            contoh_cell_position = find_in_worksheet_values("Contoh")
            DISTANCE_BETWEEN_CONTOH_CELL_AND_FIRST_PERSON = 1
            person_row = (
                contoh_cell_position[0] + DISTANCE_BETWEEN_CONTOH_CELL_AND_FIRST_PERSON
            )
            for person in range(TOTAL_HALL_RESIDENTS):
                person_cell = find_in_worksheet_cells(
                    person_row + person, contoh_cell_position[1]
                )
                order_cell = find_in_worksheet_cells(
                    person_row + person, find_in_worksheet_values(menu_items)[1]
                )
                if (
                    person_cell.value is not None
                    and order_cell.value is not None
                    and len(person_cell.value) > 0
                    and len(order_cell.value) > 0
                ):
                    letter = 65
                    pack_count = int(order_cell.value)
                    if pack_count > 1:
                        for count in range(pack_count):
                            residents_who_ordered.append(person_cell.value)
                            who_ordered_what[menu_items] = residents_who_ordered
                            letter += 1
                            how_many_have_a_resident_ordered[person_cell.value] = letter
                    else:
                        residents_who_ordered.append(person_cell.value)
                        who_ordered_what[menu_items] = residents_who_ordered
                        letter += 1
                        how_many_have_a_resident_ordered[person_cell.value] = letter
                else:
                    continue
        # Find how many food one resident
        # ordered across different menus
        # on the same day
        # eg. Iwan order 1 nasi tomato & 2 bubur ayam
        letter_A = 65
        letter_tracking = {}
        who_ordered_what_count = {}
        those_ordered_more_than_one = {}
        for menu_items, residents in who_ordered_what.items():
            for resident in residents:
                if resident not in who_ordered_what_count:
                    who_ordered_what_count[resident] = 1
                else:
                    who_ordered_what_count[resident] += 1
                    those_ordered_more_than_one[resident] = who_ordered_what_count[
                        resident
                    ]
                    letter_tracking[resident] = letter_A
        total_pax = 0
        pax_for_menu_items = {}
        for menu_items, residents in who_ordered_what.items():
            i = 1
            body += "\n" + menu_items + "\n\n"
            for resident in residents:
                if resident in those_ordered_more_than_one:
                    current_letter = letter_tracking[resident]
                    body += f"{str(i)}. {resident.capitalize()} {chr(current_letter)}\n"
                    letter_tracking[resident] += 1
                else:
                    body += f"{str(i)}. {resident.capitalize()}\n"
                i += 1
                total_pax += 1
            pax_for_menu_items[menu_items] = i
        for menu, pax in pax_for_menu_items.items():
            body += f"\n{pax - 1} pax for {menu}\n\n"
        body += "\n" + f"Total {total_pax} pax hari ni.\nThank you Abg Sam!\n"
        message = client.messages.create(
            messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
            body=body,
            to=os.getenv("FOOD_DIRECTOR_PHONE_NUMBER"),
        )


todays_order()
