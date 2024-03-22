#! /usr/bin/env python3

import os
import sys
import readline
from unilog import *
from datetime import datetime


path = "./tasks.csv"
logo = [
    f"{FG.CYAN}{UTIL.BOLD} _____               _             ",
    f"|_   _| __ __ _  ___| | _____ _ __ ",
    f"  | || '__/ _` |/ __| |/ / _ \ '__|",
    f"  | || | | (_| | (__|   <  __/ |   ",
    f"  |_||_|  \__,_|\___|_|\_\___|_|   ",
    f"{UTIL.RESET}"
]
                                        

def ReadTasks():
    tasks = []
    try:
        with open(path, "r") as file:
            for line in file.readlines():
                tasks.append(line.rstrip("\n"))
    except:
        pass
    return tasks


def WriteTask(task):
    date    = datetime.now().strftime("%Y-%m-%d")
    time    = datetime.now().strftime("%H:%M")
    weekday = datetime.now().strftime("%A")
    result = f""

    with open(path, "a") as file:
        file.write(f"{date},{weekday[:2]},{time},{task}\n")
    
    return True


def DisplayTasks():
    tasks = ReadTasks()

    for task in tasks[-(os.get_terminal_size().lines - 8):]:
        task = task.split(",")

        for t in task:
            print(f"  {t}",end="")
        
        print("")


def Prompt():
    print(f"{UTIL.CLEAR}{UTIL.TOP}",end="")

    for line in logo:
        print(line)

    DisplayTasks()
    
    task = input(f"\n{UTIL.BOLD}Add Task: {UTIL.RESET}")

    if task == "exit":
        exit(0)
    elif task == "":
        return
    elif task == "edit":
        os.system(f"vim {path}")
    else:
        if WriteTask(task):
            print(f"{UTIL.UP}{FG.GREEN}Add Task:{UTIL.RESET}")


def GetTermSize():
    size = os.get_terminal_size()
    return size.columns, size.lines


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]

    while True:
        try:
            Prompt()
        except KeyboardInterrupt:
            exit(1)