from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from flask import jsonify, g

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return {'token': token}