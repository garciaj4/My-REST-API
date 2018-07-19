from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(default=None)
    length = ndb.IntegerProperty(default=None)
    at_sea = ndb.BooleanProperty(default=True)
    slip = ndb.StringProperty(default=None)

class Slip(ndb.Model):
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty(default=None)
    arrival_date = ndb.StringProperty(default=None)

class BoatHandler(webapp2.RequestHandler):
    def post(self):
        boat_data = json.loads(self.request.body)
        b=Boat()
        if 'name' in boat_data:
            b.name = boat_data['name']
        if 'type' in boat_data:
            b.type = boat_data['type']
        if 'length' in boat_data:
            b.length = boat_data['length']
        if 'at_sea' in boat_data:
            b.at_sea = boat_data['at_sea']
        if 'slip' in boat_data:
            b.slip = boat_data['slip']
        b.put()

        boat_dict = b.to_dict()
        boat_dict['self'] = '/boat/' + b.key.urlsafe()
        self.response.write(json.dumps(boat_dict))

    def get(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get()
            b_d = b.to_dict()
            b_d['self'] = "/boat/" + id
            self.response.write(json.dumps(b_d))
        #credit to Ian Buchanan on Piazza Post for else block
        else:
            all_boats = [] 
            boat_query = Boat.query()
            boats = boat_query.fetch()
            for each_boat in boats:
                newBoat = each_boat.to_dict()
                newBoat['self'] = '/boat/' + each_boat.key.urlsafe()
                all_boats.append(newBoat)
                self.response.write(json.dumps(all_boats))

    def put(self, id=None):
        if id:
            b= ndb.Key(urlsafe=id).get()
            b.at_sea = True

            if b.slip:

                s= ndb.Key(urlsafe=b.slip).get()
                s.current_boat = None
                s.put()

                b.slip = None

            b.put()
            b = ndb.Key(urlsafe=id).get()
            b_d = b.to_dict()
            b_d['self'] = "/boat/" + id
            self.response.write(json.dumps(b_d))

    def patch(self, id=None):
        if id:
            boat_data = json.loads(self.request.body)
            b=ndb.Key(urlsafe=id).get()
            if 'name' in boat_data:
                b.name = boat_data['name']
            if 'type' in boat_data:
                b.type = boat_data['type']
            if 'length' in boat_data:
                b.length = boat_data['length']
            if 'at_sea' in boat_data:
                b.at_sea = boat_data['at_sea']
            if 'slip' in boat_data:
                b.slip = boat_data['slip']
            b.put()
            b = ndb.Key(urlsafe=id).get()
            b_d = b.to_dict()
            b_d['self'] = "/boat/" + id
            self.response.write(json.dumps(b_d))

    def delete(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get()
            ndb.Key(urlsafe=id).delete()

            if b.slip:
                s = ndb.Key(urlsafe=b.slip).get()
                s.current_boat = None
                s.put()

            b_d = b.to_dict()
            b_d['self'] = "/boat/" + id
            self.response.write(json.dumps(b_d))

class SlipHandler(webapp2.RequestHandler):
    def post(self):
        slip_data = json.loads(self.request.body)
        s=Slip()
        if 'number' in slip_data:
            s.number = slip_data['number']
        if 'current_boat' in slip_data:
            s.current_boat = slip_data['current_boat']
        if 'date' in slip_data:
            s.date = slip_data['date']
        s.put()
        slip_dict = s.to_dict()
        slip_dict['self'] = '/slip/' + s.key.urlsafe()
        self.response.write(json.dumps(slip_dict))

    def get(self, id=None):
        if id:
            s = ndb.Key(urlsafe=id).get()
            s_d = s.to_dict()
            s_d['self'] = "/slip/" + id
            self.response.write(json.dumps(s_d))
        #credit to Ian Buchanan on Piazza Post for else block
        else:
            all_slips = [] 
            slip_query = Slip.query()
            slips = slip_query.fetch()
            for each_slip in slips:
                newSlip = each_slip.to_dict()
                newSlip['self'] = '/slip/' + each_slip.key.urlsafe()
                all_slips.append(newSlip)
                self.response.write(json.dumps(all_slips))

    def put(self, id=None):
        arrival_data = json.loads(self.request.body)
        s = ndb.Key(urlsafe=id).get()
        if s.current_boat:
            self.response.set_status(403)
            self.response.write("There is already a boat occupying that slip.")
        else:
            s.current_boat = arrival_data['current_boat']
            s.arrival_date = arrival_data['arrival_date']
            s.put()

            b = ndb.Key(urlsafe=s.current_boat).get()
            b.slip = s.key.urlsafe()
            b.at_sea = False
            b.put()

            s_d = s.to_dict()
            s_d['self'] = "/slip/" + id
            self.response.write(json.dumps(s_d))

    def patch(self, id=None):
        if id:
            slip_data = json.loads(self.request.body)
            s=ndb.Key(urlsafe=id).get()
            if 'number' in slip_data:
                s.number = slip_data['number']
            if 'current_boat' in slip_data:
                s.current_boat = slip_data['current_boat']
            if 'arrival_date' in slip_data:
                s.arrival_date = slip_data['arrival_date']
            s.put()
            s_d = s.to_dict()
            s_d['self'] = "/slip/" + id
            self.response.write(json.dumps(s_d))

    def delete(self, id=None):
        if id:
            s = ndb.Key(urlsafe=id).get()
            ndb.Key(urlsafe=id).delete()

            if s.current_boat:
                b = ndb.Key(urlsafe=s.current_boat).get()
                b.slip = None
                b.at_sea = True
                b.put()

            s_d = s.to_dict()
            s_d['self'] = "/slip/" + id
            self.response.write(json.dumps(s_d))

class SlipBoatHandler(webapp2.RequestHandler):
    def get(self, sid=None):
        s = ndb.Key(urlsafe=sid).get()
        if s.current_boat:
            b = ndb.Key(urlsafe=s.current_boat).get()

            b_d = b.to_dict()
            b_d['self'] = "/boat/" + b.key.urlsafe()
            self.response.write(json.dumps(b_d))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Ships & Slips')

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START app]
app = webapp2.WSGIApplication([

    ('/', MainPage),

    ('/boat/(.*)/at_sea', BoatHandler),
    ('/boat/(.*)', BoatHandler),
    ('/boat', BoatHandler),

    ('/slip/(.*)/boat', SlipBoatHandler),

    ('/slip/(.*)', SlipHandler),
    ('/slip', SlipHandler)
], debug=True)
# [END app]
