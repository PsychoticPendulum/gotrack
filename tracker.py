#! /usr/bin/env python3

import os
import sys
import readline
from unilog import *
from datetime import datetime

import csv
from tabulate import tabulate


path = "./tasks.csv"
logo = [
    f"{FG.CYAN}{UTIL.BOLD}",
    f"{FG.CYAN}  ██████╗  ██████╗ {FG.WHITE}████████╗██████╗  █████╗  ██████╗██╗  ██╗",
    f"{FG.CYAN} ██╔════╝ ██╔═══██╗{FG.WHITE}╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝",
    f"{FG.CYAN} ██║  ███╗██║   ██║{FG.WHITE}   ██║   ██████╔╝███████║██║     █████╔╝ ",
    f"{FG.CYAN} ██║   ██║██║   ██║{FG.WHITE}   ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ",
    f"{FG.CYAN} ╚██████╔╝╚██████╔╝{FG.WHITE}   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗",
    f"{FG.CYAN}  ╚═════╝  ╚═════╝ {FG.WHITE}   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝",
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


def DisplayTasks(date="any"):

    with open("tasks.csv", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        data = list(csvreader)

    headers = [
        f"{UTIL.BOLD}Date{UTIL.RESET}",
        f"{UTIL.BOLD}Day{UTIL.RESET}",
        f"{UTIL.BOLD}Time{UTIL.RESET}",
        f"{UTIL.BOLD}Category{UTIL.RESET}",
        f"{UTIL.BOLD}Task{UTIL.RESET}"
    ]
    lines = tabulate(data[-(os.get_terminal_size().lines - 12):], headers=headers).split('\n')
    for line in lines:
        print(f"  {line}")


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
    elif task.split(" ")[0] == "search":
        DisplayTasks(task.split(" ")[1])
        input()
    elif task == "all":
        DisplayTasks()
        exit(0)
    else:
        if not "," in task:
            category = input(f"{UTIL.BOLD}Category: {UTIL.RESET}")
            task = f"{category},{task}"
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
