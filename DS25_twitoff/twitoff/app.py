"""This is what brings the application together"""
from os import getenv
from flask import Flask, render_template, request
from .predict import predict_user
from .models import DB, User
from .twitter import add_or_update_user

def create_app():
    
    """Main app function for twitoff"""
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACKING_MODIFICATIONS"] = False
    

    DB.init_app(app)
    
    @app.route('/')
    def root():
        return render_template('base.html', title="Home", users=User.query.all())
    
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset Database")
    
    @app.route('/update')
    def update():
        add_or_update_user()
        return User.query.all(), "Users {} Updated!"
    
    @app.route('/addusers')
    def add_users():
        """adding new users"""
        add_or_update_user("elonmusk")
        
    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):
        
        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through
        # user submission
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} Successfully Added!".format(name)
                
            tweets = User.query.filter(User.name == name).one().tweets
            
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            
            tweets = []
            
        return render_template("user.html", title=name, tweets=tweets, message=message)
            
    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])
        if user0 == user1:
            message = "Cannot compare users to themselves"
        else:
            prediction = predict_user(user0, user1, request.values["tweet_text"])
            message = "{} is more likely to be said by {} than {}!".format(request.values["tweet_text"],
            user1 if prediction else user0,
            user0 if prediction else user1)
        return render_template("prediction.html", title="Prediction", message=message)
    return app


def insert_example_users():
    """Will insert hypothetical users we've made"""
    nick = User(id=1, name= "Nick")
    elon = User(id=2, name= "Elon")
    andrew = User(id=3, name= "Andrew")
    griffin = User(id=4, name= "Griffin")
    matt = User(id=5, name= "Matt")
    tristan = User(id=6, name= "Tristan")
    james = User(id=7, name= "James")
    kelsea = User(id=8, name= "Kelsea")
    josh = User(id=9, name= "Josh")
    emily = User(id=10, name= "Emily")

    DB.session.add(nick)
    DB.session.add(elon)
    DB.session.add(andrew)
    DB.session.add(griffin)
    DB.session.add(matt)
    DB.session.add(tristan)
    DB.session.add(james)
    DB.session.add(kelsea)
    DB.session.add(josh)
    DB.session.add(emily)
    DB.session.commit()
