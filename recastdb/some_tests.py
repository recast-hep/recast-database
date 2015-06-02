#from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/recast.db'
#db = SQLAlchemy(app)

"""
   Simple script to play around with the models
       - Just adds one record in every table
       - will want to make Flask-related test suites
   use SQLite Database Browser to view all data entered

"""
from database import db


from models import User
from models import Analysis
from models import Model

db.create_all()

user1 = User('user1', 'user1@email.com')
db.session.add(user1)
db.session.commit()

analysis2 = Analysis(description_of_original_analysis="testing analysis", user=user1)
db.session.add(analysis2)
db.session.commit()

print user1

print user1.analyses[0]


model1 = Model("description of models")

from models import LHEFile
from models import BasicRequest

lheFile = LHEFile(file_name="test file", path="/files/")
basicR = BasicRequest(number_of_events=50, reference_cross_section=30, conditions_description=30, analysis=analysis2, file_name=[lheFile])

from models import PointRequest


pointR = PointRequest(analysis=analysis2, model=model1)

from models import ScanRequest

scanR = ScanRequest(model=model1, analysis=analysis2, description_of_model="descriptions")

scanR.scan_points = [pointR]


from models import Parameters


param1 = Parameters(parameter=20)
param2 = Parameters(parameter=30, scan_request=scanR)

param1.scan_requests = scanR

from models import ParameterPoint

paramPoint1 = ParameterPoint(title="initial", value=10)
paramPoint1.point_request = pointR

#now let's add all the objects created to the db and commit
db.session.add(model1)
db.session.add(lheFile)
db.session.add(basicR)
db.session.add(pointR)
db.session.add(scanR)
db.session.add(param1)
db.session.add(paramPoint1)
db.session.commit()

from models import Histogram

histo = Histogram(file_name="histo.root", file_path="./", histo_name="hist", histo_path=".")

from models import BasicResponse

basicResponse = BasicResponse(overall_efficiency=20.3, nominal_luminosity=3.4, lower_1sig_limit_on_cross_section=4.3, upper_1sig_limit_on_cross_section=4.9, lower_2sig_limit_on_cross_section=6.19, upper_2sig_limit_on_cross_section=4.23, lower_1sig_limit_on_rate=43.9, upper_1sig_limit_on_rate=32.4, lower_2sig_limit_on_rate=32.9, upper_2sig_limit_on_rate=32.43, signal_template=[histo], log_likelihood_at_reference=32.23, reference_cross_section=32439.32, analysis=analysis2, model=model1, basic_request=basicR)


from models import PointResponse

pointResponse = PointResponse(lumi_weighted_efficiency=32.21, total_luminosity=32.43, lower_1sig_limit_on_cross_section_wrt_reference=3.5, upper_1sig_limit_on_cross_section_wrt_reference=321.2, lower_2sig_limit_on_cross_section_wrt_reference=32.32, upper_2sig_limit_on_cross_section_wrt_reference=3.32, merged_signal_template_wrt_reference=[histo], log_likelihood_at_reference=32.12, analysis=analysis2, model=model1, basic_answers=[basicResponse], point_request=pointR)

from models import ScanResponse

scanResponse = ScanResponse(analysis=analysis2, model=model1, scan_response=[pointResponse], scan_request=scanR)


from models import RequestNotification

requestNotification = RequestNotification(scan_request=scanR, description_of_original_analysis=analysis2.description_of_original_analysis, description_of_model=model1.description_of_model, description_of_recast_potential="testing....")

db.session.add(histo)
db.session.add(basicResponse)
db.session.add(pointResponse)
db.session.add(scanResponse)
db.session.add(requestNotification)
db.session.commit()


# Now we use a software like "SQLite Database Browser" to view what we added to the db

user2 = User("user2", "user2@email.com")
user3 = User("user3", "user3@email.com")

user2.requests = [scanR]
user2.point_requests = [pointR]
user2.basic_requests = [basicR]

analysis2.subscribers = [user2, user3]

scanR.subscribers = [user2, user1]

pointR.subscribers = [user3, user1]

basicR.subscribers = [user1, user2, user3]

db.session.add(user2)
db.session.add(user3)
db.session.commit()

scan_request2 = ScanRequest(model=model1, analysis=analysis2, description_of_model="models", requester=user3, subscribers=[user1, user2])

db.session.add(scan_request2)
db.session.commit()
