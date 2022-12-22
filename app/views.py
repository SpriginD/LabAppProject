from app import app, db, login

import os, sqlite3
from flask import flash, render_template, redirect, url_for, request
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from markupsafe import escape

from app.models import Feedback, User

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/pcs/")
def pc_list():
	db = sqlite3.connect(app.config["DATABASE"])
	cursor = db.cursor()
	
	rows = cursor.execute("SELECT * FROM pc WHERE NOT state='OK' OR NOT vstudio='OK'").fetchall()
	cursor.close()
	db.close()

	if rows:
		return render_template('pcs.html', rows=rows)
	else:
		"Error 404"

@app.route("/pcs/<int:id>")
def pc_info(id):
	return f"You're looking at the pc has {escape(id)} id."

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def check_error(fname, lname, desc, pcno, filename):
	if not (fname or lname):
		return "Lütfen adınızı ve soyadınızı giriniz."
	elif not fname:
		return "Lütfen adınızı giriniz."
	elif not lname:
		return "Lütfen soyadınızı giriniz."
	
	if len(desc) > 512:
		return "Açıklama çok uzun, lütfen 512 karakterden kısa tutun."

	if filename and not allowed_file(filename):
		return "Lütfen .png, .jpg, .jpeg ve .gif uzantıları haricinde bir dosya yüklemeyin."

	try:
		pcno = int(pcno)
		if not (0 < pcno and pcno < 63):
			return "PC Numarası 1 ila 63 arasında bir sayı olmalıdır.\nLütfen monitörün arkasındaki numarayı giriniz."
	except:
		return "PC Numarası 1 ila 63 arasında bir sayı olmalıdır.\nLütfen monitörün arkasındaki numarayı giriniz."

	return None

@app.route('/feedback')
def give_feedback():
	
	return render_template('feedback.html')

@app.route('/sent', methods=["GET", "POST"])
def sent():
	if request.method == "POST":
		fname = request.form.get('fname')
		lname = request.form.get('lname')
		desc = request.form.get('desc')
		pcno = request.form.get('pcno')
		
		file = request.files['file']
		
		error = check_error(fname, lname, desc, pcno, file.filename)

		if error:
			flash(error)
			return redirect(url_for('give_feedback'))

		newFeedback = None

		if file:
			filename = secure_filename(file.filename)
			filedata = file.read()
			
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

			if not os.path.isfile(file_path):
				with open(file_path, 'wb') as file:
					print(filename + " has been retrieved from database")
					file.write(filedata)
			
			newFeedback = Feedback(
				firstname = fname,
				lastname = lname,
				description = desc,
				filename = filename,
				filedata = filedata,
				pc_no = pcno
			)
		else:
			newFeedback = Feedback(
				firstname = fname,
				lastname = lname,
				description = desc,
				pc_no = pcno
			)
			
		db.session.add(newFeedback)
		db.session.commit()

		return redirect(url_for('sent'))

	return render_template('sent.html')

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		mail = request.form.get("mail")
		password = request.form.get("psw")

		print(mail, password, sep="\n")
		
		user = User.query.filter_by(mail=mail).first()
		print(user)

		if user and check_password_hash(user.password, password):
			print("logged")
			login_user(user, remember=user)
			return redirect(url_for('admin.index'))
		else:
			flash("Hatalı giriş!")
			return redirect(url_for('login'))
	else:
		return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

class MyAdminView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated
	
	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))

	@expose('/')
	def index(self):
		feedbacks = Feedback.query.order_by(Feedback.pc_no.asc())
		
		return self.render('admin/index.html', feedbacks=feedbacks)

class MyModelView(ModelView):
	form_columns = ["firstname", "lastname", "description", "pc_no"]