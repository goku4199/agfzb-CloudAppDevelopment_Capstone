from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about/', view=views.get_about, name='about'),

    # path for contact us view
    path(route='contact_us/', view=views.get_contact_us, name='contact'),

    # path for registration
    path(route='registration/', view=views.registration_request, name='registration'),

    # path for login
    path(route='login/', view=views.login_request, name='login'),

    # path for logout
    path(route='logout/', view=views.logout_request, name='logout'),

    path(route='index/<int:dealer_id>', view=views.get_dealerships_by_id, name='index_id'),
    path(route='index/', view=views.get_dealerships, name='index'),

    # path for dealer reviews view 
    path(route='index/<int:dealer_id>/reviews', view=views.get_dealer_details, name='dealer_details'),

     path(route='index/<int:dealer_id>/add_review', view=views.add_review, name='add_review'),

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)