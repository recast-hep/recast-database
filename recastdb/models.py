from database import db

# relations
# Analysis <-> Run Condition: many-to-one
#   * an analysis is always for a single run condition (yes? combined analyses? 7+8 TeV?)
#   * there are many analyses for a single run condition (say all Run 1 analyses)
#
# Analysis <-> Owner (User): many-to-one
#   * an analysis has always one owner
#   * one user can own multiple analyses
#
# Analysis <-> Request: one-to-many
#   * a request is always for a single analysis
#   * an analysis can have multiple requests
#
# Request <-> Result: one-to-(zero or one) .. implemented as one-to-many...
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

class RunCondition(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  analyses = db.relationship('Analysis',backref='runcondition',lazy='dynamic')

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  analyses = db.relationship('Analysis',backref='owner',lazy='dynamic')

class Analysis(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  runcondition_id = db.Column(db.Integer,db.ForeignKey('run_condition.id'))
  owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
  requests = db.relationship('Request',backref='analysis',lazy='dynamic')


subscriptions = db.Table('subscriptions',
                         db.Column('subscriber_id',db.Integer,db.ForeignKey('user.id')),
                         db.Column('reqeust_id',db.Integer,db.ForeignKey('request.id'))
                         )


class Request(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  analysis_id = db.Column(db.Integer,db.ForeignKey('analysis.id'))
  responses = db.relationship('Response', backref='request')
  parameter_points = db.relationship('ParameterPoint',backref = 'request',lazy='dynamic')
  subscribers = db.relationship('User',secondary=subscriptions)
  
  
class ParameterPoint(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  request_id = db.Column(db.Integer,db.ForeignKey('request.id'))

class Response(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  request_id = db.Column(db.Integer,db.ForeignKey('request.id'))

class Processing(db.Model):
  """ this is an actual request to process the recast request """
  id            = db.Column(db.Integer, primary_key = True)
  jobguid       = db.Column(db.String(36), unique = True)
  celerytaskid  = db.Column(db.String(36), unique = True)
