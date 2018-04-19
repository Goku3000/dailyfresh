from django.conf.urls import url
from apps.user.views import RegisterView,ActiveView

urlpatterns = [
    url(r'^register$',RegisterView.as_view(),name='register'),
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),
]
