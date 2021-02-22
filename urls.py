from views import SimpleView, AboutView, ContactsView, CreateCourseView, CourseListView, CreateCategoryView, \
    CategoryListView


routes = {
    '/': SimpleView,
    '/about/': AboutView,
    '/contacts/': ContactsView,
    '/create_course/': CreateCourseView,
    '/course_list/': CourseListView,
    '/create_category/': CreateCategoryView,
    '/category_list/': CategoryListView,
}
