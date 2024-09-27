from flask import Flask,redirect,flash , url_for , render_template , request
from forms import RegistrationForm,MyForm

app = Flask(__name__)
app.secret_key='mindsecretkey'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form',methods=["GET","POST"])

def form():
    form= MyForm()
    if form.validate_on_submit():
        flash(f"Thanks for registering, {form.name.data}!",'success')
        return redirect('/dashboard')
    return render_template('form.html',form=form)

@app.route('/dashboard')

def dashboard():
    return render_template('dashboard.html')

if __name__== "__main__":
    app.run(debug= True)
