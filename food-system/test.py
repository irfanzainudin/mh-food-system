from datetime import datetime
import pywhatkit

pywhatkit.sendwhatmsg(
    "+61401570603", "Test", datetime.now().hour, datetime.now().minute + 1
)
# print(datetime.now().hour)
# print(datetime.now().minute)
