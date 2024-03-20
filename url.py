from wheezy.routing import url, PathRouter
from views import (
    HomeHandler, ProfileHandler, RegisterFormHandler, RegisterHandler,
    LoginFormHandler, LoginHandler, LogoutHandler, SaveTextHandler,
    DeleteTextHandler, EditTextHandler
)

url_patterns = [
    ('/', HomeHandler, 'home'),
    ('/profile', ProfileHandler, 'profile'),
    ('/register/form', RegisterFormHandler, 'register_form'),
    ('/register', RegisterHandler, 'register'),
    ('/login/form', LoginFormHandler, 'login_form'), 
    ('/login', LoginHandler, 'login'),
    ('/logout', LogoutHandler, 'logout'),
    ('/save_text', SaveTextHandler, 'save_text'),
    ('/profile/delete_text/{node_id}', DeleteTextHandler, 'delete_text'),
    ('/profile/edit_text/{node_id}', EditTextHandler, 'edit_text')
]

router = PathRouter()
for pattern, handler, name in url_patterns:
    router.add_route(pattern, handler, name=name)

all_urls = [url(r, router, name=n) for r, _, n in url_patterns]


# from views import (
#     HomeHandler, ProfileHandler, RegisterFormHandler, RegisterHandler,
#     LoginFormHandler, LoginHandler, LogoutHandler, SaveTextHandler,
#     DeleteTextHandler, EditTextHandler
# )

# all_urls = [
#     ('/', HomeHandler, 'home'),
#     ('/profile', ProfileHandler, 'profile'),
#     ('/register/form', RegisterFormHandler, 'register_form'),
#     ('/register', RegisterHandler, 'register'),
#     ('/login/form', LoginFormHandler, 'login_form'), 
#     ('/login', LoginHandler, 'login'),
#     ('/logout', LogoutHandler, 'logout'),
#     ('/save_text', SaveTextHandler, 'save_text'),
#     ('/profile/delete_text/{node_id}', DeleteTextHandler, 'delete_text'),
#     ('/profile/edit_text/{node_id}', EditTextHandler, 'edit_text')
# ]
