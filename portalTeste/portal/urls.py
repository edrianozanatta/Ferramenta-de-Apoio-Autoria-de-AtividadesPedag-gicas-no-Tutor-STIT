from django.conf.urls import include, url
from django.conf.urls.static import static
from portalTeste import settings
from .views import *

app_name = "portal_teste"

urlpatterns = [
    url(r'^$', home, name='home'),

    url(r'add_module/$', add_module, name='add_module'),
    url(r'add_instruction/$', add_instruction, name='add_instruction'),
    url(r'add_exercise/$', add_exercise, name='add_exercise'),
    url(r'add_feedback_positive/$', add_feedback_positive, name='add_feedback_positive'),
    url(r'add_feedback_negative/$', add_feedback_negative, name='add_feedback_negative'),
    url(r'add_step/$', add_step, name='add_step'),
    url(r'add_alternatives/$', add_alternatives, name='add_alternatives'),

    url(r'exercise_step_view/$', exercise_step_view, name='exercise_step_view'),
    url(r'instruction_view/$', instruction_view, name='instruction_view'),
    url(r'view_feedback/$', view_feedback, name='view_feedback'),
    url(r'alternative_feedback_view/$', alternative_feedback_view, name='alternative_feedback_view'),
    url(r'step_alternative_view/$', step_alternative_view, name='step_alternative_view'),
    url(r'module_list_view/$', module_list_view, name='module_list_view'),

    url(r'exercise_delete/$', exercise_delete, name='exercise_delete'),
    url(r'step_remove/$', step_remove, name='step_remove'),
    url(r'remove_alternative/$', remove_alternative, name='remove_alternative'),
    url(r'feedback_remove/$', feedback_remove, name='feedback_remove'),
    url(r'instruction_remove/$', instruction_remove, name='instruction_remove'),
    url(r'module_delete/$', module_delete, name='module_delete'),

    url(r'exercise_edit/$', exercise_edit, name='exercise_edit'),
    url(r'step_edit/$', step_edit, name='step_edit'),
    url(r'edit_alternative/$', edit_alternative, name='edit_alternative'),
    url(r'feedback_edit/$', feedback_edit, name='feedback_edit'),
    url(r'instruction_edit/$', instruction_edit, name='instruction_edit'),
    url(r'module_edit/$', module_edit, name='module_edit'),

    # ajax methods
    url(r'ajax_ordena_sequence_curriculum/$', ajax_ordena_sequence_curriculum, name='ajax_ordena_sequence_curriculum'),


]

