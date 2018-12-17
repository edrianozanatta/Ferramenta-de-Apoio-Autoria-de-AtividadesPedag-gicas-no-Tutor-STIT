from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


# assunto
class Subject(models.Model):
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    content = RichTextUploadingField(max_length=1500)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Activity ' + self.subject.name + ' ' + str(self.id)


class Exercise(Activity):
    difficulties = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    difficulty = models.IntegerField(choices=difficulties)
    user_exercise = models.BooleanField()

    def __str__(self):
        return 'Exercise ' + str(self.id)


class Instruction(Activity):
    title = models.CharField(max_length=85)
    levels = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    level = models.IntegerField(choices=levels)

    def __str__(self):
        return 'Instruction ' + str(self.id)


class Curriculum(models.Model):
    sequence = models.IntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity.__class__.__name__ + ' ' + str(self.sequence)


class Step(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    content = RichTextUploadingField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class AlternativeCategory(models.Model):
    name = models.CharField(max_length=85)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Alternative(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    content = RichTextUploadingField(max_length=500)
    answer = models.CharField(max_length=500)
    answer_ck = models.CharField(max_length=500)
    answer_text = RichTextUploadingField(max_length=500)
    category = models.ForeignKey(AlternativeCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Feedback(models.Model):
    alternative = models.ForeignKey(Alternative, on_delete=models.CASCADE)
    feedback = RichTextUploadingField(max_length=500)
    state = models.BooleanField()
    levels = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    level = models.IntegerField(choices=levels)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Feedback' + self.feedback


class Module(models.Model):
    title = models.CharField(max_length=85)
    sequence = models.IntegerField()

    def __str__(self):
        return self.title


class SequenceActivity(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    sequence = models.IntegerField()


class Evidence(models.Model):
    name = models.CharField(max_length=85)


class TutorStep(Step):
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)
    difficulties = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    difficulty = models.IntegerField(choices=difficulties)

    def __str__(self):
        return self.evidence.name

