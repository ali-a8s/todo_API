from django.urls import path, include 
from . import views
from rest_framework import routers


urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogouView.as_view()),
]


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
urlpatterns += router.urls

# {
#     "token": "fcc962273557ad8b88370e3785bc042a5c196710",
#     "user_id": 1,
#     "username": "root",
#     "email": "root@email.com"
# }