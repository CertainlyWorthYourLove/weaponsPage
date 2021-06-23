from flask import url_for, redirect, render_template, session, request, Flask, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weapons.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Weapons(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column('priceInHryvnia', db.Float, nullable=False)

    def __str__(self) :
        return f"Name: {self.name}; " \
               f"Price: {self.price}"


@app.route('/')
def home() :
    return render_template('index.html')


@app.route('/about')
def about() :
    weap = Weapons.query.first()
    return render_template('about.html', myweapon=weap)


@app.route('/login', methods=['POST', 'GET'])
def login() :
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            flash('Please fill all fields', 'error')
        session['name'] = username
        session['pass'] = password
    return render_template('login.html')


@app.route('/logout')
def logout() :
    session.pop('name', None)
    return render_template('logout.html')


@app.route('/weapons', methods=['POST', 'GET'])
def weapons() :
    if request.method == 'POST' :
        w_name = request.form['weapon_name']
        w_price = request.form['price']
        if w_name == '' or w_price == '' :
            flash('Please,enter data', 'error')
        elif not w_price.isnumeric() :
            flash('Enter price in numbers', 'error')
        else :
            w1 = Weapons(name=w_name, price=float(w_price))
            db.session.add(w1)
            db.session.commit()
            flash('Data added successfully', 'info')

    return render_template('weapons.html')


if __name__ == "__main__" :
    app.run(debug=True)
