""" Class to represent an Visitor object """

from google.appengine.ext import db

class Visitor(db.Model):
    visitor_id = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)