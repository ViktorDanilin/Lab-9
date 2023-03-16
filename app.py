from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template("index.html")


@app.route('/support', methods=['POST', 'GET'])
def support():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        question = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(question)
            db.session.commit()
            return redirect('/questions')
        except:
            return "Error"
    else:
        return render_template("support.html")


@app.route('/questions')
def post_questions():
    questions = Article.query.order_by(Article.date.desc()).all()
    return render_template('questions.html', questions=questions)


@app.route('/questions/<int:id>')
def questions_details(id):
    questions = Article.query.get(id)
    return render_template('questions_detail.html', questions=questions)


@app.route('/questions/<int:id>/delete')
def posts_delete(id):
    question = Article.query.get_or_404(id)
    try:
        db.session.delete(question)
        db.session.commit()
        return redirect('/questions')
    except:
        return 'Error'


@app.route('/questions/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    question = Article.query.get(id)
    if request.method == 'POST':
        question.title = request.form['title']
        question.intro = request.form['intro']
        question.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/questions')
        except:
            return "Error"
    else:
        return render_template("question_update.html", question=question)


@app.route('/description')
def description():
    return render_template("description.html")


if __name__ == '__main__':
    app.run(debug=True)
