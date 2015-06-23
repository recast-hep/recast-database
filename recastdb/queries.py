from database import db


#query all users
from models import User
users = db.session.query(User).all()

#query all analysis
from models import Analysis
analyses = db.session.query(Analysis).all()

#query all models
from models import Model
models = db.session.query(Model).all()

#query all scan request
from models import ScanRequest
scan_requests = db.session.query(ScanRequest).all()

#query all BasicResponse
from models import BasicResponse
basic_responses = db.session.query(BasicResponse).all()

#query all PointResponse
from models import PointResponse
point_responses = db.session.query(PointResponse).all()

#query all LHE files
from models import LHEFile
lhe_files = db.session.query(LHEFile).all()

#query all histograms
from models import Histogram
histograms = db.session.query(Histogram).all()

#query all scan response
from models import ScanResponse
scan_responses = db.session.query(ScanResponse).all()

#query all analysis associated with a user

#query all Basic Request
from models import BasicRequest
basic_requests = db.session.query(BasicRequest).all()

#query all Point Request
from models import PointRequest
point_requests = db.session.query(PointRequest).all()

#query all Run conditions
from models import RunCondition
run_conditions = db.session.query(RunCondition).all()


#query all Processing
from models import Processing
processes = db.session.query(Processing).all()

#query all notifications
from models import RequestNotification
request_notifications = db.session.query(RequestNotification).all()


#query all Parameter points 
from models import ParameterPoint
parameter_points = db.session.query(ParameterPoint).all()


def getUserById(user_id):
    return db.session.query(User).filter(User.id==user_id).all()

def getAnalysisById(analysis_id):
    return db.session.query(Analysis).filter(Analysis.id==analysis_id).all()

#get all analysis owned by a user
def getAllAnalysisForUser(user_id):
    return db.session.query(Analysis).filter(Analysis.owner_id==user_id).all()

#given an analysis object, who's the owner
def getUserGivenAnalysis(analysis):
    return db.session.query(User).filter(User.id==analysis.owner_id).all()

#get all LHE files associated to a BasicRequest
def getLHEFile(basic_request_id):
    return db.session.query(LHEFile).filter(LHEFile.basic_request_id==basic_request_id).all()

#get all Histograms associated to a BasicResponse
def getHistogramForBasicResponse(basic_response_id):
    return db.session.query(Histogram).filter(Histogram.basic_response_id==basic_response_id).all()

#get all Histograms associated to a PointResponse
def getHistogramForPointResponse(point_response_id):
    return db.session.query(Histogram).filter(Histogram.point_response_id==point_response_id).all()

#get all point requests associated to a scan request
def getPointRequest(scan_request_id):
    return db.session.query(PointRequest).filter(PointRequest.scan_request_id==scan_request_id).all()


#get all basic request associated to a point resquest
def getBasicRequest(point_request_id):
    return db.session.query(BasicRequest).filter(BasicRequest.point_request_id==point_request_id).all()


#get all basic response associated to a point response
def getBasicResponse(point_response_id):
    return db.session.query(BasicResponse).filter(BasicResponse.point_response_id==point_response_id).all()

#get all point response associated to a scan response
def getPointResponse(scan_response_id):
    return db.session.query(PointResponse).filter(PointResponse.scan_response_id==scan_response_id).all()


#return the basic responses associated to an analysis id
def getBasicResponseGivenAnalysisID(analysis_id):
    return db.session.query(BasicResponse).filter(BasicResponse.analysis_id==analysis_id).all()

#return the Point responses associated to analysis id
def getPointResponseGivenAnalysisID(analysis_id):
    return db.session.query(PointResponse).filter(PointResponse.analysis_id==analysis_id).all()

#return the scan responses associated to analysis id
def getScanResponseGivenAnalysisID(analysis_id):
    return db.session.query(ScanResponse).filter(ScanResponse.analysis_id==analysis_id).all()

#return the Basic responses given a model id
def getBasicResponseGivenModelID(model_id):
    return db.session.query(BasicResponse).filter(BasicResponse.model_id==model_id).all()

#return the Point responses given a model id
def getPointResponseGivenModelID(model_id):
    return db.session.query(PointResponse).filter(PointResponse.model_id==model_id).all()

#return the Scan response given a model id
def getScanResponseGivenModelID(model_id):
    return db.session.query(ScanResponse).filter(ScanResponse.model_id==model_id).all()

#return the basic request given a model id
def getBasicRequestGivenModelID(model_id):
    return db.session.query(BasicRequest).filter(BasicRequest.model_id==model_id).all()


#return the point request given a model id
def getPointRequestGivenModelID(model_id):
    return db.session.query(PointRequest).filter(PointRequest.model_id==model_id).all()

#return the scan request given a model id
def getScanRequestGivenModelID(model_id):
    return db.session.query(ScanRequest).filter(ScanRequest.model_id==model_id).all()


