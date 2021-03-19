from flask import Flask, render_template, request, flash, redirect, session, json, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from secrets import key
import requests
from models import db, connect_db, User, Superhero
from forms import UserForm

BASE_URL = f"https://superheroapi.com/api/{key}"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///superheros_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

# route to register user
@app.route('/register', methods=['GET', 'POST'])
def regiseter_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        flash('Welcome! Successfully created your account!')
        return redirect('/')

    return render_template('register.html', form=form)


# log in form
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back, {user.username}!')
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)

# get request to log out
@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash('Goodbye, see you soon!')
    return redirect('/')


# superhero JSON data
@app.route("/superheros")
def list_superheros():
    """Return all heros in system
    Returns JSON like so [{id, name, powerstats,....}]
    """
    all_superhero = [superhero.to_dict() for superhero in Superhero.query.all()]
    return jsonify(superheros=all_superhero)

@app.route("/superheros", methods=["POST"])
def create_superhero():
    """Add a superhero, and return data about new hero."""

    data = request.json 

    superhero = Superhero(
        name=data['name'],
        powerstats=data['powerstats'],
        bio=data['bio'],
        image=data['image'])

    db.session.add(superhero)
    db.session.commit()

    # POST request should return HTTP status of 201 created
    return(jsonify(superheros=superhero.to_dict()), 201)

@app.route("/superheros/<int:superhero_id>")
def get_superhero():
    """Return data on a specific superhero"""
    superhero = Superhero.query.get_or_404(superhero_id)
    return jsonify(superheros=superhero.to_dict())

@app.route("/superheros/<int:superhero_id>", methods=["DELETE"])
def delete_superhero(superhero_id):
    """Deletes superhero and return confirm message
    Returns JSON of {message: "Deleted"}
    """

    superhero = Superhero.query.get_or_404(superhero_id)

    de.session.delete(superhero)
    db.session.commit()

    return jsonify(message="Deleted")



# @app.route('/hero_data')
# def get_hero():
#     """
#     Just a test get request
#     Access form on index.html
#     Send a get request to the api, and search the heros name.
#     get json data. And print it to the index.html

#     """
#     hero = request.args['hero']
#     res = requests.get(f"{BASE_URL}/search/{hero}", params={'hero': hero})
#     data = res.json()
#     hero_name = data['results'][0]['name']
#     hero_powerstats = data['results'][0]['powerstats']
#     hero_bio = data['results'][0]['biography']
#     info = {'hero_name': hero_name, 'hero_powerstats': hero_powerstats, 'hero_bio': hero_bio}
#     return render_template('base.html', info=info)