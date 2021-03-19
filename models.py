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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    powerstats = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db. relationship('User', backref="superheros")

    def to_dict(self):
        """Serialize superheros to a dictionary of hero info"""

        return {
            "id": self.id,
            "name": self.name,
            "powerstats": self.powerstats,
            "bio": self.bio,
            "image": self.image
        }


# table for favorited heros by user
class Favoritehero(db.Model):
    __tablename__ = 'fav_heros'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db. relationship('User', backref="fav_heros")