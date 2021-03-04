"""
За основу взят пример из репозитория:
https://github.com/PrettySolution/Design-patterns-python/blob/master/3_Prototype/prototype.py
"""
from __future__ import annotations

import copy
from enum import Enum, auto
from contextlib import suppress
from typing import List, Optional, Protocol


# define a generic observer type
# https://www.python.org/dev/peps/pep-0544/#defining-a-protocol
class Observer(Protocol):
    def update(self, subject: Subject):
        pass


class Subject:
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        with suppress(ValueError):
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


class User:
    class UserTypes(Enum):
        STUDENT = auto()
        TEACHER = auto()

    auto_id = 0

    def __init__(self, name, email, user_type):
        self.user_id = User.auto_id
        User.auto_id += 1
        self.name = name
        self.email = email
        self.courses = []
        self.user_type = user_type


class UserFactory:
    type_student = User('', '', User.UserTypes.STUDENT)
    type_teacher = User('', '', User.UserTypes.TEACHER)

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


class Course(Subject):
    auto_id = 0

    def __init__(self, name, course_type, category):
        super().__init__()
        self.id = Course.auto_id
        Course.auto_id += 1
        self.name = name
        self.category = category
        self.course_type = course_type

    def __str__(self):
        return f'{self.name}, {self.course_type}'

    def change(self, course_new_name, course_new_category, course_new_type):
        self.category = course_new_category
        self.name = course_new_name
        self.course_type = course_new_type
        self.notify()  # notify all observers


class EmailNotifier:
    def update(self, subject: Course):
        print('sent via Email: course was changed:', subject.name)


class SMSNotifier:
    def update(self, subject: Course):
        print('sent via SMS: course was changed:', subject.name)


class TelegramNotifier:
    def update(self, subject: Course):
        print('sent via Telegram: course was changed:', subject.name)


class WhatsAppNotifier:
    def update(self, subject: Course):
        print('sent via WhatsApp: course was changed:', subject.name)


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
        self.sms_notifier = SMSNotifier()
        self.email_notifier = EmailNotifier()

    def create_course(self, name, category, course_type):
        course = CourseFactory.new_course(name, category, course_type)
        course.attach(self.sms_notifier)
        course.attach(self.email_notifier)
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

    def create_new_student(self, name, email) -> User:
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

    def change_course(self, course_id, course_new_name, course_new_category, course_new_type):
        course_object = self.get_course_by_id(course_id)
        course_object.change(course_new_name, course_new_category, course_new_type)
        return course_object
