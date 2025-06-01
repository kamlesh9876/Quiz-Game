import html

class QuizLogic:
    def __init__(self, question_data):
        self.questions = [
            {
                "question": html.unescape(q["question"]),
                "correct_answer": html.unescape(q["correct_answer"]),
                "incorrect_answers": [html.unescape(ans) for ans in q["incorrect_answers"]]
            }
            for q in question_data
        ]
        self.current = 0
        self.score = 0

    def get_next(self):
        if self.current < len(self.questions):
            q = self.questions[self.current]
            self.current += 1
            return q
        return None

    def check_answer(self, user_ans, correct_ans):
        if user_ans == correct_ans:
            self.score += 1
            return True
        return False
