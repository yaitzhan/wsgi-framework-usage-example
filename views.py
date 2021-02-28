import os

from app_site import OnlineUniversitySite

from wsgi_framework.views import BaseView
from wsgi_framework.response import HTTPResponse
from wsgi_framework.templating import render
from wsgi_framework.logger import Logger


app_site = OnlineUniversitySite()

if not os.path.exists('logs'):
    os.makedirs('logs')

logger = Logger(name='app-logger', logs_dir='logs')


class SimpleView(BaseView):
    def get(self, request):
        content = render('index.html', **request)
        return HTTPResponse(content)()


class AboutView(BaseView):
    def get(self, request):
        content = render('about.html', **request)
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

    def post(self, request):
        body = request.get('body')
        logger.info('Got POST data for ContactsView request: {}'.format(body))
        return HTTPResponse()()


class CreateCourseView(BaseView):
    def get(self, request):
        content = render('create_course.html', categories=app_site.categories)
        return HTTPResponse(content)()

    def post(self, request):
        content = render('create_course.html', message='Новый курс добавлен!')
        data = request.get('body')
        logger.info('Got POST data for CreateCourseView request: {}'.format(data))
        course_type = data.get('course_type')
        course_name = data.get('course_name')
        category_id = int(data.get('category_id'))
        category_object = app_site.get_category_by_id(category_id)
        app_site.create_course(course_name, category_object, course_type)
        logger.info('Created new course')
        return HTTPResponse(content)()


class CourseListView(BaseView):
    def get(self, request):
        content = render('course_list.html', objects_list=app_site.courses)
        return HTTPResponse(content)()


class CreateCategoryView(BaseView):
    def get(self, request):
        content = render('create_category.html')
        return HTTPResponse(content)()

    def post(self, request):
        body = request.get('body')
        logger.info('Got POST data for CreateCategoryView request: {}'.format(body))
        name = body.get('name')
        app_site.create_category(name)
        content = render('create_category.html', message='Категория добавлена!')
        logger.info('Created new category')
        return HTTPResponse(content)()


class CategoryListView(BaseView):
    def get(self, request):
        content = render('category_list.html', objects_list=app_site.categories)
        return HTTPResponse(content)()


class CopyCourseView(BaseView):
    def get(self, request):
        params = request.get('query_params')
        course_name = params.get('name')
        course_object = app_site.get_course(course_name)
        content = render('copy_course.html', course=course_object)
        return HTTPResponse(content)()

    def post(self, request):
        data = request.get('body')
        name = data.get('course_name')
        course_type = data.get('course_type')
        course_category_id = data.get('course_category_id')
        category_object = app_site.get_category_by_id(course_category_id)
        old_course = app_site.get_course(name)
        if old_course:
            new_name = f'copy_{name}'
            app_site.create_course(new_name, category_object, course_type)
        content = render('course_list.html', objects_list=app_site.courses)
        return HTTPResponse(content)()
