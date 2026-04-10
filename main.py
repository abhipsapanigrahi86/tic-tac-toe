# =====================================
# Tic Tac Toe Game
# Developed by Abhipsa
# © 2026 All rights reserved
# =====================================
import tkinter as tk
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("420x600")

        # 🎨 Colors
        self.bg_main = "#0f172a"
        self.bg_card = "#1e293b"
        self.accent = "#3b82f6"
        self.green = "#22c55e"
        self.red = "#ef4444"
        self.text = "#e2e8f0"

        self.root.configure(bg=self.bg_main)

        # Game variables
        self.buttons = []
        self.current = "X"
        self.winner = False
        self.mode = "AI"
        self.difficulty = "Medium"

        self.player1 = ""
        self.player2 = ""

        self.x_score = 0
        self.o_score = 0

        self.create_menu()
        self.create_game_ui()

        # 🎨 WATERMARK (ADDED HERE)
        tk.Label(
            self.root,
            text="Made by Abhipsa",
            font=("Arial", 8),
            bg=self.bg_main,
            fg=self.text
        ).pack(side="bottom")

    # ---------- UI HELPERS ----------
    def styled_button(self, parent, text, cmd, color):
        btn = tk.Button(parent, text=text,
                        command=cmd,
                        bg=color, fg="white",
                        activebackground=color,
                        relief="flat",
                        font=("Arial", 11, "bold"),
                        padx=10, pady=6,
                        cursor="hand2")
        self.add_hover(btn, color)
        return btn

    def add_hover(self, btn, color):
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563eb"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    # ---------- MENU ----------
    def create_menu(self):
        self.menu = tk.Frame(self.root, bg=self.bg_main)
        self.menu.pack(expand=True)

        self.card = tk.Frame(self.menu, bg=self.bg_card)
        self.card.pack(pady=20, padx=20, ipadx=20, ipady=20)

        tk.Label(self.card, text="TIC TAC TOE",
                 font=("Arial", 26, "bold"),
                 fg=self.accent, bg=self.bg_card).pack(pady=10)

        tk.Label(self.card, text="Player Name",
                 bg=self.bg_card, fg=self.text).pack()

        self.name1 = tk.Entry(self.card)
        self.name1.pack(pady=5)

        self.p2_frame = tk.Frame(self.card, bg=self.bg_card)

        tk.Label(self.p2_frame, text="Player 2",
                 bg=self.bg_card, fg=self.text).pack()

        self.name2 = tk.Entry(self.p2_frame)
        self.name2.pack(pady=5)

        self.ai_btn = self.styled_button(self.card, "Play vs Computer",
                                         lambda: self.set_mode("AI"), self.accent)
        self.ai_btn.pack(pady=5)

        self.pvp_btn = self.styled_button(self.card, "2 Player Mode",
                                          lambda: self.set_mode("PVP"), self.green)
        self.pvp_btn.pack(pady=5)

        tk.Label(self.card, text="Difficulty",
                 bg=self.bg_card, fg=self.text).pack(pady=5)

        self.styled_button(self.card, "Easy",
                           lambda: self.set_difficulty("Easy"), "#475569").pack(pady=2)

        self.styled_button(self.card, "Medium",
                           lambda: self.set_difficulty("Medium"), "#475569").pack(pady=2)

        self.styled_button(self.card, "Hard 💀",
                           lambda: self.set_difficulty("Hard"), "#475569").pack(pady=2)

        self.styled_button(self.card, "Start Game",
                           self.start_game, "#f59e0b").pack(pady=10)

        self.set_mode("AI")

    def set_mode(self, mode):
        self.mode = mode

        if mode == "AI":
            self.p2_frame.pack_forget()
            self.name2.delete(0, tk.END)
            self.ai_btn.config(bg=self.accent)
            self.pvp_btn.config(bg="#334155")
        else:
            self.p2_frame.pack(pady=5)
            self.pvp_btn.config(bg=self.green)
            self.ai_btn.config(bg="#334155")

    def set_difficulty(self, level):
        self.difficulty = level

    def start_game(self):
        p1 = self.name1.get().strip()
        p2 = self.name2.get().strip()

        if p1 == "":
            self.show_popup("Enter Player Name!")
            return

        self.player1 = p1

        if self.mode == "AI":
            self.player2 = "Computer"
        else:
            if p2 == "":
                self.show_popup("Enter Player 2 Name!")
                return
            self.player2 = p2

        self.menu.pack_forget()
        self.game.pack(expand=True)
        self.update_score()

    # ---------- GAME UI ----------
    def create_game_ui(self):
        self.game = tk.Frame(self.root, bg=self.bg_main)

        self.score_label = tk.Label(self.game, font=("Arial", 16, "bold"),
                                    bg=self.bg_main, fg=self.text)
        self.score_label.pack(pady=10)

        self.turn_label = tk.Label(self.game, text="Turn: X",
                                  font=("Arial", 14),
                                  bg=self.bg_main, fg=self.text)
        self.turn_label.pack()

        grid = tk.Frame(self.game, bg=self.bg_main)
        grid.pack()

        for i in range(9):
            btn = tk.Button(grid, text="", font=("Arial", 32, "bold"),
                            width=4, height=2,
                            bg=self.bg_card, fg=self.text,
                            relief="flat",
                            activebackground="#334155",
                            command=lambda i=i: self.click(i))
            btn.grid(row=i//3, column=i%3, padx=8, pady=8)
            self.buttons.append(btn)

        self.styled_button(self.game, "Reset Game",
                           self.reset_game, self.accent).pack(pady=5)

        self.styled_button(self.game, "Reset Score",
                           self.reset_score, self.red).pack(pady=5)

    # ---------- GAME ----------
    def click(self, i):
        if self.buttons[i]["text"] != "" or self.winner:
            return

        if self.current == "X":
            self.buttons[i].config(text="X", fg="#60a5fa")
            self.current = "O"
        else:
            self.buttons[i].config(text="O", fg="#f87171")
            self.current = "X"

        self.turn_label.config(text=f"Turn: {self.current}")
        self.check_winner()

        if self.mode == "AI" and self.current == "O" and not self.winner:
            self.root.after(300, self.ai_move)

    # ---------- AI ----------
    def ai_move(self):
        if self.difficulty == "Easy":
            move = self.random_move()
        elif self.difficulty == "Medium":
            move = self.smart_move()
        else:
            move = self.best_move()

        self.click(move)

    def random_move(self):
        empty = [i for i in range(9) if self.buttons[i]["text"] == ""]
        return random.choice(empty)

    def smart_move(self):
        for i in range(9):
            if self.buttons[i]["text"] == "":
                self.buttons[i]["text"] = "O"
                if self.check_temp_win("O"):
                    self.buttons[i]["text"] = ""
                    return i
                self.buttons[i]["text"] = ""

        for i in range(9):
            if self.buttons[i]["text"] == "":
                self.buttons[i]["text"] = "X"
                if self.check_temp_win("X"):
                    self.buttons[i]["text"] = ""
                    return i
                self.buttons[i]["text"] = ""

        if self.buttons[4]["text"] == "":
            return 4

        for i in [0,2,6,8]:
            if self.buttons[i]["text"] == "":
                return i

        return self.random_move()

    def best_move(self):
        best_score = -float("inf")
        move = None

        for i in range(9):
            if self.buttons[i]["text"] == "":
                self.buttons[i]["text"] = "O"
                score = self.minimax(False)
                self.buttons[i]["text"] = ""

                if score > best_score:
                    best_score = score
                    move = i

        return move

    def minimax(self, is_max):
        result = self.check_winner_static()

        if result == "O":
            return 1
        elif result == "X":
            return -1
        elif result == "Draw":
            return 0

        if is_max:
            best = -float("inf")
            for i in range(9):
                if self.buttons[i]["text"] == "":
                    self.buttons[i]["text"] = "O"
                    best = max(best, self.minimax(False))
                    self.buttons[i]["text"] = ""
            return best
        else:
            best = float("inf")
            for i in range(9):
                if self.buttons[i]["text"] == "":
                    self.buttons[i]["text"] = "X"
                    best = min(best, self.minimax(True))
                    self.buttons[i]["text"] = ""
            return best

    def check_temp_win(self, p):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(self.buttons[a]["text"] == self.buttons[b]["text"] == self.buttons[c]["text"] == p
                   for a,b,c in combos)

    def check_winner_static(self):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for a,b,c in combos:
            if self.buttons[a]["text"] == self.buttons[b]["text"] == self.buttons[c]["text"] != "":
                return self.buttons[a]["text"]

        if all(b["text"] != "" for b in self.buttons):
            return "Draw"

        return None

    # ---------- WIN ----------
    def check_winner(self):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for a,b,c in combos:
            if self.buttons[a]["text"] == self.buttons[b]["text"] == self.buttons[c]["text"] != "":
                self.winner = True

                for i in [a,b,c]:
                    self.buttons[i].config(bg="#16a34a")

                if self.buttons[a]["text"] == "X":
                    self.x_score += 1
                    name = self.player1
                else:
                    self.o_score += 1
                    name = self.player2

                self.update_score()
                self.show_popup(f"{name} Wins 🎉")
                return

        if all(b["text"] != "" for b in self.buttons):
            self.winner = True
            self.show_popup("Draw 😐")

    # ---------- HELPERS ----------
    def update_score(self):
        self.score_label.config(
            text=f"{self.player1}: {self.x_score}   |   {self.player2}: {self.o_score}"
        )

    def reset_game(self):
        self.winner = False
        self.current = "X"
        self.turn_label.config(text="Turn: X")

        for b in self.buttons:
            b.config(text="", bg=self.bg_card)

    def reset_score(self):
        self.x_score = 0
        self.o_score = 0
        self.update_score()

    def show_popup(self, msg):
        popup = tk.Toplevel(self.root)
        popup.title("Result")
        popup.geometry("250x150")
        popup.configure(bg=self.bg_card)

        tk.Label(popup, text=msg, font=("Arial", 14, "bold"),
                 bg=self.bg_card, fg=self.text).pack(pady=20)

        self.styled_button(popup, "OK",
                           lambda: [popup.destroy(), self.reset_game()],
                           self.accent).pack()

# ---------- RUN ----------
root = tk.Tk()
app = TicTacToe(root)
root.mainloop()