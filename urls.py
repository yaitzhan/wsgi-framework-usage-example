from views import SimpleView, AboutView, ContactsView


routes = {
    '/': SimpleView,
    '/about/': AboutView,
    '/contacts': ContactsView
}
