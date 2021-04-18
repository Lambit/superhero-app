from flask import Flask, render_template, request, flash, redirect, session, json, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from secrets import key
import requests
from models import db, connect_db, User, Superhero, Favoritehero
from forms import UserForm
from flask_cors import CORS
from flask_wtf.csrf import CsrfProtect
from sqlalchemy.exc import IntegrityError

BASE_URL = f"https://superheroapi.com/api/{key}"

app = Flask(__name__)

# enables CORS for all routes

CORS(app)

# CSFR Token 

# CsrfProtect(app)

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
    """
    Index of app.
    """
    return render_template('index.html')

@app.route('/superheros')
def get_hero():
    """
    Getting data from API through form name and print it to page,
    and saving it to db.
    """
    try:
        name = request.args['name']
        res = requests.get(f"{BASE_URL}/search/{name}", params={'name': name})
        data = res.json() 

        superhero = Favoritehero(
            id = data['results'][0]['id'],
            name = data['results'][0]['name'],
            intelligence = data['results'][0]['powerstats']['intelligence'],
            strength = data['results'][0]['powerstats']['strength'],
            speed = data['results'][0]['powerstats']['speed'],
            durability = data['results'][0]['powerstats']['durability'],
            power = data['results'][0]['powerstats']['power'],
            combat = data['results'][0]['powerstats']['combat'],
            full_name = data['results'][0]['biography']['full-name'],
            pof = data['results'][0]['biography']['place-of-birth'],
            image = data['results'][0]['image']['url'],
            user_id= session['user_id'])
    
        db.session.add(superhero)
        db.session.commit()
    except (KeyError, IntegrityError) as e:
        flash('Not a valid superhero or superhero already exists')    
        return render_template('index.html')

    else:
            
        info = {
            'name': superhero.name,     
            'image': superhero.image,
            'intelligence': superhero.intelligence,
            'strength': superhero.strength,
            'speed': superhero.speed,
            'durability': superhero.durability,
            'power': superhero.power,
            'combat': superhero.combat,
            'full_name': superhero.full_name,
            'pof': superhero.pof,
            }

    return render_template('index.html', superhero=superhero, info=info)


# ------------FAVORITES PAGE-----------

@app.route("/favorites")
def favorite_page():
    superheros = Favoritehero.query.all()
    return render_template('favorites.html', superheros=superheros)
    

# -----------REGISTER, LOGIN & LOGOUT PAGES------------
# route to register user
@app.route('/register', methods=['GET', 'POST'])
def regiseter_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except InterruptedError:
            form.usernameerrors.append("Username already exists!")
            return render_template('register.html', form=form)
        
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


# log out
@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash('Goodbye, see you soon!')
    return redirect('/')



# ----------------------API---------------------------
# superhero JSON data

@app.route("/api/superheros")
def list_superheros():
    """Return all heros in system
    Returns JSON like so [{id, name, powerstats,....}]
    """
    all_superhero = [superhero.to_dict() for superhero in Favoritehero.query.all()]
    return jsonify(superheros=all_superhero)


@app.route("/api/superheros/<int:id>", methods=["DELETE"])
def delete_superhero(id):
    """Deletes superhero and return confirm message
    Returns JSON of {message: "Deleted"}
    """

    superhero = Favoritehero.query.get_or_404(id)

    db.session.delete(superhero)
    db.session.commit()

    return jsonify(message="Deleted")






# superhero JSON data
# @app.route("/api/superheros")
# def list_superheros():
#     """Return all heros in system
#     Returns JSON like so [{id, name, powerstats,....}]
#     """
#     all_superhero = [superhero.to_dict() for superhero in Superhero.query.all()]
#     return jsonify(superheros=all_superhero)



# @app.route("/api/superheros/<int:id>")
# def get_superhero():
#     """Return data on a specific superhero"""
#     superhero = Superhero.query.get_or_404(superhero_id)
#     return jsonify(superheros=superhero.to_dict())







# @app.route("/superheros", methods=["GET","POST"])
# def add_superhero():
#     """Add a superhero, and return data about new hero."""

#     if form.validate_on_submit():
#         name = form.name.data
#         intelligence = form.intelligence.data
#         strength = form.strength.data
#         speed = form.speed.data
#         durability = form.durability.data
#         power = form.power.data
#         combat = form.combat.data
#         full_name = form.full_name.data
#         pof = form.pof.data
#         image = form.image.data
#         user_id= form.user_id.data

#         # the data to be inserted into model 
#         superhero = Superhero(
#             id=id,
#             name=name, 
#             intelligence=intelligence,
#             strength=strength,
#             speed=speed,
#             durability=durability,
#             power=power,
#             combat=combat,
#             full_name=full_name,
#             pof=pof,
#             image=image,
#             user_id=user_id)
        
#         db.session.add(superhero)
#         db.session.commit()

#         # create a message to send to the template
#         flash('Superhero added to favorites!')
#         return redirect('/favorites')
#     else:
#         # show validaton errors
#         for field, errors in form.errors.items():
#             for error in errors:
#                 flash("Error in {}: {}".format(
#                     getattr(form, field).label.text,
#                     error
#                 ), 'error')
#         return render_template('index.html', form=form)




# @app.route("/superheros", methods=["GET", "POST"])
# def add_superhero():
#     """Add a superhero, and return data about new hero."""

    # data = request.form

    # superhero = Superhero(
    #     id=data['id'],
    #     name=data['name'],
    #     intelligence=data['intelligence'],
    #     strength=data['strength'],
    #     speed=data['speed'],
    #     durability=data['durability'],
    #     power=data['power'],
    #     combat=data['combat'],
    #     full_name=data['full_name'],
    #     pof=data['pof'],
    #     image=data['image'])

    # db.session.add(superhero)
    # db.session.commit()

# # #     # POST request should return HTTP status of 201 created
#     return(jsonify(superhero=superhero.to_dict()), 201)
