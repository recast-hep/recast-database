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
    access_tokens = db.relationship('AccessToken', backref='user')
    analyses = db.relationship('Analysis', backref='owner')
    requests = db.relationship('ScanRequest', backref='requester')
    point_requests = db.relationship('PointRequest', backref='requester')
    basic_requests = db.relationship('BasicRequest', backref='requester')
    subscriptions = db.relationship('Subscription', backref='subscriber')

class AccessToken(db.Model):
    __tablename__ = 'access_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    token_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Analysis(CommonColumns):
    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    collaboration = db.Column(db.String)
    
    doi = db.Column(db.String)
    arxiv_id = db.Column(db.String)
    inspire_id = db.Column(db.String)
    cds_id = db.Column(db.String)

    description = db.Column(db.Text)
    scan_requests = db.relationship('ScanRequest', backref='analysis')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    run_condition_id = db.Column(db.Integer, db.ForeignKey('run_conditions.id'))
    subscriptions = db.relationship('Subscription', backref='analysis')

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

class RunCondition(CommonColumns):
    __tablename__ = 'run_conditions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    analyses = db.relationship('Analysis',backref='run_condition')
  
class Processing(CommonColumns):
    """ this is an actual request to process the recast request """
    __tablename__ = 'processing'
    id            = db.Column(db.Integer, primary_key = True)
    jobguid       = db.Column(db.String(36), unique = True)
    celerytaskid  = db.Column(db.String(36), unique = True)

class Model(CommonColumns):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    description_of_model = db.Column(db.String, nullable=True)
    scan_requests = db.relationship('ScanRequest', backref='model')
    point_requests = db.relationship('PointRequest', backref='model')
    basic_requests = db.relationship('BasicRequest', backref='model')
    scan_responses = db.relationship('ScanResponse', backref='model')
    point_responses = db.relationship('PointResponse', backref='model')
    basic_responses = db.relationship('BasicResponse', backref='model')

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
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    scan_points = db.relationship('PointRequest', backref='scan_request')
    parameters = db.relationship('Parameters', backref='scan_request')
    scan_responses = db.relationship('ScanResponse', uselist=False, backref='scan_request')
    notifications = db.relationship('RequestNotification', uselist=False, backref='scan_request')
  
class PointRequest(CommonColumns):
    __tablename__ = 'point_requests'    
    id = db.Column(db.Integer, primary_key=True)

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    point_coordinates = db.relationship('PointCoordinate', backref='point_request')
    point_coordinates = db.relationship('PointCoordinate', backref='point_request')

    requests = db.relationship('BasicRequest', backref='point_request')
    point_responses = db.relationship('PointResponse', uselist=False, backref='point_request')

class BasicRequest(CommonColumns):
    __tablename__ = 'basic_requests'  
    id = db.Column(db.Integer, primary_key=True)
    conditions_description = db.Column(db.Integer)
    request_format = db.Column(db.String)

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    file_name = db.relationship('RequestArchive', backref='basic_request', uselist=False)
    basic_responses = db.relationship('BasicResponse', backref='basic_request')


class PointCoordinate(CommonColumns):
    __tablename__ = 'point_coordinates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    value = db.Column(db.Float)

    point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))

class Parameters(CommonColumns):
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.Integer)

    scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))

class RequestArchive(CommonColumns):
    __tablename__ = 'request_archives'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String) #uuid
    path = db.Column(db.String)
    doi = db.Column(db.String)    #Digital Object Identifier
    zenodo_file_id = db.Column(db.String)
    original_file_name = db.Column(db.String) # original filename since file is renamed to uuid

    basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))

# Response related tables

class ScanResponse(CommonColumns):
    __tablename__ = 'scan_responses'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    scan_response = db.relationship('PointResponse', backref='scan_response')

    scan_request_id = db.Column(db.Integer, db.ForeignKey('scan_requests.id'))
    
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

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    scan_response_id = db.Column(db.Integer, db.ForeignKey('scan_responses.id'))
    point_request_id = db.Column(db.Integer, db.ForeignKey('point_requests.id'))

    archives = db.relationship('ResponseArchive', backref='point_response', uselist=False)
    basic_answers = db.relationship('BasicResponse', backref='point_response')

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
    description = db.Column(db.String)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    point_response_id = db.Column(db.Integer, db.ForeignKey('point_responses.id'))
    basic_request_id = db.Column(db.Integer, db.ForeignKey('basic_requests.id'))
    archives = db.relationship('ResponseArchive', backref='basic_response', uselist=False)

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

