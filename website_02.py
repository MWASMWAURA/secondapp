from flask import Flask, render_template, redirect, flash, request
from forms import MyForm

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed to protect forms from CSRF attacks

# Route to display the form and handle submission
@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()  # Create an instance of the form
    
    if form.validate_on_submit():  # Check if form is submitted and validated
        name = form.name.data  # Retrieve the validated data
        email = form.email.data
        
        # Flash a success message
        flash(f"Form submitted successfully! Name: {name}, Email: {email}")
        
        # Redirect to the same page to clear the form after submission
        return redirect('/submit')
    
    return render_template('form.html', form=form)
# Define the route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']  # Grab the name from the form
    email = request.form['email']  # Grab the email from the form
    return f"Hello, {name}. Your email is {email}."
if __name__ =="__main__":
    app.run(debug=True)
