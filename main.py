from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# Get Cafe from ID
def get_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    return cafe


def refresh_db():
    return db.session.query(Cafe).order_by('name').all()


def convert_dict(db_entry):
    obj_dict = db_entry.__dict__
    del obj_dict['_sa_instance_state']
    return obj_dict


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all")
def all():
    return jsonify(dict([(cafe.id, convert_dict(cafe)) for cafe in refresh_db()]))


@app.route('/cafes')
def cafes():
    cafes=refresh_db()
    print(cafes)
    return render_template('cafes.html', cafes=cafes)


if __name__ == '__main__':
    app.run(debug=True)