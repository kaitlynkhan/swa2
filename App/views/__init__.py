from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .studentv import student_views  

views = [user_views, index_views, auth_views, student_views]
