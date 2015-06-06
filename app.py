from flask import Flask, render_template, Response, stream_with_context
from flask.ext.script import Manager
from database import db, Pepe, PepeCombination, pending_votes
import db_tools
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
	return Pepe.get_two().info()

@app.route("/api/vote/<string:uuid>", methods=["POST"])
def vote(uuid):
	def generate():
		yield json.dumps(Pepe.get_two().info())
		if uuid in pending_votes:
			pending_votes[uuid]()
	return Response(stream_with_context(generate()), mimetype='application/json')


manager = Manager(app)

@manager.command
def build_db():
	db_tools.build_db(app)

@manager.command
def get_md5s():
	db_tools.get_md5s(app)

@manager.command
def deduplicate():
	db_tools.deduplicate(app)

@manager.command
def crawl_reddit(amount):
	db_tools.crawl_reddit(app, amount=int(amount))


if __name__ == '__main__':
	manager.run()