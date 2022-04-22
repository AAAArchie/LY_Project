# import password_reset
# xadmin的url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from identify.viewsets import ImagesPostViewSet, MergedImageViewSet
from users.viewsets import UserViewSet

router = DefaultRouter()
router.register('images', ImagesPostViewSet, 'images')
router.register('user', UserViewSet, 'users')
router.register('merged-images', MergedImageViewSet, 'merged-images')


class RedirectToAPI(RedirectView):
    url = '/api/'


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/token/obtain/', obtain_jwt_token),
    path('api/', include(router.urls)),

    path('process/', RedirectToAPI.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', RedirectView.as_view(url='/api/')),

    # path('password_reset/', include('password_reset.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # 全局404页面配置
# handler404 = 'users.views.pag_not_found'
# # 全局500页面配置
# handler500 = 'users.views.page_error'
