from django.forms import ModelForm
from .models import *


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['content', 'subject']


class AlternativeCategoryForm(ModelForm):
    class Meta:
        model = AlternativeCategory
        fields = ['name']


class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ['content']


class AlternativeForm(ModelForm):
    class Meta:
        model = Alternative
        fields = ['content', 'answer_text']


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'level']


class InstructionForm(ModelForm):
    class Meta:
        model = Instruction
        fields = ['content', 'subject',
                  'title', 'level']


class CurriculumForm(ModelForm):
    class Meta:
        model = Curriculum
        fields = ['sequence', 'activity']


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['title']


class TutorStepForm(ModelForm):
    class Meta:
        model = TutorStep
        fields = ['content', 'difficulty']
