from flask import Flask,redirect,flash , url_for , render_template , request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,MyForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key='mindsecretkey'

# Set up the SQLite database

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db= SQLAlchemy(app)
# Create a model for the user registration data
class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(150),nullable =False )
    email =db.Column(db.String(150),nullable=False,unique =True)
    password=db.Column(db.String(10),nullable=False)

    def __repr__(self):
        return f"User('{self.name}','{self.email}')"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form',methods=["GET","POST"])

def form():
    form= MyForm()

    if form.validate_on_submit():
        try:
            user = User(name=form.name.data,email=form.email.data,password=form.password.data)
            db.session.add(user) # Add the new user to the database session
            db.session.commit() # Commit the session to save the user in the database

            flash(f"Thanks for registering, {form.name.data}!",'success')
            if form.email.data == "jamesmwauramwas@gmail.com" and form.password.data == "admin":
                return redirect('/dashboard')
            else:
                return redirect('/login')
        except IntegrityError:
            db.session.rollback() #Rollback the session to prevent the app from crashing
            flash('Email already exists. Please log in.','danger')
            return redirect('/login') #Redirect the login page if email is already registered
    return render_template('form.html',form=form)

@app.route('/dashboard')

def dashboard():
    users =User.query.all() #Query all users from the database to display
    return render_template('dashboard.html',users = users)


@app.route('/login')
def login():
    return render_template('login.html')

if __name__== "__main__":
    app.run(debug= True)
