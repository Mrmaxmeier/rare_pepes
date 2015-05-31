from flask import Flask, render_template, Response
from flask.ext.script import Manager
from database import db, Pepe
import sys
import os
import random
import json
from functools import wraps



def json_out(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		def jsonify_wrap(obj):
			return Response(json.dumps(obj), mimetype='application/json')

		result = f(*args, **kwargs)
		if isinstance(result, tuple):
			# (resp, status_code)
			return jsonify_wrap(result[0]), result[1]
		if isinstance(result, dict):
			return jsonify_wrap(result)
		if isinstance(result, list):
			return jsonify_wrap(result)

		# isnt tuple, dict or list -> must be a Response
		return result

	return wrapper


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db.init_app(app)

@app.route("/")
def index():
	return render_template("index.html", num_pepes=db.session.query(Pepe).count())

@app.route("/api/get_pepes", methods=["POST"])
@json_out
def get_pepes(nsfw=False):
	allowed_nsfwness = 0.0 if nsfw else 1.0
	all_pepes = db.session.query(Pepe).filter(Pepe.nsfwness <= allowed_nsfwness)
	r1 = random.randrange(0, all_pepes.count())
	r2 = random.randrange(0, all_pepes.count())
	p1 = all_pepes[r1]
	p2 = all_pepes[r2]
	return [p1.info(), p2.info()]

@app.route("/api/vote/<int:id>", methods=["POST"])
def vote(id):
	pepe = Pepe.query.get(id)
	if pepe:
		pepe.rareness += 1
	return get_pepes()


manager = Manager(app)

@manager.command
def build_db():
	from build_db import main
	main(app)


if __name__ == '__main__':
	manager.run()