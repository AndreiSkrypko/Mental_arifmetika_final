# Руководство по стилям - Тренажёр по ментальной арифметике

## Обзор

Этот документ описывает единую систему стилей для всего приложения, обеспечивающую консистентность и профессиональный внешний вид.

## Цветовая палитра

### Основные цвета
- **Primary**: `#667eea` - основной цвет приложения
- **Secondary**: `#6c757d` - вторичный цвет
- **Info**: `#17a2b8` - информационный цвет
- **Success**: `#28a745` - цвет успеха
- **Warning**: `#ffc107` - цвет предупреждения
- **Danger**: `#dc3545` - цвет опасности

### Градиенты
- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Info Gradient**: `linear-gradient(135deg, #17a2b8, #138496)`
- **Success Gradient**: `linear-gradient(135deg, #28a745, #20c997)`
- **Warning Gradient**: `linear-gradient(135deg, #ffc107, #fd7e14)`
- **Danger Gradient**: `linear-gradient(135deg, #dc3545, #c82333)`

### Текстовые цвета
- **Primary Text**: `#2d3748` - основной текст
- **Secondary Text**: `#4a5568` - вторичный текст
- **Muted Text**: `#718096` - приглушенный текст

## Кнопки

### Основные классы
Все кнопки используют базовый класс с дополнительными модификаторами:

```html
<button class="btn-primary">Основная кнопка</button>
<a href="#" class="btn-secondary">Вторичная кнопка</a>
<button class="btn-info">Информационная кнопка</button>
<button class="btn-danger">Опасная кнопка</button>
<button class="btn-success">Кнопка успеха</button>
<button class="btn-warning">Кнопка предупреждения</button>
```

### Стили кнопок
- **Размер**: `padding: 14px 28px`
- **Радиус**: `border-radius: 12px`
- **Шрифт**: `font-weight: 600`, `font-size: 1rem`
- **Минимальная ширина**: `min-width: 140px`
- **Переходы**: `transition: all 0.3s ease`
- **Эффекты при наведении**: `transform: translateY(-2px)`

### Маленькие кнопки
Для компактных элементов используйте класс `btn-small`:

```html
<a href="#" class="btn-small btn-primary">Редактировать</a>
<a href="#" class="btn-small btn-danger">Удалить</a>
```

## Информационные блоки

### Типы блоков
```html
<div class="info-box">
    <h4>Информация</h4>
    <p>Содержимое информационного блока</p>
</div>

<div class="warning-box">
    <h4>Предупреждение</h4>
    <p>Важная информация</p>
</div>

<div class="success-box">
    <h4>Успех</h4>
    <p>Операция выполнена</p>
</div>
```

## Карточки

### Базовая структура
```html
<div class="card">
    <div class="card-header">
        Заголовок карточки
    </div>
    <div class="card-body">
        Содержимое карточки
    </div>
</div>
```

### Стили карточек
- **Фон**: `rgba(255, 255, 255, 0.95)` с `backdrop-filter: blur(20px)`
- **Радиус**: `border-radius: 16px`
- **Тень**: `box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1)`
- **Эффекты при наведении**: `transform: translateY(-4px)`

## Формы

### Поля ввода
```html
<div class="form-group">
    <label for="field">Название поля</label>
    <input type="text" class="form-control" id="field">
</div>
```

### Стили полей
- **Граница**: `2px solid rgba(102, 126, 234, 0.2)`
- **Радиус**: `border-radius: 12px`
- **Отступы**: `padding: 12px 16px`
- **Фокус**: `border-color: #667eea` с тенью

## Таблицы

### Базовая структура
```html
<table class="table">
    <thead>
        <tr>
            <th>Заголовок</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Данные</td>
        </tr>
    </tbody>
</table>
```

### Стили таблиц
- **Заголовки**: градиентный фон с белым текстом
- **Строки**: `padding: 16px`
- **Эффекты при наведении**: `background: rgba(102, 126, 234, 0.05)`

## Утилиты

### Выравнивание текста
```html
<p class="text-center">По центру</p>
<p class="text-left">По левому краю</p>
<p class="text-right">По правому краю</p>
```

### Отступы
```html
<div class="mt-4">Отступ сверху</div>
<div class="mb-4">Отступ снизу</div>
<div class="py-5">Отступы сверху и снизу</div>
```

### Цвета текста
```html
<p class="text-muted">Приглушенный текст</p>
```

## Адаптивность

### Медиа-запросы
```css
@media (max-width: 768px) {
    /* Стили для мобильных устройств */
}
```

### Адаптивные кнопки
На мобильных устройствах кнопки занимают всю ширину:
- `width: 100%`
- `justify-content: center`
- `padding: 12px 20px`

## Анимации

### Доступные анимации
```html
<div class="fade-in-up">Появление снизу</div>
<div class="fade-in-down">Появление сверху</div>
```

### Параметры анимаций
- **Длительность**: `0.6s`
- **Функция**: `ease-out`
- **Задержка**: настраивается индивидуально

## CSS переменные

### Использование
```css
.my-element {
    background: var(--primary-color);
    border-radius: var(--border-radius);
    transition: var(--transition);
}
```

### Доступные переменные
- `--primary-color`
- `--primary-gradient`
- `--border-radius`
- `--box-shadow`
- `--transition`
- `--text-primary`
- `--text-secondary`
- `--text-muted`
- `--bg-white`

## Рекомендации по использованию

### 1. Консистентность
- Всегда используйте предопределенные классы кнопок
- Следуйте установленной цветовой схеме
- Используйте стандартные отступы и радиусы

### 2. Доступность
- Обеспечивайте достаточный контраст для текста
- Используйте семантически правильные HTML-элементы
- Добавляйте `alt` атрибуты для изображений

### 3. Производительность
- Минимизируйте количество кастомных CSS-правил
- Используйте CSS-переменные для повторяющихся значений
- Применяйте `will-change` только при необходимости

### 4. Поддержка браузеров
- Используйте `backdrop-filter` с fallback
- Проверяйте поддержку CSS Grid и Flexbox
- Обеспечивайте базовую функциональность для старых браузеров

## Примеры использования

### Форма с кнопками
```html
<div class="form-actions">
    <a href="#" class="btn-secondary">
        <i class="fas fa-arrow-left"></i>
        Назад
    </a>
    <button type="submit" class="btn-primary">
        <i class="fas fa-save"></i>
        Сохранить
    </button>
</div>
```

### Информационная карточка
```html
<div class="card">
    <div class="card-header">
        <i class="fas fa-info-circle"></i>
        Информация
    </div>
    <div class="card-body">
        <p>Важная информация для пользователя</p>
        <div class="info-box">
            <h4>Дополнительно</h4>
            <p>Дополнительная информация</p>
        </div>
    </div>
</div>
```

### Таблица с действиями
```html
<table class="table">
    <thead>
        <tr>
            <th>Название</th>
            <th>Действия</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Элемент</td>
            <td>
                <a href="#" class="btn-small btn-primary">Редактировать</a>
                <a href="#" class="btn-small btn-danger">Удалить</a>
            </td>
        </tr>
    </tbody>
</table>
```

## Обновление стилей

При необходимости обновления стилей:

1. Изменяйте CSS-переменные в `:root`
2. Обновляйте базовые классы в `static/styles.css`
3. Тестируйте изменения на всех устройствах
4. Обновляйте документацию
5. Уведомляйте команду об изменениях

## Поддержка

При возникновении вопросов по стилям:
1. Обратитесь к этому руководству
2. Проверьте существующие примеры в коде
3. Свяжитесь с командой разработки
4. Создайте issue с описанием проблемы
