from django.urls import path

from lacommunaute.www.pages import views


# https://docs.djangoproject.com/en/dev/topics/http/urls/#url-namespaces-and-included-urlconfs
app_name = "pages"

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("contact/", views.contact, name="contact"),
    path("statistiques/", views.statistiques, name="statistiques"),
    path("accessibilite/", views.accessibilite, name="accessibilite"),
    path("sentry-debug/", views.trigger_error, name="sentry_debug"),
]
