from django.urls import path

from micro_client_service.controller.planSelection_views import plan_selection,is_plan_selected
from micro_client_service.controller.extra_views import contact,webfootprint

urlpatterns = [
    path('webfootprint',webfootprint),
    path('plan_selection/client_id=<str:client_id>',plan_selection),
    path('is_plan_selected/client_id=<str:client_id>',is_plan_selected),
    path('contact',contact)
]
