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
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	link = db.Column(db.Text)
	rareness = db.Column(db.Float)
	visits = db.Column(db.Integer)
	nsfw = db.Column(db.Boolean)
	md5 = db.Column(db.String(32))
	origin = db.Column(db.Text)

	def __init__(self, link):
		self.link = link
		self.rareness = 0
		self.visits = 0

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
		if r2 <= r1:
			r2 -= 1
		db.session.expunge_all()
		return PepeCombination(all_pepes[r1], all_pepes[r2])

	@classmethod
	def rarest(cls):
		return cls.query.order_by(cls.rareness.desc()).first()

	@classmethod
	def least_rare(cls):
		return cls.query.first()

	@classmethod
	def most_controversial(cls, num=10):
		q = cls.query
		#q = q.order_by(cls.rareness)
		#qc = q.count()
		#q = q.slice(qc//2 - num, qc//2 + num)
		return sorted(q.all(), key=lambda p: p.visits * abs(0.5 - p.rareness))[-num:][::-1]

	def __repr__(self):
		return "<Pepe(id={}, link={}, rareness={}, visits={}, nsfw={}>".format(\
			self.id, self.link, self.rareness, self.visits, self.nsfw)

class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	voted_pepe_id = db.Column(db.Integer, db.ForeignKey("pepe.id"))
	# voted_pepe = db.relationship("Pepe", foreign_keys=[voted_pepe_id])
	other_pepe_id = db.Column(db.Integer, db.ForeignKey("pepe.id"))
	# other_pepe = db.relationship("Pepe", foreign_keys=[other_pepe_id])
	timestamp = db.Column(db.DateTime, server_default=db.func.now())

	def execute(self):
		## dont query for votes!
		more_rare_pepe = Pepe.query.get(self.voted_pepe_id)
		more_rare_pepe.rareness += 1
		less_rare_pepe = Pepe.query.get(self.other_pepe_id)
		more_rare_pepe.visits += 1
		less_rare_pepe.visits += 1

	def __repr__(self):
		return "<Vote(voted_pepe_id={}, other_pepe_id={}>".format(self.voted_pepe_id, self.other_pepe_id)

class PepeCombination:
	def __init__(self, p1, p2):
		global last_pending_votes_change
		self.p1 = p1
		self.p2 = p2
		self.u1 = str(uuid.uuid4())
		self.u2 = str(uuid.uuid4())

		def vote(more_rare_pepe_id, less_rare_pepe_id):
			def f():
				v = Vote(voted_pepe_id=more_rare_pepe_id, other_pepe_id=less_rare_pepe_id)
				print(v)
				v.execute()
				db.session.add(v)
				db.session.commit()
				if self.u1 in pending_votes:
					del pending_votes[self.u1]
				if self.u2 in pending_votes:
					del pending_votes[self.u2]
			return f

		self.v1 = vote(p1.id, p2.id)
		self.v2 = vote(p2.id, p1.id)

		check_pending()

		pending_votes[self.u1] = self.v1
		pending_votes[self.u2] = self.v2
		last_pending_votes_change = time.time()

	def info(self):
		return [
			self.p1.link, self.u1,
			self.p2.link, self.u2
		]
