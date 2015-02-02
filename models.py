from peewee import *

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

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


class User(BaseModel):
  pass
        
class Request(BaseModel):
  analysis = ForeignKeyField(Analysis, related_name='requests')
  
class ParameterPoint(BaseModel):
  request = ForeignKeyField(Request, related_name='parampoints')    
  
class Analysis(BaseModel):
  user = ForeignKeyField(User, related_name='owned_analyses')
  run_condition = ForeignKeyField(RunCondition, related_name='analyses')

class RunCondition(BaseModel):
  pass
  
class Response(BaseModel):
  request = ForeignKeyField(Response, related_name='response')