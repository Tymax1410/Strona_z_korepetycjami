from django.contrib import admin
from django.urls import path, include
from korepetycje.views import UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('api/', include('korepetycje.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
