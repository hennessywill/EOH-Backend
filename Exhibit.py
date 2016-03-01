""" Class to represent an Exhibit object """

from google.appengine.ext import db

class Exhibit(db.Model):
    name = db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    department = db.StringProperty()
    building = db.StringProperty(required=True)
    room_number = db.StringProperty()
    address = db.StringProperty(required=True)
    url = db.StringProperty()

    def getJson(self):
        return {"name":self.name,
                "description":self.description,
                "department":self.department,
                "building":self.building,
                "room":self.room_number,
                "address":self.address,
                "url":self.url
                }