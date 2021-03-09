import os
import sqlite3
import json

from app_site import User

connection = sqlite3.connect(os.path.join('database', 'patterns.sqlite'))


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    # to store such data as list of object
    # like User.courses in db we can store is as string interpretation
    # of list of integers: '["1", "2", "23"]'
    # so we need to use json module to serialize and deserialize to/from str
    def _parse_list_str(self, list_str: str):
        return [int(x) for x in json.loads(list_str)]

    def _serialize_data(self, data_list: list):
        return json.dumps(data_list)

    def all(self):
        statement = f'SELECT * FROM {self.tablename} WHERE user_type=1'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            _id, name, email, courses_str, user_type = item
            courses_ids = self._parse_list_str(courses_str)
            student = User(name, email, user_type)
            student.id = _id
            student.email = email
            student.courses = courses_ids
            student.user_type = user_type
            result.append(student)
        return result

    def find_by_id(self, _id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=? AND user_type=1"
        self.cursor.execute(statement, (_id,))
        result = self.cursor.fetchone()
        if result:
            return User(*result)
        else:
            raise RecordNotFoundException(f'record with id={_id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, email, courses, user_type) VALUES (?,?,?,?)"
        self.cursor.execute(statement, (obj.name, obj.email, self._serialize_data(obj.courses), obj.user_type))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'student': StudentMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, User) and obj.user_type == User.UserTypes.STUDENT:
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
