album = "U2dTR"

from imgurpython import ImgurClient
from time import sleep
from database import db, Pepe
import os

c_id = os.environ.get("IMGUR_ID")
c_secret = os.environ.get("IMGUR_SECRET")

client = ImgurClient(c_id, c_secret)

def main(app):
	with app.app_context():
		print("dropping...")
		db.drop_all()
		print("creating structure...")
		db.create_all()
	for i, img in enumerate(client.get_album_images(album)):
		pepe = Pepe(link=img.link)
		db.session.add(pepe)
		if i%100==0:
			print("comitting")
			db.session.commit()
		print(pepe)
		#sleep(1)
	db.session.commit()
