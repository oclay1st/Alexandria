# -*- coding: utf-8 -*-
"""
Extensions module.
Each extension is initialized in the app factory located in factory.py
 """
from flask_cors import CORS
from flask_elasticsearch import FlaskElasticsearch
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal
from alexandria.modules.utils.vendor.flask_restplus_patched import Api
from flask_babel import Babel
from flask_migrate import Migrate
# from flask_caching import Cache
from flask_rq2 import RQ
from flask_uploads import IMAGES, UploadSet

__author__ = 'oclay'

es = FlaskElasticsearch(using='default')
db = SQLAlchemy()
api = Api(prefix='/api', doc='/api/doc', ui=False, title='Alexandria API')
jwt = JWTManager()
rq = RQ()
principal = Principal()
mail = Mail()
migrate = Migrate()
babel = Babel()
# cache = Cache()
corsd = CORS()
document_file = UploadSet('documents', ('pdf',))
thumbnail_image = UploadSet('thumbnails', IMAGES)
profile_image = UploadSet('profiles', IMAGES)
