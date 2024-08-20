import tkinter as tk

root = tk.Tk()
root.geometry("868x131")
button = tk.Button(root, text="A Button")
button.place(x=2, y=2)

frame = tk.LabelFrame(root, text="A LabelFrame using place", bg="cyan")
# Frame using place with x, y, width, height in absolute coordinates
frame.place(x=250, y=20, width=600, height=70)

child_button = tk.Button(frame, text="A Button IN LabelFrame", bg="white")
# Note: place x,y is referenced to the container (Frame)
# Note: place uses just x,y and allows Button to determine width and height
child_button.place(x=2, y=2)

label = tk.Label(
    root,
    text="A Label on LabelFrame\nWith multiple lines\nOf Text.",
    bg="light green",
)
# Label sits on top of buttonFrame and Frame
# Note place uses just x,y and allows Label to determine width and height
label.place(x=330, y=60)

root.mainloop()