from flask import Flask, render_template, redirect, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length
from models import db, User, Feedback
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'  # Required for session handling and form security

db.init_app(app)
bcrypt = Bcrypt(app)


# Routes
@app.route('/')
def home():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # (Existing registration code...)
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    # (Existing login code...)
    pass


@app.route('/logout')
def logout():
    session.clear()  # Clears the session, logging the user out
    return redirect('/')


@app.route('/users/<username>')
def show_user(username):
    if 'username' not in session or session['username'] != username:
        return redirect('/login')

    user = User.query.filter_by(username=username).first_or_404()
    feedbacks = Feedback.query.filter_by(username=username).all()

    return render_template('user.html', user=user, feedbacks=feedbacks)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session or session['username'] != username:
        return redirect('/login')

    user = User.query.filter_by(username=username).first_or_404()
    Feedback.query.filter_by(username=username).delete()
    db.session.delete(user)
    db.session.commit()

    session.clear()
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session or session['username'] != username:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template('add_feedback.html')


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or session['username'] != feedback.username:
        return redirect('/login')

    if request.method == 'POST':
        feedback.title = request.form['title']
        feedback.content = request.form['content']
        db.session.commit()
        return redirect(f'/users/{feedback.username}')

    return render_template('update_feedback.html', feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or session['username'] != feedback.username:
        return redirect('/login')

    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')


if __name__ == '__main__':
    app.run(debug=True)
