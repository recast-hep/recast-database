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
  username = db.Column(db.String)
  analyses = db.relationship('Analysis',backref='owner',lazy='dynamic')

class Analysis(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  runcondition_id = db.Column(db.Integer,db.ForeignKey('run_condition.id'))
  owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
  requests = db.relationship('Request',backref='analysis',lazy='dynamic')


subscriptions = db.Table('subscriptions',
                         db.Column('subscriber_id',db.Integer,db.ForeignKey('user.id')),
                         db.Column('request_id',db.Integer,db.ForeignKey('request.id'))
                         )


class Request(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  analysis_id = db.Column(db.Integer,db.ForeignKey('analysis.id'))
  responses = db.relationship('Response', backref='request', lazy = 'dynamic')
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



# Many to many relationship between User & Analysis
#subscribers = db.Table('subscribers',
#                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#                       db.Column('analysis_id', db.Integer, db.ForeignKey('analysis.id'))
#                       )


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  analyses = db.relationship("Analysis", backref="users", lazy='dynamic')

  def __init__(self, name, email):
    self.name = name
    self.email = email

  def __repr__(self):
    return "<User(name='%s', email='%s')>" % (self.name, self.email)

class Model(db.Model):
  __tablename__ = 'models'
  id = db.Column(db.Integer, primary_key=True)
  description_of_model = db.Column(db.String, nullable=False)
  scan_requests = db.relationship("ScanRequest", backref="models", lazy='dynamic')
  point_requests = db.relationship("PointRequest", backref="models", lazy='dynamic')
  basic_requests = db.relationship("BasicRequest", backref="models", lazy='dynamic')
  scan_responses = db.relationship("ScanResponse", backref="models", lazy='dynamic')
  point_responses = db.relationship("PointResponse", backref="models", lazy='dynamic')
  basic_responses = db.relationship("BasicResponse", backref="models", lazy='dynamic')

  def __init__(self, description):
    self.descrition_of_model = description

  def __repr__(self):
    return "<Model(ID='%d', description='%s')>" % (self.id, self.description_of_model)

class Analysis(db.Model):
  __tablename__ = 'analysis'
  id = db.Column(db.Integer, primary_key=True)
  description_of_original_analysis = db.Column(db.String, nullable=False)
  scan_requests = db.relationship("ScanRequest", backref="analysis", lazy='dynamic')
  point_requests = db.relationship("PointRequest", backref="analysis", lazy='dynamic')
  basic_requests = db.relationship("BasicRequest", backref="analysis", lazy='dynamic')
  scan_responses = db.relationship("ScanResponse", backref="analysis", lazy='dynamic')
  point_responses = db.relationship("PointResponse", backref="analysis", lazy='dynamic')
  basic_responses = db.relationship("BasicResponse", backref="analysis", lazy='dynamic')
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def __init__(self, description):
    self.description_of_original_analysis = description

  def __repr__(self):
    return "<Analysis(id='%r', description='%s')>" % (self.id, self.description_of_original_analysis)


# Relationships from here on are uncomplete
# RequestNotification <-> ScanRequest: one-to-one
#   ( Not sure about what notifications mean )
#   * one scan request can have a single notification
#   * a single notification corresponds to a single scan request
class RequestNotification(db.Model):
  __tablename__ ='request_notifications'
  id = db.Column(db.Integer, primary_key=True)
  description_of_original_analysis = db.Column(db.String)
  description_of_model = db.Column(db.String)
  description_of_recast_potential = db.Column(db.String)
  scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

  def __repr__(self):
    return "RequestNotification(descriptionOfOriginalAnalysis='%s', descriptionOfModel='%s',descriptionOfRecastPotential='%s')>" %(self.description_of_original_analysis, self.description_of_model, self.description_of_recast_potential)

# Requests related tables

# Request <-> Response(Result) one-to-one
#   * one request only has a single result
#   * one result contains a single request

# ScanRequest <-> PointRequest one-to-many
#   * to implement the list functionality

# PointRequest <-> BasicRequest one-to-many
#   * to implement the list functionality

# BasicRequest <-> LHEFile : one-to-one
#    ( I am assuming ...
#   * one request will be associated with one LHE file
#   * one LHE file will be used for a single request

# Request <-> User : many-to-many 

# ScanRequest <-> Parameters : one-to-many
#   * to implement the list functionality

class ScanRequest(db.Model):
  __tablename__ = 'scan_requests'    
  id = db.Column(db.Integer, primary_key=True)
  description_of_model = db.Column(db.String)
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  scan_points = db.relationship("PointRequest", backref="scan_requests", lazy='dynamic')
  parameters = db.relationship("Parameters", backref="scan_requests", lazy='dynamic')
  subscribers = db.relationship("User", secondary=subscriptions)
  scan_responses = db.relationship("ScanResponse", uselist=False, backref="scan_requests")
  notifications = db.relationship("RequestNotication", uselist=False, backref="scan_requests")

  def __repr__(self):
    return "<ScanRequest(descriptionOfModel='%s')>" % (self.description_of_model)


class PointRequest(db.Model):
  __tablename__ = 'point_requests'    
  id = db.Column(db.Integer, primary_key=True)
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  parameter_points = db.relationship("ParameterPoint", backref="point_requests", lazy='dynamic')
  requests = db.relationship("BasicRequest", backref="point_requests", lazy='dynamic')
  point_responses = db.relationship("PointResponse", uselist=False, backref="point_requests")
  subscribers = db.relationship("User", secondary=subscriptions)

  def __repr__(self):
    return "PointRequest()>"


class BasicRequest(db.Model):
  __tablename__ = 'basic_requests'  
  id = db.Column(db.Integer, primary_key=True)
  file_name = db.relationship("LHEFile", uselist=False, backref="basic_requests")
  number_of_events = db.Column(db.Integer, nullable=False)
  reference_cross_section = db.Column(db.Integer)
  conditions_description = db.Column(db.Integer)
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  basic_responses = db.relationship("BasicResponse", backref="basic_requests", lazy='dynamic')
  subscribers = db.relationship("User", secondary=subscriptions)

  def __repr__(self):
    return "<BasicRequest(numberOfEvents='%s', referenceCrossSection='%s', conditions description='%s')>" % (self.number_of_events, self.reference_cross_section, self.conditions_description)

class ParameterPoints(db.Model):
  __tablename__ = 'parameter_points'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  value = db.Column(db.Double)
  point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))

  def __repr__(self):
    return "<ParameterPoints(title='%s', value='%s')>" % (self.title, self.value)

class Parameters(db.Model):
  __tablename__ = 'parameters'
  id = db.Column(db.Integer, primary_key=True)
  parameter = db.Column(db.Integer)
  scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

  def __repr__(self):
    return "<Parameters(parameter='%s')>" % (self.parameter)

class LHEFile(db.Model):
  __tablename__ = 'lhe_files'
  id = db.Column(db.Integer, primary_key=True)
  file_name = db.Column(db.String)
  path = db.Column(db.String)
  basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))

  def __repr__(self):
    return "<LHEFile(file name='%s', path='%s')>" % (self.file_name, self.path)

# Response related tables

class ScanResponse(db.Model):
  __tablename__ = 'scan_responses'
  id = db.Column(db.Integer, primary_key=True)
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  scan_response = db.relationship("PointResponse", backref="scan_responses", lazy='dynamic')
  scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

  def __repr__(self):
    return "<ScanResponse()>"
    
class PointResponse(db.Model):
  __tablename__ = 'point_responses'
  id = db.Column(db.Integer, primary_key=True)
  lumi_weighted_efficiency = db.Colum(db.Double)
  total_luminosity = db.Column(db.Double)
  lower_1sig_limit_on_cross_section_wrt_reference = db.Column(db.Double)
  upper_1sig_limit_on_cross_section_wrt_reference = db.Column(db.Double)
  lower_2sig_limit_on_cross_section_wrt_reference = db.Column(db.Double)
  upper_2sig_limit_on_cross_section_wrt_reference = db.Column(db.Double)
  merged_signal_template_wrt_reference = db.Column(db.PickleType)
  log_likelihood_at_reference = db.Column(db.Double)
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  basic_answers = db.relationship("BasicResponse", backref="point_responses", lazy='dynamic')
  scan_response_id = db.Column(db.Integer, db.ForeignKey('scan_responses.id'))
  point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))
                               
  def __repr__(self):
    return "<PointResponse(lumiWeightedEfficiency='%d', totalLuminosity='%d', lower1sigLimitOnCrossSectionWrtReference='%d', upper1sigLimitOnCrossSectionWrtReference='%d', lower2sigLimitOnCrossSectionWrtReference='%d', upper2sigLimitOnCrossSectionWrtReference='%d', logLikelihoodAtReference='%d')>" % \
(self.lumi_weighted_efficiency, self.total_lumininosity, self.lower_1sig_Limit)on_cross_section_wrt_reference, self.upper_1sig_limit_on_cross_section_wrt_reference, self.lower_2sig_limit_on_cross_section_wrt_reference, self.upper_2sig_limit_on_cross_section_wrt_reference, self.log_likelihood_at_reference)
    
class BasicResponse(db.Model):
  __tablename__ = 'basic_responses'
  id = db.Column(db.Integer, primary_key=True)
  overall_efficiency = db.Column(db.Double)
  nominal_luminosity = db.Column(db.Double)
  lower_1sig_limit_on_cross_section = db.Column(db.Double)
  upper_1sig_limit_on_cross_section = db.Column(db.Double)
  lower_2sig_limit_on_cross_section = db.Column(db.Double)
  upper_2sig_limit_on_cross_section = db.Column(db.Double)
  lower_1sig_on_rate = db.Column(db.Double)
  upper_1sig_on_rate = db.Column(db.Double)
  lower_2sig_limit_on_rate = db.Column(db.Double)
  upper_2sig_limit_on_rate = db.Column(db.Double)
  signal_template = db.Column(db.PickleType)
  log_likelihood_at_reference = db.Column(db.Double)
  reference_cross_section = db.Column(db.Double)
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  point_response_id = db.Column(db.Integer, db.ForeignKey('point_responses.id'))
  basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))

  def __repr__(self):
    return "<BasicResponse(overallEfficiency='%f', nominalLuminosity='%f;, \
lower1sigLimitOnCrossSection='%d', upper1sigLimitOnCrossSection='%d', lower2sigLimitOnCrossSection='%d', upper2sigLimitOnCrossSection='%d', lower1sigLimitOnRate='%d', upper1sigLimitOnRate='%d', lower2sigLimitOnRate='%d', upper2sigLimitOnRate='%d', logLikelihoodAtReference='%d', referenceCrossSection='%d')>" % \
(self.overall_efficiency, self.nominal_luminosity, self.lower_1sig_limit_on_cross_section, self.upper_1sig_limit_on_cross_section, self.lower_2sig_limit_on_cross_section, self.upper_2sig_limit_on_cross_section, self.lower_1sig_limit_on_rate, self.upper_1sig_limit_on_rate, self.lower_2sig_limit_on_rate, self.upper_2sig_limit_on_rate, self.log_likelihood_at_reference, self.reference_cross_section)
