import tkinter as tk
from quize_api import fetch_questions
from quiz_logic import QuizLogic
from ui import QuizUI

# Fetch online questions
question_data = fetch_questions(amount=10, category=None, difficulty='easy')
quiz = QuizLogic(question_data)

# Launch UI
root = tk.Tk()
quiz_ui = QuizUI(root, quiz)
root.mainloop()
