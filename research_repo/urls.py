from django.urls import path
from .views import LoginView, PublicationListView, PublicationDetailView, LogoutView, SignUpView, PublicationCreateView, PublicationUpdateView, PublicationDeleteView, UploadDocumentView

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
]