from wsgi_framework.views import BaseView
from wsgi_framework.templating import render


class SimpleView(BaseView):
    return_code = '200 OK'

    def __call__(self, request):
        # ugly - have to rewrite __call__()
        # the problem is to pass request context...
        body = render('index.html', title='some test title', text='Some test view with jinja2 templating', **request)
        return self.return_code, body


class AboutView(BaseView):
    return_code = '200 OK'

    def __call__(self, request):
        body = render('about.html', text='Some text about something interesting', **request)
        return self.return_code, body
