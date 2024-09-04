from flask import Flask, redirect, render_template, url_for, request, flash, session, send_file
from functools import wraps
from datetime import datetime
from datetime import date
from app import db, User, Book, Section, Mybooks, Feedback
import os
from flask import send_from_directory
import subprocess


from app import app

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SECRET_KEY"] = "SDKVBNSDV98SDHV98H"
app.config["UPLOAD_FOLDER"] = "uploads"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

with app.app_context():
    db.create_all()

def login_required(function):
    @wraps(function)
    def inner_func(*args, **kargs):
        if 'user_id' not in session:
            flash('Please Login First')
            return redirect('/login')
        return function(*args, **kargs)
    return inner_func

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':
            return """<h1>Please Provide a valid input !</h1>
            <a href="/login">Click here to Login</a>"""
        user = User.query.filter_by(username=username).first()
        if not user:
            return """<h1>User does not exist</h1>
                <a href="/login">Click here to login</a>"""
        elif not user.check_password(password):
            return """<h1>User does not exist</h1>
                <a href="/login">Click here to login</a>"""
        else:
            session['user_id'] = user.id
            return redirect(url_for('user_dashboard', user=user))
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':
            return """<h1>Please Provide a valid input !</h1>
            <a href="/register">Click here to register</a>"""
        else:
            try:
                user = User(username=username, password=password, name=name)
                db.session.add(user)
                db.session.commit()
                flash('user registration sucessfull')
            except:
                return """<h1>Username is already used ! </h1>
            <a href="/register">Click here to register</a>"""
        return render_template('login.html')
    return render_template('register.html')

@app.route('/admin-login', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':
            return """<h1>Please Provide a valid input !</h1>
            <a href="admin-login.html">Click here to login again</a>"""
        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return "You are not admin"
    return render_template('admin-login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin-dashboard.html', Section=Section.query.all())

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/profile', methods=['POST','GET'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user = user)

@app.route('/section/add_section', methods=['POST', 'GET'])
def add_section():
    if request.method == 'POST':
        section_name = request.form.get('section_name')
        date_object = request.form.get('date_created')
        date_created = datetime.strptime(date_object, "%Y-%m-%d").date()
        description = request.form.get('description')
        if section_name == '' or date_created == "" or description == '':
            return """<h1> Invalid input</h1>
            <a href="/section/add_section">Click here to try again<a>"""
        else:
            section = Section(section_name=section_name, date_created=date_created, description=description)
            db.session.add(section)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
    return render_template('section/add_section.html')

@app.route('/section/<int:id>/edit_section', methods=['POST', 'GET'])
def edit_section(id):
    if request.method == 'POST':
        name = request.form.get('section_name')
        date_object = request.form.get('date_created')
        date_created = datetime.strptime(date_object, "%Y-%m-%d").date()
        description = request.form.get('description')
        if name == '' or date_created == '' or description == '':
            return """<h1> Invalid input</h1>
            <a href="/section/add_section">Click here to try again<a>"""
        else:
            section = Section.query.get(id)
            section.section_name = name
            section.date_created = date_created
            section.description = description
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
    return render_template('section/edit_section.html', section=Section.query.filter_by(id=id).first())

@app.route('/section/<int:id>/delete_section', methods=['POST', 'GET'])
def delete_section(id):
    if request.method == 'POST':
        try:
            section = Section.query.get(id)
            db.session.delete(section)
            db.session.commit()
        except:
            return """<h1>You can only delete a section when it is empty</h1>
            <a href="/admin-dashboard">Go to admin dashboard<a>"""
        return redirect(url_for('admin_dashboard'))
    return render_template('section/delete_section.html', section=Section.query.filter_by(id=id).first())

@app.route('/section/<int:id>/add_book', methods=['POST', 'GET'])
def add_book(id):
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        section_id = id
        content = request.form.get('content')
        author = request.form.get('author')
        upload_pdf = request.files['file']
        if upload_pdf.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_pdf.filename)
            upload_pdf.save(filepath)
        if book_name == '' or content == '' or author == '':
            return """<h1> Invalid input</h1>
            <a href="{{url_for('add_book', id = section.id)}}">Click here to try again<a>"""
        else:
            book = Book(book_name=book_name, section_id=section_id, content=content, author=author, pdf_path=upload_pdf.filename)
            db.session.add(book)
            db.session.commit()
            # return redirect(url_for('open_section', section=Section.query.filter_by(id=id).first(),
            #                         Book=Book.query.all()))
            return redirect(url_for('open_section',id=section_id, filename=upload_pdf.filename))
    return render_template('section/add_book.html', section=Section.query.filter_by(id=id).first())

@app.route('/open/<int:id>')
def open(id):
    #print(id)
    book = Book.query.filter_by(id=id).first()
    book_path = book.pdf_path
    return send_file('uploads\\{}'.format(book_path))

@app.route('/section/<int:id>/open_section')
def open_section(id):
    return render_template('section/open_section.html', section=Section.query.filter_by(id=id).first(),
                           Book=Book.query.all())

@app.route('/section/<int:id>/edit_book', methods=['POST','GET'])
def edit_book(id):
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        content = request.form.get('content')
        author = request.form.get('author')
        if book_name == '' or content == '' or author == '':
            return """<h1> Invalid input</h1>
            <a href="{{url_for('add_book', id = section.id)}}">Click here to try again<a>"""
        else:
            book = Book.query.get(id)
            book.book_name = book_name
            book.content=content
            book.author=author
            db.session.commit()
            return redirect(url_for('open_section', id=book.section_id))
    return render_template('section/edit_book.html', book=Book.query.filter_by(id=id).first())

@app.route('/section/<int:id>/delete_book', methods=['POST','GET'])
def delete_book(id):
    if request.method == 'POST':
        book=Book.query.filter_by(id=id).first()
        section_id = book.section_id
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('open_section', id=section_id))
    return render_template('section/delete_book.html', book=Book.query.filter_by(id=id).first())

@app.route('/issue_books', methods=['POST','GET'])
def issue_books():
    return render_template('issue_books.html', mybooks=Mybooks.query.filter_by(status='Pending'), issuedbooks=Mybooks.query.filter_by(status='Issued'))

@app.route('/reject_issue_request/<int:book_id>', methods=['POST','GET'])
def reject_issue_request(book_id):
    mybooks=Mybooks.query.filter_by(book_id=book_id).first()
    if not mybooks:
        return redirect(url_for('issue_books'))
    db.session.delete(mybooks)
    db.session.commit()
    return redirect(url_for('issue_books'))

@app.route('/accept_issue_request/<int:book_id>', methods=['POST','GET'])
def accept_issue_request(book_id):
   issue_object = request.form.get('issue_date')
   issue_date = datetime.strptime(issue_object, "%Y-%m-%d").date()
   status = 'Issued'
   if issue_object == '':
       return "<h1>Enter a valid Issue Date</h1>"
   mybooks = Mybooks.query.get(book_id)
   #print(mybooks)
   mybooks.issue_date=issue_date
   mybooks.status=status
   db.session.commit()
   return redirect(url_for('issue_books'))

@app.route('/revoke/<int:book_id>', methods=['POST', 'GET'])
def revoke(book_id):
    current_date = datetime.now().date()
    revoke_books=Mybooks.query.filter_by(book_id=book_id).first()
    time_revoke=Mybooks.query.filter_by(status='Issued').all()
    for i in time_revoke:
        if i.return_date < current_date:
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('issue_books'))
    if not revoke_books:
        return redirect(url_for('issue_books'))
    db.session.delete(revoke_books)
    db.session.commit()
    return redirect(url_for('issue_books'))

#------------------------------------------------user pages------------------------------------------------#


@app.route('/user-dashboard', methods=['POST','GET'])
@login_required
def user_dashboard():
    user = User.query.get(session['user_id'])
    user_id=session['user_id']
    book_count = Mybooks.query.filter_by(user_id=user_id).count()
    if request.method == 'GET':
        parameter=request.args.get('param')
        search=request.args.get('search')
        parameters={
            'section':'Section',
            'book':'Book',
            'author':'Author'
        }
        #print(search)
        #print(book_count)
        if not parameter or not search:
            return render_template('user-dashboard.html', user = user, Section=Section.query.all(), 
                                   parameters=parameters, book_count=book_count)
        if parameter == 'Section':
            sections = Section.query.filter(Section.section_name.like('%' + search + '%')).all()
            return render_template('user-dashboard.html', user=user, Section=sections, value=search,
                                   parameter=parameter, parameters=parameters, book_count=book_count)
        if parameter == 'Book':
            return render_template('user-dashboard.html', user=user, Section=Section.query.all(),
                                    book_search=search, value=search, parameter=parameter, parameters=parameters, book_count=book_count)
        if parameter == 'Author':
            return render_template('user-dashboard.html', user=user, Section=Section.query.all(),
                                    author_search=search, value=search, parameter=parameter, parameters=parameters, book_count=book_count)
    #return redirect(url_for('user_dashboard', user = user, Section=Section.query.all()))
    return render_template('user-dashboard.html', user = user, Section=Section.query.all(),parameters=parameters, book_count=book_count)

@app.route('/add_to_pending_request/<int:book_id>', methods=['POST','GET'])
@login_required
def add_to_pending_request(book_id):
    user=session['user_id']
    bookid=book_id
    return_object=request.form.get('return_date')
    return_date = datetime.strptime(return_object, "%Y-%m-%d").date()
    book_count = Mybooks.query.filter_by(user_id=user).count()

    '''
    if book_count > 4:
        return "<h1>cannot add more than 5 books !</h1>"
        '''
    #print(book_count)
    #"<h1>Cannot add more than 5 books!</h1>"
    #if Mybooks.query.filter_by(user_id=user, book_id=book_id).count() > 5:
    #    return "Cannot add more than 5 books"
    if return_object == '':
        return "<h1>Please enter a valid return date</h1>"
    if Mybooks.query.filter_by(user_id=user, book_id=book_id).first():
        return "<h1>Cannot add this book. This book is allready added!</h1>"
    mybooks=Mybooks(user_id=user, book_id=bookid, return_date=return_date)
    db.session.add(mybooks)
    db.session.commit()
    return redirect(url_for('user_dashboard', user=user, book_count=book_count))

@app.route('/pending_request')
@login_required
def pending_request():
    book_id = Mybooks.query.filter_by(status='Issued').first()
    feedbacks = Feedback.query.filter_by(user_id=session['user_id']).all()
    feedback_ids = []
    for feedback in feedbacks:
        feedback_ids.append(feedback.book_id)
    return render_template('pending_request.html', user=User.query.get(session['user_id']),
                            carts=Mybooks.query.filter_by(user_id=session['user_id'], status='Pending').all(),
                            issued_books_user=Mybooks.query.filter_by(user_id=session['user_id'], status='Issued').all(),
                            feedbacks_id=feedback_ids)

@app.route('/delete_from_pending_request/<int:book_id>', methods=['POST','GET'])
@login_required
def delete_from_pending_request(book_id):
    user=session['user_id']
    mybooks=Mybooks.query.filter_by(user_id=session['user_id'], book_id=book_id).first()
   # print(mybooks)
    if not mybooks:
        flash('book does not exist in your cart')
        return redirect(url_for('pending_request'))
    db.session.delete(mybooks)
    db.session.commit()
    return redirect(url_for('pending_request'))

@app.route('/return_book/<int:book_id>', methods=['POST','GET'])
@login_required
def return_book(book_id):
    user=session['user_id']
    mybooks=Mybooks.query.filter_by(user_id=session['user_id'], book_id=book_id).first()
    feedback_count = Feedback.query.filter_by(user_id=user, book_id=book_id).count()
    if not mybooks:
        return redirect(url_for('pending_request'))
    db.session.delete(mybooks)
    db.session.commit()
    return redirect(url_for('pending_request'))

@app.route('/open_book/<int:book_id>')
@login_required
def open_book_user(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book_path = book.pdf_path
    return send_file('uploads\\{}'.format(book_path))

@app.route('/feedback/<int:book_id>', methods=['POST','GET'])
@login_required
def feedback(book_id):
    if request.method == 'POST':
        user=session['user_id']
        feedback = request.form.get('feedback')
        feedback_count = Feedback.query.filter_by(user_id=user, book_id=book_id).count()
        #if feedback_count > 0:
        #    return "<h1>Feedback already given</h1>"
        feedback = Feedback(user_id=user, book_id=book_id, feedback=feedback)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('pending_request'))
    return render_template('feedback.html')

@app.route('/view_feedback/<int:book_id>', methods=['POST', 'GET'])
@login_required
def view_feedback(book_id):
    feedbacks = Feedback.query.filter_by(book_id=book_id).all()
    bookname = Book.query.filter_by(id=book_id).first()
    return render_template('view_feedback.html', feedbacks=feedbacks, user_id=session['user_id'], bookname=bookname)


if __name__ == "__main__": 
    app.run(debug=True)