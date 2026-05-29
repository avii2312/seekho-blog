# =============================================================
# auth.py — Authentication routes
# VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
# =============================================================
# Routes in this file:
#   GET  /register  — show the registration form
#   POST /register  — handle the submitted form
#   GET  /login     — show the login form
#   POST /login     — handle the submitted form
#   GET  /logout    — clear session and redirect home
# =============================================================

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from db import query_db, execute_db

# A Blueprint groups related routes.
# This blueprint is registered in app.py.
auth_bp = Blueprint('auth', __name__)


# ------------------------------------------------------------------
# REGISTER
# ------------------------------------------------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET:  Show the empty registration form.
    POST: Read the form data, validate it, and create the account.
    """
    if request.method == 'GET':
        return render_template('register.html')

    # --- POST: process the submitted form ---

    # Read values from the form
    full_name        = request.form.get('full_name', '').strip()
    username         = request.form.get('username', '').strip()
    email            = request.form.get('email', '').strip().lower()
    password         = request.form.get('password', '')
    password_confirm = request.form.get('password_confirm', '')

    # --- Server-side validation ---
    # (The browser checks required fields too, but we must check here
    # as well — the browser check is cosmetic and can be bypassed.)

    errors = []

    if not full_name:
        errors.append("Full name is required.")
    if not username:
        errors.append("Username is required.")
    if not email:
        errors.append("Email is required.")
    if not password:
        errors.append("Password is required.")
    if password != password_confirm:
        errors.append("Passwords do not match.")
    if len(password) < 6:
        errors.append("Password must be at least 6 characters.")

    # Check if username is already taken
    existing_user = query_db(
        "SELECT id FROM users WHERE username = %s", (username,), one=True
    )
    if existing_user:
        errors.append("That username is already taken. Please choose another.")

    # Check if email is already registered
    existing_email = query_db(
        "SELECT id FROM users WHERE email = %s", (email,), one=True
    )
    if existing_email:
        errors.append("An account with that email already exists.")

    if errors:
        # Show all errors on the form page
        for error in errors:
            flash(error, 'danger')
        # Return the form with values filled in so the user
        # does not have to retype everything
        return render_template('register.html',
                               full_name=full_name,
                               username=username,
                               email=email)

    # --- Everything valid — create the account ---

    # IMPORTANT: Never store the plain password.
    # generate_password_hash converts it to a long hash string.
    password_hash = generate_password_hash(password)

    execute_db(
        "INSERT INTO users (full_name, username, email, password_hash) VALUES (%s, %s, %s, %s)",
        (full_name, username, email, password_hash)
    )

    flash("Account created! Please log in.", 'success')
    return redirect(url_for('auth.login'))


# ------------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET:  Show the login form.
    POST: Verify credentials and start a session.
    """
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    # Look up the user by username
    user = query_db(
        "SELECT * FROM users WHERE username = %s", (username,), one=True
    )

    # SECURITY NOTE:
    # We show the same error message whether the username does not exist
    # or the password is wrong. Never tell the user which one failed —
    # that leaks information about who has accounts.
    if not user or not check_password_hash(user['password_hash'], password):
        flash("Invalid username or password.", 'danger')
        return render_template('login.html', username=username)

    # Credentials correct — store the user's id in the session
    session.clear()
    session['user_id']  = user['id']
    session['username'] = user['username']
    session['is_admin'] = bool(user['is_admin'])

    flash(f"Welcome back, {user['full_name']}!", 'success')
    return redirect(url_for('posts.dashboard'))


# ------------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------------

@auth_bp.route('/logout')
def logout():
    """
    Clear the session and send the user to the home page.
    """
    session.clear()
    flash("You have been logged out.", 'info')
    return redirect(url_for('posts.index'))


# ------------------------------------------------------------------
# Login-required decorator
# ------------------------------------------------------------------
# Import and use this in posts.py to protect routes.
#
# Usage in posts.py:
#   from auth import login_required
#
#   @posts_bp.route('/dashboard')
#   @login_required
#   def dashboard():
#       ...
# ------------------------------------------------------------------

from functools import wraps

def login_required(f):
    """
    Decorator: redirects to login if the user is not logged in.
    Put @login_required below @app.route (or @blueprint.route)
    on any route that should only be reached by logged-in users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access that page.", 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator: only allows the admin account through.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("You do not have permission to access that page.", 'danger')
            return redirect(url_for('posts.index'))
        return f(*args, **kwargs)
    return decorated_function
