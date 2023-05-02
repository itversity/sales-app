import os
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

@app.route('/')
def hello_world():
    rec = db.get_or_404(User, 1)
    return render_template('index.html', user=rec)


@app.route('/users')
def users():
    user_recs = db.session.query(User).all()
    users = list(map(lambda rec: rec.__dict__, user_recs))
    return render_template('users.html', users=users)


@app.route('/user', methods=['GET', 'POST'])
def user():
    id = request.args.get('id')
    app.logger.info(f'Invoking user function using {request.method}')
    if request.method == 'GET':
        if id:
            user = User.query.get(id)
            return render_template('user_detail.html', user=user)
        else:
            return render_template('user_form.html')
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        user = User(
            first_name=first_name, 
            last_name=last_name, 
            username=username,
            email=email
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))

        