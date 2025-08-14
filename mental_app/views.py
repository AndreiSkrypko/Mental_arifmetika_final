import random
import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from .models import Students, TeacherProfile, Class, StudentAccount, Homework, Attendance, PaymentSettings, MonthlySchedule
from .forms import StudentForm, TeacherRegistrationForm, TeacherLoginForm, ClassForm, TeacherProfileUpdateForm, StudentAccountForm, StudentLoginForm, HomeworkForm, AttendanceForm, AttendanceDateForm, PaymentSettingsForm, MonthlyScheduleForm, MonthlyAttendanceForm

# Определяем словарь диапазонов чисел
RANGES = {
    '1-9': list(range(1, 10)),
    '10-19': list(range(10, 19)),
    '20-29': list(range(20, 29)),
    '30-70': list(range(30, 70)),
    '80-120': list(range(80, 120)),
    '10-99': list(range(10, 100)),
    '100-999': list(range(100, 1000)),
    '1000-9999': list(range(1000, 10000)),
    '10000-99999': list(range(10000, 100000)),
    '10': list(range(1, 10)),
    '50': list(range(1, 50)),
    '100': list(range(1, 100)),
    '200': list(range(1, 200)),
    '1000': list(range(1, 1000)),
    'random': list(range(1, 101)),
    'both-lower': list(range(1, 51)),
    'one-lower-one-higher': list(range(1, 101)),
    'both-higher': list(range(50, 151)),
    '2-9': list(range(2, 10)),
    "1-10": list(range(1, 10)),
    "10-100": list(range(10, 100)),
    "100-1000": list(range(100, 1000)),
    "1000-10000": list(range(1000, 10000)),
}


# Обработчик главной страницы
def index(request):
    if request.method == 'GET':  # Если запрос GET
        return render(request, 'index.html')  # Отображаем шаблон index.html
    if request.method == 'POST':  # Если запрос POST (но пока не обработан)
        pass  # Ничего не делаем


# Обработчик выбора и проверки умножения
def multiplication_choose(request, mode):
    if mode == 1:  # Этап выбора чисел
        if request.method == 'GET':  # Если запрос GET
            return render(request, 'multiplication_choose.html', {"mode": 1})  # Отображаем форму выбора чисел

        if request.method == 'POST':  # Если запрос POST
            # Получаем выбранные диапазоны чисел из формы
            first_multiplier_range = request.POST.get('first-multiplier')
            second_multiplier_range = request.POST.get('second-multiplier')

            # Получаем списки чисел из словаря RANGES
            first_multipliers = RANGES.get(first_multiplier_range, [])
            second_multipliers = RANGES.get(second_multiplier_range, [])

            # Если хотя бы один список пустой, перенаправляем пользователя обратно
            if not first_multipliers or not second_multipliers:
                return redirect('multiplication_choose', mode=1)

            # Сохраняем диапазоны и случайные числа в сессии
            request.session['first_multiplier_range'] = first_multiplier_range
            request.session['second_multiplier_range'] = second_multiplier_range
            request.session['first'] = random.choice(first_multipliers)  # Случайное число из первого списка
            request.session['second'] = random.choice(second_multipliers)  # Случайное число из второго списка

            # Переход на следующий этап (отображение примера)
            return redirect('multiplication_choose', mode=2)

    elif mode == 2:  # Этап отображения примера
        first = request.session.get('first')  # Получаем первое число из сессии
        second = request.session.get('second')  # Получаем второе число из сессии

        # Если чисел нет в сессии, возвращаем пользователя на этап выбора
        if first is None or second is None:
            return redirect('multiplication_choose', mode=1)

        # Отображаем шаблон с примером для умножения
        return render(request, 'multiplication_choose.html', {
            'first': first,
            'second': second,
            'operation': '×',  # Знак умножения
            'mode': 2
        })

    elif mode == 3:  # Этап проверки ответа
        first = request.session.get('first')  # Получаем первое число
        second = request.session.get('second')  # Получаем второе число
        first_multiplier_range = request.session.get('first_multiplier_range')  # Получаем диапазон первого числа
        second_multiplier_range = request.session.get('second_multiplier_range')  # Получаем диапазон второго числа

        if request.method == 'POST':  # Если запрос POST
            user_answer = request.POST.get('user-answer')  # Получаем ответ пользователя
            correct_answer = first * second  # Вычисляем правильный ответ

            if user_answer and user_answer.isdigit() and int(user_answer) == correct_answer:
                result_message = "Верно! Молодец!"  # Сообщение о правильном ответе
                result_color = "green"  # Цвет сообщения

                # Генерируем новый пример
                first_multipliers = RANGES.get(first_multiplier_range,
                                               [])  # Получаем список чисел для первого множителя
                second_multipliers = RANGES.get(second_multiplier_range,
                                                [])  # Получаем список чисел для второго множителя

                if first_multipliers and second_multipliers:
                    request.session['first'] = random.choice(first_multipliers)  # Случайное число для нового примера
                    request.session['second'] = random.choice(second_multipliers)  # Случайное число для нового примера
            else:
                result_message = "Неверно! Попробуйте снова."  # Сообщение о неверном ответе
                result_color = "red"  # Цвет сообщения

            # Отображаем шаблон с результатом проверки
            return render(request, 'multiplication_choose.html', {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'result': result_message,
                'result_color': result_color,
                'mode': 3
            })

        # Если запрос GET, возвращаем пользователя на предыдущий этап (отображение примера)
        return redirect('multiplication_choose', mode=2)


# Обработчик выбора и проверки умножения до 20
def multiplication_to_20(request, mode):
    if mode == 1:  # Этап выбора чисел
        if request.method == 'GET':  # Если запрос GET
            return render(request, 'multiplication_to_20.html', {"mode": 1})  # Отображаем форму выбора чисел

        if request.method == 'POST':  # Если запрос POST
            # Получаем выбранные диапазоны чисел из формы
            first_multiplier_range = request.POST.get('first-multiplier')  # Диапазон первого множителя
            second_multiplier_value = request.POST.get('second-multiplier')  # Значение второго множителя (не диапазон)

            # Получаем список чисел для первого множителя из словаря RANGES
            first_multipliers = RANGES.get(first_multiplier_range, [])

            # Для второго множителя просто сохраняем значение, так как оно не из списка
            try:
                second_multiplier = int(second_multiplier_value)  # Преобразуем значение второго множителя в число
            except ValueError:
                second_multiplier = None  # Если значение не число, сохраняем как None

            # Если хотя бы одно число пустое или второй множитель вне диапазона 1-20, перенаправляем обратно
            if not first_multipliers or second_multiplier is None or not (1 <= second_multiplier <= 20):
                return redirect('multiplication_to_20', mode=1)

            # Сохраняем диапазоны и случайные числа в сессии
            request.session['first_multiplier_range'] = first_multiplier_range  # Диапазон первого множителя
            request.session['second_multiplier'] = second_multiplier  # Указанный второй множитель
            request.session['first'] = random.choice(first_multipliers)  # Случайное число из первого диапазона
            request.session['second'] = second_multiplier  # Указанный второй множитель

            # Переход на следующий этап (отображение примера)
            return redirect('multiplication_to_20', mode=2)

    elif mode == 2:  # Этап отображения примера
        first = request.session.get('first')  # Получаем первое число из сессии
        second = request.session.get('second')  # Получаем второе число из сессии

        # Если чисел нет в сессии, возвращаем пользователя на этап выбора
        if first is None or second is None:
            return redirect('multiplication_to_20', mode=1)

        # Отображаем шаблон с примером для умножения
        return render(request, 'multiplication_to_20.html', {
            'first': first,
            'second': second,
            'operation': '×',  # Знак умножения
            'mode': 2
        })

    elif mode == 3:  # Этап проверки ответа
        first = request.session.get('first')  # Получаем первое число
        second = request.session.get('second')  # Получаем второе число
        first_multiplier_range = request.session.get('first_multiplier_range')  # Получаем диапазон первого числа
        second_multiplier = request.session.get('second_multiplier')  # Получаем второй множитель

        if request.method == 'POST':  # Если запрос POST
            user_answer = request.POST.get('user-answer')  # Получаем ответ пользователя
            correct_answer = first * second  # Вычисляем правильный ответ

            # Проверка правильности ответа
            if user_answer and user_answer.isdigit() and int(user_answer) == correct_answer:
                result_message = "Верно! Молодец!"  # Сообщение о правильном ответе
                result_color = "green"  # Цвет сообщения

                # Генерируем новый пример
                first_multipliers = RANGES.get(first_multiplier_range,
                                               [])  # Получаем список чисел для первого множителя

                if first_multipliers:
                    request.session['first'] = random.choice(first_multipliers)  # Случайное число для нового примера
                    request.session['second'] = second  # Второй множитель остается неизменным
            else:
                result_message = "Неверно! Попробуйте снова."  # Сообщение о неверном ответе
                result_color = "red"  # Цвет сообщения

            # Отображаем шаблон с результатом проверки
            return render(request, 'multiplication_to_20.html', {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'result': result_message,
                'result_color': result_color,
                'mode': 3
            })

        # Если запрос GET, возвращаем пользователя на предыдущий этап (отображение примера)
        return redirect('multiplication_to_20', mode=2)


# Обработчик выбора и проверки возведения в квадрат
def square(request, mode):
    if mode == 1:
        if request.method == 'GET':
            return render(request, 'square.html', {"mode": 1})

        if request.method == 'POST':
            selected_ranges = request.POST.getlist('number-ranges')

            first_multipliers = []
            for r in selected_ranges:
                first_multipliers.extend(RANGES.get(r, []))

            if not first_multipliers:
                return redirect('square', mode=1)

            first = random.choice(first_multipliers)
            second = random.choice(first_multipliers)

            request.session['first'] = first
            request.session['second'] = second
            request.session['selected_ranges'] = selected_ranges

            return redirect('square', mode=2)

    elif mode == 2:
        first = request.session.get('first')
        second = request.session.get('second')

        if first is None or second is None:
            return redirect('square', mode=1)

        return render(request, 'square.html', {
            'first': first,
            'second': second,
            'operation': '×',
            'mode': 2
        })

    elif mode == 3:
        first = request.session.get('first')
        second = request.session.get('second')
        selected_ranges = request.session.get('selected_ranges', [])

        if request.method == 'POST':
            user_answer = request.POST.get('user-answer')
            correct_answer = first * second

            if user_answer and user_answer.isdigit() and int(user_answer) == correct_answer:
                result_message = "Верно! Молодец!"
                result_color = "green"

                first_multipliers = []
                for r in selected_ranges:
                    first_multipliers.extend(RANGES.get(r, []))

                if first_multipliers:
                    request.session['first'] = random.choice(first_multipliers)
                    request.session['second'] = random.choice(first_multipliers)
            else:
                result_message = "Неверно! Попробуйте снова."
                result_color = "red"

            return render(request, 'square.html', {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'result': result_message,
                'result_color': result_color,
                'mode': 3
            })

        return redirect('square', mode=2)


# Обработчик выбора и проверки умножение от базы
def multiplication_base(request, mode):
    if mode == 1:
        if request.method == 'GET':
            return render(request, 'multiplication_base.html', {"mode": 1})

        if request.method == 'POST':
            selected_ranges = request.POST.getlist('multiplier-range')

            first_multipliers = []
            for r in selected_ranges:
                first_multipliers.extend(RANGES.get(r, []))

            if not first_multipliers:
                return redirect('multiplication_base', mode=1)

            first = random.choice(first_multipliers)
            second = random.choice(first_multipliers)

            request.session['first'] = first
            request.session['second'] = second
            request.session['selected_ranges'] = selected_ranges

            return redirect('multiplication_base', mode=2)

    elif mode == 2:
        first = request.session.get('first')
        second = request.session.get('second')

        if first is None or second is None:
            return redirect('multiplication_base', mode=1)

        return render(request, 'multiplication_base.html', {
            'first': first,
            'second': second,
            'operation': '×',
            'mode': 2
        })

    elif mode == 3:
        first = request.session.get('first')
        second = request.session.get('second')
        selected_ranges = request.session.get('selected_ranges', [])

        if request.method == 'POST':
            user_answer = request.POST.get('user-answer')
            correct_answer = first * second

            if user_answer and user_answer.isdigit() and int(user_answer) == correct_answer:
                result_message = "Верно! Молодец!"
                result_color = "green"

                first_multipliers = []
                for r in selected_ranges:
                    first_multipliers.extend(RANGES.get(r, []))

                if first_multipliers:
                    request.session['first'] = random.choice(first_multipliers)
                    request.session['second'] = random.choice(first_multipliers)
            else:
                result_message = "Неверно! Попробуйте снова."
                result_color = "red"

            return render(request, 'multiplication_base.html', {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'result': result_message,
                'result_color': result_color,
                'mode': 3
            })

        return redirect('multiplication_base', mode=2)


# функция для определения двух множителей при выборе двухзначных чисел
def generate_two_digit_pair():
    """Генерирует пару двузначных чисел с одинаковым десятком и суммой единиц 10."""
    tens = random.randint(1, 9)  # Выбираем десяток от 10 до 90
    unit1 = random.randint(1, 9)  # Выбираем первую единицу
    unit2 = 10 - unit1  # Вторая единица должна дополнять до 10
    first = tens * 10 + unit1
    second = tens * 10 + unit2
    return first, second


# функция для определения двух множителей при выборе трехзначных чисел
def generate_three_digit_pair():
    """Генерирует пару трехзначных чисел с одинаковыми сотнями и десятками, сумма единиц 10."""
    hundreds = random.randint(1, 9)  # Выбираем сотню (100-900)
    tens = random.randint(0, 9)  # Выбираем десяток (00-90)
    unit1 = random.randint(1, 9)  # Выбираем первую единицу
    unit2 = 10 - unit1  # Вторая единица дополняет до 10
    first = hundreds * 100 + tens * 10 + unit1
    second = hundreds * 100 + tens * 10 + unit2
    return first, second


# Обработчик выбора и проверки хитрости
def tricks(request, mode):
    if mode == 1:
        if request.method == 'GET':
            return render(request, 'tricks.html', {"mode": 1})

        if request.method == 'POST':
            number_type = request.POST.get('number-type')  # Двузначные или трехзначные

            if number_type == "2":  # Обрабатываем "2" как двузначные
                first, second = generate_two_digit_pair()
            elif number_type == "3":  # Обрабатываем "3" как трехзначные
                first, second = generate_three_digit_pair()
            else:
                return redirect('tricks', mode=1)  # В случае ошибки вернемся к выбору типа чисел

            # Сохраняем данные в сессии
            request.session['first'] = first
            request.session['second'] = second
            request.session['number_type'] = number_type

            return redirect('tricks', mode=2)  # Переход к режиму 2

    elif mode == 2:
        # Получаем данные из сессии
        first = request.session.get('first')
        second = request.session.get('second')

        if first is None or second is None:
            return redirect('tricks', mode=1)  # Если данных нет в сессии, возвращаем на выбор чисел

        return render(request, 'tricks.html', {
            'first': first,
            'second': second,
            'operation': '×',
            'mode': 2
        })

    elif mode == 3:
        first = request.session.get('first')
        second = request.session.get('second')
        number_type = request.session.get('number_type')

        if first is None or second is None:
            return redirect('tricks', mode=1)  # Если данных нет в сессии, возвращаем на выбор чисел

        if request.method == 'POST':
            user_answer = request.POST.get('user-answer')
            correct_answer = first * second

            if user_answer and user_answer.isdigit() and int(user_answer) == correct_answer:
                result_message = "Верно! Молодец!"
                result_color = "green"

                # Генерируем новую пару
                if number_type == "2":
                    first, second = generate_two_digit_pair()
                elif number_type == "3":
                    first, second = generate_three_digit_pair()

                # Сохраняем новую пару в сессии
                request.session['first'] = first
                request.session['second'] = second
            else:
                result_message = "Неверно! Попробуйте снова."
                result_color = "red"

            return render(request, 'tricks.html', {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'result': result_message,
                'result_color': result_color,
                'mode': 3
            })

        return redirect('tricks', mode=2)  # Если не было отправлено ответа, возвращаем на режим 2


# Новые представления для учителей

def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('teacher_login')
    else:
        form = TeacherRegistrationForm()
    
    return render(request, 'teacher_register.html', {'form': form})

def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                try:
                    teacher_profile = user.teacher_profile
                    if teacher_profile.status == 'approved':
                        login(request, user)
                        return redirect('teacher_dashboard')
                    elif teacher_profile.status == 'pending':
                        return redirect('teacher_login')
                    else:
                        return redirect('teacher_login')
                except TeacherProfile.DoesNotExist:
                    return redirect('teacher_login')
            else:
                return redirect('teacher_login')
    else:
        form = TeacherLoginForm()
    
    return render(request, 'teacher_login.html', {'form': form})

@login_required
def teacher_logout(request):
    logout(request)
    return redirect('index')

@login_required
def teacher_dashboard(request):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return redirect('teacher_login')
        
        classes = Class.objects.filter(teacher=teacher_profile)
        total_students = Students.objects.filter(student_class__teacher=teacher_profile).count()
        
        context = {
            'teacher_profile': teacher_profile,
            'classes': classes,
            'total_students': total_students,
        }
        return render(request, 'teacher_dashboard.html', context)
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_login')

@login_required
def class_list(request):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        classes = Class.objects.filter(teacher=teacher_profile)
        return render(request, 'class_list.html', {'classes': classes})
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def class_create(request):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        if request.method == 'POST':
            form = ClassForm(request.POST)
            if form.is_valid():
                class_obj = form.save(commit=False)
                class_obj.teacher = teacher_profile
                class_obj.save()
                messages.success(request, 'Класс успешно создан!')
                return redirect('class_list')
        else:
            form = ClassForm()
        
        return render(request, 'class_form.html', {'form': form, 'title': 'Создать класс'})
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def class_edit(request, class_id):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        class_obj = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
        
        if request.method == 'POST':
            form = ClassForm(request.POST, instance=class_obj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Класс успешно обновлен!')
                return redirect('class_list')
        else:
            form = ClassForm(instance=class_obj)
        
        return render(request, 'class_form.html', {'form': form, 'title': 'Редактировать класс', 'class_obj': class_obj})
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def class_delete(request, class_id):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        class_obj = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
        class_obj.delete()
        messages.success(request, 'Класс успешно удален!')
        return redirect('class_list')
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def students_list(request, class_id=None):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        if class_id:
            class_obj = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
            students = Students.objects.filter(student_class=class_obj)
            context = {'students': students, 'class_obj': class_obj}
        else:
            students = Students.objects.filter(student_class__teacher=teacher_profile)
            context = {'students': students}
        
        return render(request, 'students_list.html', context)
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def student_create(request, class_id=None):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                if class_id:
                    student.student_class = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
                else:
                    # Если класс не указан, предлагаем выбрать из списка классов учителя
                    classes = Class.objects.filter(teacher=teacher_profile)
                    if classes.count() == 1:
                        student.student_class = classes.first()
                    else:
                        # Получаем выбранный класс из формы
                        selected_class_id = request.POST.get('student_class')
                        if selected_class_id:
                            student.student_class = get_object_or_404(Class, id=selected_class_id, teacher=teacher_profile)
                        else:
                            # Если класс не выбран, показываем форму с выбором класса
                            return render(request, 'student_form.html', {
                                'form': form, 
                                'title': 'Добавить ученика',
                                'classes': classes,
                                'need_class_selection': True
                            })
                
                student.save()
                messages.success(request, 'Ученик успешно добавлен!')
                
                # Если ученик добавлен в класс, предлагаем создать расписание
                if class_id:
                    # Проверяем, есть ли уже ученики в классе
                    students_count = Students.objects.filter(student_class=student.student_class).count()
                    if students_count > 0:
                        messages.info(request, f'Теперь в классе "{student.student_class.name}" есть ученики. Вы можете создать месячное расписание.')
                        return redirect('monthly_schedule_create', class_id=class_id)
                    else:
                        return redirect('students_list_by_class', class_id=class_id)
                else:
                    return redirect('students_list')
        else:
            form = StudentForm()
        
        context = {
            'form': form, 
            'title': 'Добавить ученика',
            'class_id': class_id
        }
        
        if class_id:
            context['class_obj'] = get_object_or_404(Class, id=class_id, teacher=teacher_profile)
            # Проверяем, есть ли ученики в классе
            students_count = Students.objects.filter(student_class=context['class_obj']).count()
            if students_count == 0:
                context['show_schedule_info'] = True
                context['schedule_message'] = f'В классе "{context["class_obj"].name}" нет учеников. После добавления ученика вы сможете создать месячное расписание.'
        
        return render(request, 'student_form.html', context)
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def student_edit(request, student_id):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        student = get_object_or_404(Students, id=student_id, student_class__teacher=teacher_profile)
        
        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Данные ученика успешно обновлены!')
                return redirect('students_list')
        else:
            form = StudentForm(instance=student)
        
        return render(request, 'student_form.html', {
            'form': form, 
            'title': 'Редактировать ученика',
            'student': student
        })
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def student_delete(request, student_id):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        student = get_object_or_404(Students, id=student_id, student_class__teacher=teacher_profile)
        student.delete()
        messages.success(request, 'Ученик успешно удален!')
        return redirect('students_list')
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def teacher_profile_edit(request):
    try:
        teacher_profile = request.user.teacher_profile
        if request.method == 'POST':
            form = TeacherProfileUpdateForm(request.POST, instance=teacher_profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('teacher_dashboard')
        else:
            form = TeacherProfileUpdateForm(instance=teacher_profile)
        
        return render(request, 'teacher_profile_edit.html', {'form': form})
    except TeacherProfile.DoesNotExist:
        messages.error(request, 'У вас нет профиля учителя.')
        return redirect('teacher_login')


# Обработчик выбора и проверки игры "Просто"

# Определяем диапазоны (пример)
RANGES = {
    "1-10": (1, 10),
    "10-100": (10, 100),
    "100-1000": (100, 1000),
    "1000-10000": (1000, 10000),
}

def simply(request, mode):
    if mode == 1:  # Режим 1 — форма для выбора настроек
        if request.method == 'POST':
            # Получаем значения из формы
            difficulty = int(request.POST.get("difficulty", 1))
            range_key = request.POST.get("range", "1-10")
            num_examples = int(request.POST.get("examples", 10))
            speed = float(request.POST.get("speed", 1))

            # Сохраняем параметры в сессии
            request.session['difficulty'] = difficulty
            request.session['range_key'] = range_key
            request.session['num_examples'] = num_examples
            request.session['speed'] = speed

            # Переход к режиму 2 (обратный отсчёт)
            return redirect('simply', mode=2)
        return render(request, 'simply.html', {"mode": 1, "ranges": RANGES})

    elif mode == 2:  # Режим 2 — таймер отсчёта
        return render(request, 'simply.html', {"mode": 2})

    elif mode == 3:  # Режим 3 — основная игра
        # Получаем параметры из сессии
        difficulty = request.session.get('difficulty', 1)
        range_key = request.session.get('range_key', '1-10')
        num_examples = request.session.get('num_examples', 10)
        speed = request.session.get('speed', 1)

        # Получаем диапазон чисел
        range_values = RANGES.get(range_key)
        if not range_values or len(range_values) != 2:
            return render(request, 'simply.html', {"mode": 4, "result": "Ошибка: некорректный диапазон чисел"})

        min_val, max_val = range_values

        # Генерация чисел
        numbers = []
        total = 0
        for _ in range(num_examples):
            num = random.randint(min_val, max_val)
            sign = random.choice([-1, 1])
            num *= sign
            numbers.append(num)
            total += num

        return render(request, 'simply.html', {
            "mode": 3,
            "numbers": numbers,
            "total": total,
            "speed": speed,
        })

    elif mode == 4:  # Режим 4 — проверка ответа
        if request.method == 'POST':
            try:
                correct_answer = int(request.POST.get("correct_answer", 0))
                user_answer = int(request.POST.get("user_answer", 0))
                result = "Правильно!" if user_answer == correct_answer else f"Неправильно! Правильный ответ: {correct_answer}"
                return render(request, 'simply.html', {"mode": 4, "user_answer": user_answer, "correct_answer": correct_answer, "result": result})
            except ValueError:
                return render(request, 'simply.html', {"mode": 4, "result": "Ошибка в формате ответа"})

    return render(request, 'simply.html', {"mode": 4, "result": "Ошибка: неверный режим"})

# Представления для учеников

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                student_account = StudentAccount.objects.get(username=username, is_active=True)
                if student_account.password == password:  # Простая проверка пароля
                    # Обновляем время последнего входа
                    student_account.last_login = timezone.now()
                    student_account.save()
                    
                    # Сохраняем информацию об ученике в сессии
                    request.session['student_id'] = student_account.student.id
                    request.session['student_name'] = f"{student_account.student.surname} {student_account.student.name}"
                    
                    return redirect('student_dashboard')
                else:
                    return redirect('student_login')
            except StudentAccount.DoesNotExist:
                return redirect('student_login')
    else:
        form = StudentLoginForm()
    
    return render(request, 'student_login.html', {'form': form})

def student_logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
        del request.session['student_name']
    return redirect('index')

def student_dashboard(request):
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    student_id = request.session['student_id']
    student = get_object_or_404(Students, id=student_id)
    
    context = {
        'student': student,
        'student_name': request.session.get('student_name', '')
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def create_student_account(request, student_id):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        student = get_object_or_404(Students, id=student_id, student_class__teacher=teacher_profile)
        
        # Проверяем, есть ли уже аккаунт у ученика
        if hasattr(student, 'account'):
            messages.warning(request, f'У ученика {student.name} уже есть аккаунт.')
            return redirect('students_list')
        
        if request.method == 'POST':
            form = StudentAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.student = student
                account.save()
                messages.success(request, f'Аккаунт для ученика {student.name} успешно создан!')
                return redirect('students_list')
        else:
            form = StudentAccountForm()
        
        return render(request, 'create_student_account.html', {
            'form': form,
            'student': student,
            'title': 'Создать аккаунт для ученика'
        })
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

@login_required
def delete_student_account(request, student_id):
    try:
        teacher_profile = request.user.teacher_profile
        if teacher_profile.status != 'approved':
            return HttpResponseForbidden('Доступ запрещен')
        
        student = get_object_or_404(Students, id=student_id, student_class__teacher=teacher_profile)
        
        if hasattr(student, 'account'):
            student.account.delete()
            messages.success(request, f'Аккаунт ученика {student.name} успешно удален!')
        else:
            messages.warning(request, f'У ученика {student.name} нет аккаунта.')
        
        return redirect('students_list')
    except TeacherProfile.DoesNotExist:
        return HttpResponseForbidden('Доступ запрещен')

# Представления для домашних заданий
@login_required
def homework_list(request, class_id):
    """Список домашних заданий для класса"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        homeworks = Homework.objects.filter(class_group=class_obj, is_active=True)
        return render(request, 'homework_list.html', {
            'class_obj': class_obj,
            'homeworks': homeworks
        })
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')

@login_required
def homework_create(request, class_id):
    """Создание нового домашнего задания"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        if request.method == 'POST':
            form = HomeworkForm(request.POST)
            if form.is_valid():
                homework = form.save(commit=False)
                homework.class_group = class_obj
                homework.save()
                messages.success(request, 'Домашнее задание успешно создано!')
                return redirect('homework_list', class_id=class_id)
        else:
            form = HomeworkForm()
        
        return render(request, 'homework_form.html', {
            'form': form,
            'class_obj': class_obj,
            'title': 'Создать домашнее задание'
        })
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')

@login_required
def homework_edit(request, homework_id):
    """Редактирование домашнего задания"""
    try:
        homework = Homework.objects.get(id=homework_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if homework.class_group.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому заданию")
        
        if request.method == 'POST':
            form = HomeworkForm(request.POST, instance=homework)
            if form.is_valid():
                form.save()
                messages.success(request, 'Домашнее задание успешно обновлено!')
                return redirect('homework_list', class_id=homework.class_group.id)
        else:
            form = HomeworkForm(instance=homework)
        
        return render(request, 'homework_form.html', {
            'form': form,
            'homework': homework,
            'class_obj': homework.class_group,
            'title': 'Редактировать домашнее задание'
        })
    except Homework.DoesNotExist:
        messages.error(request, 'Домашнее задание не найдено')
        return redirect('class_list')

@login_required
def homework_delete(request, homework_id):
    """Удаление домашнего задания"""
    try:
        homework = Homework.objects.get(id=homework_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if homework.class_group.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому заданию")
        
        class_id = homework.class_group.id
        homework.delete()
        messages.success(request, 'Домашнее задание успешно удалено!')
        return redirect('homework_list', class_id=class_id)
    except Homework.DoesNotExist:
        messages.error(request, 'Домашнее задание не найдено')
        return redirect('class_list')

def student_homework_list(request):
    """Список домашних заданий для ученика"""
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    try:
        student = Students.objects.get(id=request.session['student_id'])
        # Получаем класс ученика
        if hasattr(student, 'student_class') and student.student_class:
            homeworks = Homework.objects.filter(
                class_group=student.student_class, 
                is_active=True
            ).order_by('-created_at')
        else:
            homeworks = []
        
        return render(request, 'student_homework_list.html', {
            'student': student,
            'homeworks': homeworks,
            'today': timezone.now().date()
        })
    except Students.DoesNotExist:
        return redirect('student_login')


# Представления для табеля посещений

@login_required
def attendance_list(request, class_id):
    """Список посещений для класса"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        # Получаем все даты занятий для класса
        attendance_dates = Attendance.objects.filter(
            class_group=class_obj
        ).values_list('date', flat=True).distinct().order_by('-date')
        
        # Получаем всех учеников класса
        students = Students.objects.filter(student_class=class_obj).order_by('surname', 'name')
        
        # Получаем настройки оплаты
        try:
            payment_settings = class_obj.payment_settings
        except PaymentSettings.DoesNotExist:
            payment_settings = None
        
        context = {
            'class_obj': class_obj,
            'students': students,
            'attendance_dates': attendance_dates,
            'payment_settings': payment_settings,
        }
        return render(request, 'attendance_list.html', context)
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')


@login_required
def attendance_create(request, class_id):
    """Создание записи о посещении для определенной даты"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        if request.method == 'POST':
            date_form = AttendanceDateForm(request.POST)
            if date_form.is_valid():
                selected_date = date_form.cleaned_data['date']
                
                # Проверяем, не существует ли уже записи для этой даты
                if Attendance.objects.filter(class_group=class_obj, date=selected_date).exists():
                    messages.warning(request, f'Записи для {selected_date} уже существуют')
                    return redirect('attendance_list', class_id=class_id)
                
                # Получаем всех учеников класса
                students = Students.objects.filter(student_class=class_obj)
                
                # Создаем записи посещения для всех учеников
                for student in students:
                    Attendance.objects.create(
                        student=student,
                        class_group=class_obj,
                        date=selected_date,
                        is_present=True,  # По умолчанию присутствовал
                        is_paid=False
                    )
                
                messages.success(request, f'Записи посещения для {selected_date} созданы!')
                return redirect('attendance_edit', class_id=class_id, date=selected_date)
        else:
            date_form = AttendanceDateForm()
        
        # Получаем всех учеников класса для отображения в шаблоне
        students = Students.objects.filter(student_class=class_obj).order_by('surname', 'name')
        
        return render(request, 'attendance_create.html', {
            'date_form': date_form,
            'class_obj': class_obj,
            'students': students,
            'title': 'Создать записи посещения'
        })
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')


@login_required
def attendance_edit(request, class_id, date):
    """Редактирование посещений для определенной даты"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        # Получаем все записи посещения для этой даты
        attendances = Attendance.objects.filter(
            class_group=class_obj,
            date=date
        ).select_related('student').order_by('student__surname', 'student__name')
        
        if request.method == 'POST':
            forms_valid = True
            for attendance in attendances:
                form = AttendanceForm(request.POST, instance=attendance, prefix=f'attendance_{attendance.id}')
                if not form.is_valid():
                    forms_valid = False
                    break
            
            if forms_valid:
                for attendance in attendances:
                    form = AttendanceForm(request.POST, instance=attendance, prefix=f'attendance_{attendance.id}')
                    form.save()
                
                messages.success(request, f'Посещения для {date} обновлены!')
                return redirect('attendance_list', class_id=class_id)
        else:
            # Создаем формы для каждой записи
            attendance_forms = []
            for attendance in attendances:
                form = AttendanceForm(instance=attendance, prefix=f'attendance_{attendance.id}')
                attendance_forms.append((attendance, form))
        
        # Получаем всех учеников класса для отображения в шаблоне
        students = Students.objects.filter(student_class=class_obj).order_by('surname', 'name')
        
        return render(request, 'attendance_edit.html', {
            'class_obj': class_obj,
            'date': date,
            'attendance_forms': attendance_forms,
            'students': students,
            'title': f'Редактировать посещения на {date}'
        })
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')


@login_required
def attendance_delete(request, class_id, date):
    """Удаление записей посещения для определенной даты"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        # Удаляем все записи для этой даты
        deleted_count = Attendance.objects.filter(
            class_group=class_obj,
            date=date
        ).delete()[0]
        
        messages.success(request, f'Удалено {deleted_count} записей посещения для {date}')
        return redirect('attendance_list', class_id=class_id)
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')


@login_required
def payment_settings_edit(request, class_id):
    """Редактирование настроек оплаты для класса"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        # Получаем или создаем настройки оплаты
        payment_settings, created = PaymentSettings.objects.get_or_create(
            class_group=class_obj,
            defaults={'price_per_lesson': 0, 'price_per_month': 0}
        )
        
        if request.method == 'POST':
            form = PaymentSettingsForm(request.POST, instance=payment_settings)
            if form.is_valid():
                form.save()
                messages.success(request, 'Настройки оплаты обновлены!')
                return redirect('attendance_list', class_id=class_id)
        else:
            form = PaymentSettingsForm(instance=payment_settings)
        
        return render(request, 'payment_settings_form.html', {
            'form': form,
            'class_obj': class_obj,
            'title': 'Настройки оплаты'
        })
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')


def student_attendance_list(request):
    """Список посещений для ученика"""
    if 'student_id' not in request.session:
        return redirect('student_login')
    
    try:
        student = Students.objects.get(id=request.session['student_id'])
        
        if not student.student_class:
            return redirect('student_login')
        
        # Получаем все посещения ученика
        attendances = Attendance.objects.filter(
            student=student
        ).order_by('-date')
        
        # Получаем настройки оплаты
        try:
            payment_settings = student.student_class.payment_settings
        except PaymentSettings.DoesNotExist:
            payment_settings = None
        
        # Рассчитываем статистику и оплату
        payment_info = None
        if payment_settings:
            current_month = timezone.now().month
            current_year = timezone.now().year
            
            # Посещения за текущий месяц
            month_attendances = attendances.filter(
                date__month=current_month,
                date__year=current_year
            )
            
            total_lessons = month_attendances.count()
            attended_lessons = month_attendances.filter(is_present=True).count()
            paid_lessons = month_attendances.filter(is_paid=True).count()
            
            # Расчет оплаты
            if payment_settings.price_per_month > 0:
                # Если установлена месячная оплата
                monthly_payment = payment_settings.price_per_month
                lessons_payment = 0
            else:
                # Если оплата по занятиям
                monthly_payment = 0
                lessons_payment = attended_lessons * payment_settings.price_per_lesson
            
            total_payment = monthly_payment + lessons_payment
            
            payment_info = {
                'total_lessons': total_lessons,
                'attended_lessons': attended_lessons,
                'paid_lessons': paid_lessons,
                'monthly_payment': monthly_payment,
                'lessons_payment': lessons_payment,
                'total_payment': total_payment,
                'price_per_lesson': payment_settings.price_per_lesson,
                'price_per_month': payment_settings.price_per_month,
                'current_month': current_month,
                'current_year': current_year
            }
        
        return render(request, 'student_attendance_list.html', {
            'student': student,
            'attendances': attendances,
            'payment_info': payment_info
        })
    except Students.DoesNotExist:
        return redirect('student_login')

@login_required
def monthly_schedule_create(request, class_id):
    """Создание месячного расписания занятий"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        if request.method == 'POST':
            form = MonthlyScheduleForm(request.POST)
            if form.is_valid():
                month = int(form.cleaned_data['month'])
                year = int(form.cleaned_data['year'])
                lesson_dates_str = form.cleaned_data['lesson_dates']
                
                # Проверяем, не существует ли уже расписание для этого месяца
                if MonthlySchedule.objects.filter(class_group=class_obj, month=month, year=year).exists():
                    messages.warning(request, f'Расписание для {month}/{year} уже существует')
                    return redirect('monthly_schedule_list', class_id=class_id)
                
                # Создаем месячное расписание
                monthly_schedule = MonthlySchedule.objects.create(
                    class_group=class_obj,
                    month=month,
                    year=year
                )
                
                # Парсим даты занятий
                try:
                    lesson_dates = [int(date.strip()) for date in lesson_dates_str.split(',') if date.strip().isdigit()]
                except ValueError:
                    messages.error(request, 'Неверный формат дат')
                    monthly_schedule.delete()
                    return redirect('monthly_schedule_create', class_id=class_id)
                
                # Получаем всех учеников класса
                students = Students.objects.filter(student_class=class_obj)
                
                # Проверяем, есть ли ученики в классе
                if not students.exists():
                    messages.error(request, f'В классе "{class_obj.name}" нет учеников. Сначала добавьте учеников в класс, а затем создавайте расписание.')
                    return redirect('student_create_in_class', class_id=class_id)
                
                # Создаем записи посещения для всех дат и учеников
                created_count = 0
                for day in lesson_dates:
                    try:
                        # Проверяем, что дата валидна для указанного месяца и года
                        from datetime import date
                        lesson_date = date(year, month, day)
                        
                        for student in students:
                            Attendance.objects.create(
                                student=student,
                                class_group=class_obj,
                                monthly_schedule=monthly_schedule,
                                date=lesson_date,
                                is_present=True,
                                is_paid=False,
                                payment_carried_over=False
                            )
                        created_count += 1
                    except ValueError:
                        # Пропускаем невалидные даты
                        continue
                
                if created_count > 0:
                    messages.success(request, f'Месячное расписание создано! Создано {created_count} занятий')
                    return redirect('monthly_schedule_edit', class_id=class_id, schedule_id=monthly_schedule.id)
                else:
                    messages.error(request, 'Не удалось создать ни одного занятия')
                    monthly_schedule.delete()
                    return redirect('monthly_schedule_create', class_id=class_id)
        else:
            form = MonthlyScheduleForm()
            # Устанавливаем текущий месяц и год по умолчанию
            from datetime import datetime
            now = datetime.now()
            form.fields['month'].initial = now.month
            form.fields['year'].initial = now.year
        
        # Получаем всех учеников класса
        students = Students.objects.filter(student_class=class_obj).order_by('surname', 'name')
        
        # Проверяем, есть ли ученики в классе
        if not students.exists():
            messages.warning(request, f'В классе "{class_obj.name}" нет учеников. Сначала добавьте учеников в класс, а затем создавайте расписание.')
            return redirect('student_create_in_class', class_id=class_id)
        
        return render(request, 'monthly_schedule_create.html', {
            'form': form,
            'class_obj': class_obj,
            'students': students,
            'title': 'Создать месячное расписание'
        })
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')


@login_required
def monthly_schedule_list(request, class_id):
    """Список месячных расписаний для класса"""
    try:
        class_obj = Class.objects.get(id=class_id)
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        # Получаем все месячные расписания для класса
        monthly_schedules = MonthlySchedule.objects.filter(
            class_group=class_obj
        ).order_by('-year', '-month')
        
        # Получаем всех учеников класса
        students = Students.objects.filter(student_class=class_obj).order_by('surname', 'name')
        
        # Получаем настройки оплаты
        try:
            payment_settings = class_obj.payment_settings
        except PaymentSettings.DoesNotExist:
            payment_settings = None
        
        context = {
            'class_obj': class_obj,
            'students': students,
            'monthly_schedules': monthly_schedules,
            'payment_settings': payment_settings,
        }
        return render(request, 'monthly_schedule_list.html', context)
    except Class.DoesNotExist:
        messages.error(request, 'Класс не найден')
        return redirect('class_list')


@login_required
def monthly_schedule_edit(request, class_id, schedule_id):
    """Редактирование месячного расписания"""
    try:
        class_obj = Class.objects.get(id=class_id)
        monthly_schedule = MonthlySchedule.objects.get(id=schedule_id, class_group=class_obj)
        
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        # Получаем все записи посещения для этого расписания
        attendances = Attendance.objects.filter(
            monthly_schedule=monthly_schedule
        ).select_related('student').order_by('date', 'student__surname', 'student__name')
        
        if request.method == 'POST':
            forms_valid = True
            for attendance in attendances:
                form = MonthlyAttendanceForm(request.POST, instance=attendance, prefix=f'attendance_{attendance.id}')
                if not form.is_valid():
                    forms_valid = False
                    break
            
            if forms_valid:
                for attendance in attendances:
                    form = MonthlyAttendanceForm(request.POST, instance=attendance, prefix=f'attendance_{attendance.id}')
                    form.save()
                
                messages.success(request, f'Расписание на {monthly_schedule} обновлено!')
                return redirect('monthly_schedule_list', class_id=class_id)
        else:
            # Создаем формы для каждой записи
            attendance_forms = []
            for attendance in attendances:
                form = MonthlyAttendanceForm(instance=attendance, prefix=f'attendance_{attendance.id}')
                attendance_forms.append((attendance, form))
        
        # Получаем всех учеников класса для отображения в шаблоне
        students = Students.objects.filter(student_class=class_obj).order_by('surname', 'name')
        
        return render(request, 'monthly_schedule_edit.html', {
            'class_obj': class_obj,
            'monthly_schedule': monthly_schedule,
            'attendance_forms': attendance_forms,
            'students': students,
            'title': f'Редактировать расписание на {monthly_schedule}'
        })
    except (Class.DoesNotExist, MonthlySchedule.DoesNotExist):
        messages.error(request, 'Класс или расписание не найдено')
        return redirect('class_list')


@login_required
def monthly_schedule_delete(request, class_id, schedule_id):
    """Удаление месячного расписания"""
    try:
        class_obj = Class.objects.get(id=class_id)
        monthly_schedule = MonthlySchedule.objects.get(id=schedule_id, class_group=class_obj)
        
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        # Удаляем все записи посещения для этого расписания
        deleted_count = Attendance.objects.filter(
            monthly_schedule=monthly_schedule
        ).delete()[0]
        
        # Удаляем само расписание
        monthly_schedule.delete()
        
        messages.success(request, f'Удалено месячное расписание и {deleted_count} записей посещения')
        return redirect('monthly_schedule_list', class_id=class_id)
    except (Class.DoesNotExist, MonthlySchedule.DoesNotExist):
        messages.error(request, 'Класс или расписание не найдено')
        return redirect('class_list')


@login_required
def carry_over_payments(request, class_id, schedule_id):
    """Перенос неоплаченных занятий на следующий месяц"""
    try:
        class_obj = Class.objects.get(id=class_id)
        monthly_schedule = MonthlySchedule.objects.get(id=schedule_id, class_group=class_obj)
        
        # Проверяем, что учитель имеет доступ к этому классу
        if class_obj.teacher != request.user.teacher_profile:
            return HttpResponseForbidden("У вас нет доступа к этому классу")
        
        if request.method == 'POST':
            # Получаем все неоплаченные занятия
            unpaid_attendances = Attendance.objects.filter(
                monthly_schedule=monthly_schedule,
                is_present=True,
                is_paid=False
            )
            
            if unpaid_attendances.exists():
                # Создаем следующий месяц
                next_month = monthly_schedule.month + 1
                next_year = monthly_schedule.year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                
                # Создаем или получаем расписание на следующий месяц
                next_schedule, created = MonthlySchedule.objects.get_or_create(
                    class_group=class_obj,
                    month=next_month,
                    year=next_year
                )
                
                # Переносим неоплаченные занятия
                carried_over_count = 0
                for attendance in unpaid_attendances:
                    # Создаем новую запись на следующий месяц
                    new_attendance = Attendance.objects.create(
                        student=attendance.student,
                        class_group=class_obj,
                        monthly_schedule=next_schedule,
                        date=attendance.date.replace(month=next_month, year=next_year),
                        is_present=True,
                        is_paid=False,
                        payment_carried_over=True,
                        notes=f"Перенесено с {monthly_schedule}"
                    )
                    carried_over_count += 1
                
                messages.success(request, f'Перенесено {carried_over_count} неоплаченных занятий на {next_schedule}')
            else:
                messages.info(request, 'Нет неоплаченных занятий для переноса')
            
            return redirect('monthly_schedule_list', class_id=class_id)
        
        return render(request, 'carry_over_payments.html', {
            'class_obj': class_obj,
            'monthly_schedule': monthly_schedule,
            'title': 'Перенос неоплаченных занятий'
        })
    except (Class.DoesNotExist, MonthlySchedule.DoesNotExist):
        messages.error(request, 'Класс или расписание не найдено')
        return redirect('class_list')
