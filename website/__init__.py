from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from website.config import NAME, DBUSER, PASSWORD, HOST, PORT


UPLOAD_FOLDER = "static/images"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DBUSER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "super secret key"

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
csrf = CSRFProtect(app)
login_manager.init_app(app)

cache = Cache()
app.config["CACHE_TYPE"] = (
    "simple"  # simple - operating potochnogo локальные и не больние проект, radis - okremo на проектах побольше, ramcheseh - оперативна память кластера на очень загружених проектах, файл систем кеш - на диск
)
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
app.config["CACHE_KEY_PREFIX"] = "myapp_"


cache.init_app(app)


from website import views
