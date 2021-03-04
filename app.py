from urls import routes

from wsgi_framework.core import Application
from wsgi_framework.response import HTTPResponse
from wsgi_framework.templating import render
from wsgi_framework.utils import debug


app = Application()
app.urls = routes


# redefine view class-based view, ugly because of circular import
@app.route('/')
@debug
def simple_view(request):
    content = render('index.html', **request)
    return HTTPResponse(content)()
