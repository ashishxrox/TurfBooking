import sqlite3
from flask import Flask, render_template, request,redirect,session,flash
import os
import uuid
import razorpay
from datetime import date

day = date.today()


app = Flask(__name__)
app.secret_key = os.urandom(24)

DATA = './database/database.db'
conn = sqlite3.connect(DATA, check_same_thread=False)
c = conn.cursor()
name = {}



#*****HOME*****
@app.route("/")
def home():

	global day

	# DELETE ALL OLD ENTRIES
	c.execute(''' DELETE FROM booking WHERE bdate < '{}' '''.format(day))
	conn.commit()
	#DELETE ALL OLD SLOTS
	c.execute(''' DELETE FROM booking WHERE bdate < '{}' '''.format(day))
	conn.commit



	if 'user_id' in session:
		return redirect('/landing')
	elif 'aname' in session:
		return redirect('/admin')
	else:
		return render_template('home.html')

@app.route('/<string:page_name>')
def html_page(page_name):
	if 'user_id' not in session:
		return redirect('/')


#*****LOGIN_PAGE*****
@app.route("/login")
def login():
	if 'user_id' in session:
		return redirect('/landing')
	else:
		return render_template('login.html')

#*****LANDING*****

@app.route("/landing")
def landing():

	slot = []
	if 'bdate' in session:
		bdate = session.get('bdate')
		c.execute(''' SELECT intime, outtime FROM slot WHERE bdate == '{}' '''.format(bdate))
		slot = c.fetchall()

	if 'user_id' in session:
		name = session.get('user_id')
		c.execute(''' SELECT * FROM booking WHERE username == '{}' '''.format(name))
		data = sorted(c.fetchall(), key = lambda x:x[1])
		

		return render_template('landing.html', u_name = name, data = data,today = day, slot = slot)
	else:
		return redirect('/')

# *****CHECKTIME*****

def genTime():
	times1 = []
	times2 = []

	for i in range(0,24):
		if i == 0:
			hour = i
			p = 'PM'
		elif i <= 12:
			hour = i
			p = 'AM'
		else:
			hour = i-12
			p = 'PM'
		for minutes in range(0,60,60):
			times1.append('{:02d}:{:02d} {}'.format(hour, minutes, p))


	for i in range(1,24):
		if i <= 12:
			hour = i
			p = 'AM'
		else:
			hour = i-12
			p = 'PM'
		for minutes in range(0,60,60):
			times2.append('{:02d}:{:02d} {}'.format(hour, minutes, p))

	times2.append('00:00 PM')
	times = tuple(zip(times1, times2))

	return times



@app.route("/checkTime", methods = ['POST'])
def checkTime():
	times = genTime()
	bdate = request.form.get('bdate')
	session['bdate'] = bdate
	flash(times)
	c.execute(''' SELECT intime, outtime FROM booking WHERE bdate == '{}' '''.format(bdate))
	val = c.fetchall()
	return redirect('landing')
	# return str(times)



#*****LOGIN*****
@app.route("/login_validation", methods = ['POST'])
def login_validation():
	username = request.form.get('username')
	password = request.form.get('password')

	c.execute(''' SELECT  * FROM user WHERE username == '{}' AND password == '{}' '''.format(username, password))


	users = c.fetchall()
	if len(users)>0:

		session['user_id'] = users[0][0]
		return redirect('landing')
	if len(users)==0:
		flash("Invalid username or password!(If new user please register yourself!)")
		return redirect('login')



#*****REGISTER*****
@app.route('/add_user', methods = ['POST'])
def add_user():
	username = request.form.get('uusername')
	email = request.form.get('uemail')
	password = request.form.get('upassword')

	c.execute(''' SELECT username FROM user''')
	names = c.fetchall()
	try:

		c.execute(''' INSERT INTO user(username, email, password) VALUES ('{}','{}','{}') '''.format(username, email, password))

		conn.commit()

		c.execute(''' SELECT * FROM user WHERE username == '{}' '''.format(username))

		myuser = c.fetchall()

		session['user_id'] = myuser[0][0]
		return redirect('/landing')
	except:
		flash("Username already in use. Try something else!") 
		return redirect('/login')

#*****LOGOUT*****
@app.route('/logout')
def logout():
	if 'user_id' in session:
		session.pop('user_id')
		return redirect('/')
	return redirect('/')


#*****ADMIN*****
@app.route('/ad_log')
def ad_log():
	return render_template('adminLog.html')



@app.route('/admin')
def admin():
	c.execute(''' SELECT * FROM booking WHERE bdate != '{}' '''.format(day))
	ad_data = c.fetchall()
	c.execute(''' SELECT * FROM booking WHERE bdate == '{}' '''.format(day))
	today = c.fetchall()


	

	if 'aname' in session:
		return render_template('admin.html', ad = sorted(ad_data, key = lambda x:x[1]), to = sorted(today, key = lambda x:x[1]))
	else:
		return redirect('/ad_log')


@app.route('/admin_validation', methods = ['POST'])
def admin_validation():
	aname = request.form.get('ausername')
	apassword = request.form.get('apassword')
	session['aname'] = aname
	if aname == 'BOSS' and apassword == 'boss':
		return redirect('/admin')
	else:
		return redirect('/ad_log')

@app.route('/ad_logout')
def ad_logout():
	if 'aname' in session:
		session.pop('aname')
		return redirect('/')

	return redirect('/')


#*****BOOKING*****
def generate():

	n = str(uuid.uuid4().int)
	n = list(n)
	n = n[:10]
	return int(''.join(n))


@app.route('/book', methods = ['POST'])
def book():

	username = session.get('user_id')
	bdate = session.get('bdate')

	op1 = request.form.getlist('checkOne')
	if len(op1) == 0:
		return redirect('/landing')

	# return str(op1)
	in_time = op1[0][2:10]
	out_time = op1[-1][14:-2]
	amt = len(op1)

	
	session['in_time'] = in_time
	session['outtime'] = out_time
	session['amount'] = amt*100
	session['slots'] = op1

	return redirect('/pay')


	if username == None:
		return redirect('/')
# *****PAYMENT INTEGRATION*****
@app.route('/pay')
def pay():
	try:
		in_time = session.get('in_time')
		out_time = session.get('outtime')
		amount = session.get('amount')
		bdate = session.get('bdate')
		data = []
		data.append(bdate)
		data.append(in_time)
		data.append(out_time)
		data.append(amount)

		client = razorpay.Client(auth = ("rzp_test_EOM7ebxof83w94", "DbTkjfXRTq4auOCroQtY6EUq"))
		payment = client.order.create({'amount': int(amount)*100, 'currency': 'INR', 'payment_capture': '1'})
		return render_template('payment.html', data = data, payment = payment)
	except:
		return redirect('/')

@app.route('/success', methods = ['POST'])
def success():
	book_No = generate() 
	in_time = session.get('in_time')
	out_time = session.get('outtime')
	amount = session.get('amount')
	bdate = session.get('bdate')
	name = session.get('user_id')
	slots = session.get('slots')

	res = []
	for time in slots:
		c.execute(''' INSERT INTO slot(bookNo, bdate, intime, outtime)
			VALUES
			('{}','{}', '{}', '{}')'''.format(book_No, bdate, time[2:10], time[14:-2]))
	
	conn.commit()

	c.execute(''' INSERT INTO booking(bookNo, bdate, intime, outtime, username, amount, paid)
			VALUES
			({},'{}', '{}', '{}', '{}',{},'{}')'''.format(book_No, bdate, in_time, out_time, name,amount,'YES'))
	conn.commit()
	return redirect('/landing')



# *****CANCELATION*****
@app.route('/cancel', methods = ['POST'])
def cancel():
	number = request.form.get('cancel')
	
	c.execute(''' DELETE FROM slot WHERE bookNo == {} '''.format(number))
	conn.commit()
	
	c.execute(''' DELETE FROM booking WHERE bookNo == {}'''.format(number))

	conn.commit()

	return redirect('/landing')


# *****SEARCH*****
@app.route('/search', methods = ['POST'])
def search():
	number = request.form.get('search')

	c.execute(''' SELECT * FROM booking WHERE bookNo == {}'''.format(number))
	res = c.fetchall()
	if len(res) == 0:
		return redirect('/admin')
	else:
		c.execute(''' SELECT * FROM booking WHERE bookNo =={} '''.format(number))
		bk = c.fetchall()

		flash(list(bk))
		return redirect('/admin')







