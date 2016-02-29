from google.appengine.ext import db
#Used for storing user intercation log data
class GetResultLog(db.Model):
    startTime = db.DateTimeProperty(required = True)
    endTime = db.DateTimeProperty()
    errorMessage = db.StringProperty(required = True)
    returnedLink = db.TextProperty()

class InteractionLog(db.Model):
    clickTime = db.DateTimeProperty()
    errorMessage = db.StringProperty()
    clickedLink = db.TextProperty()
    isHelpful = db.BooleanProperty()
