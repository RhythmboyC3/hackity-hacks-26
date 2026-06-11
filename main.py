import os
import subprocess
from unittest import case
import pandas as pd 
from time import sleep

# Notes:
# If you intend to call another function, return or else the 1st function still runs

# Begin declarations
timetabledata = pd.read_csv('timetabledata.csv', dtype=object).fillna("")

cellwidth = 11
tablewidth = cellwidth * 7
#print(timetabledata.to_string(index=False))


# Begin declaring functions and stuff
def clear_terminal():
    # Modern approach using subprocess instead of os.system
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True)

""" <- THE CODE FOR THE TIMETABLE FUNCTION BELOW ->"""

def handle_input():
    global timetabledata
    print_timetable(timetabledata)
    message = "In viewing mode. Input q to quit, e to edit, c to clear"
    print(message)
    valid_command = False
    while not valid_command:
        userinput = str(input("> ")).lower()
        match userinput:
            case "q":
                valid_command = True
                main_menu()
                return

            case "e":
                edit_mode_UI()
                return
            case "c":
                clear_terminal()
                print_timetable(timetabledata)
                print("You sure? Input c again to clear, or any other key to cancel.")
                if str(input("> ")).lower() == "c":
                    print("Clearing...")
                    sleep(1)
                    data = {
                        "Monday": ["", "", "" , "", ""],
                        "Tuesday": ["", "", "" , "", ""],
                        "Wednesday": ["", "", "" , "", ""],
                        "Thursday": ["", "", "" , "", ""],
                        "Friday": ["", "", "" , "", ""],
                        "Saturday": ["", "", "" , "", ""],
                        "Sunday": ["", "", "" , "", ""],
                            }
                    df = pd.DataFrame(data)
                    df.to_csv("timetabledata.csv", index=False)
                    timetabledata = pd.read_csv('timetabledata.csv', dtype=object).fillna("")
                    clear_terminal()
                    handle_input()
                    return
                else:
                    clear_terminal()
                    handle_input()
                    return
            case _:
                message = "Invalid command. Input q to quit, e to edit, c to clear."
                clear_terminal()
                print_timetable(timetabledata)
                print(message)
            
# All functions below are used to print the timetable.
# (print_timetable calls other functions for conciseness and mantainablilty)
    
def print_timetable(datatable):
    # Yes I'm aware of libraries that can work, but I don't want to wrestle with pip
    datatable = datatable.fillna("")
    headers = datatable.columns.tolist()

    print_spacer(datatable)

    # Print header row
    for header in headers:
        print("│ " + header, end="")
        if len(header) < cellwidth:
            for i in range(cellwidth - len(header)):
                print(" ", end="")
    print("│")

    print_spacer(datatable)

    # Print data rows

    print_data_rows(datatable)

    print()
    print()

def print_spacer(datatable):
    # Prints a spacer for each header, conforing to spacing
    headers = datatable.columns.tolist()
    for header in headers:
        print("+",end="")
        for i in range(cellwidth+1):
            print("─", end="")
    print("+")

def print_data_rows(datatable):
    # Iterate through every row
    for index, row in datatable.iterrows():
        for header in datatable.columns:
            data = str(row[header])
            print("│ " + data, end="")
            if len(data) < cellwidth:
                for i in range(cellwidth - len(data)):
                    print(" ", end="")
        print("│")
        print_spacer(datatable)

def edit_mode_UI():
    clear_terminal()
    print_timetable(timetabledata)
    message = "In edit mode. Input name of column to select it, or q to quit."
    print(message)
    valid_command = False
    while not valid_command:
        userinput = str(input("> ")).lower()
        match userinput:
            case "q":
                valid_command = True
                clear_terminal()
                handle_input()
                return

            case "monday"|"tuesday"|"wednesday"|"thursday"|"friday"|"saturday"|"sunday":
                edited = False
                while not edited:
                    clear_terminal()
                    temp = timetabledata.copy().astype(object)
                    col_idx = temp.columns.get_loc(userinput.capitalize())
                    for i in range(len(temp)):
                        temp.iat[i, col_idx] = i + 1
                    print_timetable(temp)

                    valid_rows = [str(i) for i in range(1, len(temp) + 1)]
                    rowinput = ""
                    while rowinput not in valid_rows:
                        print(f"Currently editing {userinput.capitalize()}. Input row number (1-{len(temp)}) to select, q to quit.")
                        rowinput = str(input("> ")).strip().lower()
                        if rowinput == "q":
                            clear_terminal()
                            print_timetable(timetabledata)
                            print(message)
                            break
                        clear_terminal()
                        print_timetable(temp)

                    if rowinput == "q":
                        break

                    row_index = int(rowinput) - 1
                    clear_terminal()
                    temp = timetabledata.copy().astype(object)
                    temp.iat[row_index, col_idx] = "SELECTED"
                    print_timetable(temp)
                    message = "Max characters 10. Input new value for "
                    print(message + userinput.capitalize() + ", " + rowinput)
                    textinput = ""
                    while not textinput:
                        textinput = str(input("> ")).strip()
                        if len(textinput) > 10:
                            clear_terminal()
                            print_timetable(temp)
                            print("Max characters exceeded. Input a shorter value for " + userinput.capitalize() + ", " + rowinput)
                            textinput = ""
                    clear_terminal()
                    print_timetable(temp)
                    print("Saving...")
                    timetabledata.iat[row_index, col_idx] = textinput
                    sleep(1)
                    print("Saved!")
                    edited = True
                    sleep(1)
                    clear_terminal()
                    timetabledata.to_csv("timetabledata.csv", index=False)
                    handle_input()
                    return  
            case _:
                message = "Invalid command. Input name of column to select it, or q to quit"
                clear_terminal()
                print_timetable(timetabledata)
                print(message)

def edit_data():
    pass

""" <- THE CODE FOR THE TIMETABLE FUNCTION ENDS HERE ->"""

""" <-- THIS IS THE MAIN MENU FUNCTION (Expand off the case here) ->"""
def main_menu():
    clear_terminal()
    message = "This is the main menu. Input 1 to go to Timetable Mode, q to quit."
    while True: 
        # Looks cool
        print(r""" ___       __   _______   ___       ________  ________  _____ ______   _______   ___       
|\  \     |\  \|\  ___ \ |\  \     |\   ____\|\   __  \|\   _ \  _   \|\  ___ \ |\  \      
\ \  \    \ \  \ \   __/|\ \  \    \ \  \___|\ \  \|\  \ \  \\\__\ \  \ \   __/|\ \  \     
 \ \  \  __\ \  \ \  \_|/_\ \  \    \ \  \    \ \  \\\  \ \  \\|__| \  \ \  \_|/_\ \  \    
  \ \  \|\__\_\  \ \  \_|\ \ \  \____\ \  \____\ \  \\\  \ \  \    \ \  \ \  \_|\ \ \__\   
   \ \____________\ \_______\ \_______\ \_______\ \_______\ \__\    \ \__\ \_______\|__|   
    \|____________|\|_______|\|_______|\|_______|\|_______|\|__|     \|__|\|_______|   ___ 
                                                                                      |\__\
                                                                                      \|__|
                                                                                           """)

        print(message)
        user_input = str(input("> ")).lower()
        match user_input:
            case "1":
                clear_terminal()
                handle_input()
                return
            case "q":
                print("Saving...")
                timetabledata.to_csv("timetabledata.csv", index=False)
                sleep(1)
                print("Bye!")
                quit()
            case _:
                message = "Invalid command. Input 1 to go to Timetable Mode, q to quit."
                clear_terminal()

main_menu()