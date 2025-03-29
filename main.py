import tkinter as tk
from tkinter import messagebox

my_lightblue = '#b2d6fe'

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

def get_current_data():
    """Retrieves the currently selected data from all listboxes."""
    data = {
        "1st": (listbox_1st_direction.get(tk.ACTIVE) if listbox_1st_direction.curselection() else "Wide") + ' ' + (listbox_1st_result.get(tk.ACTIVE) if listbox_1st_result.curselection() else ""),
        "2nd": (listbox_2nd_direction.get(tk.ACTIVE) if listbox_2nd_direction.curselection() else "") + ' ' + (listbox_2nd_result.get(tk.ACTIVE) if listbox_2nd_result.curselection() else ""), 
        "Return": (listbox_return_type.get(tk.ACTIVE) if listbox_return_type.curselection() else "") + ' ' + (listbox_return_shot.get(tk.ACTIVE) if listbox_return_shot.curselection() else "") + ' ' + (listbox_return_outcome.get(tk.ACTIVE) if listbox_return_outcome.curselection() else ""),
        "Winner": listbox_point_winner.get(tk.ACTIVE) if listbox_point_winner.curselection() else "",
        "End": (listbox_end_type.get(tk.ACTIVE) if listbox_end_type.curselection() else "") + ' ' + (listbox_end_shot.get(tk.ACTIVE) if listbox_end_shot.curselection() else "") + ' ' + (listbox_end_outcome.get(tk.ACTIVE) if listbox_end_outcome.curselection() else ""),
        "Strategy": (listbox_strategy_position.get(tk.ACTIVE) if listbox_strategy_position.curselection() else "") + (listbox_strategy_play_style.get(tk.ACTIVE) if listbox_strategy_play_style.curselection() else ""),
    }
    
    return data

def display_stats(event=None):
    """Display the selected stats in the top Text widget."""
    data = get_current_data()
    data = {key: value for key, value in data.items() if value.strip()}
    stats = ";      ".join([f"{key}: {value}" for key, value in data.items() if value])
    if stats:
        stats_display.insert(tk.END, stats + "\n")
        stats_display.see(tk.END)  # Scroll to the latest entry
    listboxes_widgets = [
        listbox_1st_direction, listbox_1st_result,
        listbox_2nd_direction, listbox_2nd_result,
        listbox_return_type, listbox_return_shot,
        listbox_return_outcome, listbox_point_winner,
        listbox_end_type, listbox_end_shot,
        listbox_end_outcome, listbox_strategy_position,
        listbox_strategy_play_style
    ]
    point_winner = data.get("Winner")

    # Update the score based on the point winner
    if point_winner == "A":
        scoring_section.add_point("A")
    elif point_winner == "B":
        scoring_section.add_point("B")
    for lb in listboxes_widgets:
        lb.selection_clear(0, tk.END)
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

    if event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]
            # Reset background if moving back to the skipped listbox
            if next_widget == listbox_1st_result:
                listbox_1st_result.config(bg="white")
    if next_widget:
        next_widget.focus_set()
        focus_listbox(next_widget)

def move_focus_right(event):
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
        if current_widget == listbox_1st_direction:
            active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
            if active_first_serve_index != -1 and listbox_1st_direction.get(active_first_serve_index) == "In Net":
                next_widget = listbox_2nd_direction
                listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
                    # Reset background if moving away normally
                    if next_widget == listbox_1st_result:
                        listbox_1st_result.config(bg="white")
        elif current_widget == listbox_1st_result:
            active_first_result_index = listbox_1st_result.index(tk.ACTIVE)
            if active_first_result_index != -1:
                selected_result = listbox_1st_result.get(active_first_result_index)
                if selected_result == "In":
                    next_widget = listbox_return_type
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                elif selected_result == "Ace" or selected_result == "Winner":
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                    listbox_return_type.config(bg="lightgray") # Indicate skip
                    listbox_return_shot.config(bg="lightgray") # Indicate skip
                    listbox_return_outcome.config(bg="lightgray") # Indicate skip
                    listbox_point_winner.focus_set()
                    focus_listbox(listbox_point_winner)
                    return  
                else:
                    next_index = current_index + 1
                    if next_index < num_listboxes:
                        next_widget = listboxes[next_index]
                # Reset background if moving away normally
                if current_widget == listbox_1st_result and next_widget != listbox_return_type and next_widget != listbox_point_winner:
                    listbox_1st_result.config(bg="white")
        # Special case for 'In Net' in the second serve direction
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
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
        # Special case for 'Fault' in the second serve result
        elif current_widget == listbox_2nd_result:
            active_second_result_index = listbox_2nd_result.index(tk.ACTIVE)
            if active_second_result_index != -1 and listbox_2nd_result.get(active_second_result_index) == "Fault":
                listbox_return_type.config(bg="lightgray") # Indicate skip
                listbox_return_shot.config(bg="lightgray") # Indicate skip
                listbox_return_outcome.config(bg="lightgray") # Indicate skip
                listbox_point_winner.focus_set()
                focus_listbox(listbox_point_winner)
                return  # Exit to prevent further processing
            elif active_second_result_index != -1 and listbox_2nd_result.get(active_second_result_index) in ['Ace','Winner']:
                listbox_return_type.config(bg="lightgray") # Indicate skip
                listbox_return_shot.config(bg="lightgray") # Indicate skip
                listbox_return_outcome.config(bg="lightgray") # Indicate skip
                listbox_point_winner.focus_set()
                focus_listbox(listbox_point_winner)
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
        elif current_widget == listbox_2nd_result:
            active_index = listbox_2nd_result.index(tk.ACTIVE)
            if active_index != -1:
                selected_value = listbox_2nd_result.get(active_index)
                if selected_value in ["Ace", "Winner"]:
                    # Move focus to the Point Winner listbox
                    listbox_point_winner.focus_set()
                    focus_listbox(listbox_point_winner)
                    return  # Exit to prevent further processing

def move_focus_up(event):
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

    if event.keysym == "Up":
        if isinstance(current_widget, tk.Listbox):
            active_index_up = current_widget.index(tk.ACTIVE)
            if active_index_up == 0 and current_widget.size() > 1:  # Check if at the top and has more than one item
                last_index = current_widget.size() - 1
                current_widget.activate(last_index)
                current_widget.selection_clear(0, tk.END)
                current_widget.selection_set(last_index)
                for i in range(current_widget.size()):
                    current_widget.itemconfig(i, bg=current_widget.cget("background"))
                current_widget.itemconfig(last_index, bg=my_lightblue)


def move_focus(event):
    """Move the focus between listboxes when left or right arrow is pressed, with special cases for 'In Net' in 1st Serve Direction, 'In' in 1st Serve Result, 'Ace' or 'Winner' in 1st Serve Result, 'In Net' in 2nd Serve Direction, and 'Fault' in 2nd Serve Result, and visual indication of skip. Also handles wrap-around with single Up Arrow."""
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
        # Special case for 'In Net' in the first serve direction
        if current_widget == listbox_1st_direction:
            active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
            if active_first_serve_index != -1 and listbox_1st_direction.get(active_first_serve_index) == "In Net":
                next_widget = listbox_2nd_direction
                listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
                    # Reset background if moving away normally
                    if next_widget == listbox_1st_result:
                        listbox_1st_result.config(bg="white")
        # Special case for 'In', 'Ace', or 'Winner' in the first serve result
        elif current_widget == listbox_1st_result:
            active_first_result_index = listbox_1st_result.index(tk.ACTIVE)
            if active_first_result_index != -1:
                selected_result = listbox_1st_result.get(active_first_result_index)
                if selected_result == "In":
                    next_widget = listbox_return_type
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                elif selected_result == "Ace" or selected_result == "Winner":
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                    listbox_return_type.config(bg="lightgray") # Indicate skip
                    listbox_return_shot.config(bg="lightgray") # Indicate skip
                    listbox_return_outcome.config(bg="lightgray") # Indicate skip
                    listbox_point_winner.focus_set()
                    focus_listbox(listbox_point_winner)
                    return  # Exit to prevent further processing
                else:
                    next_index = current_index + 1
                    if next_index < num_listboxes:
                        next_widget = listboxes[next_index]
                # Reset background if moving away normally
                if current_widget == listbox_1st_result and next_widget != listbox_return_type and next_widget != listbox_point_winner:
                    listbox_1st_result.config(bg="white")
        # Special case for 'In Net' in the second serve direction
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
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
        # Special case for 'Fault' in the second serve result
        elif current_widget == listbox_2nd_result:
            active_second_result_index = listbox_2nd_result.index(tk.ACTIVE)
            if active_second_result_index != -1 and listbox_2nd_result.get(active_second_result_index) == "Fault":
                listbox_return_type.config(bg="lightgray") # Indicate skip
                listbox_return_shot.config(bg="lightgray") # Indicate skip
                listbox_return_outcome.config(bg="lightgray") # Indicate skip
                listbox_point_winner.focus_set()
                focus_listbox(listbox_point_winner)
                return  # Exit to prevent further processing
            elif active_second_result_index != -1 and listbox_2nd_result.get(active_second_result_index) in ['Ace','Winner']:
                listbox_return_type.config(bg="lightgray") # Indicate skip
                listbox_return_shot.config(bg="lightgray") # Indicate skip
                listbox_return_outcome.config(bg="lightgray") # Indicate skip
                listbox_point_winner.focus_set()
                focus_listbox(listbox_point_winner)
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
        elif current_widget == listbox_2nd_result:
            active_index = listbox_2nd_result.index(tk.ACTIVE)
            if active_index != -1:
                selected_value = listbox_2nd_result.get(active_index)
                if selected_value in ["Ace", "Winner"]:
                    # Move focus to the Point Winner listbox
                    listbox_point_winner.focus_set()
                    focus_listbox(listbox_point_winner)
                    return  # Exit to prevent further processing
    elif event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]
            # Reset background if moving back to the skipped listbox
            if next_widget == listbox_1st_result:
                listbox_1st_result.config(bg="white")
            elif current_widget == listbox_2nd_direction:
                listbox_1st_result.config(bg="lightgray") # Keep it gray if skipping again
    elif event.keysym == "Up":
        if isinstance(current_widget, tk.Listbox):
            active_index_up = current_widget.index(tk.ACTIVE)
            if active_index_up == 0 and current_widget.size() > 1:  # Check if at the top and has more than one item
                last_index = current_widget.size() - 1
                current_widget.activate(last_index)
                current_widget.selection_clear(0, tk.END)
                current_widget.selection_set(last_index)
                for i in range(current_widget.size()):
                    current_widget.itemconfig(i, bg=current_widget.cget("background"))
                current_widget.itemconfig(last_index, bg=my_lightblue)

    if next_widget:
        next_widget.focus_set()
        focus_listbox(next_widget)
    """Move the focus between listboxes when left or right arrow is pressed, with special cases for 'In Net' in 1st Serve Direction, 'In' in 1st Serve Result, 'Ace' or 'Winner' in 1st Serve Result, and 'In Net' in 2nd Serve Direction, and visual indication of skip. Also handles wrap-around with single Up Arrow."""
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
        # Special case for 'In Net' in the first serve direction
        if current_widget == listbox_1st_direction:
            active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
            if active_first_serve_index != -1 and listbox_1st_direction.get(active_first_serve_index) == "In Net":
                next_widget = listbox_2nd_direction
                listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
                    # Reset background if moving away normally
                    if next_widget == listbox_1st_result:
                        listbox_1st_result.config(bg="white")
        # Special case for 'In', 'Ace', or 'Winner' in the first serve result
        elif current_widget == listbox_1st_result:
            active_first_result_index = listbox_1st_result.index(tk.ACTIVE)
            if active_first_result_index != -1:
                selected_result = listbox_1st_result.get(active_first_result_index)
                if selected_result == "In":
                    next_widget = listbox_return_type
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                elif selected_result == "Ace" or selected_result == "Winner":
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                    listbox_return_type.config(bg="lightgray") # Indicate skip
                    listbox_return_shot.config(bg="lightgray") # Indicate skip
                    listbox_return_outcome.config(bg="lightgray") # Indicate skip
                    listbox_point_winner.focus_set()
                    focus_listbox(listbox_point_winner)
                    return  # Exit to prevent further processing
                else:
                    next_index = current_index + 1
                    if next_index < num_listboxes:
                        next_widget = listboxes[next_index]
                # Reset background if moving away normally
                if current_widget == listbox_1st_result and next_widget != listbox_return_type and next_widget != listbox_point_winner:
                    listbox_1st_result.config(bg="white")
        # Special case for 'In Net' in the second serve direction
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
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
    elif event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]
            # Reset background if moving back to the skipped listbox
            if next_widget == listbox_1st_result:
                listbox_1st_result.config(bg="white")
            elif current_widget == listbox_2nd_direction:
                listbox_1st_result.config(bg="lightgray") # Keep it gray if skipping again
    elif event.keysym == "Up":
        if isinstance(current_widget, tk.Listbox):
            active_index_up = current_widget.index(tk.ACTIVE)
            if active_index_up == 0 and current_widget.size() > 1:  # Check if at the top and has more than one item
                last_index = current_widget.size() - 1
                current_widget.activate(last_index)
                current_widget.selection_clear(0, tk.END)
                current_widget.selection_set(last_index)
                for i in range(current_widget.size()):
                    current_widget.itemconfig(i, bg=current_widget.cget("background"))
                current_widget.itemconfig(last_index, bg=my_lightblue)

    if next_widget:
        next_widget.focus_set()
        focus_listbox(next_widget)
    """Move the focus between listboxes when left or right arrow is pressed, with special cases for 'In Net' in 1st Serve Direction, 'In' in 1st Serve Result, 'Ace' or 'Winner' in 1st Serve Result, and visual indication of skip. Also handles wrap-around with single Up Arrow."""
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
        # Special case for 'In Net' in the first serve direction
        if current_widget == listbox_1st_direction:
            active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
            if active_first_serve_index != -1 and listbox_1st_direction.get(active_first_serve_index) == "In Net":
                next_widget = listbox_2nd_direction
                listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
                    # Reset background if moving away normally
                    if next_widget == listbox_1st_result:
                        listbox_1st_result.config(bg="white")
        # Special case for 'In' in the first serve result
        # Special case for 'In', 'Ace', or 'Winner' in the first serve result
        elif current_widget == listbox_1st_result:
            active_first_result_index = listbox_1st_result.index(tk.ACTIVE)
            if active_first_result_index != -1:
                selected_result = listbox_1st_result.get(active_first_result_index)
                if selected_result == "In":
                    next_widget = listbox_return_type
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                elif selected_result == "Ace" or selected_result == "Winner":
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                    listbox_return_type.config(bg="lightgray") # Indicate skip
                    listbox_return_shot.config(bg="lightgray") # Indicate skip
                    listbox_return_outcome.config(bg="lightgray") # Indicate skip
                    listbox_point_winner.focus_set()
                    focus_listbox(listbox_point_winner)
                    return  # Exit to prevent further processing
                else:
                    next_index = current_index + 1
                    if next_index < num_listboxes:
                        next_widget = listboxes[next_index]
                # Reset background if moving away normally
                if current_widget == listbox_1st_result and next_widget != listbox_return_type and next_widget != listbox_point_winner:
                    listbox_1st_result.config(bg="white")
    elif event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]
            # Reset background if moving back to the skipped listbox
            if next_widget == listbox_1st_result:
                listbox_1st_result.config(bg="white")
            elif current_widget == listbox_2nd_direction:
                listbox_1st_result.config(bg="lightgray") # Keep it gray if skipping again
    elif event.keysym == "Up":
        if isinstance(current_widget, tk.Listbox):
            active_index_up = current_widget.index(tk.ACTIVE)
            if active_index_up == 0 and current_widget.size() > 1:  # Check if at the top and has more than one item
                last_index = current_widget.size() - 1
                current_widget.activate(last_index)
                current_widget.selection_clear(0, tk.END)
                current_widget.selection_set(last_index)
                for i in range(current_widget.size()):
                    current_widget.itemconfig(i, bg=current_widget.cget("background"))
                current_widget.itemconfig(last_index, bg=my_lightblue)

    if next_widget:
        next_widget.focus_set()
        focus_listbox(next_widget)
    """Move the focus between listboxes when left or right arrow is pressed, with special cases for 'In Net' in 1st Serve Direction and 'In' in 1st Serve Result, and visual indication of skip. Also handles wrap-around with single Up Arrow."""
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
        # Special case for 'In Net' in the first serve direction
        if current_widget == listbox_1st_direction:
            active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
            if active_first_serve_index != -1 and listbox_1st_direction.get(active_first_serve_index) == "In Net":
                next_widget = listbox_2nd_direction
                listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
                    # Reset background if moving away normally
                    if next_widget == listbox_1st_result:
                        listbox_1st_result.config(bg="white")
        # Special case for 'In' in the first serve result
        elif current_widget == listbox_1st_result:
            active_first_result_index = listbox_1st_result.index(tk.ACTIVE)
            if active_first_result_index != -1 and listbox_1st_result.get(active_first_result_index) == "In":
                listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                listbox_2nd_result.config(bg="lightgray") # Indicate skip
                listbox_return_type.focus_set()
                focus_listbox(listbox_return_type)
                return  # Exit the function to prevent further processing
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
        else:
            next_index = current_index + 1
            if next_index < num_listboxes:
                next_widget = listboxes[next_index]
                # Reset background if moving away normally
                if current_widget == listbox_1st_result:
                    listbox_1st_result.config(bg="white")
    elif event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]
            # Reset background if moving back to the skipped listbox
            if next_widget == listbox_1st_result:
                listbox_1st_result.config(bg="white")
            elif current_widget == listbox_2nd_direction:
                listbox_1st_result.config(bg="lightgray") # Keep it gray if skipping again
    elif event.keysym == "Up":
        if isinstance(current_widget, tk.Listbox):
            active_index_up = current_widget.index(tk.ACTIVE)
            if active_index_up == 0 and current_widget.size() > 1:  # Check if at the top and has more than one item
                last_index = current_widget.size() - 1
                current_widget.activate(last_index)
                current_widget.selection_clear(0, tk.END)
                current_widget.selection_set(last_index)
                for i in range(current_widget.size()):
                    current_widget.itemconfig(i, bg=current_widget.cget("background"))
                current_widget.itemconfig(last_index, bg=my_lightblue)

    if next_widget:
        next_widget.focus_set()
        focus_listbox(next_widget)
    """Move the focus between listboxes when left or right arrow is pressed, with special cases for 'In Net' and 'In' in 1st Serve Direction, and visual indication of skip. Also handles wrap-around with single Up Arrow."""
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
        # Special case for 'In Net' in the first serve direction
        if current_widget == listbox_1st_direction:
            active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
            if active_first_serve_index != -1:
                if listbox_1st_direction.get(active_first_serve_index) == "In Net":
                    next_widget = listbox_2nd_direction
                    listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
                elif listbox_1st_direction.get(active_first_serve_index) == "In":
                    next_widget = listbox_return_type
                    listbox_1st_result.config(bg="lightgray") # Indicate skip
                    listbox_2nd_direction.config(bg="lightgray") # Indicate skip
                    listbox_2nd_result.config(bg="lightgray") # Indicate skip
                else:
                    next_index = current_index + 1
                    if next_index < num_listboxes:
                        next_widget = listboxes[next_index]
                        # Reset background if moving away normally
                        if next_widget == listbox_1st_result:
                            listbox_1st_result.config(bg="white")
        else:
            next_index = current_index + 1
            if next_index < num_listboxes:
                next_widget = listboxes[next_index]
                # Reset background if moving away normally
                if current_widget == listbox_1st_result:
                    listbox_1st_result.config(bg="white")
    elif event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]
            # Reset background if moving back to the skipped listbox
            if next_widget == listbox_1st_result:
                listbox_1st_result.config(bg="white")
            elif current_widget == listbox_2nd_direction:
                listbox_1st_result.config(bg="lightgray") # Keep it gray if skipping again
    elif event.keysym == "Up":
        if isinstance(current_widget, tk.Listbox):
            active_index_up = current_widget.index(tk.ACTIVE)
            if active_index_up == 0 and current_widget.size() > 1:  # Check if at the top and has more than one item
                last_index = current_widget.size() - 1
                current_widget.activate(last_index)
                current_widget.selection_clear(0, tk.END)
                current_widget.selection_set(last_index)
                for i in range(current_widget.size()):
                    current_widget.itemconfig(i, bg=current_widget.cget("background"))
                current_widget.itemconfig(last_index, bg=my_lightblue)

    if next_widget:
        next_widget.focus_set()
        focus_listbox(next_widget)
    """Move the focus between listboxes when left or right arrow is pressed, with a special case for 'In Net' and visual indication of skip."""
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
        # Special case for 'In Net' in the first serve direction
        if current_widget == listbox_1st_direction:
            active_first_serve_index = listbox_1st_direction.index(tk.ACTIVE)
            if active_first_serve_index != -1 and listbox_1st_direction.get(active_first_serve_index) == "In Net":
                next_widget = listbox_2nd_direction
                listbox_1st_result.config(bg="lightgray")  # Set background to light gray when skipped
            else:
                next_index = current_index + 1
                if next_index < num_listboxes:
                    next_widget = listboxes[next_index]
                    # Reset background if moving away normally
                    if next_widget == listbox_1st_result:
                        listbox_1st_result.config(bg="white")
        else:
            next_index = current_index + 1
            if next_index < num_listboxes:
                next_widget = listboxes[next_index]
                # Reset background if moving away normally
                if current_widget == listbox_1st_result:
                    listbox_1st_result.config(bg="white")
    elif event.keysym == "Left":
        previous_index = current_index - 1
        if previous_index >= 0:
            next_widget = listboxes[previous_index]
            # Reset background if moving back to the skipped listbox
            if next_widget == listbox_1st_result:
                listbox_1st_result.config(bg="white")
            elif current_widget == listbox_2nd_direction:
                listbox_1st_result.config(bg="lightgray") # Keep it gray if skipping again

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
    """Handle selection change in a listbox to highlight the active item and implement special navigation for 'In Net'."""
    listbox = event.widget
    for i in range(listbox.size()):
        listbox.itemconfig(i, bg=listbox.cget("background")) # Reset all to listbox background
    if listbox.curselection():
        index = int(listbox.curselection()[0])
        listbox.itemconfig(index, bg=my_lightblue)

def ask_player_names():
    """Pop-up window to ask for player names."""
    def save_names():
        """Save the entered names and update the labels."""
        player_a_name = player_a_entry.get().strip()
        player_b_name = player_b_entry.get().strip()

        if not player_a_name or not player_b_name:
            messagebox.showerror("Error", "Both player names must be entered!")
            return

        # Update the labels in the scoring section
        scoring_section.player_a_label.config(text=f"{player_a_name} ●" if scoring_section.server == "A" else player_a_name)
        scoring_section.player_b_label.config(text=f"{player_b_name} ●" if scoring_section.server == "B" else player_b_name)

        # Save the names in the scoring section for future reference
        scoring_section.player_a_name = player_a_name
        scoring_section.player_b_name = player_b_name

        # Close the pop-up window
        name_window.destroy()

    # Create the pop-up window
    name_window = tk.Toplevel(app)
    name_window.title("Enter Player Names")
    name_window.geometry("400x400")
    name_window.transient(app)  # Keep it on top of the main window
    name_window.grab_set()  # Prevent interaction with the main window

    # Labels and entry fields for player names
    tk.Label(name_window, text="Enter Player A's Name:", font=("Helvetica", 12)).pack(pady=10)
    player_a_entry = tk.Entry(name_window, font=("Helvetica", 12))
    player_a_entry.pack(pady=5)

    tk.Label(name_window, text="Enter Player B's Name:", font=("Helvetica", 12)).pack(pady=10)
    player_b_entry = tk.Entry(name_window, font=("Helvetica", 12))
    player_b_entry.pack(pady=5)

    # Save button
    save_button = tk.Button(name_window, text="Save", command=save_names, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
    save_button.pack(pady=15)

    # Focus on the first entry field
    player_a_entry.focus_set()

class TennisScoring:
    def __init__(self, parent):
        self.parent = parent
        self.player_a_score = 0
        self.player_b_score = 0
        self.player_a_games = 0
        self.player_b_games = 0
        self.server = "A"  # Player A starts serving
        self.scoring_progression = [0, 15, 30, 40]  # Tennis scoring progression

        # Create the scoring section
        self.score_frame = tk.Frame(parent, bg="#ffffff")
        self.score_frame.grid(row=5, column=0, columnspan=8, pady=20)

        # Player A Label
        self.player_a_label = tk.Label(
            self.score_frame,
            text="Player A ●" if self.server == "A" else "Player A",
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
            text="Player B ●" if self.server == "B" else "Player B",
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
        if winner == "A":
            self.update_score("A")
        elif winner == "B":
            self.update_score("B")

    def update_score(self, player):
        """Update the score for the specified player."""
        if player == "A":
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
        elif player == "B":
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

    def toggle_server(self):
        """Toggle the server and update the labels."""
        if self.server == "A":
            self.server = "B"
        else:
            self.server = "A"

    def update_display(self):
        """Update the score and game labels."""
        self.player_a_score_label.config(text=str(self.player_a_score))
        self.player_b_score_label.config(text=str(self.player_b_score))
        self.player_a_games_label.config(text=f"Games: {self.player_a_games}")
        self.player_b_games_label.config(text=f"Games: {self.player_b_games}")

        # Update the serving dot
        self.player_a_label.config(
            text=f"{scoring_section.player_a_name} ●" if self.server == "A" else f"{scoring_section.player_a_name}"
        )
        self.player_b_label.config(
            text=f"{scoring_section.player_b_name}●" if self.server == "B" else f"{scoring_section.player_b_name}"
        )
# Main app window
app = tk.Tk()
app.title("Tennis Data Entry App")
app.geometry("1200x700")
app.configure(bg="#f0f0f0")
app.after(100, ask_player_names)

top_frame = tk.Frame(app, height=200, bg=my_lightblue)
top_frame.pack(side="top", fill="both", expand=True)

bottom_frame = tk.Frame(app, height=500, bg="#ffffff", relief="ridge", bd=2)
bottom_frame.pack(side="bottom", fill="both", expand=True)

scoring_section = TennisScoring(bottom_frame)

# Add a Text widget to the top frame for displaying stats
stats_display = tk.Text(top_frame, height=10, width=100, state="normal", bg="white", font=("Helvetica", 10))
stats_display.pack(padx=10, pady=10)

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


listbox_1st_direction = CustomListbox(bottom_frame, serve_direction_items, 10, 1, 0)
listbox_1st_direction.bind("<Left>", move_focus)  # Bind Left arrow
listbox_1st_direction.bind("<Right>", move_focus)  # Bind Right arrow

listbox_1st_result = CustomListbox(bottom_frame, serve_result_items, 10, 1, 1)
listbox_1st_result.bind("<Left>", move_focus)  # Bind Left arrow
listbox_1st_result.bind("<Right>", move_focus)  # Bind Right arrow

# --- 2nd Serve ---
listbox_2nd_direction = CustomListbox(bottom_frame, serve_direction_items, 10, 1, 2)
listbox_2nd_direction.bind("<Left>", move_focus)  # Bind Left arrow
listbox_2nd_direction.bind("<Right>", move_focus)  # Bind Right arrow

listbox_2nd_result = CustomListbox(bottom_frame, serve_result_items, 10, 1, 3)
listbox_2nd_result.bind("<Left>", move_focus)  # Bind Left arrow
listbox_2nd_result.bind("<Right>", move_focus)  # Bind Right arrow

# -------------------------
# 🎾 Vertical Lists for Return
# -------------------------

# List items for Return
return_type_items = ["Forehand", "Backhand"]
return_shot_items = ["Return", "Pass", "Approach", "Drop", "Lob"]
return_outcome_items = ["Winner", "Unforced", "Forced"]

# --- Return - Type ---
listbox_return_type = CustomListbox(bottom_frame, return_type_items, 10, 1, 4)
listbox_return_type.bind("<Left>", move_focus)  # Bind Left arrow
listbox_return_type.bind("<Right>", move_focus)  # Bind Right arrow

# --- Return - Shot ---
listbox_return_shot = CustomListbox(bottom_frame, return_shot_items, 12, 1, 5)
listbox_return_shot.bind("<Left>", move_focus)  # Bind Left arrow
listbox_return_shot.bind("<Right>", move_focus)  # Bind Right arrow

# --- Return - Outcome ---
listbox_return_outcome = CustomListbox(bottom_frame, return_outcome_items, 10, 1, 6)
listbox_return_outcome.bind("<Left>", move_focus)  # Bind Left arrow
listbox_return_outcome.bind("<Right>", move_focus)  # Bind Right arrow

# listbox point winner

point_winners = ["A", "B"]

# --- Point Winner ---
listbox_point_winner = CustomListbox(bottom_frame, point_winners, 10, 1, 7)
listbox_point_winner.bind("<Left>", move_focus)  # Bind Left arrow
listbox_point_winner.bind("<Right>", move_focus)  # Bind Right arrow

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
listbox_end_type = CustomListbox(bottom_frame, end_type_items, 10, 3, 0)
listbox_end_type.bind("<Left>", move_focus)  # Bind Left arrow
listbox_end_type.bind("<Right>", move_focus)  # Bind Right arrow

# --- End - Shot ---
listbox_end_shot = CustomListbox(bottom_frame, end_shot_items, 12, 3, 1)
listbox_end_shot.bind("<Left>", move_focus)  # Bind Left arrow
listbox_end_shot.bind("<Right>", move_focus)  # Bind Right arrow

# --- End - Outcome ---
listbox_end_outcome = CustomListbox(bottom_frame, end_outcome_items, 10, 3, 2)
listbox_end_outcome.bind("<Left>", move_focus)  # Bind Left arrow
listbox_end_outcome.bind("<Right>", move_focus)  # Bind Right arrow

# -------------------------
# 🎯 New Row - Strategy Section (same row as End)
# -------------------------

# Label
tk.Label(bottom_frame, text="Strategy", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=3, column=3, padx=10, pady=15, sticky="nw")

# List items for Strategy
strategy_position_items = ["Baseline", "A at net", "B at net", "Both at net"]
strategy_play_style_items = ["", "Serve and Volley"]

# --- Strategy - Position ---
listbox_strategy_position = CustomListbox(bottom_frame, strategy_position_items, 15, 3, 4)
listbox_strategy_position.bind("<Left>", move_focus)  # Bind Left arrow
listbox_strategy_position.bind("<Right>", move_focus)  # Bind Right arrow

# --- Strategy - Play Style ---
listbox_strategy_play_style = CustomListbox(bottom_frame, strategy_play_style_items, 15, 3, 5)
listbox_strategy_play_style.bind("<Left>", move_focus)  # Bind Left arrow
listbox_strategy_play_style.bind("<Right>", move_focus)  # Bind Right arrow

# -------------------------
# 🚀 Submit button
# -------------------------
submit_btn = tk.Button(bottom_frame, text="Submit", command=display_stats, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
submit_btn.grid(row=4, column=0, columnspan=8, pady=15)

# Bind the Enter key to display stats
app.bind("<Return>", display_stats)

listbox_1st_direction.focus_set()

# Create a simple object with a 'widget' attribute
class FakeEvent:
    def __init__(self, widget):
        self.widget = widget

on_focus_in(FakeEvent(widget=listbox_1st_direction))


# Run the app
app.mainloop()