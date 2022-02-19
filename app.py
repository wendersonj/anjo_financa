from os import urandom

from flask import Flask, render_template, request, url_for, session
from sqlalchemy import and_, func
from sqlalchemy.exc import NoResultFound
from werkzeug.utils import redirect
from db import db, sql_uri
from models.bill_model import Bill, sum_all_bills
from models.user_model import User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = sql_uri
db.init_app(app)

app.secret_key = urandom(24)


@app.route('/bills/add', methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('create_bill.html')
    else:
        db.session.add(Bill(description=request.form['description'], final_date=request.form['final_date'],
                            initial_date=request.form['initial_date'], value=request.form['bill_value'],
                            user_id=session.get('user_id')))
        db.session.commit()
        return redirect(url_for('list_bills'))


@app.route('/bills/list', methods=["GET"])
def list_bills():
    user_id = session['user_id']
    bills = Bill.query.filter_by(user_id=user_id)
    return render_template('list_bills.html', bills=bills)


@app.route('/bills/delete/<int:bill_id>')
def remove_bill(bill_id):
    bill = Bill.query.get(bill_id)
    db.session.delete(bill)
    db.session.commit()
    return redirect(url_for('list_bills'))


@app.route('/bills/edit/<int:bill_id>', methods=["GET", "POST"])
def edit(bill_id):
    bill = Bill.query.get(bill_id)
    if request.method == "GET":
        return render_template("edit_bill.html", bill=bill)
    else:
        bill.description = request.form['description']
        bill.set_initial_date(request.form['initial_date'])
        bill.set_final_date(request.form['final_date'])
        bill.value = request.form['bill_value']
        print(bill)
        db.session.commit()
        return redirect(url_for('list_bills'))


@app.route("/bills/generate_report/", methods=["GET", "POST"])
def generate_report():
    if request.method == "POST":
        initial_date = request.form.get('initial_date', None)
        final_date = request.form.get('final_date', None)
        print(initial_date)
        print(final_date)
        bills = db.session.query(Bill).filter(and_(
            func.date(Bill.initial_date) >= initial_date,
            func.date(Bill.final_date) <= final_date))

        return render_template('report.html', bills=bills.all(), total_value=sum_all_bills(bills),
                               initial_date=initial_date,
                               final_date=final_date)

    else:
        return render_template('generate_report.html')


@app.route('/bills')
def bills_index():
    if session.get('user_id', None) is not None:
        return render_template('bills_index.html')
    else:
        return redirect(url_for('login'))


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('user_id', None) is not None:
        return redirect(url_for('bills_index'))

    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.form)
        try:
            temp_user: User = User.query.filter_by(username=request.form['username']).one()
        except NoResultFound:
            return 'usuario nao encontrado'

        if temp_user.password != request.form['password']:
            return 'senha incorreta <a href="/login"> voltar</a>'
        else:
            session['user_id'] = temp_user.id
            print(session['user_id'])
        return redirect(url_for('bills_index'))


@app.route("/logout")
def logout():
    try:
        session.pop('user_id')
    except KeyError:
        return redirect(url_for('login'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.run()
