import tkinter as tk
from tkinter import messagebox


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


def on_enter(event, listbox):
    """Highlight the entire vertical list when mouse enters"""
    listbox.config(selectbackground="lightgreen")


def on_leave(event, listbox):
    """Remove highlight when mouse leaves the vertical list"""
    listbox.config(selectbackground="green")


# Main app window
app = tk.Tk()
app.title("Tennis Data Entry App")
app.geometry("1200x700")
app.configure(bg="#f0f0f0")

# -------------------------
# 💡 Split the window into top and bottom halves
# -------------------------
top_frame = tk.Frame(app, height=200, bg="#d0e0f0")
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
listbox_1st_direction = tk.Listbox(bottom_frame, height=len(serve_direction_items), width=10, exportselection=False, selectbackground="green")
for item in serve_direction_items:
    listbox_1st_direction.insert(tk.END, item)
listbox_1st_direction.grid(row=1, column=0, padx=10, pady=0, sticky="nw")
listbox_1st_direction.select_set(0)  # Select "Wide" (first item)

listbox_1st_result = tk.Listbox(bottom_frame, height=len(serve_result_items), width=10, exportselection=False, selectbackground="green")
for item in serve_result_items:
    listbox_1st_result.insert(tk.END, item)
listbox_1st_result.grid(row=1, column=1, padx=10, pady=0, sticky="nw")
listbox_1st_result.select_clear(0)  # Deselect all items

# --- 2nd Serve ---
listbox_2nd_direction = tk.Listbox(bottom_frame, height=len(serve_direction_items), width=10, exportselection=False, selectbackground="green")
for item in serve_direction_items:
    listbox_2nd_direction.insert(tk.END, item)
listbox_2nd_direction.grid(row=1, column=2, padx=10, pady=0, sticky="nw")
listbox_2nd_direction.select_clear(0)  # Deselect all items

listbox_2nd_result = tk.Listbox(bottom_frame, height=len(serve_result_items), width=10, exportselection=False, selectbackground="green")
for item in serve_result_items:
    listbox_2nd_result.insert(tk.END, item)
listbox_2nd_result.grid(row=1, column=3, padx=10, pady=0, sticky="nw")
listbox_2nd_result.select_clear(0)  # Deselect all items

# -------------------------
# 🎾 Vertical Lists for Return
# -------------------------

# List items for Return
return_type_items = ["Forehand", "Backhand"]
return_shot_items = ["Return", "Pass", "Approach", "Drop", "Lob"]
return_outcome_items = ["Winner", "Unforced", "Forced"]

# --- Return - Type ---
listbox_return_type = tk.Listbox(bottom_frame, height=len(return_type_items), width=10, exportselection=False, selectbackground="green")
for item in return_type_items:
    listbox_return_type.insert(tk.END, item)
listbox_return_type.grid(row=1, column=4, padx=10, pady=0, sticky="nw")
listbox_return_type.select_clear(0)  # Deselect all items

# --- Return - Shot ---
listbox_return_shot = tk.Listbox(bottom_frame, height=len(return_shot_items), width=12, exportselection=False, selectbackground="green")
for item in return_shot_items:
    listbox_return_shot.insert(tk.END, item)
listbox_return_shot.grid(row=1, column=5, padx=10, pady=0, sticky="nw")
listbox_return_shot.select_clear(0)  # Deselect all items

# --- Return - Outcome ---
listbox_return_outcome = tk.Listbox(bottom_frame, height=len(return_outcome_items), width=10, exportselection=False, selectbackground="green")
for item in return_outcome_items:
    listbox_return_outcome.insert(tk.END, item)
listbox_return_outcome.grid(row=1, column=6, padx=10, pady=0, sticky="nw")
listbox_return_outcome.select_clear(0)  # Deselect all items

# -------------------------
# 🎯 Vertical List for Point Winner
# -------------------------

# List items for Point Winner
point_winner_items = ["A", "B"]

listbox_point_winner = tk.Listbox(bottom_frame, height=len(point_winner_items), width=5, exportselection=False, selectbackground="green")
for item in point_winner_items:
    listbox_point_winner.insert(tk.END, item)
listbox_point_winner.grid(row=1, column=7, padx=10, pady=0, sticky="nw")
listbox_point_winner.select_clear(0)  # Deselect all items

# -------------------------
# 🎾 New Row - End Section
# -------------------------

# Label
tk.Label(bottom_frame, text="End", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=2, column=0, padx=10, pady=15, sticky="nw")

# List items for End
end_type_items = ["Forehand", "Backhand"]
end_shot_items = ["Drive", "Volley", "Smash", "Pass", "Approach", "Lob", "Drop"]
end_outcome_items = ["Winner", "Force", "Unforced"]

# --- End - Type ---
listbox_end_type = tk.Listbox(bottom_frame, height=len(end_type_items), width=10, exportselection=False, selectbackground="green")
for item in end_type_items:
    listbox_end_type.insert(tk.END, item)
listbox_end_type.grid(row=3, column=0, padx=10, pady=0, sticky="nw")
listbox_end_type.select_clear(0)  # Deselect all items

# --- End - Shot ---
listbox_end_shot = tk.Listbox(bottom_frame, height=len(end_shot_items), width=12, exportselection=False, selectbackground="green")
for item in end_shot_items:
    listbox_end_shot.insert(tk.END, item)
listbox_end_shot.grid(row=3, column=1, padx=10, pady=0, sticky="nw")
listbox_end_shot.select_clear(0)  # Deselect all items

# --- End - Outcome ---
listbox_end_outcome = tk.Listbox(bottom_frame, height=len(end_outcome_items), width=10, exportselection=False, selectbackground="green")
for item in end_outcome_items:
    listbox_end_outcome.insert(tk.END, item)
listbox_end_outcome.grid(row=3, column=2, padx=10, pady=0, sticky="nw")
listbox_end_outcome.select_clear(0)  # Deselect all items

# -------------------------
# 🎯 New Row - Strategy Section (same row as End)
# -------------------------

# Label
tk.Label(bottom_frame, text="Strategy", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=3, column=3, padx=10, pady=15, sticky="nw")

# List items for Strategy
strategy_position_items = ["Baseline", "A at net", "B at net", "Both at net"]
strategy_play_style_items = ["Serve and Volley"]

# --- Strategy - Position ---
listbox_strategy_position = tk.Listbox(bottom_frame, height=len(strategy_position_items), width=15, exportselection=False, selectbackground="green")
for item in strategy_position_items:
    listbox_strategy_position.insert(tk.END, item)
listbox_strategy_position.grid(row=3, column=4, padx=10, pady=0, sticky="nw")
listbox_strategy_position.select_clear(0)  # Deselect all items

# --- Strategy - Play Style ---
listbox_strategy_play_style = tk.Listbox(bottom_frame, height=len(strategy_play_style_items), width=15, exportselection=False, selectbackground="green")
for item in strategy_play_style_items:
    listbox_strategy_play_style.insert(tk.END, item)
listbox_strategy_play_style.grid(row=3, column=5, padx=10, pady=0, sticky="nw")
listbox_strategy_play_style.select_clear(0)  # Deselect all items

# -------------------------
# 🚀 Submit button
# -------------------------
submit_btn = tk.Button(bottom_frame, text="Submit", command=submit_data, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
submit_btn.grid(row=4, column=0, columnspan=8, pady=15)

# Bind events to highlight the list and items
listbox_1st_direction.bind("<Enter>", lambda event, lb=listbox_1st_direction: on_enter(event, lb))
listbox_1st_direction.bind("<Leave>", lambda event, lb=listbox_1st_direction: on_leave(event, lb))

listbox_1st_result.bind("<Enter>", lambda event, lb=listbox_1st_result: on_enter(event, lb))
listbox_1st_result.bind("<Leave>", lambda event, lb=listbox_1st_result: on_leave(event, lb))

listbox_2nd_direction.bind("<Enter>", lambda event, lb=listbox_2nd_direction: on_enter(event, lb))
listbox_2nd_direction.bind("<Leave>", lambda event, lb=listbox_2nd_direction: on_leave(event, lb))

listbox_2nd_result.bind("<Enter>", lambda event, lb=listbox_2nd_result: on_enter(event, lb))
listbox_2nd_result.bind("<Leave>", lambda event, lb=listbox_2nd_result: on_leave(event, lb))

# Function to move focus between adjacent lists
def move_focus(event, current_listbox, direction):
    """Move focus to the adjacent listbox."""
    listboxes = [
        listbox_1st_direction,
        listbox_1st_result,
        listbox_2nd_direction,
        listbox_2nd_result,
        listbox_return_type,
        listbox_return_shot,
        listbox_return_outcome,
        listbox_point_winner,
        listbox_end_type,
        listbox_end_shot,
        listbox_end_outcome,
        listbox_strategy_position,
        listbox_strategy_play_style,
    ]
    try:
        current_index = listboxes.index(current_listbox)
        if direction == "left" and current_index > 0:
            listboxes[current_index - 1].focus_set()
        elif direction == "right" and current_index < len(listboxes) - 1:
            listboxes[current_index + 1].focus_set()
    except ValueError:
        pass

# Bind arrow keys to move focus
for listbox in [
    listbox_1st_direction,
    listbox_1st_result,
    listbox_2nd_direction,
    listbox_2nd_result,
    listbox_return_type,
    listbox_return_shot,
    listbox_return_outcome,
    listbox_point_winner,
    listbox_end_type,
    listbox_end_shot,
    listbox_end_outcome,
    listbox_strategy_position,
    listbox_strategy_play_style,
]:
    listbox.bind("<Left>", lambda event, lb=listbox: move_focus(event, lb, "left"))
    listbox.bind("<Right>", lambda event, lb=listbox: move_focus(event, lb, "right"))

# Run the app
app.mainloop()
