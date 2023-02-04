import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#CONFIG area
app = Flask(__name__)


#establish the connection                 dbms                  db_user     pwd    URI      PORT  db_name
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config["JWT_SECRET_KEY"] = os.getenv("ACCESS_TOKEN_SECRET_KEY")
#database instance with SQLALCHEMY
db = SQLAlchemy(app)
#Marshmallow instance
ma = Marshmallow(app)

#models area
class Book (db.Model):
    # define tablename
    __tablename__ = "books"
    # define the primary key
    id = db.Column(db.Integer(), primary_key = True)
    # more attributes
    title = db.Column(db.String())
    genre = db.Column(db.String())
    year = db.Column(db.Integer())
    length = db.Column(db.Integer())


class User (db.Model):
    # define tablename
    __tablename__ = "users"
    # define the primary key
    id = db.Column(db.Integer(), primary_key = True)
    # more attributes
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    role = db.Column(db.String())

#SCHEMAS area
class BookSchema(ma.Schema):
    class Meta:
        #fields
        fields = ("id", "title", "genre", "year", "length")

#multiple Book schema, to handle a books list
books_schema = BookSchema(many=True)
#single Book schema, to handle a books object
book_schema = BookSchema()


class UserSchema(ma.Schema):
    class Meta:
        #fields
        fields = ("id", "username", "password", "role")

#multiple Book schema, to handle a books list
users_schema = UserSchema(many=True)
#single Book schema, to handle a books object
user_schema = UserSchema()

# CLI commands area
@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print ("tables dropped")


# ROUTES area
@app.route("/")
def index():
    return "Welcome to Coder Library"

#retrieves the list of all books
@app.route("/books", methods=["GET"])
def get_books():
    # access to the database and get all the books and store them in a list
    books_list = Book.query.all() # 'SELECT * FROM BOOKS' in ORM language
    # data stores the book list converted to a readable format thanks to the schema
    data = books_schema.dump(books_list) #dump
    return data

#retrieves one book found by book_id
@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book =  Book.query.get(id) # SELECT * FROM BOOKS where book_id = id the parameter  
    # alternative to get. Filters by any criteria and returns a list. first is to get just one element of that list
    #book =  Book.query.filter_by(book_id=id).first()
    #data = book_schema.dump(book) #dump
    return book_schema.dump(book)

@app.route("/books", methods=["POST"])
def post_book():
    # Receive the book fields from the request (imported from flask), use schema to load them
    book_fields = book_schema.load(request.json)
    #Accessing to book_fields' keys, we can get its values
    book = Book(
        title = book_fields["title"],
        genre = book_fields["genre"],
        length = book_fields["length"],
        year = book_fields["year"]
    ) 
    db.session.add(book)
    db.session.commit()
    return book_schema.dump(book)

#retrieves the list of all users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.dump(users)

#retrieves one user found by id
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user =  User.query.get(id)
    return user_schema.dump(user)

@app.route("/register", methods=["POST"])
def post_user():
    user_fields = user_schema.load(request.json) # user_req_schema
    user = User(
        username = user_fields["username"],
        password = user_fields["password"],
        role = user_fields["role"]
    ) 
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user)

if __name__ == "__main__":
    app.run(debug=True)
