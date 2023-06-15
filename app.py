"""Flask app for Cupcakes"""

from flask import Flask, redirect, request, render_template, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from sqlalchemy.sql import text
from sqlalchemy import exc

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True

app.config['SECRET_KEY'] = 'not-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def homepage():
    cupcakes=Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def all_cupcakes():
    
    resp = [cup.serialize() for cup in Cupcake.query.all()]
    return jsonify(cupcakes=resp)

@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake_details(cupcake_id):
    resp = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=resp.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    flavor = request.json.get('flavor')
    size = request.json.get('size')
    rating = request.json.get('rating')
    image = request.json.get('image')

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(deleted="cupcake")
