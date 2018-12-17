from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Subject)
admin.site.register(Exercise)
admin.site.register(Activity)
admin.site.register(AlternativeCategory)
admin.site.register(Step)
admin.site.register(Alternative)
admin.site.register(Feedback)
admin.site.register(Instruction)
admin.site.register(Curriculum)
admin.site.register(TutorStep)
admin.site.register(Evidence)

admin.site.register(Module)
admin.site.register(SequenceActivity)