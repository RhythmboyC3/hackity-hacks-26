import os
from wsgiref import headers
import pandas as pd 
import csv


# Begin declarations
timetabledata = pd.read_csv('timetabledata.csv')

#print(timetabledata.to_string(index=False))


# Begin declaring functions and stuff
def clearterm():
    # 'cls' is for Windows, 'clear' is for Mac and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_input():
    print_timetable()
    print("In viewing mode. Input q to quit, e to edit")
    valid_command = False
    while not valid_command:
        userinput = str(input(">"))
        match userinput:
            case "q":
                pass
            case "e":
                edit_mode_UI()
            case _:
                print("Invalid command. Input q to quit, e to edit")
            
    
def print_timetable():
    # Yes I'm aware of libraries that can work, but I don't want to wrestle with pip
    cellwidth = 11
    tablewidth = cellwidth * 7
    headers = timetabledata.columns.tolist()

    # Print pretty little top part
    for header in headers:
        print("+",end="")
        for i in range(cellwidth+1):
            print("─", end="")
    print("+")

    # Print header row
    for header in headers:
        print("| " + header, end="")
        if len(header) < cellwidth:
            for i in range(cellwidth - len(header)):
                print(" ", end="")
    print("|")

    
    print()
    print()


def edit_mode_UI():
    clearterm()

def edit_data():
    pass

handle_input()