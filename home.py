from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.StringProperty()
    length = ndb.IntegerProperty()
    at_sea = ndb.BooleanProperty()

class BoatHandler(webapp2.RequestHandler):
    def post(self):
        boat_data = json.loads(self.request.body) 
        new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'], at_sea=boat_data['at_sea'])
        new_boat.put()
        boat_dict = new_boat.to_dict()
        boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
        self.response.write(json.dumps(boat_dict))

    def get(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get()
            b_d = b.to_dict()
            b_d['self'] = "/boat/" + id
            self.response.write(json.dumps(b.to_dict()))
        else:
            all_boats = [] 
            boat_query = Boat.query()
            boats = boat_query.fetch()
            for each_boat in boats:
                newBoat_d = each_boat.to_dict()
                all_boats.append(newBoat_d)
                #boats_d = all_boats.to_dict()
                self.response.write(json.dumps(all_boats))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('hello')

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', BoatHandler),
    ('/boat/(.*)', BoatHandler)
], debug=True)
# [END app]
