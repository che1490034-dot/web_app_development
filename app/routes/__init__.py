from flask import Blueprint

# 初始化 Blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
plan_bp = Blueprint('plan', __name__, url_prefix='/itineraries')
