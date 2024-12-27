from posts.views import hello_view, html_view, list_view, main_view, detail_view, create_post, post_update
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from user.views import register_view, login_view, logout_view, profile_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", hello_view),
    path("tea/", html_view),
    path("posts/", list_view, name="posts"),  # Исправлено
    path("", main_view, name="main-page"),
    path('post_detail/<int:id>/', detail_view),
    path("create_post/", create_post),
    path("register/", register_view),
    path("login/", login_view, name="login-view"),
    path("logout/", logout_view, name="logout-view"),
    path("profile/", profile_view),
    path("posts/<int:id/update/", post_update)
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)