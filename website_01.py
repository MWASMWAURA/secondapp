from flask import Flask, render_template, url_for , request,redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit',methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']

    if name and email:
        print(f"Name:{name},Email:{email}")
        return f"Thank you, {name}.We have received your email ({email})."
    else:
        return "Error: All form fields are required."
if __name__ == '__main__':
    app.run(debug=True)

