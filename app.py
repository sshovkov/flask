from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5231/postgres'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def repr(self):
        return '<Name %r>' % self.first_name
    
    def __init__(self, first_name, last_name, email, age):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
    
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home_screen():
    return render_template('home_screen.html')


@app.route('/all', methods=['GET'])
def show_all():
    return render_template('all_people.html', people=Person.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new_person():
    if request.method == 'POST':
        if not request.form['first_name'] or not request.form['last_name'] or not request.form['email'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            new_person = Person(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['age'])
            db.session.add(new_person)
            db.session.commit()

            flash('Form added successfully!')
            return redirect(url_for('show_all'))
    return render_template('add_person.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_form():
    if request.method == 'POST':
        checked_people = request.form.getlist('form_checkbox')
        for person_id in checked_people:
            person = Person.query.get(person_id)
            if person:
                db.session.delete(person)
        
        db.session.commit()
        
        flash('Form(s) deleted successfully!')
        return redirect(url_for('show_all'))
    return render_template('delete_person.html', people=Person.query.all())