from wsgi_framework.views import BaseView
from wsgi_framework.response import HTTPResponse
from wsgi_framework.templating import render


class SimpleView(BaseView):
    def get(self, request):
        content = render('index.html')
        return HTTPResponse(content)()


class AboutView(BaseView):
    def get(self, request):
        content = render('about.html')
        return HTTPResponse(content)()


class ContactsView(BaseView):
    def get(self, request):
        content = render('contacts.html')
        params = request.get('query_params')
        if params:
            print('User: {} typed into form message: {} with title: {}'.format(params.get('email'),
                                                                               params.get('message_text'),
                                                                               params.get('message_title')))
        return HTTPResponse(content)()


class CreateCourseView(BaseView):
    def get(self, request):
        content = render('create_course.html')
        return HTTPResponse(content)()


class CourseListView(BaseView):
    def get(self, request):
        content = render('course_list.html')
        return HTTPResponse(content)()


class CreateCategoryView(BaseView):
    def get(self, request):
        content = render('create_category.html')
        return HTTPResponse(content)()


class CategoryListView(BaseView):
    def get(self, request):
        content = render('category_list.html')
        return HTTPResponse(content)()
