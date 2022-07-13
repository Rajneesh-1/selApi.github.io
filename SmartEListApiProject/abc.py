from datetime import datetime

import pytz


def isTodayDate(input_date):
    inputFormattedDate = datetime.strptime(str(datetime.strptime(input_date.split('+')[0], '%a, %d %b %Y %H:%M:%S ')).split(" ")[0], '%Y-%m-%d')
    current_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    currentFormattedDate = datetime.strptime(str(datetime.strptime(str(current_date).split('.')[0], '%Y-%m-%d %H:%M:%S')).split(" ")[0], '%Y-%m-%d')
    print("inputFormattedDate: ", inputFormattedDate)
    print("currentFormattedDate: ", currentFormattedDate)

    if (currentFormattedDate - inputFormattedDate).total_seconds() == 0:
        return True
    else:
        return False


input_data = "Sun, 27 Feb 2022 16:33:51 +0530"
try:
    if isTodayDate(input_data):
        print("Matched")
    else:
        print("Not Matched")
except:
    print("Not Matched")
