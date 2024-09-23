from pathlib import Path

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
import sqlite3

from werkzeug.utils import secure_filename

from . import app, db
from .forms import NewsForm, FeedbackForm, LoginForm, RegistrationForm, CategoryForm

from .models import Category, News, Feedback, User

from .forms import NewsForm, LoginForm, RegistrationForm  # CategoryForm

BASEDIR = Path(__file__).parent
UPLOAD_FOLDER = BASEDIR / 'static' / 'images'


@app.route('/')
def index():
    news_list = News.query.all()
    categories = Category.query.all()
    return render_template('index.html',
                           news=news_list,
                           categories=categories)


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        category = Category()
        category.title = form.title.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_category.html',
                           form=form,
                           categories=categories)


@app.route('/news_detail/<int:id>')
def news_detail(id):
    news = News.query.get(id)
    categories = Category.query.all()
    return render_template('news_detail.html',
                           news=news,
                           categories=categories
                           )


@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news
    category_name = category.title
    categories = Category.query.all()
    return render_template('category.html',
                           news=news,
                           category_name=category_name,
                           categories=categories)


@app.route('/add_news/', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        news.category_id = form.category.data
        image = form.image.data
        if image:
            image_name = secure_filename(image.filename)
            UPLOAD_FOLDER.mkdir(exist_ok=True)
            image.save(UPLOAD_FOLDER / image_name)
            news.image = image_name
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('news_detail', id=news.id))
    return render_template('add_news.html', form=form, categories=categories)


@app.route('/feedback/', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback_entry = Feedback(
            name=form.name.data,
            text=form.text.data,
            email=form.email.data,
            rating=form.rating.data
        )
        db.session.add(feedback_entry)
        db.session.commit()
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)


def get_db_connection():
    conn = sqlite3.connect('/home/pliskinaolia/flask_news/app/db.sqlite3')
    # conn = sqlite3.connect('app/db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/delete_news/<int:id>', methods=['POST'])
def delete_news(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM news WHERE id = ?', (id,))
    conn.commit()
    if cursor.rowcount > 0:
        flash('Новость была успешно удалена.', 'success')
    else:
        flash('Новость не найдена.', 'error')
    conn.close()
    return redirect(url_for('index'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вход выполнен!', 'alert-success')
            return redirect(url_for('index'))
        else:
            flash('Вход не выполнен!', 'alert-danger')
    return render_template('login.html', form=form, categories=categories)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'alert-success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form, categories=categories)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))