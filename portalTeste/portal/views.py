import re
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.views.decorators.csrf import csrf_exempt
import ipdb


# ------HOME-----------------------------------------------#####
def home(request):
    generate_sequence_curriculum()
    exercises = Exercise.objects.all()
    instructions = Instruction.objects.all()
    modules = Module.objects.all().order_by('sequence')
    sequence_activitys = SequenceActivity.objects.all().order_by('sequence')
    curriculums = Curriculum.objects.all().order_by('sequence')

    context = {
        'exercises': exercises,
        'instructions': instructions,
        'modules': modules,
        'sequence_activitys': sequence_activitys,
        'curriculums': curriculums,
    }
    return render(request, 'home.html', context)
# --------------------------------------------------------------


# ------ADD------------------------------------------------#####
def add_module(request):
    if request.method == "POST":

        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)

            modules = Module.objects.all()
            module.sequence = len(modules) + 1

            module.save()

            return redirect('/')
    else:
        form = ModuleForm()
    generate_sequence_curriculum()
    return render(request, 'module_edit.html', {'form': form, 'tit': 'Novo Módulo'})


def add_instruction(request):
    modules = Module.objects.all()

    if request.method == "POST":

        form = InstructionForm(request.POST)
        if form.is_valid():
            instruction = form.save(commit=False)
            pk = request.POST.get('modulo', None)

            module = get_object_or_404(Module, pk=int(pk))

            instruction.save()

            # buscando o maior numero da sequencia do modulo, para adicionar a instrucao como ultimo elemento do modulo
            sequence_activitys = SequenceActivity.objects.all()
            aux = 0
            for sequence_activity in sequence_activitys:
                if sequence_activity.module == module:
                    if sequence_activity.sequence > aux:
                        aux = sequence_activity.sequence

            if aux == 0:
                for sequence_activity in sequence_activitys:
                    if sequence_activity.sequence > aux:
                        aux = sequence_activity.sequence

            new_sequence_activity = SequenceActivity()
            new_sequence_activity.sequence = aux
            new_sequence_activity.module = module
            new_sequence_activity.activity = instruction
            new_sequence_activity.save()

            # ordenando sequence do curriculum
            generate_sequence_curriculum()

            # redireciona para a url home
            return redirect('/instruction_view/?pk=' + str(instruction.pk))
    else:
        form = InstructionForm()
    return render(request, 'instruction_edit.html', {'form': form, 'tit': 'Nova Instrução', 'modules': modules})


def add_exercise(request):
    modules = Module.objects.all()
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user_exercise = False
            exercise.difficulty = 1
            pk = request.POST.get('modulo', None)

            module = get_object_or_404(Module, pk=int(pk))

            exercise.save()

            # buscando o maior numero da sequencia do modulo, para adicionar a instrucao como ultimo elemento do modulo
            sequence_activitys = SequenceActivity.objects.all()
            aux = 0
            for sequence_activity in sequence_activitys:
                if sequence_activity.module == module:
                    if sequence_activity.sequence > aux:
                        aux = sequence_activity.sequence

            new_sequence_activity = SequenceActivity()
            new_sequence_activity.sequence = aux
            new_sequence_activity.module = module
            new_sequence_activity.activity = exercise
            new_sequence_activity.save()

            # ordenando sequence do curriculum
            generate_sequence_curriculum()

            return redirect('/exercise_step_view/?pk=' + str(exercise.pk))
    else:
        form = ExerciseForm()
    return render(request, 'exercise_edit.html', {'form': form, 'tit': 'Novo Exercício', 'modules': modules})


def add_step(request):
    pkExercise = request.GET.get('pk', None)
    exercise = get_object_or_404(Exercise, pk=pkExercise)

    if request.method == "POST":
        form = TutorStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.exercise = exercise
            step.evidence = get_object_or_404(Evidence, pk=1)
            step.save()

            steps = TutorStep.objects.filter(exercise=exercise)
            aux = 1
            for step in steps:
                if step.difficulty > aux:
                    aux = step.difficulty

            exercise.difficulty = aux
            exercise.save()

            return redirect('/exercise_step_view/?pk=' + str(exercise.pk))
    else:
        form = TutorStepForm()
    return render(request, 'step_edit.html', {'form': form, 'tit': 'Novo Passo', 'exercise': exercise})


def add_alternatives(request):
    pkStep = request.GET.get('pk', None)
    step = get_object_or_404(Step, pk=pkStep)

    if request.method == "POST":

        form = AlternativeForm(request.POST)
        if form.is_valid():
            alternative = form.save(commit=False)
            alternative.step = step
            category = request.POST.get('categoria', None)
            alternative.category = get_object_or_404(AlternativeCategory, name=category)

            if category == 'BLANK_EXPRESSION':
                answer = request.POST.get('answer_blank', None)
                alternative.answer_ck = answer
                s = answer
                if re.search('alt="(.*)" s', s):
                    s2 = re.search('alt="(.*)" s', s)
                    aux = s2.group(0)
                    n = aux[5:len(aux) - 3]
                    alternative.answer = n
                    alternative.save()
                    return redirect('/step_alternative_view/?pk=' + str(step.pk))
                else:
                    return render(request, 'alternative_edit.html', {'form': form, 'step': step, 'tit': 'Nova Alternativa', 'erro': 'erro'})
            else:
                answer = request.POST.get('answer_multiple', None)
                alternative.answer_ck = answer
                alternative.answer = answer
                alternative.save()
                return redirect('/step_alternative_view/?pk=' + str(step.pk))
        else:
            if len(request.POST.get('content', None)) > 500:
                return render(request, 'alternative_edit.html', {'form': form, 'step': step, 'tit': 'Nova Alternativa', 'erro': 'content'})
            else:
                return render(request, 'alternative_edit.html', {'form': form, 'step': step, 'tit': 'Nova Alternativa', 'erro': 'blank'})
    else:
        form = AlternativeForm()
    return render(request, 'alternative_edit.html', {'form': form, 'step': step, 'tit': 'Nova Alternativa'})


def add_feedback_positive(request):
    pkAlternative = request.GET.get('pk', None)
    alternative = get_object_or_404(Alternative, pk=pkAlternative)

    if request.method == "POST":

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.alternative = alternative
            feedback.state = True
            feedback.save()
            return redirect('/alternative_feedback_view/?pk=' + str(alternative.pk))
    else:
        form = FeedbackForm()
    return render(request, 'feedback_edit.html', {'form': form, 'tit': 'Novo Feedback', 'alternative': alternative})


def add_feedback_negative(request):
    pkAlternative = request.GET.get('pk', None)
    alternative = get_object_or_404(Alternative, pk=pkAlternative)

    if request.method == "POST":

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.alternative = alternative
            feedback.state = False
            feedback.save()
            return redirect('/alternative_feedback_view/?pk=' + str(alternative.pk))
    else:
        form = FeedbackForm()
    return render(request, 'feedback_edit.html', {'form': form, 'tit': 'Novo Feedback', 'alternative': alternative})
# -----------------------------------------------------------


# ----VIEW---------------------------------------------------
def exercise_step_view(request):
    pkExercise = request.GET.get('pk', None)
    exercise = get_object_or_404(Exercise, pk=pkExercise)
    steps = Step.objects.filter(exercise=exercise)
    context = {
        'exercise': exercise,
        'steps': steps,
    }
    return render(request, 'exercise_step_view.html', context)


def step_alternative_view(request):
    if request.method == 'GET':
        pkStep = request.GET.get('pk', None)
        step = get_object_or_404(TutorStep, pk=pkStep)
        exercise = get_object_or_404(Exercise, pk=step.exercise.pk)

        alternatives = Alternative.objects.filter(step=step)

        context = {
            'step': step,
            'alternatives': alternatives,
        }
    return render(request, 'step_alternative_view.html', context)


def alternative_feedback_view(request):
    if request.method == 'GET':
        pkAlternative = request.GET.get('pk', None)
        alternative = get_object_or_404(Alternative, pk=pkAlternative)
        feedbacks = Feedback.objects.filter(alternative=alternative)

        context = {
            'alternative': alternative,
            'feedbacks': feedbacks,
        }
    return render(request, 'alternative_feedback_view.html', context)


def view_feedback(request):
    if request.method == 'GET':
        pkFeedback = request.GET.get('pk', None)
        feedback = get_object_or_404(Feedback, pk=pkFeedback)

        context = {
            'feedback': feedback,
        }
    return render(request, 'feedback_view.html', context)


def instruction_view(request):
    if request.method == 'GET':
        pkInstruction = request.GET.get('pk', None)
        instruction = get_object_or_404(Instruction, pk=pkInstruction)

        context = {
            'instruction': instruction,
        }
    return render(request, 'instruction_view.html', context)


def module_list_view(request):
    if request.method == 'GET':
        modules = Module.objects.all()

        context = {
            'modules': modules,
        }
    return render(request, 'module_list_view.html', context)
# -----------------------------------------------------------


# ----DELETE-------------------------------------------------
def exercise_delete(request):
    if request.method == 'GET':
        pkExercise = request.GET.get('pk', None)
        exercise = get_object_or_404(Exercise, pk=pkExercise)
        exercise.delete()
        generate_sequence_curriculum()
    return redirect('/')


def step_remove(request):
    if request.method == 'GET':
        pkStep = request.GET.get('pk', None)
        step = get_object_or_404(Step, pk=pkStep)
        exercise = get_object_or_404(Exercise, pk=step.exercise.pk)
        step.delete()
    return redirect('/exercise_step_view/?pk=' + str(exercise.pk))


def feedback_remove(request):
    if request.method == 'GET':
        pkFeedback = request.GET.get('pk', None)
        feedback = get_object_or_404(Feedback, pk=pkFeedback)
        alternative = feedback.alternative
        feedback.delete()
    return redirect('/alternative_feedback_view/?pk=' + str(alternative.pk))


def remove_alternative(request):
    if request.method == 'GET':
        pkAlternative = request.GET.get('pk', None)
        alternative = get_object_or_404(Alternative, pk=pkAlternative)
        step = alternative.step
        alternative.delete()
    return redirect('/step_alternative_view/?pk=' + str(step.pk))


def instruction_remove(request):
    if request.method == 'GET':
        pkInstruction = request.GET.get('pk', None)
        instruction = get_object_or_404(Instruction, pk=pkInstruction)
        instruction.delete()
        generate_sequence_curriculum()
    return redirect('/')


def module_delete(request):
    if request.method == 'GET':
        modules = Module.objects.all()
        pkModule = request.GET.get('pk', None)
        module = get_object_or_404(Module, pk=pkModule)
        if len(modules) > 1:
            sequence_activitys = SequenceActivity.objects.all().order_by('sequence')
            if modules[0] == module:
                for sequence_activity in sequence_activitys:
                    if sequence_activity.module.pk == module.pk:
                        sequence_activity.module = modules[1]
                        sequence_activity.save()
                module.delete()
            else:
                for sequence_activity in sequence_activitys:
                    if sequence_activity.module.pk == module.pk:
                        sequence_activity.module = modules[0]
                        sequence_activity.save()
                module.delete()
    generate_sequence_curriculum()
    return redirect('/')
# ------------------------------------------------------------


# ----EDIT---------------------------------------------------
def exercise_edit(request):
    pkExercise = request.GET.get('pk', None)
    exercise = get_object_or_404(Exercise, pk=pkExercise)
    modules = Module.objects.all()
    sequence_activitys = SequenceActivity.objects.all()
    pk_module_selected = 0

    for seq_act in sequence_activitys:
        if seq_act.activity.pk == exercise.pk:
            pk_module_selected = seq_act.module.pk

    if request.method == "POST":
        form = ExerciseForm(request.POST, instance=exercise)

        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user_exercise = False

            pk = request.POST.get('modulo', None)
            module = get_object_or_404(Module, pk=int(pk))

            exercise.save()

            for seq_act in sequence_activitys:
                if seq_act.activity.pk == exercise.pk:
                    if seq_act.module != module:
                        seq_act.module = module
                        seq_act.save()
            generate_sequence_curriculum()
            return redirect('/exercise_step_view/?pk=' + str(exercise.pk))
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercise_edit.html', {'form': form, 'tit': 'Editar Exercício', 'modules': modules, 'pk_module_selected':  pk_module_selected})


def step_edit(request):
    pkStep = request.GET.get('pk', None)
    step = get_object_or_404(TutorStep, pk=pkStep)
    exercise = get_object_or_404(Exercise, pk=step.exercise.pk)

    if request.method == "POST":
        form = TutorStepForm(request.POST, instance=step)
        if form.is_valid():
            step = form.save(commit=False)
            step.save()

            steps = TutorStep.objects.filter(exercise=exercise)
            aux = 1
            for step in steps:
                if step.difficulty > aux:
                    aux = step.difficulty

            if exercise.difficulty != aux:
                exercise.difficulty = aux
                exercise.save()

            return redirect('/step_alternative_view/?pk=' + str(step.pk))
    else:
        form = TutorStepForm(instance=step)
    return render(request, 'step_edit.html', {'form': form, 'tit': 'Editar Passo', 'exercise': exercise})


def module_edit(request):
    pkModule = request.GET.get('pk', None)
    module = get_object_or_404(Module, pk=pkModule)

    if request.method == "POST":
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            module = form.save(commit=False)

            module.save()

            return redirect('/')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'module_edit.html', {'form': form, 'tit': 'Editar Módulo', 'module': module})


def edit_alternative(request):
    pkAlternative = request.GET.get('pk', None)
    alternative = get_object_or_404(Alternative, pk=pkAlternative)
    step = get_object_or_404(TutorStep, pk=alternative.step.pk)

    if request.method == "POST":
        form = AlternativeForm(request.POST, instance=alternative)

        category = request.POST.get('categoria', None)
        alternative.category = get_object_or_404(AlternativeCategory, name=category)

        if form.is_valid():
            alternative = form.save(commit=False)

            if category == 'BLANK_EXPRESSION':
                answer = request.POST.get('answer_blank', None)
                alternative.answer_ck = answer
                s = answer
                if re.search('alt="(.*)" s', s):
                    s2 = re.search('alt="(.*)" s', s)
                    aux = s2.group(0)
                    n = aux[5:len(aux) - 3]
                    alternative.answer = n
                    alternative.save()
                    return redirect('/step_alternative_view/?pk=' + str(step.pk))
                else:
                    return render(request, 'alternative_edit.html',
                                  {'form': form, 'step': step, 'tit': 'Editar Alternativa', 'erro': 'erro', 'answer': alternative.answer_ck})
            else:
                answer = request.POST.get('answer_multiple', None)
                alternative.answer_ck = answer
                alternative.answer = answer
                alternative.save()
                return redirect('/step_alternative_view/?pk=' + str(step.pk))
        else:
            return render(request, 'alternative_edit.html',
                          {'form': form, 'step': step, 'tit': 'Editar Alternativa', 'erro': 'blank', 'answer': alternative.answer_ck})
    else:
        form = AlternativeForm(instance=alternative)
    return render(request, 'alternative_edit.html', {'form': form, 'step': step, 'tit': 'Editar Alternativa', 'answer': alternative.answer_ck})


def feedback_edit(request):
    pkFeedback = request.GET.get('pk', None)
    feedback = get_object_or_404(Feedback, pk=pkFeedback)
    alternative = get_object_or_404(Alternative, pk=feedback.alternative.pk)

    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.save()
            return redirect('/alternative_feedback_view/?pk=' + str(feedback.alternative.pk))
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback_edit.html', {'form': form, 'tit': 'Editar Feedback', 'alternative': alternative})


def instruction_edit(request):
    pkInstruction = request.GET.get('pk', None)
    instruction = get_object_or_404(Instruction, pk=pkInstruction)
    modules = Module.objects.all()
    sequence_activitys = SequenceActivity.objects.all()
    pk_module_selected = 0
    for seq_act in sequence_activitys:
        if seq_act.activity.pk == instruction.pk:
            pk_module_selected = seq_act.module.pk

    if request.method == "POST":
        form = InstructionForm(request.POST, instance=instruction)
        if form.is_valid():
            instruction = form.save(commit=False)

            pk = request.POST.get('modulo', None)
            module = get_object_or_404(Module, pk=int(pk))

            instruction.save()

            for seq_act in sequence_activitys:
                if seq_act.activity.pk == instruction.pk:
                    if seq_act.module != module:
                        seq_act.module = module
                        seq_act.save()
            generate_sequence_curriculum()
            return redirect('/instruction_view/?pk=' + str(instruction.pk))
    else:
        form = InstructionForm(instance=instruction)
    return render(request, 'instruction_edit.html', {'form': form, 'tit': 'Editar Instrução', 'modules': modules, 'pk_module_selected': pk_module_selected})
# -------------------------------------------------------------


# -------------------------------------------------------------
@csrf_exempt
def ajax_ordena_sequence_curriculum(request):
    l = []
    new_sequence = request.POST.get('sequence', None)
    sequence_activity = SequenceActivity.objects.all()
    if new_sequence:
        new_sequence_list = new_sequence.split(',')
        new_sequence_list = new_sequence_list[:-1]

        auxModule = 1
        auxActivity = 1

        for li in new_sequence_list:
            m = li.split('_')
            if m[1] == "aa":
                module = get_object_or_404(Module, pk=int(m[0]))
                module.sequence = auxModule
                module.save()
                auxModule = auxModule + 1
            else:
                for seq in sequence_activity:
                    if int(m[1]) == seq.activity.pk:
                        seq_act = get_object_or_404(SequenceActivity, pk=seq.pk)
                        seq_act.module = module
                        seq_act.sequence = auxActivity
                        seq_act.save()
                        auxActivity = auxActivity + 1
    generate_sequence_curriculum()
    return JsonResponse({'message': 'sucess'})


def generate_sequence_curriculum():
    sequence_activitys = SequenceActivity.objects.all().order_by('sequence')
    curriculums = Curriculum.objects.all()
    instructions = Instruction.objects.all()
    exercises = Exercise.objects.all()
    aux = 0
    aux_count = 1
    i = 0
    l = []
    for sequence_activity in sequence_activitys:

        # se for uma instrucao altera ou adiciona na sequencia curriculum
        for instruction in instructions:
            if sequence_activity.activity.pk == instruction.pk:
                aux = 1
        if aux == 1:

            # testa se a instrucao ja esta na sequencia do curriculum
            aux = 0
            for curriculum in curriculums:
                if sequence_activity.activity == curriculum.activity:
                    curriculum.sequence = aux_count
                    aux_count = aux_count + 1
                    curriculum.save()
                    aux = 1

            # se nao esta na sequencia do curriculum adiciona um novo
            if aux == 0:
                curriculum = Curriculum()
                curriculum.activity = sequence_activity.activity
                curriculum.sequence = aux_count
                aux_count = aux_count + 1
                curriculum.save()
        else:
            # se o primeiro elemento da lista for exercicio adiciona, senao testa
            if i == 0:
                aux = 0
                curriculums = Curriculum.objects.all()
                for curriculum in curriculums:
                    if sequence_activity.activity.pk == curriculum.activity.pk:
                        curriculum.sequence = aux_count
                        aux_count = aux_count + 1
                        curriculum.save()
                        aux = 1
                # se nao esta na sequencia do curriculum adiciona um novo
                if aux == 0:
                    curriculum = Curriculum()
                    curriculum.activity = sequence_activity.activity
                    curriculum.sequence = aux_count
                    aux_count = aux_count + 1
                    curriculum.save()
            else:
                aux = 0
                sequence_activity_anterior = sequence_activitys[i - 1]
                sequence_activity_atual = sequence_activity

                for exercise in exercises:
                    if sequence_activity_anterior.activity.pk == exercise.pk:
                        aux = 1
                        activity_anterior = sequence_activity_anterior.activity

                if aux == 1:
                    activity_atual = sequence_activity_atual.activity
                    if activity_anterior.subject != activity_atual.subject:
                        aux = 0
                        curriculums = Curriculum.objects.all()
                        for curriculum in curriculums:
                            if sequence_activity_atual.activity.pk == curriculum.activity.pk:
                                aux = 1
                                curriculum.sequence = aux_count
                                aux_count = aux_count + 1
                                curriculum.save()
                        if aux == 0:
                            curriculum = Curriculum()
                            curriculum.activity = sequence_activity.activity
                            curriculum.sequence = aux_count
                            aux_count = aux_count + 1
                            curriculum.save()
                    else:
                        for curriculum in curriculums:
                            if curriculum.activity == activity_atual:
                                curriculum.delete()
                else:
                    aux = 0
                    curriculums = Curriculum.objects.all()
                    for curriculum in curriculums:
                        if sequence_activity_atual.activity.pk == curriculum.activity.pk:
                            aux = 1
                            curriculum.sequence = aux_count
                            aux_count = aux_count + 1
                            curriculum.save()
                    if aux == 0:
                        curriculum = Curriculum()
                        curriculum.activity = sequence_activity.activity
                        curriculum.sequence = aux_count
                        aux_count = aux_count + 1
                        curriculum.save()
        i = i + 1
        aux = 0
    return l

