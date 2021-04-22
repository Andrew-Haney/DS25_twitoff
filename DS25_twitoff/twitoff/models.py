"""SQLAlchemy User and Tweet models for out Database"""
from flask_sqlalchemy import SQLAlchemy

"""Creates a DB object from SQLAlchemy class"""
DB = SQLAlchemy()


"""Make User table using SQLAlchemy"""
class User(DB.Model):
    """Creates a User Table with sqlalchemy"""
    #id column
    id = DB.Column(DB.BigInteger, primary_key = True)
    #name column
    name = DB.Column(DB.String, nullable = False)
    # keeps track of id for newest tweet by user
    newest_tweet_id = DB.Column(DB.BigInteger)
    
    
    def __repr__(self):
        return "<User: {}>".format(self.name)

class Tweet(DB.Model):
    """Keeps track of Tweets for each User"""
    id = DB.Column(DB.BigInteger, primary_key = True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable= False)
    user = DB.relationship('User', backref=DB.backref(
        'tweets', lazy=True))
    
    
    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
    
    
CREATE_USER_TABLE_SQL = """
    CREATE TABLE IF NOT EXIST user(
        id INT PRIMARY,
        name STRING NOT NULL,
        newest_tweet_id INT NOT NULL,
    );"""