import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


my_lightblue = '#b2d6fe'

def get_current_data():
    """Retrieves the currently selected data from all listboxes."""
    data = {
        "1st": (listbox_1st_direction.get(tk.ACTIVE) if listbox_1st_direction.curselection() else "Wide") + ' ' + (listbox_1st_result.get(tk.ACTIVE) if listbox_1st_result.curselection() else ""),
        "2nd": (listbox_2nd_direction.get(tk.ACTIVE) if listbox_2nd_direction.curselection() else "") + ' ' + (listbox_2nd_result.get(tk.ACTIVE) if listbox_2nd_result.curselection() else ""), 
        "Return": (listbox_return_type.get(tk.ACTIVE) if listbox_return_type.curselection() else "") + ' ' + (listbox_return_shot.get(tk.ACTIVE) if listbox_return_shot.curselection() else "") + ' ' + (listbox_return_outcome.get(tk.ACTIVE) if listbox_return_outcome.curselection() else ""),
        "Winner": listbox_point_winner.get(tk.ACTIVE) if listbox_point_winner.curselection() else "",
        "End": (listbox_end_type.get(tk.ACTIVE) if listbox_end_type.curselection() else "") + ' ' + (listbox_end_shot.get(tk.ACTIVE) if listbox_end_shot.curselection() else "") + ' ' + (listbox_end_outcome.get(tk.ACTIVE) if listbox_end_outcome.curselection() else ""),
        "Strategy": (listbox_strategy_position.get(tk.ACTIVE) if listbox_strategy_position.curselection() else "") +  '+' +(listbox_strategy_play_style.get(tk.ACTIVE) if listbox_strategy_play_style.curselection() else ""),
    }
    
    return data

def display_stats(player_a_name, player_b_name):
    """Display the selected stats in the top Text widget."""
    data = get_current_data()
    data = {key: value for key, value in data.items() if value.strip()}
    stats = ";  ".join([f"{key}: {value}" for key, value in data.items() if value])
    if stats:
        stats_display.insert(tk.END, stats + "\n")
        stats_display.see(tk.END)  # Scroll to the latest entry

    point_winner = data.get("Winner")
    if point_winner == player_a_name:
        scoring_section.add_point(player_a_name)
    elif point_winner == player_b_name:
        scoring_section.add_point(player_b_name)

    listboxes_widgets = [
        listbox_1st_direction, listbox_1st_result,
        listbox_2nd_direction, listbox_2nd_result,
        listbox_return_type, listbox_return_shot,
        listbox_return_outcome, listbox_point_winner,
        listbox_end_type, listbox_end_shot,
        listbox_end_outcome, listbox_strategy_position,
        listbox_strategy_play_style
    ]
    for lb in listboxes_widgets:
        lb.selection_clear(0, tk.END)
        lb.config(bg='white')
        for i in range(lb.size()):
            lb.itemconfig(i, bg="white")
    listbox_1st_direction.focus_set()
    focus_listbox(listbox_1st_direction)  

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

def move_focus_left(event):
    current_widget = event.widget
    next_widget = None
    listboxes = [
        listbox_1st_direction, listbox_1st_result,
        listbox_2nd_direction, listbox_2nd_result,
        listbox_return_type, listbox_return_shot,
        listbox_return_outcome, listbox_point_winner,
        listbox_end_type, listbox_end_shot,
        listbox_end_outcome, listbox_strategy_position,
        listbox_strategy_play_style
    ]
    current_index = listboxes.index(current_widget)

    # Unhighlight the current listbox
    active_index = current_widget.index(tk.ACTIVE) if current_widget.size() > 0 else None
    unfocus_listbox(current_widget, active_index)

    next_widget = listboxes[current_index - 1]
    next_widget.focus_set()
    focus_listbox(next_widget)

def move_focus_right(event):
    current_widget = event.widget
    next_widget = None
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

    # The following 2 lines 'unfocus' the current listbox.
    active_index = current_widget.index(tk.ACTIVE) if current_widget.size() > 0 else None
    unfocus_listbox(current_widget, active_index)

    if current_widget == listbox_1st_direction:
        active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
        if active_first_serve_index != -1 and listbox_1st_direction.get(active_first_serve_index) == "In Net":
            next_widget = listbox_2nd_direction
            listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
            for i in range(listbox_1st_result.size()):
                listbox_1st_result.itemconfig(i, bg="lightgray")
            next_widget.focus_set()
            focus_listbox(next_widget)        
        else:
            next_widget = listbox_1st_result
            next_widget.focus_set()
            focus_listbox(next_widget)
    elif current_widget == listbox_1st_result:
        active_first_result_index = listbox_1st_result.index(tk.ACTIVE)
        if active_first_result_index != -1: # If is not 'fault'
            selected_result = listbox_1st_result.get(active_first_result_index)
            if selected_result == "In": # If 1st serve goes 'In' but not ace, skip to return
                listbox_2nd_direction.config(bg="lightgray")
                listbox_2nd_result.config(bg="lightgray")
                for i in range(listbox_2nd_direction.size()):
                    listbox_2nd_direction.itemconfig(i, bg="lightgray")
                for i in range(listbox_2nd_result.size()):
                    listbox_2nd_result.itemconfig(i, bg="lightgray")
                
                next_widget = listbox_return_type
                listbox_return_type.focus_set()
                focus_listbox(listbox_return_type)
            elif selected_result == "Ace" or selected_result == "Winner":
                listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                listbox_2nd_result.config(bg="lightgray") # Indicate skip
                listbox_return_type.config(bg="lightgray") # Indicate skip
                listbox_return_shot.config(bg="lightgray") # Indicate skip
                listbox_return_outcome.config(bg="lightgray") # Indicate skip
                for i in range(listbox_2nd_direction.size()):
                    listbox_2nd_direction.itemconfig(i, bg="lightgray")
                for i in range(listbox_2nd_result.size()):
                    listbox_2nd_result.itemconfig(i, bg="lightgray")
                for i in range(listbox_return_type.size()):
                    listbox_return_type.itemconfig(i, bg="lightgray")
                for i in range(listbox_return_shot.size()):
                    listbox_return_shot.itemconfig(i, bg="lightgray")    
                for i in range(listbox_return_outcome.size()):
                    listbox_return_outcome.itemconfig(i, bg="lightgray")    

                listbox_point_winner.focus_set()
                focus_listbox(listbox_point_winner)
                return  
            else: # If fault, move to 2nd serve
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
                    next_widget.focus_set()
                    focus_listbox(next_widget) 
    elif current_widget == listbox_2nd_direction:
        active_second_serve_index = listbox_2nd_direction.index(tk.ACTIVE)
        if active_second_serve_index != -1 and listbox_2nd_direction.get(active_second_serve_index) == "In Net":
            listbox_2nd_result.config(bg="lightgray") # Indicate skip
            listbox_return_type.config(bg="lightgray") # Indicate skip
            listbox_return_shot.config(bg="lightgray") # Indicate skip
            listbox_return_outcome.config(bg="lightgray") # Indicate skip
            listbox_point_winner.focus_set()
            focus_listbox(listbox_point_winner)
            return  # Exit to prevent further processing
        else:
            next_widget = listbox_2nd_result
            next_widget.focus_set()
            focus_listbox(next_widget)  
    elif current_widget == listbox_2nd_result:
        active_second_result_index = listbox_2nd_result.index(tk.ACTIVE)
        if active_second_result_index != -1 and listbox_2nd_result.get(active_second_result_index) in ['Ace','Winner', 'Fault']:
            listbox_return_type.config(bg="lightgray") # Indicate skip
            listbox_return_shot.config(bg="lightgray") # Indicate skip
            listbox_return_outcome.config(bg="lightgray") # Indicate skip
            for i in range(listbox_return_type.size()):
                    listbox_return_type.itemconfig(i, bg="lightgray")
            for i in range(listbox_return_shot.size()):
                listbox_return_shot.itemconfig(i, bg="lightgray")
            for i in range(listbox_return_outcome.size()):
                listbox_return_outcome.itemconfig(i, bg="lightgray")

            listbox_point_winner.focus_set()
            focus_listbox(listbox_point_winner)
        else:
            next_index = current_index + 1
            if next_index < num_listboxes:
                next_widget = listboxes[next_index]
                next_widget.focus_set()
                focus_listbox(next_widget)
    else:
        next_index = current_index + 1
        if next_index < num_listboxes:
            next_widget = listboxes[next_index]
            next_widget.focus_set()
            focus_listbox(next_widget)

def move_focus_up(event):
    pass

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
    """Handle selection change in a listbox to highlight the active item and implement special navigation for 'In Net'."""
    listbox = event.widget
    for i in range(listbox.size()):
        listbox.itemconfig(i, bg=listbox.cget("background")) # Reset all to listbox background
    if listbox.curselection():
        index = int(listbox.curselection()[0])
        listbox.itemconfig(index, bg=my_lightblue)

class CustomListbox(tk.Listbox):
    """Custom Listbox class to encapsulate behavior."""
    def __init__(self, parent, items, width, row, column, **kwargs):
        super().__init__(parent, height=len(items), width=width, exportselection=False, **kwargs)
        for item in items:
            self.insert(tk.END, item)
        self.grid(row=row, column=column, padx=10, pady=0, sticky="nw")
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<<ListboxSelect>>", self.on_listbox_select)

    def on_focus_in(self, event):
        """Handle focus entering the listbox."""
        self.config(bg="lightgreen")
        if self.size() > 0:
            active_index = self.index(tk.ACTIVE)
            if active_index != -1:
                for i in range(self.size()):
                    self.itemconfig(i, bg=self.cget("background"))
                self.itemconfig(active_index, bg=my_lightblue)
            else:
                self.activate(0)
                self.selection_clear(0, tk.END)
                self.selection_set(0)
                self.itemconfig(0, bg=my_lightblue)

    def on_listbox_select(self, event):
        """Handle selection change in the listbox."""
        for i in range(self.size()):
            self.itemconfig(i, bg=self.cget("background"))
        if self.curselection():
            index = int(self.curselection()[0])
            self.itemconfig(index, bg=my_lightblue)

class EnterConfirmation():
    def __init__(self, root, player_a_name, player_b_name):
        self.root = root
        self.player_a_name = player_a_name
        self.player_b_name = player_b_name
        # Variable to track if confirmation pop-up is open
        self.confirmation_active = False
        
        # Label for instructions
        self.label = tk.Label(root, text="Press Enter to confirm results.", font=("Helvetica", 14))
        self.label.pack(pady=20)

        # Bind Enter key to show confirmation pop-up
        self.root.bind('<Return>', self.show_confirmation)

    def show_confirmation(self, event):
        """Handles the first Enter press (shows confirmation pop-up)"""
        if not self.confirmation_active:
            self.confirmation_active = True  # Mark the pop-up as active

            # Create confirmation window
            self.popup = tk.Toplevel(self.root)
            self.popup.title("Confirmation")
            self.popup.geometry("350x150")
            
            label = tk.Label(self.popup, text="Are you sure you want to enter these results?", font=("Helvetica", 12))
            label.pack(pady=10)

            # Bind Enter key to confirm action
            self.popup.bind('<Return>', self.enter_results)

            # Handle window closing
            self.popup.protocol("WM_DELETE_WINDOW", self.cancel_confirmation)

    def enter_results(self, event):
        """Handles the second Enter press (confirms the action)"""
        display_stats(self.player_a_name, self.player_b_name)
        self.confirmation_active = False
        self.popup.destroy()

    def cancel_confirmation(self):
        """Handles closing the pop-up without confirming"""
        self.confirmation_active = False
        self.popup.destroy()

class TennisScoring:
    def __init__(self, parent, player_a_name, player_b_name):
        self.parent = parent
        self.player_a_name = player_a_name
        self.player_b_name = player_b_name
        self.player_a_score = 0
        self.player_b_score = 0
        self.player_a_games = 0
        self.player_b_games = 0
        self.server = player_a_name  # Player A starts serving
        self.scoring_progression = [0, 15, 30, 40]  # Tennis scoring progression

        # Create the scoring section
        self.score_frame = tk.Frame(parent, bg="#ffffff")
        self.score_frame.grid(row=5, column=0, columnspan=8, pady=20)
        self.toggle_server_button = tk.Button(self.parent, text="Toggle Server", command=self.toggle_server)
        self.toggle_server_button.grid(row=3,column=7)
        self.reset_score_btn = tk.Button(self.parent, text='Reset In-Game Score', command=self.reset_scores_and_display)
        self.reset_score_btn.grid(row=3,column=8)

        # Player A Label
        self.player_a_label = tk.Label(
            self.score_frame,
            text=f"{self.player_a_name} ●" if self.server == self.player_a_name else f"{self.player_a_name}",
            font=("Helvetica", 14, "bold"),
            fg="black",
            bg="#ffffff"
        )
        self.player_a_label.grid(row=0, column=0, padx=20)

        # Player A Score
        self.player_a_score_label = tk.Label(
            self.score_frame,
            text="0",
            font=("Helvetica", 14),
            fg="black",
            bg="#ffffff"
        )
        self.player_a_score_label.grid(row=0, column=1, padx=10)

        # Player B Label
        self.player_b_label = tk.Label(
            self.score_frame,
            text=f"{self.player_b_name} ●" if self.server == self.player_b_name else f"{self.player_b_name}",
            font=("Helvetica", 14, "bold"),
            fg="black",
            bg="#ffffff"
        )
        self.player_b_label.grid(row=0, column=2, padx=20)

        # Player B Score
        self.player_b_score_label = tk.Label(
            self.score_frame,
            text="0",
            font=("Helvetica", 14),
            fg="black",
            bg="#ffffff"
        )
        self.player_b_score_label.grid(row=0, column=3, padx=10)

        # Player A Games
        self.player_a_games_label = tk.Label(
            self.score_frame,
            text="Games: 0",
            font=("Helvetica", 12),
            fg="black",
            bg="#ffffff"
        )
        self.player_a_games_label.grid(row=1, column=0, padx=10)

        # Player B Games
        self.player_b_games_label = tk.Label(
            self.score_frame,
            text="Games: 0",
            font=("Helvetica", 12),
            fg="black",
            bg="#ffffff"
        )
        self.player_b_games_label.grid(row=1, column=2, padx=10)

    def add_point(self, winner):
        """Add a point to the specified player and handle scoring logic."""
        if winner == self.player_a_name:
            self.update_score(self.player_a_name)
        elif winner == self.player_b_name:
            self.update_score(self.player_b_name)

    def update_score(self, player):
        """Update the score for the specified player."""
        if player == self.player_a_name:
            if self.player_a_score == 40 and self.player_b_score == 40:
                self.player_a_score = "Adv"
            elif self.player_a_score == "Adv" and self.player_b_score == 40:
                self.player_a_score = "Game"
            elif self.player_b_score == "Adv":
                self.player_a_score = 40
                self.player_b_score = 40
            elif self.player_a_score == 40 and self.player_b_score != 40:
                self.player_a_score = "Game"
            else:
                self.player_a_score = self.scoring_progression[
                    self.scoring_progression.index(self.player_a_score) + 1
                ]
        elif player == self.player_b_name:
            if self.player_b_score == 40 and self.player_a_score == 40:
                self.player_b_score = "Adv"
            elif self.player_b_score == "Adv" and self.player_a_score == 40:
                self.player_b_score = "Game"
            elif self.player_b_score == 40 and self.player_a_score == "Adv":
                self.player_a_score = 40
                self.player_b_score = 40
            elif self.player_b_score == 40 and self.player_a_score != 40:
                self.player_b_score = "Game"
            else:
                self.player_b_score = self.scoring_progression[
                    self.scoring_progression.index(self.player_b_score) + 1
                ]

        # Check for game win
        if self.player_a_score == "Game":
            self.player_a_games += 1
            self.reset_scores()
            self.toggle_server()
        elif self.player_b_score == "Game":
            self.player_b_games += 1
            self.reset_scores()
            self.toggle_server()

        self.update_display()

    def reset_scores(self):
        """Reset the scores to 0 after a game is won."""
        self.player_a_score = 0
        self.player_b_score = 0

    def reset_scores_and_display(self):
        """Reset the scores to 0 after a game is won."""
        self.player_a_score = 0
        self.player_b_score = 0
        self.update_display()
        listboxes_widgets = [
            listbox_1st_direction, listbox_1st_result,
            listbox_2nd_direction, listbox_2nd_result,
            listbox_return_type, listbox_return_shot,
            listbox_return_outcome, listbox_point_winner,
            listbox_end_type, listbox_end_shot,
            listbox_end_outcome, listbox_strategy_position,
            listbox_strategy_play_style
        ]
        for lb in listboxes_widgets:
            lb.selection_clear(0, tk.END)
            lb.config(bg='white')
            for i in range(lb.size()):
                lb.itemconfig(i, bg="white")
        listbox_1st_direction.focus_set()
        focus_listbox(listbox_1st_direction) 


    def toggle_server(self):
        """Toggle the server and update the labels."""
        if self.server == self.player_a_name:
            self.server = self.player_b_name
        else:
            self.server = self.player_a_name
        self.player_a_label.config(
            text=f"{self.player_a_name} ●" if self.server == self.player_a_name else f"{self.player_a_name}"
        )
        self.player_b_label.config(
            text=f"{self.player_b_name} ●" if self.server == self.player_b_name else f"{self.player_b_name}"
        )


    def update_display(self):
        """Update the score and game labels."""
        self.player_a_score_label.config(text=str(self.player_a_score))
        self.player_b_score_label.config(text=str(self.player_b_score))
        self.player_a_games_label.config(text=f"Games: {self.player_a_games}")
        self.player_b_games_label.config(text=f"Games: {self.player_b_games}")

        # Update the serving dot
        self.player_a_label.config(
            text=f"{self.player_a_name} ●" if self.server == self.player_a_name else f"{self.player_a_name}"
        )
        self.player_b_label.config(
            text=f"{self.player_b_name} ●" if self.server == self.player_b_name else f"{self.player_b_name}"
        )

# Main app window
app = tk.Tk()
app.title("Tennis Data Entry App")
app.geometry("1200x700")
app.configure(bg="#f0f0f0")

top_frame = tk.Frame(app, height=200, bg=my_lightblue)
top_frame.pack(side="top", fill="both", expand=True)

bottom_frame = tk.Frame(app, height=500, bg="#ffffff", relief="ridge", bd=2)
bottom_frame.pack(side="bottom", fill="both", expand=True)

player_a_name = simpledialog.askstring("Player A", "Enter the name of Player A:")
player_b_name = simpledialog.askstring("Player B", "Enter the name of Player B:")
scoring_section = TennisScoring(bottom_frame, player_a_name, player_b_name)

enter_confirmation = EnterConfirmation(app, player_a_name, player_b_name) # Needs to be after scoring_section obj

# Add a Text widget to the top frame for displaying stats
stats_display = tk.Text(top_frame, height=10, width=140, state="normal", bg="white", font=("Helvetica", 10))
stats_display.pack(padx=10, pady=10)

# -------------------------
# 🎯 Labels in One Row (Serve, Return, Point Winner)
# -------------------------
# Labels (single row)
tk.Label(bottom_frame, text="1st Serve", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="nw")
tk.Label(bottom_frame, text="2nd Serve", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=2, padx=10, pady=5, sticky="nw")
tk.Label(bottom_frame, text="Return", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=4, padx=10, pady=5, sticky="nw")
tk.Label(bottom_frame, text="Point Winner", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=7, padx=10, pady=5, sticky="nw")


# List items
serve_direction_items = ["Wide", "Body", "Center", "In Net"]
serve_result_items = ["In", "Winner", "Ace", "Fault"]


listbox_1st_direction = CustomListbox(bottom_frame, serve_direction_items, 8, 1, 0)
listbox_1st_direction.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_1st_direction.bind("<Right>", move_focus_right)  # Bind Right arrow

listbox_1st_result = CustomListbox(bottom_frame, serve_result_items, 8, 1, 1)
listbox_1st_result.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_1st_result.bind("<Right>", move_focus_right)  # Bind Right arrow

# --- 2nd Serve ---
listbox_2nd_direction = CustomListbox(bottom_frame, serve_direction_items, 8, 1, 2)
listbox_2nd_direction.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_2nd_direction.bind("<Right>", move_focus_right)  # Bind Right arrow

listbox_2nd_result = CustomListbox(bottom_frame, serve_result_items, 8, 1, 3)
listbox_2nd_result.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_2nd_result.bind("<Right>", move_focus_right)  # Bind Right arrow

# -------------------------
# 🎾 Vertical Lists for Return
# -------------------------

# List items for Return
return_type_items = ["Forehand", "Backhand"]
return_shot_items = ["Return", "Pass", "Approach", "Drop", "Lob"]
return_outcome_items = ["In", "Winner", "Unforced", "Forced"]

# --- Return - Type ---
listbox_return_type = CustomListbox(bottom_frame, return_type_items, 8, 1, 4)
listbox_return_type.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_return_type.bind("<Right>", move_focus_right)  # Bind Right arrow

# --- Return - Shot ---
listbox_return_shot = CustomListbox(bottom_frame, return_shot_items, 8, 1, 5)
listbox_return_shot.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_return_shot.bind("<Right>", move_focus_right)  # Bind Right arrow

# --- Return - Outcome ---
listbox_return_outcome = CustomListbox(bottom_frame, return_outcome_items, 8, 1, 6)
listbox_return_outcome.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_return_outcome.bind("<Right>", move_focus_right)  # Bind Right arrow

# listbox point winner

point_winners = [player_a_name, player_b_name]

# --- Point Winner ---
listbox_point_winner = CustomListbox(bottom_frame, point_winners, 8, 1, 7)
listbox_point_winner.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_point_winner.bind("<Right>", move_focus_right)  # Bind Right arrow

# -------------------------
# 🎯 New Row - End Section
# -------------------------

# Label
tk.Label(bottom_frame, text="End", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=2, column=0, padx=10, pady=15, sticky="nw")

# List items for End
end_type_items = ["Forehand", "Backhand"]
end_shot_items = ["Drive", "Volley", "Smash", "Pass", "Approach", "Lob", "Drop"]
end_outcome_items = ["Winner", "Forced", "Unforced"]

# --- End - Type ---
listbox_end_type = CustomListbox(bottom_frame, end_type_items, 8, 3, 0)
listbox_end_type.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_end_type.bind("<Right>", move_focus_right)  # Bind Right arrow

# --- End - Shot ---
listbox_end_shot = CustomListbox(bottom_frame, end_shot_items, 8, 3, 1)
listbox_end_shot.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_end_shot.bind("<Right>", move_focus_right)  # Bind Right arrow

# --- End - Outcome ---
listbox_end_outcome = CustomListbox(bottom_frame, end_outcome_items, 8, 3, 2)
listbox_end_outcome.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_end_outcome.bind("<Right>", move_focus_right)  # Bind Right arrow

# -------------------------
# 🎯 New Row - Strategy Section (same row as End)
# -------------------------

# Label
tk.Label(bottom_frame, text="Strategy", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=2, column=3, padx=10, pady=15, sticky="nw")

# List items for Strategy
strategy_position_items = ["Baseline", f"{player_a_name} at net", f"{player_b_name} at net", "Both at net"]
strategy_play_style_items = ["", "Serve & Volley"]

# --- Strategy - Position ---
listbox_strategy_position = CustomListbox(bottom_frame, strategy_position_items, 9, 3, 3)
listbox_strategy_position.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_strategy_position.bind("<Right>", move_focus_right)  # Bind Right arrow

# --- Strategy - Play Style ---
listbox_strategy_play_style = CustomListbox(bottom_frame, strategy_play_style_items, 11, 3, 4)
listbox_strategy_play_style.bind("<Left>", move_focus_left)  # Bind Left arrow
listbox_strategy_play_style.bind("<Right>", move_focus_right)  # Bind Right arrow

# -------------------------
# 🚀 Submit button
# -------------------------

listbox_1st_direction.focus_set()

# Create a simple object with a 'widget' attribute
class FakeEvent:
    def __init__(self, widget):
        self.widget = widget

on_focus_in(FakeEvent(widget=listbox_1st_direction))

app.mainloop()