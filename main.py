import tkinter as tk
from tkinter import simpledialog, messagebox

MY_LIGHTBLUE = "#b2d6fe"


class CustomListbox(tk.Listbox):
    """Listbox with your highlight/focus behavior baked in."""
    def __init__(self, parent, items, width, row, column, **kwargs):
        super().__init__(parent, height=len(items), width=width, exportselection=False, **kwargs)
        for item in items:
            self.insert(tk.END, item)
        self.grid(row=row, column=column, padx=10, pady=0, sticky="nw")
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<<ListboxSelect>>", self._on_listbox_select)

    def _on_focus_in(self, _event):
        self.config(bg="lightgreen")
        if self.size() > 0:
            active_index = self.index(tk.ACTIVE)
            if active_index != -1:
                for i in range(self.size()):
                    self.itemconfig(i, bg=self.cget("background"))
                self.itemconfig(active_index, bg=MY_LIGHTBLUE)
            else:
                self.activate(0)
                self.selection_clear(0, tk.END)
                self.selection_set(0)
                self.itemconfig(0, bg=MY_LIGHTBLUE)

    def _on_listbox_select(self, _event):
        for i in range(self.size()):
            self.itemconfig(i, bg=self.cget("background"))
        if self.curselection():
            index = int(self.curselection()[0])
            self.itemconfig(index, bg=MY_LIGHTBLUE)


class TennisScoring:
    def __init__(self, parent, player_a_name, player_b_name):
        self.parent = parent
        self.player_a_name = player_a_name
        self.player_b_name = player_b_name
        self.player_a_score = 0
        self.player_b_score = 0
        self.player_a_games = 0
        self.player_b_games = 0
        self.server = player_a_name
        self.scoring_progression = [0, 15, 30, 40]

        self.score_frame = tk.Frame(parent, bg="#ffffff")
        self.score_frame.grid(row=5, column=0, columnspan=8, pady=20)

        self.toggle_server_button = tk.Button(self.parent, text="Toggle Server", command=self.toggle_server)
        self.toggle_server_button.grid(row=3, column=7)

        self.reset_score_btn = tk.Button(self.parent, text='Reset In-Game Score', command=self.reset_scores_and_display)
        self.reset_score_btn.grid(row=3, column=8)

        self.player_a_label = tk.Label(self.score_frame,
            text=f"{self.player_a_name} ●" if self.server == self.player_a_name else f"{self.player_a_name}",
            font=("Helvetica", 14, "bold"), fg="black", bg="#ffffff")
        self.player_a_label.grid(row=0, column=0, padx=20)

        self.player_a_score_label = tk.Label(self.score_frame, text="0", font=("Helvetica", 14), fg="black", bg="#ffffff")
        self.player_a_score_label.grid(row=0, column=1, padx=10)

        self.player_b_label = tk.Label(self.score_frame,
            text=f"{self.player_b_name} ●" if self.server == self.player_b_name else f"{self.player_b_name}",
            font=("Helvetica", 14, "bold"), fg="black", bg="#ffffff")
        self.player_b_label.grid(row=0, column=2, padx=20)

        self.player_b_score_label = tk.Label(self.score_frame, text="0", font=("Helvetica", 14), fg="black", bg="#ffffff")
        self.player_b_score_label.grid(row=0, column=3, padx=10)

        self.player_a_games_label = tk.Label(self.score_frame, text="Games: 0", font=("Helvetica", 12), fg="black", bg="#ffffff")
        self.player_a_games_label.grid(row=1, column=0, padx=10)

        self.player_b_games_label = tk.Label(self.score_frame, text="Games: 0", font=("Helvetica", 12), fg="black", bg="#ffffff")
        self.player_b_games_label.grid(row=1, column=2, padx=10)

    def add_point(self, winner):
        if winner == self.player_a_name:
            self._update_score_a()
        elif winner == self.player_b_name:
            self._update_score_b()
        self.update_display()

    def _progress(self, value):
        return self.scoring_progression[self.scoring_progression.index(value) + 1]

    def _update_score_a(self):
        a, b = self.player_a_score, self.player_b_score
        if a == 40 and b == 40:
            self.player_a_score = "Adv"
        elif a == "Adv" and b == 40:
            self.player_a_score = "Game"
        elif b == "Adv":
            self.player_a_score = 40; self.player_b_score = 40
        elif a == 40 and b != 40:
            self.player_a_score = "Game"
        else:
            self.player_a_score = self._progress(a)
        self._check_game()

    def _update_score_b(self):
        a, b = self.player_a_score, self.player_b_score
        if b == 40 and a == 40:
            self.player_b_score = "Adv"
        elif b == "Adv" and a == 40:
            self.player_b_score = "Game"
        elif b == 40 and a == "Adv":
            self.player_a_score = 40; self.player_b_score = 40
        elif b == 40 and a != 40:
            self.player_b_score = "Game"
        else:
            self.player_b_score = self._progress(b)
        self._check_game()

    def _check_game(self):
        if self.player_a_score == "Game":
            self.player_a_games += 1
            self.reset_scores(); self.toggle_server()
        elif self.player_b_score == "Game":
            self.player_b_games += 1
            self.reset_scores(); self.toggle_server()

    def reset_scores(self):
        self.player_a_score = 0
        self.player_b_score = 0

    def reset_scores_and_display(self):
        self.reset_scores()
        self.update_display()

    def toggle_server(self):
        self.server = self.player_b_name if self.server == self.player_a_name else self.player_a_name
        self.update_display()

    def update_display(self):
        self.player_a_score_label.config(text=str(self.player_a_score))
        self.player_b_score_label.config(text=str(self.player_b_score))
        self.player_a_games_label.config(text=f"Games: {self.player_a_games}")
        self.player_b_games_label.config(text=f"Games: {self.player_b_games}")
        self.player_a_label.config(text=f"{self.player_a_name} ●" if self.server == self.player_a_name else f"{self.player_a_name}")
        self.player_b_label.config(text=f"{self.player_b_name} ●" if self.server == self.player_b_name else f"{self.player_b_name}")


class EnterConfirmation:
    """Handles the double-Enter confirm flow."""
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.confirmation_active = False

        self.label = tk.Label(self.root, text="Press Enter to confirm results.", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.root.bind('<Return>', self.show_confirmation)

    def show_confirmation(self, _event):
        if self.confirmation_active:
            return
        self.confirmation_active = True
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Confirmation")
        self.popup.geometry("350x150")

        tk.Label(self.popup, text="Are you sure you want to enter these results?", font=("Helvetica", 12)).pack(pady=10)
        self.popup.bind('<Return>', self.enter_results)
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel_confirmation)

    def enter_results(self, _event):
        self.app.display_stats()
        self.confirmation_active = False
        self.popup.destroy()

    def cancel_confirmation(self):
        self.confirmation_active = False
        self.popup.destroy()


class App:
    def __init__(self, root):
        self.root = root
        root.title("Tennis Data Entry App")
        root.geometry("1200x700")
        root.configure(bg="#f0f0f0")

        self.top_frame = tk.Frame(root, height=200, bg=MY_LIGHTBLUE)
        self.top_frame.pack(side="top", fill="both", expand=True)

        self.bottom_frame = tk.Frame(root, height=500, bg="#ffffff", relief="ridge", bd=2)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

        # player names (tests will monkeypatch askstring)
        self.player_a_name = simpledialog.askstring("Player A", "Enter the name of Player A:")
        self.player_b_name = simpledialog.askstring("Player B", "Enter the name of Player B:")

        self.scoring = TennisScoring(self.bottom_frame, self.player_a_name, self.player_b_name)
        self.confirm = EnterConfirmation(self)

        # stats display
        self.stats_display = tk.Text(self.top_frame, height=10, width=140, state="normal", bg="white", font=("Helvetica", 10))
        self.stats_display.pack(padx=10, pady=10)

        # labels
        tk.Label(self.bottom_frame, text="1st Serve", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        tk.Label(self.bottom_frame, text="2nd Serve", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=2, padx=10, pady=5, sticky="nw")
        tk.Label(self.bottom_frame, text="Return",    font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=4, padx=10, pady=5, sticky="nw")
        tk.Label(self.bottom_frame, text="Point Winner", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=0, column=7, padx=10, pady=5, sticky="nw")
        tk.Label(self.bottom_frame, text="End", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=2, column=0, padx=10, pady=15, sticky="nw")
        tk.Label(self.bottom_frame, text="Strategy", font=("Helvetica", 12, "bold"), bg="#ffffff").grid(row=2, column=3, padx=10, pady=15, sticky="nw")

        # lists
        serve_direction_items = ["Wide", "Body", "Center", "In Net"]
        serve_result_items    = ["In", "Winner", "Ace", "Fault"]

        self.lb_1st_dir = CustomListbox(self.bottom_frame, serve_direction_items, 8, 1, 0)
        self.lb_1st_res = CustomListbox(self.bottom_frame, serve_result_items, 8, 1, 1)
        self.lb_2nd_dir = CustomListbox(self.bottom_frame, serve_direction_items, 8, 1, 2)
        self.lb_2nd_res = CustomListbox(self.bottom_frame, serve_result_items, 8, 1, 3)

        return_type_items    = ["Forehand", "Backhand"]
        return_shot_items    = ["Return", "Pass", "Approach", "Drop", "Lob"]
        return_outcome_items = ["In", "Winner", "Unforced", "Forced"]

        self.lb_ret_type = CustomListbox(self.bottom_frame, return_type_items, 8, 1, 4)
        self.lb_ret_shot = CustomListbox(self.bottom_frame, return_shot_items, 8, 1, 5)
        self.lb_ret_out  = CustomListbox(self.bottom_frame, return_outcome_items, 8, 1, 6)

        point_winners = [self.player_a_name, self.player_b_name]
        self.lb_winner = CustomListbox(self.bottom_frame, point_winners, 8, 1, 7)

        end_type_items    = ["Forehand", "Backhand"]
        end_shot_items    = ["Drive", "Volley", "Smash", "Pass", "Approach", "Lob", "Drop"]
        end_outcome_items = ["Winner", "Forced", "Unforced"]

        self.lb_end_type = CustomListbox(self.bottom_frame, end_type_items, 8, 3, 0)
        self.lb_end_shot = CustomListbox(self.bottom_frame, end_shot_items, 8, 3, 1)
        self.lb_end_out  = CustomListbox(self.bottom_frame, end_outcome_items, 8, 3, 2)

        strategy_position_items = ["Baseline", f"{self.player_a_name} at net", f"{self.player_b_name} at net", "Both at net"]
        strategy_play_style_items = ["", "Serve & Volley"]
        self.lb_strat_pos = CustomListbox(self.bottom_frame, strategy_position_items, 12, 3, 3)
        self.lb_strat_ps  = CustomListbox(self.bottom_frame, strategy_play_style_items, 11, 3, 4)

        # key bindings (migrated from your free functions)
        for lb in [self.lb_1st_dir, self.lb_1st_res, self.lb_2nd_dir, self.lb_2nd_res,
                   self.lb_ret_type, self.lb_ret_shot, self.lb_ret_out, self.lb_winner,
                   self.lb_end_type, self.lb_end_shot, self.lb_end_out, self.lb_strat_pos, self.lb_strat_ps]:
            lb.bind("<Left>",  self.move_focus_left)
            lb.bind("<Right>", self.move_focus_right)

        # initial focus
        self.lb_1st_dir.focus_set()
        self._focus_style(self.lb_1st_dir)

    # ---------- UI helpers / behavior ----------
    def _focus_style(self, lb: tk.Listbox):
        lb.config(bg="lightgreen")
        if lb.size() > 0:
            lb.activate(0)
            lb.selection_clear(0, tk.END)
            lb.selection_set(0)
            lb.itemconfig(0, bg=MY_LIGHTBLUE)

    def _unfocus_style(self, lb: tk.Listbox, last_active_index: int | None):
        lb.config(bg="white")
        for i in range(lb.size()):
            lb.itemconfig(i, bg="white")
        if last_active_index is not None and 0 <= last_active_index < lb.size():
            lb.itemconfig(last_active_index, bg=MY_LIGHTBLUE)

    def _all_listboxes_in_order(self):
        return [
            self.lb_1st_dir, self.lb_1st_res,
            self.lb_2nd_dir, self.lb_2nd_res,
            self.lb_ret_type, self.lb_ret_shot, self.lb_ret_out,
            self.lb_winner,
            self.lb_end_type, self.lb_end_shot, self.lb_end_out,
            self.lb_strat_pos, self.lb_strat_ps,
        ]

    def move_focus_left(self, event):
        lbs = self._all_listboxes_in_order()
        cur = event.widget
        idx = lbs.index(cur)
        active = cur.index(tk.ACTIVE) if cur.size() > 0 else None
        self._unfocus_style(cur, active)
        nxt = lbs[idx - 1]
        nxt.focus_set(); self._focus_style(nxt)

    def move_focus_right(self, event):
        lbs = self._all_listboxes_in_order()
        cur = event.widget
        n = len(lbs); i = lbs.index(cur)
        active = cur.index(tk.ACTIVE) if cur.size() > 0 else None
        self._unfocus_style(cur, active)

        if cur is self.lb_1st_dir:
            if cur.get(tk.ACTIVE) == "In Net":
                self.lb_1st_res.config(bg="lightgray")
                for j in range(self.lb_1st_res.size()):
                    self.lb_1st_res.itemconfig(j, bg="lightgray")
                nxt = self.lb_2nd_dir
            else:
                nxt = self.lb_1st_res

        elif cur is self.lb_1st_res:
            sel = self.lb_1st_res.get(tk.ACTIVE)
            if sel == "In":
                for lb in (self.lb_2nd_dir, self.lb_2nd_res):
                    lb.config(bg="lightgray")
                    for j in range(lb.size()):
                        lb.itemconfig(j, bg="lightgray")
                nxt = self.lb_ret_type
            elif sel in ("Ace", "Winner"):
                for lb in (self.lb_2nd_dir, self.lb_2nd_res, self.lb_ret_type, self.lb_ret_shot, self.lb_ret_out):
                    lb.config(bg="lightgray")
                    for j in range(lb.size()):
                        lb.itemconfig(j, bg="lightgray")
                nxt = self.lb_winner
            else:
                nxt = lbs[min(i + 1, n - 1)]

        elif cur is self.lb_2nd_dir:
            if cur.get(tk.ACTIVE) == "In Net":
                for lb in (self.lb_2nd_res, self.lb_ret_type, self.lb_ret_shot, self.lb_ret_out):
                    lb.config(bg="lightgray")
                    for j in range(lb.size()):
                        lb.itemconfig(j, bg="lightgray")
                nxt = self.lb_winner
            else:
                nxt = self.lb_2nd_res

        elif cur is self.lb_2nd_res:
            if self.lb_2nd_res.get(tk.ACTIVE) in ("Ace", "Winner", "Fault"):
                for lb in (self.lb_ret_type, self.lb_ret_shot, self.lb_ret_out):
                    lb.config(bg="lightgray")
                    for j in range(lb.size()):
                        lb.itemconfig(j, bg="lightgray")
                nxt = self.lb_winner
            else:
                nxt = lbs[min(i + 1, n - 1)]
        else:
            nxt = lbs[min(i + 1, n - 1)]

        nxt.focus_set(); self._focus_style(nxt)

    # ---------- data / submit ----------
    def get_current_data(self):
        def safe(lb, default=""):
            return (lb.get(tk.ACTIVE) if lb.curselection() else default).strip()

        return {
            "1st":     f"{safe(self.lb_1st_dir, 'Wide')} {safe(self.lb_1st_res)}".strip(),
            "2nd":     f"{safe(self.lb_2nd_dir)} {safe(self.lb_2nd_res)}".strip(),
            "Return":  f"{safe(self.lb_ret_type)} {safe(self.lb_ret_shot)} {safe(self.lb_ret_out)}".strip(),
            "Winner":  safe(self.lb_winner),
            "End":     f"{safe(self.lb_end_type)} {safe(self.lb_end_shot)} {safe(self.lb_end_out)}".strip(),
            "Strategy": (safe(self.lb_strat_pos) + (" + " if safe(self.lb_strat_pos) and safe(self.lb_strat_ps) else "") + safe(self.lb_strat_ps)).strip(),
        }

    def display_stats(self):
        data = {k: v for k, v in self.get_current_data().items() if v}
        if not data:
            return
        stats = ";  ".join(f"{k}: {v}" for k, v in data.items())
        self.stats_display.insert(tk.END, stats + "\n")
        self.stats_display.see(tk.END)

        # scoring
        winner = data.get("Winner")
        if winner == self.player_a_name:
            self.scoring.add_point(self.player_a_name)
        elif winner == self.player_b_name:
            self.scoring.add_point(self.player_b_name)

        # clear selections + refocus first
        for lb in self._all_listboxes_in_order():
            lb.selection_clear(0, tk.END)
            lb.config(bg='white')
            for i in range(lb.size()):
                lb.itemconfig(i, bg="white")
        self.lb_1st_dir.focus_set()
        self._focus_style(self.lb_1st_dir)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
