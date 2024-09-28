from flask import Flask, redirect, flash, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from sqlalchemy.exc import IntegrityError
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.secret_key = 'mindsecretkey'

# Set up the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jamesmwauramwas@gmail.com'
app.config['MAIL_PASSWORD'] = 'welcomejames1'
app.config['MAIL_DEFAULT_SENDER'] = 'jamesmwauramwas@gmail.com'

mail = Mail(app)

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Create a model for the user registration data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # Increased length for hashed passwords
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('You are already registered. Please log in.', 'info')
                return render_template('message.html', redirect_url=url_for('login'))

            user = User(name=form.name.data, email=form.email.data, password=form.password.data)  # Consider hashing the password
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            # Send email logic here

            flash(f"Thanks for registering, {form.name.data}!", 'success')

            session['user_id'] = user.id
            session['is_admin'] = (user.email == "jamesmwauramwas@gmail.com" and user.password == "adminroot")

            return redirect(url_for('dashboard') if session['is_admin'] else url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', users=users)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt=app.secret_key)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)  # Ensure this function is defined
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.is_verified = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.password == form.password.data:  # Consider checking hashed password
                session['user_id'] = user.id
                session['is_admin'] = (user.email == "jamesmwauramwas@gmail.com" and user.password == "adminroot")
                flash("Welcome back, Admin!" if session['is_admin'] else "Welcome back!", "success")
                return redirect(url_for('dashboard' if session['is_admin'] else 'home'))
            else:
                flash("Incorrect password. Please try again.", "danger")
                return render_template('message.html', redirect_url=url_for('login'))
        else:
            flash("Email not found. Please register.", "danger")
            return render_template('message.html', redirect_url=url_for('register'))
    return render_template('login.html', form=form)

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
