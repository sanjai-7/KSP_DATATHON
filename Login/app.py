from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import secrets

app = Flask(__name__)
# Generate a secure random secret key
app.secret_key = secrets.token_hex(16)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['school']  # Replace 'your_database_name' with your actual database name
users_collection = db['ksp']  # Assuming you have a collection named 'users'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    # Check if user exists in MongoDB
    user = users_collection.find_one({'username': username, 'password': password})

    if user:
        session['username'] = username
        # If user exists, redirect to the homepage
        return redirect(url_for('homepage'))
    else:
        # If user doesn't exist, redirect back to the login page with an error message
        return redirect(url_for('login'))

@app.route('/homepage')
def homepage():
    # Retrieve the username from the session
    username = session.get('username')
    return render_template('home.html', username=username)

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session data
    session.pop('username', None)
    # Redirect to the login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
