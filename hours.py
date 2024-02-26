import os
import csv

def main():
    name = get_name()
    day = get_day()
    hours = get_hours()
    mins = get_minutes()
    mins = int(mins)
    hours = int(hours)
    time_worked = f"{hours}:{mins:02d}"
    save_data(name, day, time_worked)

def get_name():
    valid_first = False
    valid_last = False
    while not valid_first:
        first = input("Enter your first name: ")
        if not first.isalpha():
            valid_first = False
        else:
            valid_first = True
    while not valid_last:
        last = input("Enter your last name: ")
        if not last.isalpha():
            valid_last = False
        else:
            valid_last = True
    full_name = f"{first.title()} {last.title()}"
    return full_name
def get_day():
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    valid_day = False
    while not valid_day:
        day = input("Enter a day of the week: ").title()
        if day not in days:
            valid_day = False
        else:
            valid_day = True
    return day

def get_hours():
    valid_hours = False
    while not valid_hours:
        hours = input("Enter number of hours worked: ")
        if not hours.isdigit():
            valid_hours = False
        else:
            if len(hours) != 1 and len(hours) != 2:
                valid_hours = False
            else:
                if int(hours) > 24 or int(hours) < 0:
                    valid_hours = False
                else:
                    valid_hours = True
    return hours

def get_minutes():
    valid_mins = False
    while not valid_mins:
        mins = input("Enter number of minutes worked: ")
        if not mins.isdigit():
            valid_mins = False
        else:
            if len(mins) > 2 and len(mins) < 0:
                valid_mins = False
            else:
                if int(mins) > 59 or int(mins) < 0:
                    valid_mins = False
                else:
                    valid_mins = True
    return mins

def save_data(name, day, time_worked):
    headers = ["Employee", "Day Worked", "Hours Worked"]
    data = [name, day, time_worked]
    if os.path.isfile("Timepunches.txt"):
        with open("Timepunches.txt", "a", newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(data)
    elif not os.path.isfile("Timepunches.txt"):
        with open("Timepunches.txt", "w", newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(headers)
            writer.writerow(data)

if __name__ == "__main__":
    main()
