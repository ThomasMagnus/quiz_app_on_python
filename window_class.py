import time
from tkinter import *
import requests
import html
from time import sleep


class QuizInterface:
    questions = []
    count = 0
    user_score = 0

    def __init__(self):
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=50, bg="#375362")
        self.score = Label(text=f'Score: {self.user_score}', bg="#375362", fg='white', pady=20, font=('Arial', 10))
        self.score.grid(row=0, column=1)

        self.create_quiz()
        self.canvas = Canvas(width=300, height=300, bg='white')
        self.question_txt = self.canvas.create_text(
            150, 125,
            width=280,
            text=f'Q{self.count + 1}.{self.questions[self.count]["question"]}',
            font=('Arial', 20, 'italic'))
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.true_img = PhotoImage(file='images/true.png')
        self.true_btn = Button(image=self.true_img, command=self.true_answer)
        self.true_btn.grid(row=2, column=0, pady=20)

        self.false_img = PhotoImage(file='images/false.png')
        self.false_btn = Button(image=self.false_img, command=self.false_answer)
        self.false_btn.grid(row=2, column=1, pady=20)

        self.window.mainloop()

    def create_quiz(self):
        response = requests.get(
            'https://opentdb.com/api.php?amount=10&category=22&difficulty=medium&type=boolean').json()
        print(response['results'])
        for res in response['results']:
            self.questions.append({
                'category': res['category'],
                'question': html.unescape(res['question']),
                'correct_answer': res['correct_answer']
            })

    def next_question(self):
        if self.count <= len(self.questions) - 2:
            self.count += 1
            self.canvas.itemconfig(self.question_txt,
                                   text=f'Q{self.count + 1}.{self.questions[self.count]["question"]}')
            self.canvas.config(bg='white')

    def correct_answer(self, answer):
        if self.count <= len(self.questions) - 2 and self.questions[self.count]['correct_answer'] == answer:
            self.canvas.config(bg='green')
            self.user_score += 1
            self.score.config(text=f'Score: {self.user_score}')
        else:
            self.canvas.config(bg='red')
        self.window.after(2000, func=self.next_question)

    def true_answer(self):
        self.correct_answer('True')

    def false_answer(self):
        self.correct_answer('False')
