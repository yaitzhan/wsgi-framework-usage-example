import os
from urllib.parse import unquote, unquote_plus

from app_site import OnlineUniversitySite

from wsgi_framework.views import BaseView, CreateView, ListView
from wsgi_framework.response import HTTPResponse
from wsgi_framework.templating import render
from wsgi_framework.logger import Logger


app_site = OnlineUniversitySite()

if not os.path.exists('logs'):
    os.makedirs('logs')

logger = Logger(name='app-logger', logs_dir='logs')


class SimpleView(BaseView):
    def get(self, request):
        content = render('course_list.html', **request)
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


class CreateCourseView(CreateView):
    template_name = 'create_course.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = app_site.categories
        return context

    def create_obj(self, data: dict):
        category_id = data.get('category_id')
        course_type = data.get('course_type')
        course_name = unquote_plus(data.get('course_name'))
        category_object = app_site.get_category_by_id(int(category_id))
        app_site.create_course(course_name, category_object, course_type)


class CreateStudentView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = unquote_plus(data.get('name'))
        email = unquote(data.get('email'))
        app_site.create_new_student(name, email)
        logger.info('Created new student')


class CourseEnrollmentView(CreateView):
    template_name = 'enroll_course.html'

    def create_obj(self, data: dict):
        student_id = int(data.get('student_id'))
        student_object = app_site.get_student_by_id(student_id)
        course_id = int(data.get('course_id'))
        course_object = app_site.get_course_by_id(course_id)
        student_object.courses.append(course_object)
        logger.info('Student {} enrolled into course {}'.format(student_object.name, course_object.name))


class StudentListView(ListView):
    template_name = 'student_list.html'
    queryset = app_site.students


class CourseListView(ListView):
    template_name = 'course_list.html'
    queryset = app_site.courses


class CreateCategoryView(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):
        name = unquote_plus(data.get('name'))
        app_site.create_category(name)
        logger.info('Created new category')


class CategoryListView(ListView):
    template_name = 'category_list.html'
    queryset = app_site.categories


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


class ChangeCourse(BaseView):
    def get(self, request):
        content = render('change_course.html', courses=app_site.courses, categories=app_site.categories)
        return HTTPResponse(content)()

    def post(self, request):
        content = render('change_course.html')
        data = request.get('body')
        course_id = int(data.get('course_id'))
        course_new_name = unquote_plus(data.get('course_name'))
        category_id = int(data.get('category_id'))
        course_new_category = app_site.get_category_by_id(category_id)
        course_new_type = unquote_plus(data.get('course_type'))
        changed_course = app_site.change_course(course_id, course_new_name, course_new_category, course_new_type)
        logger.info('Created new course: {}'.format(changed_course.id))
        return HTTPResponse(content)()
