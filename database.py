from flask.ext.sqlalchemy import SQLAlchemy
import random
import uuid
import time

db = SQLAlchemy(session_options={"expire_on_commit": False})

pending_votes = {}
last_pending_votes_change = time.time()

def check_pending():
	if last_pending_votes_change < (time.time() - 120):
		print("cleaned pending_votes")
		pending_votes.clear()

class Pepe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.Text)
	rareness = db.Column(db.Float)
	nsfw = db.Column(db.Boolean)
	md5 = db.Column(db.String(32))

	def __init__(self, link):
		self.link = link
		self.rareness = 0

	def info(self):
		return {
			"link": self.link,
			"id": self.id,
			"rareness": self.rareness,
			"nsfw": self.nsfw
		}

	@classmethod
	def get_two(cls):
		all_pepes = db.session.query(Pepe)
		r1 = random.randrange(0, all_pepes.count())
		r2 = random.randrange(1, all_pepes.count())
		if r2 <= r1: r2 -= 1
		db.session.expunge_all()
		return PepeCombination(all_pepes[r1], all_pepes[r2])

	def __repr__(self):
		return "<Pepe(id={}, link={}, rareness={}, nsfw={}>".format(self.id, self.link, self.rareness, self.nsfw)

class PepeCombination:
	def __init__(self, p1, p2):
		global last_pending_votes_change
		self.p1 = p1
		self.p2 = p2
		self.u1 = str(uuid.uuid4())
		self.u2 = str(uuid.uuid4())

		def vote(more_rare_pepe, less_rare_pepe):
			def f():
				more_rare_pepe.rareness += 1
				db.session.commit()
				if self.u1 in pending_votes:
					del pending_votes[self.u1]
				if self.u2 in pending_votes:
					del pending_votes[self.u2]
			return f

		self.v1 = vote(p1, p2)
		self.v2 = vote(p2, p1)

		check_pending()

		pending_votes[self.u1] = self.v1
		pending_votes[self.u2] = self.v2
		last_pending_votes_change = time.time()

	def info(self):
		return [
			self.p1.link, self.u1,
			self.p2.link, self.u2
		]
