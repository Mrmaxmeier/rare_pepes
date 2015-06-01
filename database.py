from flask.ext.sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

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
		return all_pepes[r1], all_pepes[r2]

	def __repr__(self):
		return "<Pepe(id={}, link={}, rareness={}, nsfw={}>".format(self.id, self.link, self.rareness, self.nsfw)