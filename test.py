import tkinter as tk

def on_enter(event):
    # Changes background to light gray and text to blue on hover
    event.widget.config(background="#d9d9d9", foreground="blue")

def on_leave(event):
    # Reverts back to standard system colors when mouse leaves
    event.widget.config(background="SystemButtonFace", foreground="black")

root = tk.Tk()
root.geometry("300x200")

# Create a standard button
my_button = tk.Button(root, text="Hover Over Me", bg="SystemButtonFace", fg="black")
my_button.pack(pady=50)

# Bind the hover actions
my_button.bind("<Enter>", on_enter)
my_button.bind("<Leave>", on_leave)

root.mainloop()
