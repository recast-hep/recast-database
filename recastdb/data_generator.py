import string
import random

from models import User
from models import Analysis
from models import Model
from models import LHEFile
from models import BasicRequest
from models import PointRequest
from models import ScanRequest
from models import Histogram
from models import ParameterPoint
from models import Parameters

from models import ScanResponse
from models import PointResponse
from models import BasicResponse


from database import db

n_items = 200


def id_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_users(n=50):
    users = []
    for i in range(n):
        username = "Name_" + id_generator(size=10, chars=string.ascii_lowercase)
        email = username + '@email.com'
        users.append(User(username, email))

    return users
    
def generate_analyses(n=50):
    analyses = []
    for i in range(n):
        analysis = "Analysis_" + id_generator(size=10, chars=string.ascii_lowercase)
        analyses.append(Analysis(description_of_original_analysis=analysis))

    return analyses


def generate_models(n=50):
    models = []
    
    for i in range(n):
        model = "Model_" + id_generator(size=10, chars=string.ascii_lowercase)
        models.append(Model(model))
        
    return models


def generate_lheFiles(n=50):
    files = []    
    for i in range(n):
        name = "File_" + id_generator(size=10, chars=string.ascii_lowercase)
        path = "/path/" + name
        files.append(LHEFile(file_name=name, path=path))
    
    return files
                

def generate_basic_requests(n=50):
    requests = []
    for i in range(n):
        n_events = random.randrange(10000)
        rcs = random.randrange(1000)
        cd = random.randrange(1000)
        requests.append(BasicRequest(number_of_events=n_events, reference_cross_section=rcs, conditions_description=cd))

    return requests

def generate_point_requests(n=50):
    requests = []
    for i in range(n):
        requests.append(PointRequest())

    return requests

def generate_scan_requests(n=50):
    requests = []
    for i in range(n):
        name = "scan_request_" + id_generator(size=10, chars=string.ascii_lowercase)
        requests.append(ScanRequest(description_of_model=name))

    return requests

def generate_parameters(n=50):
    params = []
    for i in range(n):
        param = random.randrange(10000)
        params.append(Parameters(parameter=param))

    return params


def generate_parameter_points(n=50):
    points = []
    for i in range(n):
        title = "title_ " + id_generator()
        value = random.randrange(10000)
        points.append(ParameterPoint(title=title, value=value))

    return points


def generate_histograms(n=50):
    histos = []
    for i in range(n):
        file_name = "histo_" + id_generator(size=7) + ".root"
        file_path = "/path/" + file_name
        histo_name = "hist_" + id_generator(size=5, chars=string.ascii_lowercase)
        histo_path = "/path/" + histo_name
        
        histos.append(Histogram(file_name=file_name, file_path=file_path, histo_name=histo_name, histo_path=histo_path))

    return histos


def generate_basic_responses(n=50):
    responses = []
    for i in range(n):
        oe = random.randrange(100)
        nl = random.randrange(1000)
        l1locs = random.randrange(10000)
        u1locs = random.randrange(10000)
        l2locs = random.randrange(1000)
        u2locs = random.randrange(1000)
        l1lor = random.randrange(1000)
        u1lor = random.randrange(1000)
        l2lor = random.randrange(1000)
        u2lor = random.randrange(1000)
        llatr = random.randrange(1000)
        rcs = random.randrange(1000)
        
        
        responses.append(BasicResponse(overall_efficiency=oe, nominal_luminosity=nl, lower_1sig_limit_on_cross_section=l1locs, upper_1sig_limit_on_cross_section=u1locs, lower_2sig_limit_on_cross_section=l2locs, upper_2sig_limit_on_cross_section=u2locs, lower_1sig_limit_on_rate=l1lor, upper_1sig_limit_on_rate=u1lor, lower_2sig_limit_on_rate=l2lor, upper_2sig_limit_on_rate=u2lor, log_likelihood_at_reference=llatr, reference_cross_section=rcs))
        
    return responses


def generate_point_responses(n=50):
    responses = []
    for i in range(n):
        lwe = random.randrange(1000)
        tl = random.randrange(1000)
        l1locswr = random.randrange(1000)
        u1locswr = random.randrange(1000)
        l2locswr = random.randrange(10000)
        u2locswr = random.randrange(100)
        llar = random.randrange(1000)

        responses.append(PointResponse(lumi_weighted_efficiency=lwe, total_luminosity=tl, lower_1sig_limit_on_cross_section_wrt_reference=l1locswr, upper_1sig_limit_on_cross_section_wrt_reference=u1locswr, lower_2sig_limit_on_cross_section_wrt_reference=l2locswr, upper_2sig_limit_on_cross_section_wrt_reference=u2locswr, log_likelihood_at_reference=llar))

    return responses


def generate_scan_responses(n=50):
    responses = []
    for i in range(n):
        responses.append(ScanResponse())

    return responses
                  



users = generate_users(n=n_items)
analyses = generate_analyses(n=n_items)
models = generate_models(n=n_items)
lhefiles = generate_lheFiles(n=n_items)

scan_responses = generate_scan_responses(n_items)                        
        

basic_requests = generate_basic_requests(n_items)
point_requests = generate_point_requests(n_items)
scan_requests = generate_scan_requests(n_items)

parameters = generate_parameters(n_items)
parameter_points = generate_parameter_points(n_items)
histograms = generate_histograms(n_items)
basic_responses = generate_basic_responses(n_items)
point_responses = generate_point_responses(n_items)




# Do some relationships
# Users <-> Analysis
for i in range(len(analyses)):
    analyses[i].user = users[random.randint(0,(n_items-1))]

# BacicResponse <-> LHEfile
for i in range(len(lhefiles)):
    lhefiles[i].basic_response = basic_responses[random.randint(0, (n_items-1))]

# PointRequest <-> BasicRequest
for i in range(len(basic_requests)):
    basic_requests[i].point_request = point_requests[random.randint(0, (n_items-1))]
    

# ScanRequest <-> PointRequest
for i in range(len(point_requests)):
    point_requests[i].scan_request = scan_requests[random.randint(0, (n_items-1))]

# Parameters <-> ScanRequest
for i in range(len(parameters)):
    parameters[i].scan_request = scan_requests[random.randint(0, (n_items-1))]
    
# PointRequest <-> ParameterPoint
for i in range(len(parameter_points)):
    parameter_points[i].point_request = point_requests[random.randint(0, (n_items-1))]
    
# ScanResponse <-> PointResponse
for i in range(len(point_responses)):
    point_responses[i].scan_response = scan_responses[random.randint(0, (n_items-1))]

# PointResponse <-> BasicResponses
for i in range(len(basic_responses)):
    basic_responses[i].point_response = point_responses[random.randint(0, (n_items-1))]

# BasicResponse <-> Histogram
# PointResponse <-> Histogram
for i in range(len(histograms)):
    histograms[i].basic_response = basic_responses[random.randint(0, (n_items-1))]
    histograms[i].point_response = point_responses[random.randint(0, (n_items-1))]


# add to database
for i in range(n_items):
    db.session.add(users[i])
    db.session.add(analyses[i])
    db.session.add(models[i])
    db.session.add(lhefiles[i])
    
    db.session.add(histograms[i])
    db.session.add(parameter_points[i])
    db.session.add(parameters[i])
    db.session.add(scan_requests[i])
    db.session.add(point_requests[i])
    db.session.add(basic_requests[i])

    db.session.add(scan_responses[i])
    db.session.add(point_responses[i])
    db.session.add(basic_responses[i])


db.session.commit()

