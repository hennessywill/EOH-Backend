""" A class to represent a Restaurant object """

from google.appengine.ext import db

class Restaurant(db.Model):
    name = db.StringProperty(required=True)
    category = db.StringProperty(required=True)
    menu = db.StringProperty(required=True)

    def getJson(self):
        return {"name":self.name,
                "category":self.category,
                "menu":self.menu }