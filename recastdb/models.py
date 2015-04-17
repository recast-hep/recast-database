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
                         db.Column('reqeust_id',db.Integer,db.ForeignKey('request.id'))
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



# many to many relationship between User & Analysis
# Many users can subscribe to a single analysis
# A user can subscrible to one or more analyses
subscribers = db.Table('subscribers',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('analysis_id', db.Integer, db.ForeignKey('analysis.id'))
                       )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    analyses = db.relationship('Analysis',
                               secondary=subscribers,
                               backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User(name='%s', email='%s')>" % (self.name, self.email)


class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    description_of_model = db.Column(db.String)

    def __init__(self, description):
        self.descrition_of_model = description

    def __repr__(self):
        return "<Model(ID='%d', description='%s')>" % (self.id, self.description_of_model)


class Analysis(db.Model):
    __tablename__ = 'analysis'

    id = db.Column(db.Integer, primary_key=True)
    description_of_original_analysis = db.Column(db.String)

    def __init__(self, description):
        self.description_of_original_analysis = description

    def __repr__(self):
        return "<Analysis(id='%r', description='%s')>" % (self.id, self.description_of_original_analysis)



# Relationships from here on are uncomplete
    
class RequestNotification(db.Model):
    __tablename__ ='request_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    description_of_recast_potential = db.Column(db.Integer, primary_key=True)
    #relationship with analysis
    #relationship with model
    
    def __repr__(self):
        return "RequestNotification(descriptionOfRecastPotential='%s')>"



class ScanRequest(db.Model):
    __tablename__ = 'scan_requests'
    

    id = db.Column(db.Integer, primary_key=True)
    #relationship with model
    #relationship with analysis, user, 
    #relationship with point_request
    
    def __repr__(self):
        return "<ScanRequest()>"

class PointProcess(db.Model):
    __tablename__ = 'point_processes'
    
    id = db.Column(db.Integer, primary_key=True)
    #relationship with analyis
    #relationship with model
    #relationship with user
    
    def __repr__(self):
        return "PointProcess()>"


class ScanResponse(db.Model):
    __tablename__ = 'scan_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    
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

    def __repr__(self):
        return "<BasicResponse(overallEfficiency='%f', nominalLuminosity='%f;, \
lower1sigLimitOnCrossSection='%d', upper1sigLimitOnCrossSection='%d', lower2sigLimitOnCrossSection='%d', upper2sigLimitOnCrossSection='%d', lower1sigLimitOnRate='%d', upper1sigLimitOnRate='%d', lower2sigLimitOnRate='%d', upper2sigLimitOnRate='%d', logLikelihoodAtReference='%d', referenceCrossSection='%d')>" % \
(self.overall_efficiency, self.nominal_luminosity, self.lower_1sig_limit_on_cross_section, self.upper_1sig_limit_on_cross_section, self.lower_2sig_limit_on_cross_section, self.upper_2sig_limit_on_cross_section, self.lower_1sig_limit_on_rate, self.upper_1sig_limit_on_rate, self.lower_2sig_limit_on_rate, self.upper_2sig_limit_on_rate, self.log_likelihood_at_reference, self.reference_cross_section)
        

