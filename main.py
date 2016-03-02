#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# author Will Hennessy

import webapp2
import os
import jinja2
import json
import csv
from Exhibit import Exhibit

from google.appengine.ext import db
from google.appengine.api import memcache

ALL_EXHIBITS_JSON_KEY = "allexhibitsjson"

ADDRESSES = {
    "Altgeld Hall":"1409 West Green Street, Urbana, IL 61801",
    "Bardeen Quad":"40.111709,-88.227028",
    "Ceramics Building":"105 S Goodwin Ave, Urbana, IL 61801",
    "Coordinated Science Laboratory":"1308 West Main Street, Urbana, IL 61801",
    "Digital Computer Lab":"1304 West Springfield, Urbana, IL 61801, United States",
    "Engineering Hall":"1308 West Green Street, Urbana, IL 61801",
    "Electrical and Computer Engineering Building":"40.114974,-88.227787",
    "ESPL Lot":"40.111799,-88.222469",
    "Everitt Lab":"1406 West Green Street, Urbana, IL 61801",
    "Hydrosystems Lab":"301 North Mathews Avenue, Urbana, IL 61801",
    "Loomis Lab":"1110 W Green Street, Urbana, IL, United States",
    "Mechanical Engineering Lab":"105 South Mathews Avenue, Urbana, IL 61801",
    "Micro and Nanotechnology Lab":"208 North Wright Street, Urbana, IL 61801",
    "MatSE Building":"1304 West Green Street, Urbana, IL 61801",
    "Newmark Hall":"205 North Mathews Avenue, Urbana, IL 61801",
    "Siebel Center":"201 N Goodwin Ave, Urbana, IL, United States",
    "Talbot Lab":"104 S Wright St, Urbana, IL, United States",
    "Transportation Building":"104 South Mathews Avenue, Urbana, IL 61801",
    "Utilities Production": "40.115130,-88.226195"
}


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                    autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class MainHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def get(self):
        self.render('home.html')


class ExhibitsJSONHandler(MainHandler):
    def exhibits_list_to_json(self, exhibits):
        output = [ e.getJson() for e in exhibits ]
        result = '{"results":' + json.dumps(output) + '}'
        return result

    def get(self):
        self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
        # check if the Exhibits json is already in cache. Query db if necessary.
        json = memcache.get(ALL_EXHIBITS_JSON_KEY)
        if json is None:
            exhibits = db.GqlQuery("SELECT * FROM Exhibit ORDER BY name ASC")
            json = self.exhibits_list_to_json(exhibits=exhibits)
            memcache.set(ALL_EXHIBITS_JSON_KEY, json)

        self.response.out.write(json)



 ## Script used to parse data from "templates/exhibits_db.txt"
 ## and put it into the database. Export from Excel as a tab-delimited txt file
 class UpdateDbFromFile(MainHandler):
     def get(self):
         data = list(csv.reader(open("templates/exhibits_db.txt", 'rU'), dialect=csv.excel_tab, delimiter='\t'))
         detectedError = False
         for row in data:
             if row[0] == "%%%%":
                 break
             try:
                 e = Exhibit(name=row[0],
                             description=row[3],
                             department=row[4],
                             building=row[1],
                             room_number=row[2],
                             address=ADDRESSES[row[1]],
                             url=row[5]
                            )
                 e.put()
             except UnicodeDecodeError:
                 self.response.out.write("<p>Error: "+row[0]+" - bad character not in ascii range</p>")
                 detectedError = True

         if not detectedError:
             self.response.out.write("Success: uploaded all the exhibits into the database.")


# ## Script to delete all exhibit entities in the database. Useful to use before udpating db.
 class DeleteAllExhibitsDb(MainHandler):
     def get(self):
         db.delete(Exhibit.all())
         self.response.out.write("Success: all exhibits deleted from the database.")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/exhibits.json', ExhibitsJSONHandler)
    # ,('/private/update_db', UpdateDbFromFile)
    # ,('/private/delete_exhibits', DeleteAllExhibitsDb)
], debug=True)
