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

# Login functionality
from flask_login         import *
from werkzeug.security import generate_password_hash, check_password_hash

# SMTP functionality
from smtplib            import SMTP
from dotenv import load_dotenv
from os import getenv
from secrets import token_urlsafe
from email.mime.text import MIMEText
from email.utils import formataddr

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
        # Only want activities that have had at least 2 approvals
        sql = """
        SELECT 
            id, title, description, start_time, end_time, 
            created_time, posted_by, location
            FROM activities
            WHERE id IN (   
                SELECT
                activity FROM approvals
                GROUP BY activity
                HAVING COUNT(*) > 1
            );
        """
        params = []
        result = client.execute(sql, params)
        activities = result.rows
        
        # Get approvals for display with activities
        sql = "SELECT activity, approver FROM approvals"
        params = []
        result = client.execute(sql, params)
        approvals = result.rows

        return render_template("pages/home.jinja", activities=activities, approvals=approvals, user=current_user)


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
    def __init__(self, callsign, name, email, phone, email_public, phone_public, is_official_contact, password, is_committee): #These params are passed when unpacking using * operator 
        self.id = callsign  # Id is used by flask_login
        self.callsign = callsign
        self.password = password
        self.name = name
        self.email = email
        self.phone = phone
        self.email_public = email_public
        self.phone_public = phone_public
        self.is_official_contact = is_official_contact
        self.is_committee = is_committee



@login_manager.user_loader
def get_user_by_callsign(callsign):
    with connect_db() as client:
        sql = "SElECT callsign, name, email, phone, email_public, phone_public, is_official_contact, password, is_committee FROM members WHERE callsign=?"
        params = [callsign]
        result = client.execute(sql, params)

        # Check we dont have an invalid user
        if not result.rows: 
            return False

        print(result)
        member = result.rows[0]
        print(member)
        return User(*member)
        




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

    # Get the approvals   
    with connect_db() as client:
        sql = "SELECT id, activity, approver FROM approvals"
        params = []
        approvals = client.execute(sql, params)
        approvals_by_activity = {}
        for approval in approvals:
            activity_id = int(approval["activity"])
            if activity_id not in approvals_by_activity:
                approvals_by_activity[activity_id] = []
            approvals_by_activity[activity_id].append(approval["approver"])
            print(approvals_by_activity)
    return render_template("pages/activities.jinja", user=current_user, activities=activities, resources=resources, approvals_by_activity=approvals_by_activity)


#-----------------------------------------------------------
# Member approving activity route (login required)
#-----------------------------------------------------------
@app.get("/add-approval/<int:activity>")
@login_required
def add_approval(activity):
    callsign = current_user.callsign
    with connect_db() as client:
        sql = "SELECT posted_by FROM activities WHERE id=?"
        params = [activity]
        activity_by = client.execute(sql, params)

        # make sure user is not approving own activity (forbidden)
        if (current_user.callsign):
            return redirect("/activities/"), 403


        sql = "INSERT INTO approvals (activity, approver) VALUES (?,?)"
        params = [activity, current_user.callsign]
        client.execute(sql, params)

  
  
    return redirect("/activities/")



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
    location = request.form.get("location")
    resource = request.form.get("resource")
    approvable = request.form.get("is_approvable")

    # Sanitize 
    approvable = 1 if approvable else 0 
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)

  
    with connect_db() as client:
        sql = "INSERT INTO activities (posted_by, start_time, end_time, title, description, location, resource, approvable) VALUES (?,?,?,?,?,?,?,?)"
        params = [current_user.callsign, start_time, end_time, title, description, location, resource, approvable]
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
    title = request.form.get("title")
    url = request.form.get("url")
    with connect_db() as client:
        sql = "INSERT INTO resources (title, url)VALUES (?,?)"
        params = [title, url]
        resources = client.execute(sql, params)

        return redirect("/resources")


#-----------------------------------------------------------
# Administration page
#-----------------------------------------------------------
@app.get("/admin")
@fresh_login_required
def show_admin():
    # Determine whether user is a committee member
    if current_user.is_committee:
        #Get the list of members and activities to prompt deletion
        with connect_db() as client:
            sql = "SELECT callsign, name FROM members ORDER BY callsign ASC"
            params = []
            result = client.execute(sql, params)
            members = result.rows

        with connect_db() as client:
            sql = "SELECT id, title, description, posted_by, location FROM activities ORDER BY title ASC"
            params = []
            result = client.execute(sql, params)
            activities = result.rows

        
        return render_template("pages/administration.jinja", user=current_user, members=members, activities=activities)
    # Else
    return redirect("/")

#-----------------------------------------------------------
# Admin remove user
#-----------------------------------------------------------

@app.get("/admin/remove-member/<string:callsign>")
@fresh_login_required
def delete_user(callsign):
    #Cant rely on security check on showing admin page, could still send request manually
    if current_user.is_committee:
        with connect_db() as client:
            sql = "DELETE FROM members WHERE callsign=?"
            params = [callsign]
            client.execute(sql, params)
        flash("Member deleted successfully")
        return redirect("/admin")
    # Else
    return redirect("/")


#-----------------------------------------------------------
# Admin remove activity
#-----------------------------------------------------------

@app.get("/admin/remove-activity/<int:id>")
@fresh_login_required
def delete_activity(id):
    #Cant rely on security check on showing admin page, could still send request manually
    if current_user.is_committee:
        with connect_db() as client:
            sql = "DELETE FROM activities WHERE id=?"
            params = [id]
            client.execute(sql, params)
        flash("Activity deleted successfully")
        return redirect("/admin")
    # Else
    return redirect("/")






#-----------------------------------------------------------
# Admin Invite Member
#-----------------------------------------------------------
@app.post("/admin/invite-user")
@fresh_login_required
def invite_user():
    #Cant rely on security check on showing admin page, could still send request manually
    if current_user.is_committee:
        # Get new user info 
        user_name = request.form.get("name").title()
        user_callsign = request.form.get("callsign").upper()
        user_email = request.form.get("email")
        user_password = generate_password_hash(token_urlsafe(7)) # easy implementation of secure temporary password, approx 10 char
        hashed_user_password = generate_password_hash(user_password)


        #Send Invite Email
        send_invite_email(user_name, user_callsign, user_password, user_email)
        
        #Update database with callsign, name, email
        with connect_db() as client:
            sql = "INSERT INTO members (callsign, name, email, password) VALUES (?,?,?,?)"
            params = [user_callsign, user_name, user_email, hashed_user_password]
            client.execute(sql, params)

        

        return render_template("pages/administration.jinja", user=current_user)

    #Redirect home, 
    return redirect("/")



def send_invite_email(user_name, user_callsign, user_password, user_email):
    #Send email with generated password to email including name etc
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    load_dotenv()
    smtp_key = getenv("SMTP_KEY")

    sender_email = "nelsonradioclub@gmail.com"
    sender_name = "Nelson Amateur Radio Club"

    body = f"""Hello {user_name} ({user_callsign}),

    You have been invited to join the new NZART Branch 26 Website!
    Your temporary password is: {user_password}
    Please change this on login

    73,
    Nelson Amateur Radio Club
    """

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = user_email
    msg["Subject"] = "Invite to Branch 26 Nelson Amateur Radio Club Website"

    with SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, smtp_key)
        server.send_message(msg)  
