from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
import requests
from xml.etree import ElementTree
from app import db, login_manager
from app.models import User
from app.users import bp_users
from urllib.parse import urlencode
import yalies

CAS_SERVER = 'https://secure.its.yale.edu/cas'
CAS_LOGIN_ROUTE = '/login'
CAS_AFTER_LOGIN = 'after_login'
# CAS_VERIFY_SSL = False
CAS_LOGOUT_ROUTE = '/logout'
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "None"
CAS_VERSION = '2.0'
CAS_SERVICE_VALIDATE_URL = CAS_SERVER + 'serviceValidate'
API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODAyMjc3NzMsInN1YiI6InJhYTY2In0.PovebuIvsPzU6X5ftWJNqwku9msc6oNvFhgoANRgOdM'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flask_login import login_user, current_user

@bp_users.route('/sign_in', methods=['GET'])
def login():
    """Handles login using Yale's CAS"""
    if current_user.is_authenticated:
        print("In session.")
        return redirect(FRONTEND_URL)

    # url to be directed to when a user logs in using Yale's CAS
    service_url = url_for('users.after_login', _external=True)
    cas_login_url = CAS_SERVER + CAS_LOGIN_ROUTE + '?' + urlencode({'service': service_url})
    print("Logging in")
    return redirect(cas_login_url)

@bp_users.route('/cas-callback', methods=['GET'])
def after_login():
    """Handle the callback from CAS after login attempt."""

    # Get the CAS ticket from the query parameters
    ticket = request.args.get('ticket')
    if not ticket:
        return 'No ticket provided', 400  # Or handle as per your application's needs

    # Construct the service URL (the URL to this route)
    service_url = url_for('users.after_login', _external=True)

    # Validate the ticket with the CAS server
    cas_service_validate_url = f"{CAS_SERVER}/serviceValidate?service={service_url}&ticket={ticket}"
    response = requests.get(cas_service_validate_url)

    # Parse the XML response from CAS
    xml_tree = ElementTree.fromstring(response.content)
    cas_user_tag = xml_tree.find('.//{http://www.yale.edu/tp/cas}user')

    # Check if the validation was successful
    if cas_user_tag is None:
        return 'Invalid ticket', 400  # Or redirect to login page

    # Extract the NetID (username) from the CAS response
    netid = cas_user_tag.text.strip()

    # Find or create the user in your database
    user = User.query.filter_by(NetID=netid).first()
    if not user:
        person = get_user(netid)
        user = User(NetID=person.netid, FirstName=person.first_name, Email=person.email, LastName=person.last_name, ProfileImage=person.image)
        db.session.add(user)
        db.session.commit()

    # Use Flask-Login to log in the user
    login_user(user)

    # Redirect to the desired page after successful login
    return redirect(url_for('products.index'))

@bp_users.route('/logout')
@login_required
def logout():
    # Log out the user
    logout_user()

    # Redirect to CAS logout page or home page
    return redirect(url_for('products.index'))


####----Helper Functions----##
def get_user(netid):
    """Getting user information from yalies.io"""
    token = API_TOKEN
    api = yalies.API(token)

    person = api.person(filters={'netid': netid})
    return person