#===========================================================
# Branch 26 NZART Website
# Connor Brennan
#-----------------------------------------------------------
# Nelson Amateur Radio Club (referred to as B26/ Branch 26) needs a public facing website to promote the hobby of 
# amateur radio to the public, giving them the opportunity to join the club.

# TODO sanitize inputs
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now
from flask_login         import *
from werkzeug.security import generate_password_hash, check_password_hash

# Configure Login Manager
login_manager = LoginManager()

# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests.
init_error(app)     # Handle errors and exceptions.
init_datetime(app)  # Handle UTC dates in timestamps.
login_manager.init_app(app) # Attaches login manager for use in app.


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        # Update to where approvals>2
        sql = "SELECT id, title, description, start_time, end_time, created_time, posted_by FROM activities "
        params = []
        result = client.execute(sql, params)
        activities = result.rows
        print(activities)

        return render_template("pages/home.jinja", activities=activities, user=current_user)


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja", user=current_user)



#-----------------------------------------------------------
# Contact page route
#-----------------------------------------------------------
@app.get("/contact/")
def contact():
    with connect_db() as client:
        sql = "SELECT callsign, name, email, phone, email_public, phone_public FROM members WHERE is_official_contact=1"
        params = []
        result = client.execute(sql, params)
        contacts = result.rows
        print(contacts)

        return render_template("pages/contact.jinja", contacts=contacts, user=current_user)




#-----------------------------------------------------------
# Hamcrams page route
#-----------------------------------------------------------
@app.get("/hamcram/")
def hamcram():
    return render_template("pages/hamcram.jinja", user=current_user)



#---------------------------------------------------------------------------
# Login Initialization
#---------------------------------------------------------------------------

# User class to handle data with UserMixin for base attributes and functions from flask-login
class User(UserMixin):
    def __init__(self, callsign, name, email, phone, email_public, phone_public, is_official_contact, can_post_public, password): #These params are passed when unpacking using * operator 
        self.id = callsign  # Id is used by flask_login
        self.callsign = callsign
        self.password = password
        self.name = name
        self.email = email
        self.phone = phone
        self.email_public = email_public
        self.phone_public = phone_public
        self.is_official_contact = is_official_contact
        self.can_post_public = can_post_public



@login_manager.user_loader
def get_user_by_callsign(callsign):
    with connect_db() as client:
        sql = "SElECT callsign, name, email, phone, email_public, phone_public, is_official_contact, can_post_public, password FROM members WHERE callsign=?"
        params = [callsign]
        result = client.execute(sql, params)

        # Check we dont have an invalid user
        if not result.rows: 
            return False

        print(result)
        member = result.rows[0]
        print(member)
        return User(*member)
        


######## TESTING ONLY
@app.get("/newuser/<string:callsign>/<string:password>")
@login_required
def newuser(callsign, password):
    password_hash = generate_password_hash(password)
    with connect_db() as client:
        sql = """INSERT INTO members 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        params = [callsign, "NAME", "EMAIL@COM", "1234321", 0, 0, 0, 0, password_hash]
        result = client.execute(sql,params)

    return "User added"
    



#-----------------------------------------------------------
# Login page route
#-----------------------------------------------------------
@app.get("/login/")
def login_page():
    return render_template("pages/login.jinja", user=current_user)



#-----------------------------------------------------------
# Logout page route
#-----------------------------------------------------------
@app.get("/logout/")
@login_required
def logout():
    logout_user()
    flash("Logout Successful", "info")
    return redirect("/") 




#-----------------------------------------------------------
# Processing User Login
#-----------------------------------------------------------
@app.post("/login/submit")
def process_login():
    # Login form data
    
    callsign =  request.form.get("callsign").upper()
    entered_password = request.form.get("password")
    user = get_user_by_callsign(callsign)

    if user and check_password_hash(user.password, entered_password):
        login_user(user, remember=True)
        flash("Login successful", "info")
        return redirect("/")

    flash("Incorrect Credentials", "error")
    return redirect("/login")
    


#-----------------------------------------------------------
# Activities page route (login required)
#-----------------------------------------------------------
@app.get("/activities/")
@login_required
def activities():
    # Get ze activities
    with connect_db() as client:
        sql = "SELECT * FROM activities ORDER BY start_time ASC"
        params = []
        activities = client.execute(sql, params)
    # Get ze resources
    with connect_db() as client:
        sql = "SELECT * FROM resources ORDER BY title ASC"
        params = []
        resources = client.execute(sql, params)

    

    return render_template("pages/activities.jinja", user=current_user, activities=activities, resources=resources)


#-----------------------------------------------------------
# New Activity (login required)
#-----------------------------------------------------------
@app.post("/activities/new")
@login_required
def new_activity():
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    title = request.form.get("title")
    description = request.form.get("description")
    resource = request.form.get("resource")
    approvable = request.form.get("is_approvable")

    # Sanitize 
    approvable = 1 if approvable else 0 

  
    with connect_db() as client:
        sql = "INSERT INTO activities (posted_by, start_time, end_time, title, description, resource, approvable) VALUES (?,?,?,?,?,?,?)"
        params = [current_user.callsign, start_time, end_time, title, description, resource, approvable]
        activities = client.execute(sql, params)
    

    

    return redirect("/activities")








#-----------------------------------------------------------
# Profile page route (login required)
#-----------------------------------------------------------
@app.get("/profile/")
@login_required
def profile():
    return render_template("pages/profile.jinja", user=current_user)





#---------------------------------------------------
# Profile update password (fresh login and old pass check required)
#---------------------------------------------------

@fresh_login_required
@app.post("/profile/update-password")
def update_password():
    old_password = request.form.get("old_password")
    new_pass_1 = request.form.get("new_pass_1")
    new_pass_2 = request.form.get("new_pass_2")

    # Validate the old password matches
    if not check_password_hash(current_user.password, old_password):
        flash("Old password is not correct", "error")
        return redirect("/profile")

    # Valid the new passwords match each other
    if new_pass_1 != new_pass_2:
        flash("New passwords do not match","error")
        return redirect("/profile")
        
    # Everything is satisfactory, update the users password
    with connect_db() as client:
        sql = "UPDATE members SET password=? WHERE callsign=?"
        params = [generate_password_hash(new_pass_1), current_user.id]
        client.execute(sql, params)


    flash("Password has been updated", "info")


    return redirect("/profile")


#---------------------------------------------------
# Profile update contact information (fresh login but no credentials check needed)
#---------------------------------------------------

@fresh_login_required
@app.post("/profile/update-info")
def update_info():
    email = request.form.get("email")
    phone = request.form.get("phone")
    email_visible = request.form.get("email_visible")
    phone_visible = request.form.get("phone_visible")
    # Dont bother to get name and callsign as these are display only

    #Ensure checkboxes are bool as 1 or 0 not None or On
    email_visible = 1 if email_visible else 0
    phone_visible = 1 if phone_visible else 0

    # Make phone int
    phone = int(phone)

    # Update infomation collected
    with connect_db() as client:
        sql = "UPDATE members SET email=?, phone=?, email_public=?, phone_public=? WHERE callsign=?"
        params = [email, phone, email_visible, phone_visible, current_user.id]
        client.execute(sql, params)


    flash("Info has been updated", "info")

    return redirect("/profile")





#-----------------------------------------------------------
# Resources page route (login required)
#-----------------------------------------------------------
@app.get("/resources/")
@login_required
def resources():
    with connect_db() as client:
        sql = "SELECT * FROM resources ORDER BY title ASC"
        params = []
        resources = client.execute(sql, params)
        # We may have to double check url formatting to fix for html

        return render_template("pages/resources.jinja", user=current_user, resources=resources)


#-----------------------------------------------------------
# Resource add(login required)
#-----------------------------------------------------------
@app.post("/resources/new")
@login_required
def add_resource():
    with connect_db() as client:
        sql = "INSERT title, url INTO resources VALUES (?,?)"
        params = [title, url]
        resources = client.execute(sql, params)

        return redirect("/resources")


