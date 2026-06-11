import pandas as pd
from tabulate import tabulate

df = pd.read_csv('timetabledata.csv')

# Print using a clean grid format, hiding the index numbers
print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))