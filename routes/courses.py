from flask import render_template, request, \
    redirect, url_for, jsonify
from app import app
from app import db
from models.course import Course


@app.route('/courses')
def courses():
    course_recs = db.session.query(Course).all()
    courses = list(map(lambda rec: rec.__dict__, course_recs))
    # courses_list = map(lambda rec: rec.__dict__, course_recs)
    # courses = []
    # for course in courses_list:
    #     course.pop('_sa_instance_state')
    #     courses.append(course)
    return render_template('courses.html', courses=courses)
    # return jsonify({'courses': courses})


@app.route('/course', methods=['GET', 'POST'])
def course():
    if request.method == 'GET':
        course_id = request.args.get('course_id')
        if course_id:
            course = Course.query.get(course_id)
            form_action = request.args.get('action')
            if form_action == 'edit':
                return render_template('course_form.html', course=course)
            elif form_action == 'delete':
                db.session.delete(course)
                db.session.commit()
                return redirect(url_for('courses'))
            return render_template('course_detail.html', course=course)
        else:
            return render_template('course_form.html', course=None)
    elif request.method == 'POST':
        course_id = request.args.get('course_id')
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
