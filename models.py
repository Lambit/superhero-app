from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()
bcrypt =  Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """Register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        """turn bytestring into normal (unicode utf8) string"""

        hash_utf8 = hashed.decode("utf8")
        """return instance of user with username and hashed pwd"""
        return cls(username=username, password=hash_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists and pwd is correct
        
        Return user if correct, if not return false.
        """
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Superhero(db.Model):
    """Superhero Model"""

    __tablename__ = 'superheros'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    intelligence = db.Column(db.Text, nullable=False)
    strength = db.Column(db.Text, nullable=False)
    speed = db.Column(db.Text, nullable=False)
    durability = db.Column(db.Text, nullable=False)
    power = db.Column(db.Text, nullable=False)
    combat = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.Text)
    pof = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="superheros")

    def __init__(self, id, name, intelligence, strength, speed, durability, power, combat, full_name, pof, image):
        self.id = id
        self.name = name
        self.intelligence = intelligence
        self.strength = strength
        self.speed = speed
        self.durability = durability
        self.power = power
        self.combat = combat
        self.full_name = full_name
        self.pof = pof
        self.image = image
        self.user_id = user_id

    # def to_dict(self):
    #     """Serialize superheros to a dictionary of hero info"""

    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "intelligence": self.intelligence,
    #         "strength": self.strength,
    #         "speed": self.speed,
    #         "durability": self.durability,
    #         "power": self.power,
    #         "combat": self.combat,
    #         "full_name": self.full_name,
    #         "pof": self.pof,
    #         "image": self.image
    #     }


# table for favorited heros by user
class Favoritehero(db.Model):
    __tablename__ = 'fav_heros'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    durability = db.Column(db.Integer, nullable=False)
    power = db.Column(db.Integer, nullable=False)
    combat = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.Text)
    pof = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="fav_heros")   

    def to_dict(self):
        """Serialize superheros to a dictionary of hero info"""
        return {
            "id": self.id,
            "name": self.name,
            "intelligence": self.intelligence,
            "strength": self.strength,
            "speed": self.speed,
            "durability": self.durability,
            "power": self.power,
            "combat": self.combat,
            "full_name": self.full_name,
            "pof": self.pof,
            "image": self.image
        }

        
        