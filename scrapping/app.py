import os
from datetime import date
from flask import Flask
from flask.json import JSONEncoder
from flask_restx import Api
from flask_cors import CORS
from crawlerApi import crawlerApi

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

isDebug = os.getenv('DEBUG_MODE', 'true')
isDebug = True if isDebug == 'true' else False


class CustomJsonEncoder(JSONEncoder):
  def default(self, obj):
    try:
      if isinstance(obj, date):
        return obj.isoformat()
      iterable = iter(obj)
    except TypeError:
      pass
    else:
      return list(iterable)
    return JSONEncoder.default(self, obj)

app.json_encoder = CustomJsonEncoder

if isDebug == True:
  api = Api(app, version='0.1', title='팍스넷 Crawling API',
    description='팍스넷 crawling을 위한 backend API 입니다.')
else:
  api = Api(app, version='0.1', title='팍스넷 Crawling API',
    description='팍스넷 crawling을 위한 backend API 입니다.', doc=False)

api.add_namespace(crawlerApi)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=isDebug)