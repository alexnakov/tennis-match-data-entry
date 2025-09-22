import tkinter as tk

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

        self.player_a_label = tk.Label(self.score_frame, text=f"{self.player_a_name} ●", font=("Helvetica", 14, "bold"), bg="#ffffff")
        self.player_a_label.grid(row=0, column=0, padx=20)
        self.player_a_score_label = tk.Label(self.score_frame, text="0", font=("Helvetica", 14), bg="#ffffff")
        self.player_a_score_label.grid(row=0, column=1, padx=10)

        self.player_b_label = tk.Label(self.score_frame, text=f"{self.player_b_name}", font=("Helvetica", 14, "bold"), bg="#ffffff")
        self.player_b_label.grid(row=0, column=2, padx=20)
        self.player_b_score_label = tk.Label(self.score_frame, text="0", font=("Helvetica", 14), bg="#ffffff")
        self.player_b_score_label.grid(row=0, column=3, padx=10)

        self.player_a_games_label = tk.Label(self.score_frame, text="Games: 0", font=("Helvetica", 12), bg="#ffffff")
        self.player_a_games_label.grid(row=1, column=0, padx=10)
        self.player_b_games_label = tk.Label(self.score_frame, text="Games: 0", font=("Helvetica", 12), bg="#ffffff")
        self.player_b_games_label.grid(row=1, column=2, padx=10)

    def add_point(self, winner):
        if winner == self.player_a_name:
            self._update_score(self.player_a_name)
        elif winner == self.player_b_name:
            self._update_score(self.player_b_name)

    def _update_score(self, player):
        if player == self.player_a_name:
            if self.player_a_score == 40 and self.player_b_score == 40:
                self.player_a_score = "Adv"
            elif self.player_a_score == "Adv" and self.player_b_score == 40:
                self.player_a_score = "Game"
            elif self.player_b_score == "Adv":
                self.player_a_score = 40; self.player_b_score = 40
            elif self.player_a_score == 40 and self.player_b_score != 40:
                self.player_a_score = "Game"
            else:
                self.player_a_score = self.scoring_progression[self.scoring_progression.index(self.player_a_score) + 1]
        else:
            if self.player_b_score == 40 and self.player_a_score == 40:
                self.player_b_score = "Adv"
            elif self.player_b_score == "Adv" and self.player_a_score == 40:
                self.player_b_score = "Game"
            elif self.player_b_score == 40 and self.player_a_score == "Adv":
                self.player_a_score = 40; self.player_b_score = 40
            elif self.player_b_score == 40 and self.player_a_score != 40:
                self.player_b_score = "Game"
            else:
                self.player_b_score = self.scoring_progression[self.scoring_progression.index(self.player_b_score) + 1]

        if self.player_a_score == "Game":
            self.player_a_games += 1; self._reset_scores(); self.toggle_server()
        elif self.player_b_score == "Game":
            self.player_b_games += 1; self._reset_scores(); self.toggle_server()
        self.update_display()

    def _reset_scores(self):
        self.player_a_score = 0
        self.player_b_score = 0

    def reset_scores_and_display(self):
        self._reset_scores()
        self.update_display()

    def toggle_server(self):
        self.server = self.player_b_name if self.server == self.player_a_name else self.player_a_name
        self.update_display()

    def update_display(self):
        self.player_a_score_label.config(text=str(self.player_a_score))
        self.player_b_score_label.config(text=str(self.player_b_score))
        self.player_a_games_label.config(text=f"Games: {self.player_a_games}")
        self.player_b_games_label.config(text=f"Games: {self.player_b_games}")
        self.player_a_label.config(text=f"{self.player_a_name} {'●' if self.server == self.player_a_name else ''}".strip())
        self.player_b_label.config(text=f"{self.player_b_name} {'●' if self.server == self.player_b_name else ''}".strip())
