from flask import Flask, render_template, request, flash, redirect, session, json, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from secrets import key
import requests
from models import db, connect_db, User, Favoritehero
from forms import UserForm
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

BASE_URL = f"https://superheroapi.com/api/{key}"

app = Flask(__name__)

# enables CORS for all routes
CORS(app)


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
    and saving it to db. Try initial request and commit. Except
    key errors for missplelings. Integrity Error for a hero already 
    in the DB to still display.
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

    except KeyError:
        flash('Not a valid superhero or superhero already exists')    
        return render_template('index.html') 
    

    except IntegrityError:   
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
    """
    Query all favorited heros.
    """
    superheros = Favoritehero.query.all()
    return render_template('favorites.html', superheros=superheros)
    

# -----------REGISTER, LOGIN & LOGOUT PAGES------------
# route to register user
@app.route('/register', methods=['GET', 'POST'])
def regiseter_user():
    """
    Register form using WTForm, stores users data to the User model.
    Error handeling for is a user already exist. Use session to create
    user_id.
    """
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username already exists!")
            return render_template('register.html', form=form)
        
        session['user_id'] = new_user.id
        flash('Welcome! Successfully created your account!')
        return redirect('/')

    return render_template('register.html', form=form)


# log in form
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """
    Login form using WTForms, if statement to authenticate the user.
    """
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
    """
    A simple session.pop() on the user_id to log out.
    """
    session.pop('user_id')
    flash('Goodbye, see you soon!')
    return redirect('/')



# ----------------------API---------------------------
# superhero JSON data
# list all superheros
@app.route("/api/superheros")
def list_superheros():
    """
    Return all heros in system
    Returns JSON like so [{id, name, powerstats,....}]
    """
    all_superhero = [superhero.to_dict() for superhero in Favoritehero.query.all()]
    return jsonify(superheros=all_superhero)

# POST
@app.route("/api/superheros", methods=["POST"])
def add_superhero():
    """
    Add a superhero, and return data about new hero.
    """

    data = request.json

    superhero = Favoritehero(
        id=data['id'],
        name=data['name'],
        intelligence=data['intelligence'],
        strength=data['strength'],
        speed=data['speed'],
        durability=data['durability'],
        power=data['power'],
        combat=data['combat'],
        full_name=data['full_name'],
        pof=data['pof'],
        image=data['image'],
        user_id= session['user_id'])

    db.session.add(superhero)
    db.session.commit()

    return(jsonify(superhero=superhero.to_dict()), 201)


# DELETE
@app.route("/api/superheros/<int:id>", methods=["DELETE"])
def delete_superhero(id):
    """
    Deletes superhero and return confirm message
    Returns JSON of {message: "Deleted"}
    """

    superhero = Favoritehero.query.get_or_404(id)

    db.session.delete(superhero)
    db.session.commit()

    return jsonify(message="Deleted")





