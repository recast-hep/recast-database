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
        return "<User(name='%s', email='%s', orcid_id='%s')>" % (
    	  self.name,
    	  self.email,
    	  self.orcid_id
    	)
	
class AccessToken(db.Model):
    __tablename__ = 'access_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    token_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<AccessToken(token='%s', user_id='%s')>" % (
    	  self.token,
    	  self.user_id
    	)

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

    def __repr__(self):
        return "<Analysis(title='%s',\
        collaboration='%s',\
        e_print='%s',\
        journal='%s',\
        doi='%s',\
        inspire_URL='%s',\
        description='%s',\
        owner='%r')>" % (
          self.title,
          self.collaboration,
          self.e_print,
          self.journal,
          self.doi, 
          self.inspire_URL,
          self.description,
          self.owner_id
        )

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

    def __repr__(self):
        return "<Subscription(subscription_type='%s',\
        description='%s',\
        requirements='%s',\
        notifications='%s',\
        authoritative='%s')>" % (
          self.subscription_type, 
          self.description, 
          self.requirements, 
          self.notifications, 
          self.authoritative
        )

class RunCondition(CommonColumns):
    __tablename__ = 'run_conditions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    analyses = db.relationship('Analysis',backref='run_condition',lazy='dynamic')

    def __repr__(self):
        return "<RunCondition(name='%s', description='%s')>" % (
          self.name, 
          self.description
        )
  
class Processing(CommonColumns):
    """ this is an actual request to process the recast request """
    __tablename__ = 'processing'
    id            = db.Column(db.Integer, primary_key = True)
    jobguid       = db.Column(db.String(36), unique = True)
    celerytaskid  = db.Column(db.String(36), unique = True)

    def __repr__(self):
        return "<Processing(job uid='%r', celery task id='%r')>" % (
          self.jobuid, 
          self.celerytaskid
        )

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

    def __repr__(self):
        return "<Model(description='%s')>" % (
          self.description_of_model
        )

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
                                  
    def __repr__(self):
        return "RequestNotification(descriptionOfOriginalAnalysis='%s',\
        descriptionOfModel='%s',\
        descriptionOfRecastPotential='%s')>" % (
          self.description_of_original_analysis,
          self.description_of_model,
          self.description_of_recast_potential
        )
  
# Requests related tables

# Request <-> Response(Result) one-to-one
#   * one request only has a single result
#   * one result from  a single request

# ScanRequest <-> PointRequest one-to-many
#   * to implement the list functionality

# PointRequest <-> BasicRequest one-to-many
#   * to implement the list functionality

# BasicRequest <-> RequestArchive : one-to-many
#   * one request might be associated with many Archive files
#   * Archive file will be used for a single request

# Request <-> Subscribers : many-to-many 

# ScanRequest <-> Parameters : one-to-many
#   * to implement the list functionality

# PointResponse <-> ResponseArchive: one-to-many
#   * a response can have many ResponseArchive

# BasicResponse <-> ResponseArchive: one-to-many

class ScanRequest(CommonColumns):
    __tablename__ = 'scan_requests'    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description_of_model = db.Column(db.String)
    reason_for_request = db.Column(db.Text)
    additional_information = db.Column(db.Text)
    status = db.Column(db.Text, default="Incomplete")
    post_date = db.Column(db.Date, default=db.func.current_date())
    zenodo_deposition_id = db.Column(db.String)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    scan_points = db.relationship('PointRequest', backref='scan_request', lazy='dynamic')
    parameters = db.relationship('Parameters', backref='scan_request', lazy='dynamic')
    scan_responses = db.relationship('ScanResponse', uselist=False, backref='scan_request')
    notifications = db.relationship('RequestNotification', uselist=False, backref='scan_request')
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<ScanRequest(tilte='%s',\
        description of model='%s',\
        reason_for_request='%s',\
        additional_information='%s',\
        status='%s',\
        post_date='%r',\
        zenodo_deposition_id='%r',\
        analysis_id='%r')>" % (
          self.title,
          self.description_of_model,
          self.reason_for_request,
          self.additional_information,
          self.status,
          self.post_date,
          self.zenodo_deposition_id,
          self.analysis_id
        )
  
class PointRequest(CommonColumns):
    __tablename__ = 'point_requests'    
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    point_coordinates = db.relationship('PointCoordinate', backref='point_request', lazy='dynamic')
    requests = db.relationship('BasicRequest', backref='point_request', lazy='dynamic')
    point_responses = db.relationship('PointResponse', uselist=False, backref='point_request')
    scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "PointRequest(id='%s')>"% (self.id)

class BasicRequest(CommonColumns):
    __tablename__ = 'basic_requests'  
    id = db.Column(db.Integer, primary_key=True)
    conditions_description = db.Column(db.Integer)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    request_format = db.Column(db.String)

    file_name = db.relationship('RequestArchive', backref='basic_request', uselist=False)
    basic_responses = db.relationship('BasicResponse', backref='basic_request', lazy='dynamic')

    def __repr__(self):
        return "<BasicRequest(conditions description='%s')>" % (
          self.conditions_description
        )

class PointCoordinate(CommonColumns):
    __tablename__ = 'point_coordinates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    value = db.Column(db.Float)
    point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))

    def __repr__(self):
        return "<PointCoordinate(title='%s', value='%s')>" % (
          self.title, 
          self.value
        )

class Parameters(CommonColumns):
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.Integer)
    scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

    def __repr__(self):
        return "<Parameters(parameter='%s')>" % (
          self.parameter
        )

class RequestArchive(CommonColumns):
    __tablename__ = 'request_archives'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String) #uuid
    path = db.Column(db.String)
    doi = db.Column(db.String)    #Digital Object Identifier
    zenodo_file_id = db.Column(db.String)
    original_file_name = db.Column(db.String) # original filename since file is renamed to uuid
    basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))

    def __repr__(self):
        return "<RequestArchive(file name='%s',\
        path='%s',\
        original file name='%s',\
        doi='%s')>" % (
          self.file_name,
          self.path,
          self.original_file_name,
          self.doi
        )

# Response related tables

class ScanResponse(CommonColumns):
    __tablename__ = 'scan_responses'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    scan_response = db.relationship('PointResponse', backref='scan_response', lazy='dynamic')
    scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

    def __repr__(self):
        return "<ScanResponse()>"
    
class PointResponse(CommonColumns):
    __tablename__ = 'point_responses'
    id = db.Column(db.Integer, primary_key=True)
    lower_1sig_expected_CLs = db.Column(db.Float)
    lower_2sig_expected_CLs = db.Column(db.Float)
    expected_CLs = db.Column(db.Float)
    upper_1sig_expected_CLs = db.Column(db.Float)
    upper_2sig_expected_CLs = db.Column(db.Float)
    observed_CLs = db.Column(db.Float)
    log_likelihood_at_reference = db.Column(db.Float)
    archives = db.relationship('ResponseArchive', backref='point_response', uselist=False)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    basic_answers = db.relationship('BasicResponse', backref='point_response', lazy='dynamic')
    scan_response_id = db.Column(db.Integer, db.ForeignKey('scan_responses.id'))
    point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))
                               
    def __repr__(self):
        return "<PointResponse(lower_1sig_expected_CLs='%r',\
        lower_2sig_expected_CLs='%r',\
        expected_CLs='%r',\
        upper_1sig_expected_CLs='%r',\
        upper_2sig_expected_CLs='%r',\
        observed_CLs='%r')>" % (
          self.lower_1sig_expected_CLs,
          self.lower_2sig_expected_CLs,
          self.expected_CLs,
          self.upper_1sig_expected_CLs,
          self.upper_2sig_expected_CLs,
          self.observed_CLs
        )	  
  
class BasicResponse(CommonColumns):
    __tablename__ = 'basic_responses'
    id = db.Column(db.Integer, primary_key=True)
    lower_1sig_expected_CLs = db.Column(db.Float)
    lower_2sig_expected_CLs = db.Column(db.Float)
    expected_CLs = db.Column(db.Float)
    upper_1sig_expected_CLs = db.Column(db.Float)
    upper_2sig_expected_CLs = db.Column(db.Float)
    observed_CLs = db.Column(db.Float)
    log_likelihood_at_reference = db.Column(db.Float)
    archives = db.relationship('ResponseArchive', backref='basic_response', uselist=False)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    point_response_id = db.Column(db.Integer, db.ForeignKey('point_responses.id'))
    basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))

    def __repr__(self):
        return "<BasicResponse(lower_1sig_expected_CLs='%r',\
        lower_2sig_expected_CLs='%r',\
        expected_CLs='%r',\
        upper_1sig_expected_CLs='%r',\
        upper_2sig_expected_CLs='%r',\
        observed_CLs='%r')>" % (
          self.lower_1sig_expected_CLs,
          self.lower_2sig_expected_CLs,
          self.expected_CLs,
          self.upper_1sig_expected_CLs,
          self.upper_2sig_expected_CLs,
          self.observed_CLs
        )
  
class ResponseArchive(CommonColumns):
    __tablename__ = 'response_archives'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    original_file_name = db.Column(db.String)
    file_path = db.Column(db.String)
    doi = db.Column(db.String)
    histo_name = db.Column(db.String)
    histo_path = db.Column(db.String)
    point_response_id = db.Column(db.Integer, db.ForeignKey('point_responses.id'))
    basic_response_id = db.Column(db.Integer, db.ForeignKey('basic_responses.id'))

    def __repr__(self):
        return "<ResponseArchive(file_name='%s',\
        original_file_name='%s',\
        doi='%s',\
        point_response_id='%s',\
        basic_response_id='%s',\
        file_path='%s',\
        histo_name='%s',\
        histo_path='%s')>" % (
          self.file_name,
          self.original_file_name,
          self.doi,
          self.point_response_id,
          self.basic_response_id,
          self.file_path, 
          self.histo_name, 
          self.histo_path
        )

