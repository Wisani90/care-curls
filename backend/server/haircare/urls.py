
# from django.conf.urls import include, url, patterns
# from django.conf.urls import patterns

# urlpatterns = patterns(
#     '',
#     url(r'^$', 'haircare.views.index', name='index'),
#     url(r'^cart$', 'haircare.views.cart', name='show_cart'),
#     url(r'^careprofile$', 'haircare.views.dashboard', name='care_dashboard'),
# )

from django.contrib import admin
from django.urls import path, include

from haircare import views

urlpatterns = [
    # path('admin/', admin.site.urls)
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='home'),
    path('cart/', views.index, name='cart'),
    path('careprofile/', views.dashboard, name='care_dashboard'),
    path('i18n/', include('django.conf.urls.i18n')),
	path('language/', views.ChangeLanguageView.as_view(), name='change_language')
]
