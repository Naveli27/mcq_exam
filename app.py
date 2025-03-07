from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500))
    option_a = db.Column(db.String(200))
    option_b = db.Column(db.String(200))
    option_c = db.Column(db.String(200))
    option_d = db.Column(db.String(200))
    correct_option = db.Column(db.String(1))

    def __repr__(self):
        return f'<Question {self.id}>'

first_request_done = False

@app.before_request
def setup_database():
    global first_request_done
    if not first_request_done:
        with app.app_context():
            db.create_all()
            if Question.query.count() == 0:
                sample_questions = [
                    Question(question_text="What is 2 + 2?", option_a="3", option_b="4", option_c="5", option_d="6", correct_option="b"),
                    Question(question_text="What is the capital of France?", option_a="Berlin", option_b="Madrid", option_c="Paris", option_d="Rome", correct_option="c"),
                    Question(question_text="Which planet is known as the Red Planet?", option_a="Venus", option_b="Mars", option_c="Jupiter", option_d="Saturn", correct_option="b"),
                    Question(question_text="What is the largest mammal?", option_a="Elephant", option_b="Blue Whale", option_c="Giraffe", option_d="Hippopotamus", correct_option="b"),
                    Question(question_text="What is the chemical symbol for water?", option_a="Co2", option_b="NaCl", option_c="H2O", option_d="O2", correct_option="c"),
                    Question(question_text="Which programming language is this code written in?", option_a="Java", option_b="C++", option_c="Python", option_d="JavaScript", correct_option="c"),
                    Question(question_text="Who painted the Mona Lisa?", option_a="Michelangelo", option_b="Leonardo da Vinci", option_c="Raphael", option_d="Donatello", correct_option="b"),
                    Question(question_text="What is the square root of 16?", option_a="2", option_b="4", option_c="8", option_d="16", correct_option="b"),
                    Question(question_text="What is the currency of Japan?", option_a="Yuan", option_b="Won", option_c="Euro", option_d="Yen", correct_option="d"),
                    Question(question_text="Which gas do plants absorb from the atmosphere?", option_a="Oxygen", option_b="Nitrogen", option_c="Carbon Dioxide", option_d="Hydrogen", correct_option="c"),
                    Question(question_text="What is 10 * 5?", option_a="2", option_b="15", option_c="50", option_d="5", correct_option="c"),
                    Question(question_text="Which animal is known as the king of the jungle?", option_a="Tiger", option_b="Lion", option_c="Elephant", option_d="Bear", correct_option="b"),
                ]
                db.session.add_all(sample_questions)
                db.session.commit()
            first_request_done = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_test')
def start_test():
    questions = Question.query.all()
    selected_questions = random.sample(questions, min(10, len(questions)))  # Ensure no more than 10

    return render_template('test.html', questions=selected_questions)

@app.route('/submit_test', methods=['POST'])
def submit_test():
    questions = []
    user_answers = {}
    score = 0
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = int(key.split('_')[1])
            question = Question.query.get(question_id)
            questions.append(question)
            user_answers[question_id] = value
            if value == question.correct_option:
                score += 1

    return render_template('summary.html', questions=questions, user_answers=user_answers, score=score)

if __name__ == '__main__':
    app.run(debug=True)