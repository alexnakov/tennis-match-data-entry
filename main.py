import tkinter as tk
from tkinter import messagebox

my_lightblue = '#b2d6fe'

def submit_data():
    """Function to handle the form submission"""
    data = {
        "1st Serve Direction": listbox_1st_direction.get(tk.ACTIVE),
        "1st Serve Result": listbox_1st_result.get(tk.ACTIVE),
        "2nd Serve Direction": listbox_2nd_direction.get(tk.ACTIVE),
        "2nd Serve Result": listbox_2nd_result.get(tk.ACTIVE),
        "Return - Type": listbox_return_type.get(tk.ACTIVE),
        "Return - Shot": listbox_return_shot.get(tk.ACTIVE),
        "Return - Outcome": listbox_return_outcome.get(tk.ACTIVE),
        "Point Winner": listbox_point_winner.get(tk.ACTIVE),
        "End - Type": listbox_end_type.get(tk.ACTIVE),
        "End - Shot": listbox_end_shot.get(tk.ACTIVE),
        "End - Outcome": listbox_end_outcome.get(tk.ACTIVE),
        "Strategy - Position": listbox_strategy_position.get(tk.ACTIVE),
        "Strategy - Play Style": listbox_strategy_play_style.get(tk.ACTIVE)
    }

    # Display the form data in a message box
    messagebox.showinfo("Form Submitted", f"Data Entered:\n{data}")

def focus_listbox(listbox):
    """Helper function to apply focus styling to a listbox"""
    listbox.config(bg="lightgreen")
    if listbox.size() > 0:
        listbox.activate(0)  # Select the top item
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(0)
        listbox.itemconfig(0, bg=my_lightblue)

def unfocus_listbox(listbox, last_active_index):
    """Helper function to remove focus styling and highlight the last active item"""
    listbox.config(bg="white")
    for i in range(listbox.size()):
        listbox.itemconfig(i, bg="white")
    if last_active_index is not None and 0 <= last_active_index < listbox.size():
        listbox.itemconfig(last_active_index, bg=my_lightblue)

def move_focus(event):
    """Move the focus between listboxes when left or right arrow is pressed"""
    current_widget = event.widget
    next_widget = None
    previous_widget = None
    listboxes = [
        listbox_1st_direction, listbox_1st_result,
        listbox_2nd_direction, listbox_2nd_result,
        listbox_return_type, listbox_return_shot,
        listbox_return_outcome, listbox_point_winner,
        listbox_end_type, listbox_end_shot,
        listbox_end_outcome, listbox_strategy_position,
        listbox_strategy_play_style
    ]
    num_listboxes = len(listboxes)
    current_index = listboxes.index(current_widget)

    # Unhighlight the current listbox
    active_index = current_widget.index(tk.ACTIVE) if current_widget.size() > 0 else None
    unfocus_listbox(current_widget, active_index)

    if event.keysym == "Right":
        next_index = current_index + 1
        if next_index < num_listboxes:
            next_widget = listboxes[next_index]
    elif event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]

    if next_widget:
        next_widget.focus_set()
        focus_listbox(next_widget)

def on_focus_in(event):
    """Handle focus entering a listbox"""
    listbox = event.widget
    listbox.config(bg="lightgreen")
    if listbox.size() > 0:
        active_index = listbox.index(tk.ACTIVE)
        if active_index != -1:
            # Clear previous blue highlights
            for i in range(listbox.size()):
                listbox.itemconfig(i, bg=listbox.cget("background"))
            # Highlight the active item in blue
            listbox.itemconfig(active_index, bg=my_lightblue)
        else:
            # If no item is active, highlight the first item in blue
            listbox.activate(0)
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(0)
            listbox.itemconfig(0, bg=my_lightblue)

def on_listbox_select(event):
    """Handle selection change in a listbox to highlight the active item"""
    listbox = event.widget
    for i in range(listbox.size()):
        listbox.itemconfig(i, bg=listbox.cget("background")) # Reset all to listbox background
    if listbox.curselection():
        index = int(listbox.curselection()[0])
        listbox.itemconfig(index, bg=my_lightblue)
    """Handles the up arrow key press for listbox wrap-around."""
    listbox = event.widget
    current_index = listbox.curselection()

    if current_index:
        current_index = int(current_index[0])
        if current_index == 0:
            # Select the last item
            listbox.selection_clear(0, tk.END)
            listbox.activate(listbox.size() - 1)
            listbox.selection_set(listbox.size() - 1)
            listbox.see(listbox.size() - 1) # Ensure the last item is visible
            # Update the visual highlight (optional, depending on your highlight logic)
            on_listbox_select(event)
        elif current_index > 0:
            # Move selection up normally
            listbox.selection_clear(current_index)
            listbox.activate(current_index - 1)
            listbox.selection_set(current_index - 1)
            listbox.see(current_index - 1) # Ensure the previous item is visible
            # Update the visual highlight
            on_listbox_select(event)

# Main app window
app = tk.Tk()
app.title("Tennis Data Entry App")
app.geometry("1200x700")
app.configure(bg="#f0f0f0")

# -------------------------
# 💡 Split the window into top and bottom halves
# -------------------------
top_frame = tk.Frame(app, height=200, bg=my_lightblue)
top_frame.pack(side="top", fill="both", expand=True)

bottom_frame = tk.Frame(app, height=500, bg="#ffffff", relief="ridge", bd=2)
bottom_frame.pack(side="bottom", fill="both", expand=True)

# -------------------------
# 🎯 Labels in One Row (Serve, Return, Point Winner)
# -------------------------

# Labels (single row)
tk.Label(bottom_frame, text="1st Serve", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="nw")
tk.Label(bottom_frame, text="2nd Serve", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=2, padx=10, pady=5, sticky="nw")
tk.Label(bottom_frame, text="Return", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=4, padx=10, pady=5, sticky="nw")
tk.Label(bottom_frame, text="Point Winner", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=6, padx=10, pady=5, sticky="nw")

# -------------------------
# 🎾 Vertical Lists for Serve
# -------------------------

# List items
serve_direction_items = ["Wide", "Body", "Center", "In Net"]
serve_result_items = ["In", "Winner", "Ace", "Fault"]

# --- 1st Serve ---
listbox_1st_direction = tk.Listbox(bottom_frame, height=len(serve_direction_items), width=10, exportselection=False)
for item in serve_direction_items:
    listbox_1st_direction.insert(tk.END, item)
listbox_1st_direction.grid(row=1, column=0, padx=10, pady=0, sticky="nw")
listbox_1st_direction.bind("<Left>", move_focus)  # Bind Left arrow
listbox_1st_direction.bind("<Right>", move_focus)  # Bind Right arrow
listbox_1st_direction.bind("<FocusIn>", on_focus_in)
listbox_1st_direction.bind("<<ListboxSelect>>", on_listbox_select)

listbox_1st_result = tk.Listbox(bottom_frame, height=len(serve_result_items), width=10, exportselection=False)
for item in serve_result_items:
    listbox_1st_result.insert(tk.END, item)
listbox_1st_result.grid(row=1, column=1, padx=10, pady=0, sticky="nw")
listbox_1st_result.bind("<Left>", move_focus)  # Bind Left arrow
listbox_1st_result.bind("<Right>", move_focus)  # Bind Right arrow
listbox_1st_result.bind("<FocusIn>", on_focus_in)
listbox_1st_result.bind("<<ListboxSelect>>", on_listbox_select)

# --- 2nd Serve ---
listbox_2nd_direction = tk.Listbox(bottom_frame, height=len(serve_direction_items), width=10, exportselection=False)
for item in serve_direction_items:
    listbox_2nd_direction.insert(tk.END, item)
listbox_2nd_direction.grid(row=1, column=2, padx=10, pady=0, sticky="nw")
listbox_2nd_direction.bind("<Left>", move_focus)  # Bind Left arrow
listbox_2nd_direction.bind("<Right>", move_focus)  # Bind Right arrow
listbox_2nd_direction.bind("<FocusIn>", on_focus_in)
listbox_2nd_direction.bind("<<ListboxSelect>>", on_listbox_select)

listbox_2nd_result = tk.Listbox(bottom_frame, height=len(serve_result_items), width=10, exportselection=False)
for item in serve_result_items:
    listbox_2nd_result.insert(tk.END, item)
listbox_2nd_result.grid(row=1, column=3, padx=10, pady=0, sticky="nw")
listbox_2nd_result.bind("<Left>", move_focus)  # Bind Left arrow
listbox_2nd_result.bind("<Right>", move_focus)  # Bind Right arrow
listbox_2nd_result.bind("<FocusIn>", on_focus_in)
listbox_2nd_result.bind("<<ListboxSelect>>", on_listbox_select)

# -------------------------
# 🎾 Vertical Lists for Return
# -------------------------

# List items for Return
return_type_items = ["Forehand", "Backhand"]
return_shot_items = ["Return", "Pass", "Approach", "Drop", "Lob"]
return_outcome_items = ["Winner", "Unforced", "Forced"]

# --- Return - Type ---
listbox_return_type = tk.Listbox(bottom_frame, height=len(return_type_items), width=10, exportselection=False)
for item in return_type_items:
    listbox_return_type.insert(tk.END, item)
listbox_return_type.grid(row=1, column=4, padx=10, pady=0, sticky="nw")
listbox_return_type.bind("<Left>", move_focus)  # Bind Left arrow
listbox_return_type.bind("<Right>", move_focus)  # Bind Right arrow
listbox_return_type.bind("<FocusIn>", on_focus_in)
listbox_return_type.bind("<<ListboxSelect>>", on_listbox_select)

# --- Return - Shot ---
listbox_return_shot = tk.Listbox(bottom_frame, height=len(return_shot_items), width=12, exportselection=False)
for item in return_shot_items:
    listbox_return_shot.insert(tk.END, item)
listbox_return_shot.grid(row=1, column=5, padx=10, pady=0, sticky="nw")
listbox_return_shot.bind("<Left>", move_focus)  # Bind Left arrow
listbox_return_shot.bind("<Right>", move_focus)  # Bind Right arrow
listbox_return_shot.bind("<FocusIn>", on_focus_in)
listbox_return_shot.bind("<<ListboxSelect>>", on_listbox_select)

# --- Return - Outcome ---
listbox_return_outcome = tk.Listbox(bottom_frame, height=len(return_outcome_items), width=10, exportselection=False)
for item in return_outcome_items:
    listbox_return_outcome.insert(tk.END, item)
listbox_return_outcome.grid(row=1, column=6, padx=10, pady=0, sticky="nw")
listbox_return_outcome.bind("<Left>", move_focus)  # Bind Left arrow
listbox_return_outcome.bind("<Right>", move_focus)  # Bind Right arrow
listbox_return_outcome.bind("<FocusIn>", on_focus_in)
listbox_return_outcome.bind("<<ListboxSelect>>", on_listbox_select)

# listbox point winner

point_winners = ["A", "B"]

# --- Point Winner ---
listbox_point_winner = tk.Listbox(bottom_frame, height=len(point_winners), width=10, exportselection=False)
for item in point_winners:
    listbox_point_winner.insert(tk.END, item)
listbox_point_winner.grid(row=1, column=7, padx=10, pady=0, sticky="nw")
listbox_point_winner.bind("<Left>", move_focus)  # Bind Left arrow
listbox_point_winner.bind("<Right>", move_focus)  # Bind Right arrow
listbox_point_winner.bind("<FocusIn>", on_focus_in)
listbox_point_winner.bind("<<ListboxSelect>>", on_listbox_select)

# -------------------------
# 🎯 New Row - End Section
# -------------------------

# Label
tk.Label(bottom_frame, text="End", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=2, column=0, padx=10, pady=15, sticky="nw")

# List items for End
end_type_items = ["Forehand", "Backhand"]
end_shot_items = ["Drive", "Volley", "Smash", "Pass", "Approach", "Lob", "Drop"]
end_outcome_items = ["Winner", "Force", "Unforced"]

# --- End - Type ---
listbox_end_type = tk.Listbox(bottom_frame, height=len(end_type_items), width=10, exportselection=False)
for item in end_type_items:
    listbox_end_type.insert(tk.END, item)
listbox_end_type.grid(row=3, column=0, padx=10, pady=0, sticky="nw")
listbox_end_type.bind("<Left>", move_focus)  # Bind Left arrow
listbox_end_type.bind("<Right>", move_focus)  # Bind Right arrow
listbox_end_type.bind("<FocusIn>", on_focus_in)
listbox_end_type.bind("<<ListboxSelect>>", on_listbox_select)

# --- End - Shot ---
listbox_end_shot = tk.Listbox(bottom_frame, height=len(end_shot_items), width=12, exportselection=False)
for item in end_shot_items:
    listbox_end_shot.insert(tk.END, item)
listbox_end_shot.grid(row=3, column=1, padx=10, pady=0, sticky="nw")
listbox_end_shot.bind("<Left>", move_focus)  # Bind Left arrow
listbox_end_shot.bind("<Right>", move_focus)  # Bind Right arrow
listbox_end_shot.bind("<FocusIn>", on_focus_in)
listbox_end_shot.bind("<<ListboxSelect>>", on_listbox_select)

# --- End - Outcome ---
listbox_end_outcome = tk.Listbox(bottom_frame, height=len(end_outcome_items), width=10, exportselection=False)
for item in end_outcome_items:
    listbox_end_outcome.insert(tk.END, item)
listbox_end_outcome.grid(row=3, column=2, padx=10, pady=0, sticky="nw")
listbox_end_outcome.bind("<Left>", move_focus)  # Bind Left arrow
listbox_end_outcome.bind("<Right>", move_focus)  # Bind Right arrow
listbox_end_outcome.bind("<FocusIn>", on_focus_in)
listbox_end_outcome.bind("<<ListboxSelect>>", on_listbox_select)

# -------------------------
# 🎯 New Row - Strategy Section (same row as End)
# -------------------------

# Label
tk.Label(bottom_frame, text="Strategy", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=3, column=3, padx=10, pady=15, sticky="nw")

# List items for Strategy
strategy_position_items = ["Baseline", "A at net", "B at net", "Both at net"]
strategy_play_style_items = ["", "Serve and Volley"]

# --- Strategy - Position ---
listbox_strategy_position = tk.Listbox(bottom_frame, height=len(strategy_position_items), width=15, exportselection=False)
for item in strategy_position_items:
    listbox_strategy_position.insert(tk.END, item)
listbox_strategy_position.grid(row=3, column=4, padx=10, pady=0, sticky="nw")
listbox_strategy_position.bind("<Left>", move_focus)  # Bind Left arrow
listbox_strategy_position.bind("<Right>", move_focus)  # Bind Right arrow
listbox_strategy_position.bind("<FocusIn>", on_focus_in)
listbox_strategy_position.bind("<<ListboxSelect>>", on_listbox_select)

# --- Strategy - Play Style ---
listbox_strategy_play_style = tk.Listbox(bottom_frame, height=len(strategy_play_style_items), width=15, exportselection=False)
for item in strategy_play_style_items:
    listbox_strategy_play_style.insert(tk.END, item)
listbox_strategy_play_style.grid(row=3, column=5, padx=10, pady=0, sticky="nw")
listbox_strategy_play_style.bind("<Left>", move_focus)  # Bind Left arrow
listbox_strategy_play_style.bind("<Right>", move_focus)  # Bind Right arrow
listbox_strategy_play_style.bind("<FocusIn>", on_focus_in)
listbox_strategy_play_style.bind("<<ListboxSelect>>", on_listbox_select)

# -------------------------
# 🚀 Submit button
# -------------------------
submit_btn = tk.Button(bottom_frame, text="Submit", command=submit_data, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
submit_btn.grid(row=4, column=0, columnspan=8, pady=15)

listbox_1st_direction.focus_set()


# Create a simple object with a 'widget' attribute
class FakeEvent:
    def __init__(self, widget):
        self.widget = widget

on_focus_in(FakeEvent(widget=listbox_1st_direction))


# Run the app
app.mainloop()