import os
import logging
from flask import Flask, render_template, request, \
    redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
app = Flask(__name__)
Bootstrap(app)
host = os.environ.get('SALES_DB_HOST')
port = os.environ.get('SALES_DB_PORT')
db_name = os.environ.get('SALES_DB_NAME')
user = os.environ.get('SALES_DB_USER')
password = os.environ.get('SALES_DB_PASS')
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
db.init_app(app)


from models.user import User
from models.course import Course

@app.route('/')
def hello_world():
    rec = db.get_or_404(Course, 1)
    return render_template('index.html', user=rec)


@app.route('/users')
def users():
    user_recs = db.session.query(User).all()
    users = list(map(lambda rec: rec.__dict__, user_recs))
    return render_template('users.html', users=users)


@app.route('/courses')
def courses():
    course_recs = db.session.query(Course).all()
    courses = list(map(lambda rec: rec.__dict__, course_recs))
    return render_template('courses.html', courses=courses)


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            user = User.query.get(id)
            return render_template('user_detail.html', user=user)
        else:
            return render_template('user_form.html', user=None)
    elif request.method == 'POST':
        id = request.args.get('id')
        if id:
            user = User.query.get(id)
            form_action = request.form['action']
            if form_action == 'edit':
                return render_template('user_form.html', user=user)
            elif form_action == 'delete':
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for('users'))
        else:
            id = request.form['id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            username = request.form['username']
            email = request.form['email']
            if id:
                user = User.query.get(id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
            else:
                user = User(
                    first_name=first_name, 
                    last_name=last_name, 
                    username=username,
                    email=email
                )
                db.session.add(user)
            db.session.commit()
            return redirect(url_for('users'))


@app.route('/course', methods=['GET', 'POST'])
def course():
    if request.method == 'GET':
        course_id = request.args.get('course_id')
        if course_id:
            course = Course.query.get(course_id)
            return render_template('course_detail.html', course=course)
        else:
            return render_template('course_form.html', course=None)
    elif request.method == 'POST':
        course_id = request.args.get('course_id')
        if course_id:
            course = Course.query.get(course_id)
            form_action = request.form['action']
            if form_action == 'edit':
                return render_template('course_form.html', course=course)
            elif form_action == 'delete':
                db.session.delete(course)
                db.session.commit()
                return redirect(url_for('courses'))
        else:
            course_id = request.form['course_id']
            course_name = request.form['course_name']
            course_author = request.form['course_author']
            course_endpoint = request.form['course_endpoint']
            if course_id:
                course = Course.query.get(course_id)
                course.course_name = course_name
                course.course_author = course_author
                course.course_endpoint = course_endpoint
            else:
                course = Course(
                    course_name=course_name, 
                    course_author=course_author, 
                    course_endpoint=course_endpoint
                )
                db.session.add(course)
            db.session.commit()
            return redirect(url_for('courses'))

        
if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)