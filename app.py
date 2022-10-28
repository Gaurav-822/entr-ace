import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
date_time = datetime.now()

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Requires Change
@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

# Status: DONE
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Status: DONE
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Status: Done
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get('username')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')

    u = db.execute('SELECT username FROM users')
    u_l = []
    for i in u:
        u_l.append(i['username'])
    if username == '' or username in u_l:
        return apology('input is blank or the username already exists.')
    u_l = []
    if password == '' or password != confirmation:
        return apology('Password input is blank or the passwords do not match.')

    id = db.execute('INSERT INTO users(username, hash) VALUES(?, ?)', username, generate_password_hash(password))
    session["user_id"] = id

    # Load all the syllabus into the database with his id
    # PHYSICS
    phy = ['Physics And Measurement', 'Kinematics', 'Laws of Motion', 'Work, Energy and Power', 'Rotational Motion', 'Gravitation', 'Properties of Solid and Liquids', 'Thermodynamics','Kinetic Theory of Gases', 'Oscillation and Waves', 'Electrostatics', 'Current Electricity', 'Magnetic Effects of Current and Magnetism', 'Electromagnetic Induction and Alternating Currents', 'Electromagnetic Waves', 'Optics', 'Dual Nature of Matter and Radiation', 'Atoms and Nuclei', 'Electronic Devices', 'Communication Systems', 'Experimental Skills']
    for chapter in phy:
        db.execute('INSERT INTO physics VALUES(?, ?, ?)', session['user_id'], chapter, False)
    # CHEMISTRY
    chem = ['Some Basic Concepts in Chemistry', 'Gaseous State', 'Liquid State', 'Solid State', 'Atomic Structure', 'Chemical Bonding and Molecular Structure', 'Chemical Thermodynamics', 'Solutions', 'Equilibrium', 'Redox Reaction and Electrochemistry', 'Chemical Kinetics', 'Surface Chemistry','Periodic Property', 'General Principles and Process of Isolation of Metals', 'Hydrogen', 's-Block Elements', 'p-Block Elements', 'd and f - Block Elements', 'Co-ordination Compounds', 'Environmental Chemistry', 'Purification and Characterisation of Organic Compounds', 'Some Basic Principles of Organic Chemistry', 'Hydrocarbons', 'Organic compounds containing Halogens', 'Organic compounds containing Oxygen', 'Organic compounds containing Nitrogen', 'Polymers', 'Biomolecules', 'Chemistry in Everyday Life', 'Principles related to Practical Chemistry']
    for chapter in chem:
        db.execute('INSERT INTO chemistry VALUES(?, ?, ?)', session['user_id'], chapter, False)
    # MATHS
    maths = ['Sets, Relation and Functions', 'Complex numbers and Quadratic Equations', 'Matrices and Determinants', 'Permutations and Combinations', 'Mathematical Inductions', 'Binomial Theorem and its Simple Applications', 'Sequence and Series', 'Limit, Continuity and Differentiability', 'Integral Calculus', 'Differential Equations', 'Co-ordinate Geometry', 'Straight Line', 'Circle', 'Conic Sections', 'Three Dimensional Geometry', 'Vector Algebra', 'Statistics and Probability', 'Trignometry', 'Mathematical Reasoning']
    for chapter in maths:
        db.execute('INSERT INTO maths VALUES(?, ?, ?)', session['user_id'], chapter, False)

    return redirect("/")

# Status: DONE
@app.route("/task", methods=["GET", "POST"])
@login_required
def task():
    if request.method == 'GET':
        return render_template('task.html')

    task = request.form.get('task')
    subject = request.form.get('subject').lower()
    if subject in ['phy', 'physics']:
        subject = 'physics'
    if subject in ['chem', 'chemistry']:
        subject = 'chemistry'
    if subject in ['math', 'maths', 'mathematics', 'mathematic']:
        subject = 'maths'

    db.execute('INSERT INTO ? VALUES(?, ?, ?)', subject, session['user_id'], task, False)

    return redirect('/')


# Status: DONE
@app.route("/physics", methods=["GET", "POST"])
@login_required
def physics():
    phy = db.execute('SELECT * FROM physics WHERE id = ?', session['user_id'])
    chapters = []
    status = []
    l = []
    for i in range(len(phy)):
        chapters.append(phy[i]['chapters'])
        l.append(i + 1)
        if phy[i]['status'] == 0:
            status.append('To be Done')
        else:
            status.append('Done')
    loop = len(l)

    for i in range(loop):
        if request.form.get(str(phy[i])) == 'Done':
            db.execute('UPDATE physics SET status = 1 WHERE chapters = ? AND id = ?', chapters[i], session['user_id'])
            return redirect('/physics')

        if request.form.get(str(phy[i])) == 'Un Done':
            db.execute('UPDATE physics SET status = 0 WHERE chapters = ? AND id = ?', chapters[i], session['user_id'])
            return redirect('/physics')

    return render_template('physics.html',phy=phy, chapters=chapters, l=l, status=status, loop=loop)


# Status: DONE
@app.route("/chemistry", methods=["GET", "POST"])
@login_required
def chemistry():
    chem = db.execute('SELECT * FROM chemistry WHERE id = ?', session['user_id'])
    chapters = []
    status = []
    l = []
    for i in range(len(chem)):
        chapters.append(chem[i]['chapters'])
        l.append(i + 1)
        if chem[i]['status'] == 0:
            status.append('To be Done')
        else:
            status.append('Done')
    loop = len(l)

    for i in range(loop):
        if request.form.get(str(chem[i])) == 'Done':
            db.execute('UPDATE chemistry SET status = 1 WHERE chapters = ? AND id = ?', chapters[i], session['user_id'])
            return redirect('/chemistry')

        if request.form.get(str(chem[i])) == 'Un Done':
            db.execute('UPDATE chemistry SET status = 0 WHERE chapters = ? AND id = ?', chapters[i], session['user_id'])
            return redirect('/chemistry')

    return render_template('chemistry.html',chem=chem, chapters=chapters, l=l, status=status, loop=loop)


# Status: DONE
@app.route("/maths", methods=["GET", "POST"])
@login_required
def maths():
    math = db.execute('SELECT * FROM maths WHERE id = ?', session['user_id'])
    chapters = []
    status = []
    l = []
    for i in range(len(math)):
        chapters.append(math[i]['chapters'])
        l.append(i + 1)
        if math[i]['status'] == 0:
            status.append('To be Done')
        else:
            status.append('Done')
    loop = len(l)

    for i in range(loop):
        if request.form.get(str(math[i])) == 'Done':
            db.execute('UPDATE maths SET status = 1 WHERE chapters = ? AND id = ?', chapters[i], session['user_id'])
            return redirect('/maths')

        if request.form.get(str(math[i])) == 'Un Done':
            db.execute('UPDATE maths SET status = 0 WHERE chapters = ? AND id = ?', chapters[i], session['user_id'])
            return redirect('/maths')

    return render_template('maths.html',math=math, chapters=chapters, l=l, status=status, loop=loop)


# Status: DONE
@app.route("/leader_board", methods=["GET", "POST"])
@login_required
def leader_board():
    p = db.execute('select id, sum(status) as topper from physics group by id order by topper desc, id;')
    p_id = []
    p_top = []
    loop_p = len(p)
    for i in range(loop_p):
        p_top.append(p[i]['topper'])
        name = db.execute('SELECT username FROM users WHERE id = ?', p[i]['id'])
        p_id.append(name[0]['username'])

    c = db.execute('select id, sum(status) as topper from chemistry group by id order by topper desc, id;')
    c_id = []
    c_top = []
    loop_c = len(c)
    for i in range(loop_c):
        c_top.append(c[i]['topper'])
        name = db.execute('SELECT username FROM users WHERE id = ?', c[i]['id'])
        c_id.append(name[0]['username'])

    m = db.execute('select id, sum(status) as topper from maths group by id order by topper desc, id;')
    m_id = []
    m_top = []
    loop_m = len(m)
    for i in range(loop_m):
        m_top.append(m[i]['topper'])
        name = db.execute('SELECT username FROM users WHERE id = ?', m[i]['id'])
        m_id.append(name[0]['username'])

    return render_template('leader_board.html', p_id=p_id, p_top=p_top, loop_p=loop_p, c_id=c_id, c_top=c_top, loop_c=loop_c, m_id=m_id, m_top=m_top, loop_m=loop_m)


@app.route("/delete")
def delete():
    db.execute('DELETE FROM users WHERE id = ?', session['user_id'])
    db.execute('DELETE FROM physics WHERE id = ?', session['user_id'])
    db.execute('DELETE FROM chemistry WHERE id = ?', session['user_id'])
    db.execute('DELETE FROM maths WHERE id = ?', session['user_id'])

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/about")
@login_required
def about():
    return render_template('about.html')
