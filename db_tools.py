from imgurpython import ImgurClient
from time import sleep
from database import db, Pepe
from sqlalchemy import func
import requests
import os
import hashlib

c_id = os.environ.get("IMGUR_ID")
c_secret = os.environ.get("IMGUR_SECRET")

client = ImgurClient(c_id, c_secret)

unsaved_actions = 0

def save_if_due():
	global unsaved_actions
	unsaved_actions += 1
	if unsaved_actions >= 100:
		unsaved_actions = 0
		print("saving")
		db.session.commit()

def add_from_img(img):
	pepe = Pepe(link=img.link)
	if 1.5 > img.width / img.height > 0.5:
		print("Wrong aspect ratio")
		return
	if img.nsfw:
		pepe.nsfw = True
	pepe.rareness -= img.views * 0.0001
	db.session.add(pepe)
	save_if_due()
	print(pepe)


def build_db(app):
	with app.app_context():
		print("dropping...")
		db.drop_all()
		print("creating structure...")
		db.create_all()

	for album in ["U2dTR"]:
		for img in client.get_album_images(album):
			add_from_img(img)
			#sleep(1)
	db.session.commit()

def get_md5s(app):
	print("Downloading", Pepe.query.filter(Pepe.md5 == None).count(), "pepes...")
	rs = []
	try:
		for pepe in Pepe.query.filter(Pepe.md5 == None).all():
			r = requests.get(pepe.link)
			md5 = hashlib.md5(r.content).hexdigest()
			pepe.md5 = md5
			print("Got pepe", pepe.id, md5)
			save_if_due()
			sleep(0.5)
	except KeyboardInterrupt:
		print("KeyboardInterrupt; saving to db")
	finally:
		db.session.commit()

def deduplicate(app):
	print("Deduplicating", Pepe.query.filter(Pepe.md5 != None).count(), "pepes...")
	q = Pepe.query.filter(Pepe.md5.in_(
			db.session.query(Pepe.md5)\
					.group_by(Pepe.md5)\
					.having(func.count(Pepe.md5) > 1)
	))
	for pepe in q.all():
		if Pepe.query.filter(Pepe.md5 == pepe.md5).count() > 1:
			print("Duplicate found", pepe)
			db.session.delete(pepe)
			save_if_due()
	db.session.commit()
