""" Class to represent a ScanRecord object. Each instance represents
     one scan of a single visitor's wristband at a particular exhibit """

from google.appengine.ext import db

class ScanRecord(db.Model):
    visitor_id = db.IntegerProperty(required=True)
    exhibit_name = db.StringProperty(required=True)
    scan_time = db.DateTimeProperty(auto_now_add=True)