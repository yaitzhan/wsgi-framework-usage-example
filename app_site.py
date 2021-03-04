"""
За основу взят пример из репозитория:
https://github.com/PrettySolution/Design-patterns-python/blob/master/3_Prototype/prototype.py
"""
import copy
from enum import Enum, auto


class User:
    auto_id = 0

    def __init__(self, name, email, user_type):
        self.user_id = User.auto_id
        User.auto_id += 1
        self.name = name
        self.email = email
        self.courses = []
        self.user_type = user_type


class UserTypes(Enum):
    STUDENT = auto()
    TEACHER = auto()


class UserFactory:
    type_student = User('', '', UserTypes.STUDENT)
    type_teacher = User('', '', UserTypes.TEACHER)

    @staticmethod
    def __new_user(proto, name, email):
        result = copy.deepcopy(proto)
        result.name = name
        result.email = email
        return result

    @staticmethod
    def new_student(name, email):
        return UserFactory.__new_user(UserFactory.type_student, name, email)

    @staticmethod
    def new_teacher(name, email):
        return UserFactory.__new_user(UserFactory.type_teacher, name, email)


class Category:
    auto_id = 0

    def __init__(self, name):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.courses = []

    def course_count(self):
        return len(self.courses)


class Course:
    auto_id = 0

    def __init__(self, name, course_type, category):
        self.id = Course.auto_id
        Course.auto_id += 1
        self.name = name
        self.category = category
        self.course_type = course_type

    def __str__(self):
        return f'{self.name}, {self.course_type}'


class CourseFactory:
    online_course = Course('', 'online', None)
    offline_course = Course('', 'offline', None)

    @staticmethod
    def __new_course(proto, name, category):
        result = copy.deepcopy(proto)
        result.name = name
        result.category = category
        result.category.courses.append(result)
        return result

    @staticmethod
    def __new_online_course(name, category):
        return CourseFactory.__new_course(CourseFactory.online_course, name, category)

    @staticmethod
    def __new_offline_course(name, category):
        return CourseFactory.__new_course(CourseFactory.offline_course, name, category)

    @staticmethod
    def new_course(name, category, course_type):
        if course_type == 'online':
            return CourseFactory.__new_online_course(name, category)
        elif course_type == 'offline':
            return CourseFactory.__new_offline_course(name, category)


class OnlineUniversitySite:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_course(self, name, category, course_type):
        course = CourseFactory.new_course(name, category, course_type)
        self.courses.append(course)
        return course

    def create_category(self, name):
        category = Category(name)
        self.categories.append(category)
        return category

    def get_category_by_id(self, category_id):
        for item in self.categories:
            if item.id == category_id:
                return item
        return None

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def create_new_student(self, name, email):
        new_student = UserFactory.new_student(name, email)
        self.students.append(new_student)
        return new_student

    def create_new_teacher(self, name, email):
        new_teacher = UserFactory.new_teacher(name, email)
        self.teachers.append(new_teacher)
        return new_teacher

    def get_student_by_id(self, student_id):
        for item in self.students:
            if item.user_id == student_id:
                return item
        return None

    def get_course_by_id(self, course_id):
        for item in self.courses:
            if item.id == course_id:
                return item
        return None
