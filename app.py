from wsgi_framework.core import Application
from urls import routes


app = Application()
app.urls = routes
