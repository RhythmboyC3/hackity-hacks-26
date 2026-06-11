import os
from wsgiref import headers
import pandas as pd 
import csv


# Begin declarations
timetabledata = pd.read_csv('timetabledata.csv')

cellwidth = 11
tablewidth = cellwidth * 7
#print(timetabledata.to_string(index=False))


# Begin declaring functions and stuff
def clear_terminal():
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
            
# All functions below are used to print the timetable.
# (print_timetable calls other functions for conciseness and mantainablilty)
    
def print_timetable():
    # Yes I'm aware of libraries that can work, but I don't want to wrestle with pip
    global timetabledata
    timetabledata = timetabledata.fillna("")
    headers = timetabledata.columns.tolist()

    print_spacer()

    # Print header row
    for header in headers:
        print("│ " + header, end="")
        if len(header) < cellwidth:
            for i in range(cellwidth - len(header)):
                print(" ", end="")
    print("│")

    print_spacer()

    # Print data rows

    print_data_rows()

    print()
    print()

def print_spacer():
    # Prints a spacer for each header, conforing to spacing
    headers = timetabledata.columns.tolist()
    for header in headers:
        print("+",end="")
        for i in range(cellwidth+1):
            print("─", end="")
    print("+")

def print_data_rows():
    # Iterate through every row
    for index, row in timetabledata.iterrows():
        for header in timetabledata.columns:
            data = str(row[header])
            print("│ " + data, end="")
            if len(data) < cellwidth:
                for i in range(cellwidth - len(data)):
                    print(" ", end="")
        print("│")
        print_spacer()

        print(timetabledata)

def edit_mode_UI():
    clear_terminal()

def edit_data():
    pass

handle_input()