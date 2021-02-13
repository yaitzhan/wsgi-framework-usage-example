from views import SimpleView, AboutView


routes = {
    '/': SimpleView(),
    '/about/': AboutView()
}
