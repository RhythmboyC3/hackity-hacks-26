# Timetable Editor

This project keeps the original terminal timetable UI and adds a new Tkinter GUI editor that shares the same CSV data.

## Run the terminal version

```bash
python main.py
```

Then choose option `1` for the terminal timetable interface.

## Run the Tkinter GUI version

```bash
python main.py
```

Then choose option `2` to open the GUI and use the in-app main menu for the timetable editor.
You can also run the GUI directly:

```bash
python gui.py
```

## Data file

The timetable is stored in `timetabledata.csv`.
Changes made in either the terminal UI or the GUI are saved to the same file.

## Notes

- The terminal mode supports viewing, editing, and clearing the timetable.
- The GUI mode offers a grid editor with Save, Clear All, Reload, and Close buttons.
- The GUI code is kept in `gui.py` so it is simple to expand from there.

Please wait.