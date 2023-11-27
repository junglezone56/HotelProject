from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = '4321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
db = SQLAlchemy(app)

class CustomerBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(80), nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    check_in = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    housekeeping = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<CustomerBooking %r>' % self.guest_name

USERNAME = 'erik'
PASSWORD = '101'

@app.route('/')
def base():
    is_authenticated = session.get('is_authenticated', False)
    return render_template('base.html', is_authenticated=is_authenticated)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['is_authenticated'] = True
            return redirect(url_for('base'))
        else:
            return 'Login Failed'
    return render_template("login.html", is_authenticated=False)

@app.route('/Bookings')
def bookings():
    if not session.get('is_authenticated', False):
        return redirect(url_for('login'))

    all_bookings = CustomerBooking.query.all()  # Fetch all booking records from the database
    return render_template('Bookings.html', bookings=all_bookings)  # Pass the data to the template



@app.route('/CustomerBookings', methods=['GET', 'POST'])
def customer_bookings():
    if not session.get('is_authenticated', False):
        return redirect(url_for('login'))

    if request.method == 'POST':
        guest_name = request.form['guest_name']
        room_number = request.form['room_number']
        check_in = datetime.strptime(request.form['check_in'], '%Y-%m-%dT%H:%M')
        check_out = datetime.strptime(request.form['check_out'], '%Y-%m-%dT%H:%M')
        housekeeping = 'housekeeping' in request.form

        new_booking = CustomerBooking(
            guest_name=guest_name,
            room_number=room_number,
            check_in=check_in,
            check_out=check_out,
            housekeeping=housekeeping
        )

        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('customer_bookings'))

    all_customer_bookings = CustomerBooking.query.all()
    return render_template('CustomerBookings.html', bookings=all_customer_bookings)

@app.route('/logout')
def logout():
    session.pop('is_authenticated', None)
    return redirect(url_for('base'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
