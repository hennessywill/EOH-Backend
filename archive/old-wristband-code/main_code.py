from ScanRecord import ScanRecord
from Visitor import Visitor

SCAN_PASSWORD = "weloveeoh"
VISITOR_REGISTER_PASSWORD = "uiuceoh2014"

class PostScanHandler(MainHandler):
	""" API endpoint to post a scan to the database """
    def get(self):
        #self.render("postscan.html") # html form you can use for testing
        self.redirect("/")

    def post(self):
        visitor_id = int( self.request.get("visitor_id") )
        exhibit_name = self.request.get("exhibit_name")
        password = self.request.get("password")

        if visitor_id and exhibit_name and password == SCAN_PASSWORD:
            scan = ScanRecord(visitor_id=visitor_id, exhibit_name=exhibit_name)
            scan.put()
        else:
            print "EOH Error: invalid password, id_number, or exhibit_name in scan post"



class RegisterVisitorIdHandler(MainHandler):
    """ API endpoint to post a visitor ID registration """
    def get(self):
        self.render("registervisitor.html")

    def post(self):
        try:
            visitor_id = int( self.request.get("visitor_id") )
        except ValueError:
            visitor_id = None
        name = self.request.get("name")
        email = self.request.get("email")

        if visitor_id and name and email:
            # TODO: compare email to regex
            visitor = Visitor(visitor_id=visitor_id, name=name, email=email)
            visitor.put()
            self.response.out.write("Thank you for registering, " + name + "!")
        else:
            self.render("registervisitor.html", error="Invalid field entries.")


# add
#       ('/api/post_scan', PostScanHandler),
#       ('/api/register_visitor_id', RegisterVisitorIdHandler),
# to the webapp2.WSGIApplication call at the bottom of main.py
