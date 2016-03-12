from database import db
from sqlalchemy.ext.hybrid import hybrid_property
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

class CommonColumns(db.Model):
  __abstract__ = True
  _created = db.Column(db.DateTime, default=db.func.now())
  _updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
  _etag = db.Column(db.String(40))

  @hybrid_property
  def _id(self):
    return self.id
  
class User(CommonColumns):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, unique=False)
  orcid_id = db.Column(db.String, unique=True)
  access_tokens = db.relationship('AccessToken', backref='user', lazy='dynamic')
  analyses = db.relationship('Analysis', backref='user', lazy='dynamic')
  requests = db.relationship('ScanRequest', backref='requester', lazy='dynamic')
  point_requests = db.relationship('PointRequest', backref='user', lazy='dynamic')
  basic_requests = db.relationship('BasicRequest', backref='user', lazy='dynamic')
  subscriptions = db.relationship('Subscription', backref='subscriber', lazy='dynamic')

  def __repr__(self):
    return "<User(name='%s', email='%s', orcid_id='%s')>" % (self.name, self.email, self.orcid_id)

class AccessToken(db.Model):
  __tablename__ = 'access_tokens'
  id = db.Column(db.Integer, primary_key=True)
  token = db.Column(db.String, unique=True)
  token_name = db.Column(db.String, unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
  def __repr__(self):
    return "<AccessToken(token='%s', user_id='%s')>" % (self.token, self.user_id)

class Analysis(CommonColumns):
  __tablename__ = 'analysis'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  collaboration = db.Column(db.String)
  e_print = db.Column(db.String)
  journal = db.Column(db.String)
  doi = db.Column(db.String)
  inspire_URL = db.Column(db.String)
  description = db.Column(db.Text)
  scan_requests = db.relationship('ScanRequest', backref='analysis', lazy='dynamic')
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  run_condition_id = db.Column(db.Integer, db.ForeignKey('run_conditions.id'))
  subscriptions = db.relationship('Subscription', backref='analysis', lazy='dynamic')

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<Analysis(title='%s', collaboration='%s', e_print='%s', journal='%s', doi='%s', inspire_URL='%s', description='%s', owner='%r')>" % (self.title, self.collaboration, self.e_print, self.journal, self.doi, self.inspire_URL, self.description, self.owner_id)

class Subscription(CommonColumns):
  __tablename__ = 'subscriptions'
  id = db.Column(db.Integer, primary_key=True)
  subscription_type = db.Column(db.String)
  description = db.Column(db.Text)
  requirements = db.Column(db.Text)
  notifications = db.Column(db.String)
  authoritative = db.Column(db.Boolean, default=False)
  subscriber_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<Subscription(subscription_type='%s', description='%s', requirements='%s', notifications='%s', authoritative='%s')>" % (self.subscription_type, self.description, self.requirements, self.notifications, self.authoritative)

class RunCondition(CommonColumns):
  __tablename__ = 'run_conditions'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String)
  description = db.Column(db.String)
  analyses = db.relationship('Analysis',backref='run_condition',lazy='dynamic')

  @hybrid_property
  def _id(self):
    return self.id  
  
  def __repr__(self):
    return "<RunCondition(name='%s', description='%s')>" % (self.name, self.description)

class Processing(CommonColumns):
  """ this is an actual request to process the recast request """
  __tablename__ = 'processing'
  id            = db.Column(db.Integer, primary_key = True)
  jobguid       = db.Column(db.String(36), unique = True)
  celerytaskid  = db.Column(db.String(36), unique = True)
  
  @hybrid_property
  def _id(self):
    return self.id
  
  def __repr__(self):
    return "<Processing(job uid='%r', celery task id='%r')>" % (self.jobuid, self.celerytaskid)

class Model(CommonColumns):
  __tablename__ = 'models'
  id = db.Column(db.Integer, primary_key=True)
  description_of_model = db.Column(db.String, nullable=True)
  scan_requests = db.relationship('ScanRequest', backref='model', lazy='dynamic')
  point_requests = db.relationship('PointRequest', backref='model', lazy='dynamic')
  basic_requests = db.relationship('BasicRequest', backref='model', lazy='dynamic')
  scan_responses = db.relationship('ScanResponse', backref='model', lazy='dynamic')
  point_responses = db.relationship('PointResponse', backref='model', lazy='dynamic')
  basic_responses = db.relationship('BasicResponse', backref='model', lazy='dynamic')
    
  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<Model(description='%s')>" % (self.description_of_model)

# RequestNotification <-> ScanRequest: one-to-one
#   ( Not sure about what notifications mean )
#   * one scan request can have a single notification
#   * a single notification corresponds to a single scan request

class RequestNotification(CommonColumns):
  __tablename__ ='request_notifications'
  id = db.Column(db.Integer, primary_key=True)
  description_of_original_analysis = db.Column(db.String)
  description_of_model = db.Column(db.String)
  description_of_recast_potential = db.Column(db.String)
  scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

  @hybrid_property
  def _id(self):
    return self.id
                                  
  def __repr__(self):
    return "RequestNotification(descriptionOfOriginalAnalysis='%s', descriptionOfModel='%s',descriptionOfRecastPotential='%s')>" %(self.description_of_original_analysis, self.description_of_model, self.description_of_recast_potential)

# Requests related tables

# Request <-> Response(Result) one-to-one
#   * one request only has a single result
#   * one result from  a single request

# ScanRequest <-> PointRequest one-to-many
#   * to implement the list functionality

# PointRequest <-> BasicRequest one-to-many
#   * to implement the list functionality

# BasicRequest <-> ZipFile : one-to-many
#   * one request might be associated with many Zip files
#   * Zip file will be used for a single request

# Request <-> Subscribers : many-to-many 

# ScanRequest <-> Parameters : one-to-many
#   * to implement the list functionality

# PointResponse <-> Histogram: one-to-many
#   * a response can have many histograms

# BasicResponse <-> Histogram: one-to-many

class ScanRequest(CommonColumns):
  __tablename__ = 'scan_requests'    
  id = db.Column(db.Integer, primary_key=True)
  description_of_model = db.Column(db.String)
  reason_for_request = db.Column(db.Text)
  additional_information = db.Column(db.Text)
  status = db.Column(db.Text, default="Incomplete")
  post_date = db.Column(db.Date)
  zenodo_deposition_id = db.Column(db.String)
  uuid = db.Column(db.String)
  analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  scan_points = db.relationship('PointRequest', backref='scan_request', lazy='dynamic')
  parameters = db.relationship('Parameters', backref='scan_request', lazy='dynamic')
  scan_responses = db.relationship('ScanResponse', uselist=False, backref='scan_request')
  notifications = db.relationship('RequestNotification', uselist=False, backref='scan_request')
  requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<ScanRequest(descriptionOfModel='%s')>" % (self.description_of_model)

class PointRequest(CommonColumns):
  __tablename__ = 'point_requests'    
  id = db.Column(db.Integer, primary_key=True)
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  parameter_points = db.relationship('ParameterPoint', backref='point_request', lazy='dynamic')
  requests = db.relationship('BasicRequest', backref='point_request', lazy='dynamic')
  point_responses = db.relationship('PointResponse', uselist=False, backref='point_request')
  scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))
  requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "PointRequest()>"

class BasicRequest(CommonColumns):
  __tablename__ = 'basic_requests'  
  id = db.Column(db.Integer, primary_key=True)
  file_name = db.relationship('ZipFile', backref='basic_request', lazy='dynamic')
  conditions_description = db.Column(db.Integer)
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  basic_responses = db.relationship('BasicResponse', backref='basic_request', lazy='dynamic')
  point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))
  requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<BasicRequest(conditions description='%s')>" % (self.conditions_description)

class ParameterPoint(CommonColumns):
  __tablename__ = 'parameter_points'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  value = db.Column(db.Float)
  point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<ParameterPoints(title='%s', value='%s')>" % (self.title, self.value)

class Parameters(CommonColumns):
  __tablename__ = 'parameters'
  id = db.Column(db.Integer, primary_key=True)
  parameter = db.Column(db.Integer)
  scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<Parameters(parameter='%s')>" % (self.parameter)

class ZipFile(CommonColumns):
  __tablename__ = 'zip_files'
  id = db.Column(db.Integer, primary_key=True)
  file_name = db.Column(db.String) #uuid
  path = db.Column(db.String)
  doi = db.Column(db.String)    #Digital Object Identifier
  zenodo_file_id = db.Column(db.String)
  original_file_name = db.Column(db.String) # original filename since file is renamed to uuid
  basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<ZipFile(file name='%s', path='%s', doi='%s')>" % (self.file_name, self.path, self.doi)

# Response related tables

class ScanResponse(CommonColumns):
  __tablename__ = 'scan_responses'
  id = db.Column(db.Integer, primary_key=True)
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  scan_response = db.relationship('PointResponse', backref='scan_response', lazy='dynamic')
  scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<ScanResponse()>"
    
class PointResponse(CommonColumns):
  __tablename__ = 'point_responses'
  id = db.Column(db.Integer, primary_key=True)
  lumi_weighted_efficiency = db.Column(db.Float, nullable=False)
  total_luminosity = db.Column(db.Float)
  lower_1sig_limit_on_cross_section_wrt_reference = db.Column(db.Float)
  upper_1sig_limit_on_cross_section_wrt_reference = db.Column(db.Float)
  lower_2sig_limit_on_cross_section_wrt_reference = db.Column(db.Float)
  upper_2sig_limit_on_cross_section_wrt_reference = db.Column(db.Float)
  merged_signal_template_wrt_reference = db.relationship('Histogram', backref='point_response', lazy='dynamic')
  log_likelihood_at_reference = db.Column(db.Float)
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  basic_answers = db.relationship('BasicResponse', backref='point_response', lazy='dynamic')
  scan_response_id = db.Column(db.Integer, db.ForeignKey('scan_responses.id'))
  point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))

  @hybrid_property
  def _id(self):
    return self.id
                               
  def __repr__(self):
    return "<PointResponse(lumiWeightedEfficiency='%r', totalLuminosity='%r', lower1sigLimitOnCrossSectionWrtReference='%r', upper1sigLimitOnCrossSectionWrtReference='%r', lower2sigLimitOnCrossSectionWrtReference='%r', upper2sigLimitOnCrossSectionWrtReference='%r', logLikelihoodAtReference='%r')>" % \
(self.lumi_weighted_efficiency, self.total_lumininosity, self.lower_1sig_Limit_on_cross_section_wrt_reference, self.upper_1sig_limit_on_cross_section_wrt_reference, self.lower_2sig_limit_on_cross_section_wrt_reference, self.upper_2sig_limit_on_cross_section_wrt_reference, self.log_likelihood_at_reference)
    
class BasicResponse(CommonColumns):
  __tablename__ = 'basic_responses'
  id = db.Column(db.Integer, primary_key=True)
  overall_efficiency = db.Column(db.Float)
  nominal_luminosity = db.Column(db.Float)
  lower_1sig_limit_on_cross_section = db.Column(db.Float)
  upper_1sig_limit_on_cross_section = db.Column(db.Float)
  lower_2sig_limit_on_cross_section = db.Column(db.Float)
  upper_2sig_limit_on_cross_section = db.Column(db.Float)
  lower_1sig_limit_on_rate = db.Column(db.Float)
  upper_1sig_limit_on_rate = db.Column(db.Float)
  lower_2sig_limit_on_rate = db.Column(db.Float)
  upper_2sig_limit_on_rate = db.Column(db.Float)
  signal_template = db.relationship('Histogram', backref='basic_response', lazy='dynamic')
  log_likelihood_at_reference = db.Column(db.Float)
  reference_cross_section = db.Column(db.Float)
  model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
  point_response_id = db.Column(db.Integer, db.ForeignKey('point_responses.id'))
  basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<BasicResponse(overallEfficiency='%f', nominalLuminosity='%f', \
lower1sigLimitOnCrossSection='%r', upper1sigLimitOnCrossSection='%r', lower2sigLimitOnCrossSection='%r', upper2sigLimitOnCrossSection='%r', lower1sigLimitOnRate='%r', upper1sigLimitOnRate='%r', lower2sigLimitOnRate='%r', upper2sigLimitOnRate='%r', logLikelihoodAtReference='%r', referenceCrossSection='%r')>" % \
(self.overall_efficiency, self.nominal_luminosity, self.lower_1sig_limit_on_cross_section, self.upper_1sig_limit_on_cross_section, self.lower_2sig_limit_on_cross_section, self.upper_2sig_limit_on_cross_section, self.lower_1sig_limit_on_rate, self.upper_1sig_limit_on_rate, self.lower_2sig_limit_on_rate, self.upper_2sig_limit_on_rate, self.log_likelihood_at_reference, self.reference_cross_section)

class Histogram(CommonColumns):
  __tablename__ = 'histograms'
  id = db.Column(db.Integer, primary_key=True)
  file_name = db.Column(db.String)
  file_path = db.Column(db.String)
  histo_name = db.Column(db.String)
  histo_path = db.Column(db.String)
  point_response_id = db.Column(db.Integer, db.ForeignKey('point_responses.id'))
  basic_response_id = db.Column(db.Integer, db.ForeignKey('basic_responses.id'))

  @hybrid_property
  def _id(self):
    return self.id

  def __repr__(self):
    return "<Histogram(file_name='%s', file_path='%s', histo_name='%s', histo_path='%s')>" % (self.file_name, self.file_path, self.histo_name, self.histo_path)
