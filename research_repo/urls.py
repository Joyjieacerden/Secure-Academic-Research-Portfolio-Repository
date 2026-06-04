from django.urls import path
<<<<<<< HEAD
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

=======
from .views import LoginView, PublicationListView, PublicationDetailView, LogoutView, SignUpView, PublicationCreateView, PublicationUpdateView, PublicationDeleteView, UploadDocumentView,AccessGrantCreateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('publications/', PublicationListView.as_view(), name='publication_list'),
    path('publications/<int:pk>/', PublicationDetailView.as_view(), name='publication_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('publications/create/', PublicationCreateView.as_view(), name='publication_create'),
    path('publications/<int:pk>/update/', PublicationUpdateView.as_view(), name='publication_update'),
    path('publications/<int:pk>/delete/', PublicationDeleteView.as_view(), name='publication_delete'),
    path('upload-document/', UploadDocumentView.as_view(), name='upload_document'),
    path('access-grant/',AccessGrantCreateView.as_view(), name = 'grant_access')
>>>>>>> 037deb571a63240cf4f3f7218db32e8b127bd1c6
]