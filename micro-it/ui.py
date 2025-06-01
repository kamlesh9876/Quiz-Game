import tkinter as tk
from tkinter import messagebox, ttk
import random

class QuizUI:
    def __init__(self, master, quiz):
        self.quiz = quiz
        self.master = master
        self.master.title("Ultimate Quiz Game")
        self.master.geometry("700x550")
        self.master.configure(bg="#1e1e2f")

        # Title
        self.header = tk.Label(master, text="🧠 Ultimate Quiz Game", font=("Segoe UI", 24, "bold"), fg="#ffffff", bg="#1e1e2f")
        self.header.pack(pady=10)

        # Score Display
        self.score_label = tk.Label(master, text=f"Score: 0", font=("Segoe UI", 14), fg="#00ffcc", bg="#1e1e2f")
        self.score_label.pack()

        # Timer Display
        self.timer_label = tk.Label(master, text="Time Left: 15s", font=("Segoe UI", 14), fg="#ffcc00", bg="#1e1e2f")
        self.timer_label.pack()

        # Question Frame
        self.question_frame = tk.Frame(master, bg="#2d2d44", padx=20, pady=20)
        self.question_frame.pack(pady=10)

        self.question_text = tk.Label(self.question_frame, text="", wraplength=650, font=("Segoe UI", 16), fg="#ffffff", bg="#2d2d44")
        self.question_text.pack()

        # Buttons
        self.buttons = []
        self.button_frame = tk.Frame(master, bg="#1e1e2f")
        self.button_frame.pack(pady=20)
        for i in range(4):
            btn = tk.Button(self.button_frame, font=("Segoe UI", 14), width=40, bg="#393955", fg="white", bd=0, pady=10, relief="flat", cursor="hand2")
            btn.config(command=lambda b=i: self.check(b))
            btn.pack(pady=5)
            self.buttons.append(btn)

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["maximum"] = len(self.quiz.questions)
        self.progress["value"] = 0

        self.time_left = 15
        self.timer_id = None
        self.load_next()

    def load_next(self):
        self.time_left = 15
        self.update_timer()

        q = self.quiz.get_next()
        if not q:
            messagebox.showinfo("Quiz Over", f"🎉 Your final score: {self.quiz.score}/{self.quiz.current}")
            self.master.quit()
            return

        self.question_text.config(text=q["question"])
        answers = q["incorrect_answers"] + [q["correct_answer"]]
        random.shuffle(answers)
        for i, ans in enumerate(answers):
            self.buttons[i].config(text=ans, bg="#393955", state="normal")
        self.correct_answer = q["correct_answer"]
        self.progress["value"] = self.quiz.current
        self.update_score()

    def check(self, i):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        selected = self.buttons[i].cget("text") if i >= 0 else None
        if selected == self.correct_answer:
            self.quiz.score += 1
            self.buttons[i].config(bg="green")
        else:
            if i >= 0:
                self.buttons[i].config(bg="red")
            for btn in self.buttons:
                if btn.cget("text") == self.correct_answer:
                    btn.config(bg="green")

        for btn in self.buttons:
            btn.config(state="disabled")
        self.master.after(1000, self.reset_and_next)

    def reset_and_next(self):
        for btn in self.buttons:
            btn.config(bg="#393955", state="normal")
        self.load_next()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.quiz.score}")

    def update_timer(self):
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        if self.time_left <= 0:
            self.check(-1)  # timeout
            return
        self.time_left -= 1
        self.timer_id = self.master.after(1000, self.update_timer)
