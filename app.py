from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#CONFIG area
app = Flask(__name__)


#establish the connection                 dbms                  db_user     pwd    URI      PORT  db_name
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://std2_db_dev:123456@localhost:5432/std2_library_db"
db = SQLAlchemy(app)

#models area
class Book (db.Model):
    # define tablename
    __tablename__ = "books"
    # define the primary key
    book_id = db.Column(db.Integer(), primary_key = True)
    # more attributes
    title = db.Column(db.String())
    genre = db.Column(db.String())
    year = db.Column(db.Integer())
    length = db.Column(db.Integer())

# CLI commands area
@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command("seed")
def seed_db():
    # create a book object
    book1 = Book(
        title = "Animal Farm",
        genre = "Satire",
        year = 1945,
        length =  130
    )
    db.session.add(book1)

    book2 = Book()
    book2.title = "Dune"
    book2.genre = "Science fiction"
    book2.year = 1965
    book2.length = 530
    db.session.add(book2)

    db.session.commit()
    print ("table seeded")

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print ("tables dropped")


# ROUTES area
@app.route("/")
def index():
    return "Welcome to Coder Library"