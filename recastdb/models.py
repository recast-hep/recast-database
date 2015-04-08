# relations
# Analysis <-> Run Condition: one-to-many
#   * an analysis is always for a single run condition (yes? combined analyses? 7+8 TeV?)
#   * there are many analyses for a single run condition (say all Run 1 analyses)
#
# Analysis <-> Owner (User): one-to-many
#   * an analysis has always one owner
#   * one user can own multiple analyses
#
# Analysis <-> Request: one-to-many
#   * a request is always for a single analysis
#   * an analysis can have multiple requests
#
# Request <-> Result: one-to-one
#   * one request can only have a single result
#   * one result is always to a single request
#
# Request <-> Parameter Points: one-to-many
#   * one request can have multiple parameter points
#   * a parameter point is related to a single request (yes? multiple MSSM analyses?)
#
# Request <-> Subscriber (User): many-to-many:
#   * a request can have multiple subscribers
#   * a user can be subscribed to multiple requests
#

# class RunCondition(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#
# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#
# class Analysis(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#
# class Request(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#
# class ParameterPoint(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#
# class Response(db.Model):
#   id = db.Column(db.Integer, primary_key=True)

from database import db

class Processing(db.Model):
  """ this is an actual request to process the recast request """
  id = db.Column(db.Integer, primary_key = True)
  jobguid = db.Column(db.String(36), unique = True)
  chainresult = db.Column(db.String(36), unique = True)


  