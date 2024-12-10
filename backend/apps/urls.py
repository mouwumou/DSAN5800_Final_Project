from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('agent/', include('agent.urls')),
    path('user/', include('user.urls')),
    path('expense/', include('spending.urls')),
    # path('announcement/', include('announcement.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)