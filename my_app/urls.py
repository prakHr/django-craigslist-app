from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('new_search',views.new_search,name='new_search'),
    path('calendar',views.create_calendar,name='create_calendar'),
   # path('admin/', admin.site.urls),
]