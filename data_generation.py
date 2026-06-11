# If your folder doesn't contain the csv file, run this to generate it

import pandas as pd

# 1. Create your data table
data = {
    "Monday": ["", "", "" , "", "", "", ""],
    "Tuesday": ["", "", "" , "", "", "", ""],
    "Wednesday": ["", "", "" , "", "", "", ""],
    "Thursday": ["", "", "" , "", "", "", ""],
    "Friday": ["", "", "" , "", "", "", ""],
    "Saturday": ["", "", "" , "", "", "", ""],
    "Sunday": ["", "", "" , "", "", "", ""],
}
df = pd.DataFrame(data)

# 2. Save to CSV (index=False prevents saving row numbers)
df.to_csv("timetabledata.csv", index=False)