from django.contrib import admin
from django.urls import path
from predict import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_file, name='upload'),
    path('thank_you',views.thank_you,name='thank_you'),
    path('feedback',views.feedback_form,name='feedback'),
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
