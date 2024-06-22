from flask import Flask, render_template, request, redirect, url_for, session, abort, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),)
    last_name = db.Column(db.String(80),)
    matriculation_number = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(15), unique=True)
    level = db.Column(db.String(15))
    barcode = db.Column(db.String(20), unique=True)
   

# Authentication function to check if a user is logged in
def is_authenticated():
    return 'user_id' in session

# Admin authentication function to check if an admin is logged in
def is_admin_authenticated():
    return 'admin' in session

@app.route('/')
def login():
    if is_authenticated():
        return redirect(url_for('index'))
    return render_template('login.html')



@app.route('/authenticate', methods=['POST'])
def authenticate():
    barcode = request.form.get('barcode')
    user = User.query.filter_by(barcode=barcode).first()
    if user:
        session['user_id'] = user.id
        return redirect(url_for('index'))
    else:
        flash('Please register before logging in.', 'error')
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if is_authenticated():
        user = User.query.get(session['user_id'])
        return render_template('index.html', user=user)
    return redirect(url_for('login'))

@app.route('/100level')
def level1():
    if is_authenticated():
        user = User.query.get(session['user_id'])
        return render_template('100level.html', user=user)
    return redirect(url_for('login'))

@app.route('/200level')
def level2():
    if is_authenticated():
        user = User.query.get(session['user_id'])
        return render_template('200level.html', user=user)
    return redirect(url_for('login'))

@app.route('/300level')
def level3():
    if is_authenticated():
        user = User.query.get(session['user_id'])
        return render_template('300level.html', user=user)
    return redirect(url_for('login'))

@app.route('/400level')
def level4():
    if is_authenticated():
        user = User.query.get(session['user_id'])
        return render_template('400level.html', user=user)
    return redirect(url_for('login'))

@app.route('/500level')
def level5():
    if is_authenticated():
        user = User.query.get(session['user_id'])
        return render_template('500level.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            barcode = request.form.get('barcode')

            # Check if a user with the same barcode already exists
            existing_user = User.query.filter_by(barcode=barcode).first()
            if existing_user:
                flash('User with this barcode is already registered.', 'error')
            else:
                email = request.form.get('email')
                phone = request.form.get('phone')
                level = request.form.get('level')
                matriculation_number = request.form.get('matriculation_number')
                
                new_user = User(first_name=first_name, last_name=last_name, barcode=barcode, matriculation_number=matriculation_number, email=email, phone=phone, level=level)
                db.session.add(new_user)
                db.session.commit()
                flash('User registered successfully!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if is_admin_authenticated():
        if request.method == 'POST':
            # Check if the form has a 'delete' field and a user ID
            if 'delete' in request.form:
                user_id_to_delete = int(request.form['delete'])
                user_to_delete = User.query.get(user_id_to_delete)
                if user_to_delete:
                    db.session.delete(user_to_delete)
                    db.session.commit()
        users = User.query.all()
        return render_template('admin.html', users=users)
    return redirect(url_for('login'))

@app.route('/admin_log', methods=['GET', 'POST'])
def admin_log():
    return redirect(url_for('admin_login'))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')

        # Check if the entered password is correct
        if password == '1234':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Access Denied', 'error')
            return redirect(url_for('login'))
            s
    return render_template('admin_login.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        def clear_session():
         session.clear()
        app.run(debug=True, port=8000)
