from django.urls import path
from astree.views import combine_rules, evaluate_rule, home, ListAllRules

app_name = "astree"

urlpatterns = [
    path('', ListAllRules, name='all_rules'),
    path('create_rule/', combine_rules, name='create_rule'),
    path('evaluate_rule/', evaluate_rule, name='evaluate_rule'),
]
