# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('make_call/', make_outbound_call, name='make_outbound_call'),
#     path('handle_call/', handle_call, name='handle_call'),
#     path('call/', call_page, name='call_page'),
#     path('get_twilio_token/', get_twilio_token, name='get_twilio_token'), 

# ]

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),  # Root URL को `/` से map करें
    path('make_call/', make_outbound_call, name='make_outbound_call'),
    path('handle_call/', handle_call, name='handle_call'),
    path('call/', call_page, name='call_page'),
    path('get_twilio_token/', get_twilio_token, name='get_twilio_token'),
]
