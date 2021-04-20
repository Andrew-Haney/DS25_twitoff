"""This is what brings the application together"""
from flask import Flask, render_template
from .models import DB, User


def create_app():
    
    """Main app function for twitoff"""
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACKING_MODIFICATIONS"] = False
    

    DB.init_app(app)
    
    @app.route('/')
    def root():
        """Drops everything from DB"""
        DB.drop_all()
        
        """Creates DB"""
        DB.create_all()
        insert_example_users()
        return render_template('base.html', title="Home", 
                               users=User.query.all())
    
    @app.route('/hola')
    def hola():
        return "Hola, Twitoff"
    
    @app.route('/salut')
    def salut():
        return "Salut, twitoff"
    return app


def insert_example_users():
    """Will insert hypothetical users we've made"""
    nick = User(id=1, name= "Nick")
    elon = User(id=2, name= "Elon")
    # andrew = User(id=3, name= "Andrew")
    # griffin = User(id=4, name= "Griffin")
    # matt = User(id=5, name= "Matt")
    # tristan = User(id=6, name= "Tristan")
    # james = User(id=7, name= "James")
    # kelsea = User(id=8, name= "Kelsea")
    # josh = User(id=9, name= "Josh")
    # emily = User(id=10, name= "Emily")

    # DB.session.add(andrew)
    DB.session.add(nick)
    DB.session.add(elon)
    # DB.session.add(griffin)
    # DB.session.add(matt)
    # DB.session.add(tristan)
    # DB.session.add(james)
    # DB.session.add(kelsea)
    # DB.session.add(josh)
    # DB.session.add(emily)
    DB.session.commit()
