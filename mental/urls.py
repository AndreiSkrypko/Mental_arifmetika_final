from django.contrib import admin
from django.urls import path
from mental_app import views

# --- 1. Объяснение создания маршрута --- :
# EN - path('admin/', admin.site.urls)
# RU - ФункцияСозданияМаршрута(URL, МетодОбработкиURL, ИмяМаршрута)

# --- 2. Объяснение ДИНАМИЧЕСКОЙ части в маршруте ---
# PATH: Динамическое место в URL - <int:product_id> <ТипДанных:ИмяПеременной>
# Возможные типы данных: str, int, slug, uuid, path
# Пример: path('products/<int:product_id>/<str:name>', ...)

# --- 3. Передача данных может быть 2-умя способами: ---
# 1. Передача ДАННЫХ через [интернет-адрес] - http://127.0.0.1:8000/products/8/Samsung
#    Данные будут находиться: В аргументах метода обработки URL
# 2. Передача ДАННЫХ [по строке запроса] - http://127.0.0.1:8000/products?product_id=3&name=Samsung
#    Данные будут находиться: В первом аргументе "request" метода обработки URL - request.GET.get()


urlpatterns = [
    path('admin/', admin.site.urls),  # Стандартный путь к административной панели Django

    path('', views.index, name='index'),  # Главная страница (обрабатывается функцией index)

    path('multiplication_choose/<int:mode>/', views.multiplication_choose, name='multiplication_choose'),
    # Путь для выбора чисел, отображения примера и проверки ответа
    # <int:mode> - динамический параметр, который передается в функцию multiplication_choose

    path('multiplication_to_20/<int:mode>/', views.multiplication_to_20, name='multiplication_to_20'),

    path('square/<int:mode>/', views.square, name='square'),

    path('multiplication_base/<int:mode>/', views.multiplication_base, name='multiplication_base'),

    path('tricks/<int:mode>/', views.tricks, name='tricks'),

    path('simply/<int:mode>/', views.simply, name='simply'),

    path('students_list/', views.students_list, name='students_list_with_mode'),

    path('students_list/<int:mode>/', views.students_list, name='students_list_with_mode'),

    path('students_list/<int:mode>/<int:student_id>/', views.students_list, name='students_list_with_mode_and_id'),
    # Редактирование студента

    path('delete_student/<int:student_id>/', views.students_list, {'mode': 4}, name='delete_student'),
    # Новый URL для удаления
]
