from django.contrib import admin
from django.urls import path
import index.views as views

import opt.views as optViews




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('opt/',optViews.opt)
]
