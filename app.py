
import os
import json
from functools import wraps

from flask import Flask, Response, send_from_directory
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from database import db, Pepe, pending_votes, Vote
import db_tools


def json_out(meth):
    @wraps(meth)
    def wrapper(*args, **kwargs):
        def jsonify_wrap(obj):
            return Response(json.dumps(obj), mimetype='application/json')

        result = meth(*args, **kwargs)
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

app = Flask(__name__, static_url_path='frontend/build')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
#app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)

@app.route("/")
@app.route("/index")
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('', path)

@app.route('/api/stats')
def api_stats():
    return dict(
        pepes=db.session.query(Pepe).count(),
        votes=db.session.query(Vote).count()
    )

@app.route("/api/get_pepes", methods=["POST"])
@json_out
def get_pepes(nsfw=False):
    return Pepe.get_two().info()

@app.route("/api/vote/<string:uuid>", methods=["POST"])
@json_out
def vote(uuid):
    if uuid in pending_votes:
        pending_votes[uuid]()
    else:
        print("invalid vote", uuid)
    return Pepe.get_two().info()


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
def delete_invalid_votes():
    db_tools.delete_invalid_votes(app)

@manager.command
def crawl_reddit(amount):
    db_tools.crawl_reddit(app, amount=int(amount))

@manager.command
def rebuild_rareness():
    db_tools.rebuild_rareness(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
