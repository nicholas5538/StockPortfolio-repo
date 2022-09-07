from django.urls import path

from mainpage import views as mainview

app_name = 'mainpage'
urlpatterns = [
    path('<int:pk>/home/', mainview.HomeView.as_view(), name='home'),
    path('<int:pk>/portfolio/', mainview.PortfolioView.as_view(), name='portfolio'),
    path('<int:pk>/update-portfolio/', mainview.UpdatePortfolioView.as_view(), name='update'),
    path('<int:pk>/transactions/', mainview.TransactionsListView.as_view(), name='transactions'),
    path('<int:pk>/edit-profile/', mainview.EditProfileView.as_view(), name='edit_profile'),
    path('<int:pk>/close-position/', mainview.ClosePositionView.as_view(), name='close_position'),
    path('<int:pk>/delete-transaction/', mainview.DeleteTransactionView.as_view(), name='delete_transaction'),
    # path('<int:pk>/edit-transaction/', mainview.EditTransactionView.as_view(), name='edit_transaction'),
]