import os
import pandas as pd 
import csv


# Begin declarations
timetabledata = pd.read_csv('timetabledata.csv')

#print(timetabledata.head())


# Begin declaring functions and stuff
def clearterm():
    # 'cls' is for Windows, 'clear' is for Mac and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_input():
    print("In viewing mode. Input q to quit, e to edit")
    valid_command = False
    while not valid_command:
        userinput = str(input(">"))
        match userinput:
            case "q":
                valid_command = True
                pass
            case "e":
                edit_mode_UI()
            case _:
                print("Invalid command. Input q to quit, e to edit")
            
    


def edit_mode_UI():
    pass

def edit_data():
    pass

handle_input()