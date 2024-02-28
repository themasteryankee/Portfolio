import csv
import sys
import os

def main():
    #Requires one command-line argument
    if len(sys.argv) != 2:
        print("This program requires exactly one command-line argument.")
        sys.exit(0)
    task = sys.argv[1]
    header = "To Do:"
    flag = False
    #If Tasks.csv file exists
    if os.path.isfile("Tasks.csv"):
        #Open file
        with open("Tasks.csv", "r", newline='') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        #If task is already in file, remove it
        for line in lines:
            if line == task:
                lines.remove(task)
                flag = True
        #Rewrite the file after removing task
        if flag:
            with open("Tasks.csv", "w", newline='') as file:
                writer = csv.writer(file, delimiter='|')
                for line in lines:
                    writer.writerow([line])
        #If a task was not removed, append the new task to file
        elif not flag:
            with open("Tasks.csv", "a", newline='') as file:
                writer = csv.writer(file, delimiter='|')
                writer.writerow([task])
    #If Tasks.csv does not exist, create file and write header and task to file
    elif not os.path.isfile("Tasks.csv"):
        with open("Tasks.csv", "w", newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow([header])
            writer.writerow([task])

if __name__ == "__main__":
    main()
