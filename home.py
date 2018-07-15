from google.appengine.ext import ndb
import webapp2
import json

# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        

# [END main_page]

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
# [END app]
