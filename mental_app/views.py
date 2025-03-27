import random
import time
from django.shortcuts import render, get_object_or_404, redirect
from .models import Students
from .forms import StudentForm
from django.http import JsonResponse

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


def students_list(request, mode, student_id=None):
    # Сценарий для отображения списка студентов
    if mode == 1:
        students = Students.objects.all()
        return render(request, 'students_list.html', {'students': students, 'mode': 1})

    # Сценарий для редактирования студента
    elif mode == 2:
        student = get_object_or_404(Students, id=student_id)  # Ищем студента по id

        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()  # Сохраняем изменения
                return redirect('students_list_with_mode',
                                mode=1)  # Перенаправляем на список студентов после сохранения
        else:
            form = StudentForm(instance=student)  # Предзаполняем форму данными студента

        return render(request, 'students_list.html', {'form': form, 'student': student, 'mode': 2})

    # Сценарий для добавления нового студента
    elif mode == 3:
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()  # Сохраняем нового студента
                return redirect('students_list_with_mode',
                                mode=1)  # Перенаправляем на список студентов после добавления
        else:
            form = StudentForm()  # Создаем пустую форму для добавления студента

        return render(request, 'students_list.html', {'form': form, 'mode': 3})

    # Сценарий для удаления студента
    elif mode == 4:  # Новый режим для удаления
        student = get_object_or_404(Students, id=student_id)
        student.delete()  # Удаляем студента
        return redirect('students_list_with_mode', mode=1)  # Перенаправляем на список студентов

    # Если ни один из mode не совпадает
    return redirect('students_list_with_mode', mode=1)  # Возвращаем на список студентов по умолчанию


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
        if request.method == 'POST':  # Форма отправляется в режиме 1
            # Получаем значения из формы
            difficulty = int(request.POST.get("difficulty", 1))
            range_key = request.POST.get("range", "1-10")
            num_examples = int(request.POST.get("examples", 10))
            speed = float(request.POST.get("speed", 1))

            # Сохраняем параметры в сессии или в другом месте, если нужно
            request.session['difficulty'] = difficulty
            request.session['range_key'] = range_key
            request.session['num_examples'] = num_examples
            request.session['speed'] = speed

            # Переходим к режиму 2 (обратный отсчёт)
            return redirect('simply', mode=2)
        return render(request, 'simply.html', {"mode": 1, "ranges": RANGES})

    elif mode == 2:  # Режим 2 — таймер отсчёта
        return render(request, 'simply.html', {"mode": 2})

    elif mode == 3:  # Режим 3 — основная игра
        if request.method == 'GET':
            return render(request, 'simply.html', {"mode": 3})
        if request.method == 'POST':
            try:
                # Получаем параметры из сессии
                difficulty = request.session.get('difficulty', 1)
                range_key = request.session.get('range_key', '1-10')
                num_examples = request.session.get('num_examples', 10)
                speed = request.session.get('speed', 1)

                # Получаем диапазон чисел
                range_values = RANGES.get(range_key)
                if not range_values or len(range_values) != 2:
                    return JsonResponse({"error": "Некорректный диапазон"}, status=400)

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

            except ValueError:
                return JsonResponse({"error": "Некорректные данные формы"}, status=400)

    elif mode == 4:  # Режим 4 — проверка ответа
        if request.method == 'POST':
            try:
                correct_answer = int(request.POST.get("correct_answer", 0))
                user_answer = int(request.POST.get("user_answer", 0))

                result = "Правильно!" if user_answer == correct_answer else f"Неправильно! Правильный ответ: {correct_answer}"
                return JsonResponse({"result": result})

            except ValueError:
                return JsonResponse({"error": "Ошибка в формате ответа"}, status=400)

    return JsonResponse({"error": "Неверный режим"}, status=400)