from Restaurant import Restaurant

class AddRestaurantHandler(MainHandler):
	""" Renders a simple html form to add a restaurant to the database
		This was used for testing. You probably don't have a reason to make
		this public for production. """
    def get(self):
        self.render('addrestaurant.html')

    def post(self):
        name = self.request.get('name')
        category = self.request.get('category')
        menu = self.request.get('menu')

        if name and category and menu:
            r = Restaurant(name=name, category=category, menu=menu)
            r.put() # put this exhibit in the database
            self.render('addrestaurant.html', success="Restaurant submitted!")
        else:
            self.render('addrestaurant.html', error="Please enter a name, food category, and menu url.",
                            name=name, category=category, menu=menu)


class RestaurantsJSONHandler(MainHandler):
	""" API call that returns a JSON of all restaurants """
    def get(self):
        self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
        output = []
        restaurants = db.GqlQuery("SELECT * FROM Restaurant ORDER BY name ASC")
        for r in restaurants:
            output.append( r.getJson() )
        self.response.out.write( json.dumps(output) )


# add
#    ('/api/restaurants.json', RestaurantsJSONHandler),
# to the app = webapp2.WSGIApplication( list at the bottom of main.py
