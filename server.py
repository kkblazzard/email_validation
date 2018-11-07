from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = 'kevin' # set a secret key for security purposes
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
    print("index")
    return render_template("index.html")

@app.route("/process", methods=['Get','POST'])
def add_to_db():
    is_valid = True		
    mysql = connectToMySQL("emails")
    query = "SELECT * FROM emails where email =%(e)s;"
    data ={
            "e": request.form["email"]
    }
    repeat = mysql.query_db(query, data) # assume True
    if repeat:
        flash("Email Address Already in Database!")
        is_valid=False
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Invalid email address!")
        is_valid=False
    if is_valid:  #if not '_flashes' in session.keys():	# there are no errors
    	# add user to database
        mysql = connectToMySQL("emails")
        query = "INSERT INTO emails(email, created_at) VALUES (%(e)s, NOW());"
        data ={
            "e": request.form["email"]
        }
        flash("Valid Email Address Successfully Added!")
        new_user_is=mysql.query_db(query, data)
        return redirect("/display")
    return redirect("/")
@app.route("/display")
def display():
    print("display")
    mysql = connectToMySQL("emails")
    all_users = mysql.query_db("SELECT * FROM emails;") 
    return render_template("database.html", users = all_users)

@app.route("/delete/<id>")
def delete_user_from_db(id):
    mysql = connectToMySQL('emails')
    print('delete')
    query = ("delete from emails where idemails =%(id)s;")
    data={"id":id}
    new_user_id = mysql.query_db(query,data)
    return redirect("/display")

if __name__ == "__main__":
    app.run(debug=True)