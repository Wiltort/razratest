from app import app
from flask_login import current_user, login_user
#from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
