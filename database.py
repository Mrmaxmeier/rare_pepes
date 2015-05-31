from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pepe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.Text)
	rareness = db.Column(db.Float)
	nsfwness = db.Column(db.Float)

	def __init__(self, link):
		self.link = link
		self.rareness = 0
		self.nsfwness = 0

	def info(self):
		return {
			"link": self.link,
			"id": self.id,
			"rareness": self.rareness,
			"nsfwness": self.nsfwness
		}

	def __repr__(self):
		return "<Pepe(id={}, link={}, rareness={}, nsfwness={}>".format(self.id, self.link, self.rareness, self.nsfwness)