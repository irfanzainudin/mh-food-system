#################################
# FAILED ATTEMPT AT         	#
# DYNAMICALLY FIGURING OUT  	#
# THE NUMBER OF MENUS       	#
# FOR EACH WEEKDAY          	#
# 								#
# 								#
# ARCHIVED FOR MEMORY'S SAKE	#
#################################

# i = 0
# day_int = datetime.today().weekday()
# day_menu_count = {}
# currentDay = ""
#     for day in worksheet.row_values(day_row):
#         if len(day) == 0:
#             i += 1
#             day_menu_count[currentDay] = i
#         elif len(day) > 0 and day in weekdays:
#             if day not in day_menu_count:
#                 i = 0
#             i += 1
#             day_menu_count[day] = i
#             currentDay = day
#         else:
#             continue

# print(day_menu_count)
