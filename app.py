# from wheezy.http import WSGIApplication
# from wheezy.web.middleware import path_routing_middleware_factory
# from url import all_urls, router 

# options = {
#     "path_router": router,
#     "ENCODING": "utf-8",
#     "urls": all_urls 
# }

# main = WSGIApplication(
#     middleware=[
#         path_routing_middleware_factory
#     ],
#     options=options
# )

# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     try:
#         print('http://localhost:8080/')
#         make_server('', 8080, main).serve_forever()
#     except KeyboardInterrupt:
#         pass
#     print('Thanks!')


from wheezy.http import WSGIApplication
from wheezy.web.middleware import bootstrap_defaults
from url import all_urls
from wheezy.web.middleware import path_routing_middleware_factory


options = {}
main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        path_routing_middleware_factory
    ],
    options=options
)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')