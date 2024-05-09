#! /usr/bin/env python3

# ---------------------------------------------------------------------------------------------------------------------
# Imports and Constants

import os
import sys
import csv
import readline
from unilog import *
from datetime import datetime
from tabulate import tabulate


PATH        = f"/home/{os.getlogin()}/.config/pytrack/"
FILE        = "tasks.csv"
FILEPATH    = f"{PATH}{FILE}"

SORTING     = "default"

MAJOR       = "1"
MINOR       = "19"
PATCH       = "a"

SORTING     = [0, 2, 1, 3, 4]
FILTER      = ["","","","",""]

logo = [
    f"",
    f"{FG.BLUE}  ██████╗ ██╗   ██╗{FG.MAGENTA}████████╗██████╗  █████╗  ██████╗██╗  ██╗",
    f"{FG.BLUE}  ██╔══██╗╚██╗ ██╔╝{FG.MAGENTA}╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝",
    f"{FG.BLUE}  ██████╔╝ ╚████╔╝ {FG.MAGENTA}   ██║   ██████╔╝███████║██║     █████╔╝ \t{FG.WHITE}by luks",
    f"{FG.BLUE}  ██╔═══╝   ╚██╔╝  {FG.MAGENTA}   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ \t{FG.WHITE}v{MAJOR}.{MINOR}",
    f"{FG.BLUE}  ██║        ██║   {FG.MAGENTA}   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗",
    f"{FG.BLUE}  ╚═╝        ╚═╝   {FG.MAGENTA}   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝",
    f"{UTIL.RESET}"
]


# ---------------------------------------------------------------------------------------------------------------------


def SysReq():
    if sys.platform != "linux":
        Log(LVL.FAIL, f"Operating System not supported: {sys.platform}")
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    return True


# ---------------------------------------------------------------------------------------------------------------------


def ReadTasks():
    tasks = []
    if os.path.exists(FILEPATH):
        try:
            with open(FILEPATH, newline="") as file:
                reader = csv.reader(file)
                tasks = list(reader)
        except Exception as e:
            Log(LVL.FAIL, f"{e}")

    tasks = ApplyFilter(tasks)
    return sorted(tasks, key=lambda x: (x[SORTING[0]],x[SORTING[1]],x[SORTING[2]],x[SORTING[3]],x[SORTING[4]]))


# ---------------------------------------------------------------------------------------------------------------------


def SetSorting(values):
    values = values.split(",")
    for i in range(len(values)):
        SORTING[i] = int(values[i])


# ---------------------------------------------------------------------------------------------------------------------


def ApplyFilter(tasks):
    filtered_tasks = []
    for i in range(len(tasks)):
        valid_task = True
        for j in range(len(FILTER)):
            if tasks[i][j] == FILTER[j] or FILTER[j] == "":
                continue
            valid_task = False
        if valid_task:
            filtered_tasks.append(tasks[i])
    return filtered_tasks


def SetFilter(filters):
    filters = filters.split(",")
    for f in filters:
        f = f.split("=")
        FILTER[int(f[0])] = f[1]


# ---------------------------------------------------------------------------------------------------------------------


def WriteTask(category, task):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")
    wday = datetime.now().strftime("%A")
    with open(FILEPATH, "a") as file:
        file.write(f"{date},{wday[:2]},{time},{category},{task}\n")


# ---------------------------------------------------------------------------------------------------------------------


def DisplayTasks():
    tasks = ReadTasks()
    headers = [
        f"{UTIL.BOLD}Date{UTIL.RESET}",
        f"{UTIL.BOLD}Day{UTIL.RESET}",
        f"{UTIL.BOLD}Time{UTIL.RESET}",
        f"{UTIL.BOLD}Category{UTIL.RESET}",
        f"{UTIL.BOLD}Task{UTIL.RESET}"
    ]
    lines = tabulate(tasks[-(os.get_terminal_size().lines - 12):], headers=headers).split('\n')
    for line in lines:
        print(f"  {line}")

# ---------------------------------------------------------------------------------------------------------------------


def ParseTask(task):
    try:
        cmd, arg = task.split(" ",maxsplit=1)

    except ValueError:
        match task:
            case "exit":    exit(0)
            case "edit":    os.system(f"vim {FILEPATH}")
        return

    match cmd:
        case "sort":        SetSorting(arg)
        case "filter":      SetFilter(arg)
        case _:             WriteTask(cmd, arg)


# ---------------------------------------------------------------------------------------------------------------------


def Prompt():
    print(f"{UTIL.CLEAR}{UTIL.TOP}",end="")    
    for line in logo:
        print(line)

    DisplayTasks()

    task = input(f"\n  {UTIL.BOLD}Add Task: {UTIL.RESET}")
    if len(task):
        ParseTask(task)


# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    if len(sys.argv) > 1:
        FILEPATH = sys.argv[1]
    if not SysReq():
        exit(1)
    while True:
        try:
            Prompt()
        except KeyboardInterrupt:
            Log(LVL.WARN, "Nice try lol")
