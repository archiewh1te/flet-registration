import flet as ft
import sqlite3

# Функция для создания таблицы пользователей (если она еще не существует)
def create_db():
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 fname TEXT NOT NULL,
                 lname TEXT NOT NULL,
                 phone TEXT NOT NULL,
                 shop TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Функция для добавления пользователя в базу данных
def add_user(fname, lname, phone, shop):
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (fname, lname, phone, shop) VALUES (?, ?, ?, ?)",
              (fname, lname, phone, shop))
    conn.commit()
    conn.close()

# Главное приложение
async def main(page: ft.Page):
    # Сначала создадим таблицу в базе данных
    create_db()

    # Настройка страницы
    page.title = "Регистрация"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 900
    page.window.height = 700

    def validate_name(name):
        return name.isalpha() and len(name) > 0

    def validate_phone(phone):
        return phone.startswith("+7") and len(phone) == 12 and phone[1:].isdigit()

    def on_submit(e):
        errors = []
        if not validate_name(fname.value):
            errors.append("Некорректная Фамилия")
        if not validate_name(lname.value):
            errors.append("Некорректное Имя")
        if not validate_phone(phone.value):
            errors.append("Некорректный номер телефона")
        if not shop.value:
            errors.append("Не выбран магазин")

        if errors:
            error_msg.value = "\n".join(errors)
            error_msg.color = ft.colors.RED
            error_msg.weight = ft.FontWeight.BOLD
        else:
            # Сохранение данных пользователя в базе данных
            add_user(fname.value, lname.value, phone.value, shop.value)

            # Скрываем форму и показываем сообщение и кнопку "Назад"
            form_container.visible = False
            success_container.visible = True
            form_container.update()
            success_container.update()
        error_msg.update()

    def on_name_change(e):
        new_value = e.control.value
        if len(new_value) > 20:
            new_value = new_value[:20]
        new_value = ''.join([char for char in new_value if char.isalpha()])
        new_value = new_value.capitalize()
        e.control.value = new_value
        e.control.update()
        update_clear_button_state()

    def on_phone_change(e):
        new_value = e.control.value
        if not new_value.startswith("+7"):
            new_value = "+7" + new_value.lstrip("+7")
        # Ограничение длины номера до 12 символов
        if len(new_value) > 12:
            new_value = new_value[:12]
        # Запрет на ввод любых символов кроме цифр
        if not new_value[1:].isdigit():
            new_value = "+7" + ''.join([char for char in new_value[2:] if char.isdigit()])
        phone.value = new_value
        phone.update()
        update_clear_button_state()

    def back_to_form(e):
        # Скрываем контейнер успешной регистрации и показываем форму
        success_container.visible = False
        form_container.visible = True
        success_container.update()
        form_container.update()

    def clear_fields(e):
        fname.value = ""
        lname.value = ""
        phone.value = "+7"
        shop.value = ""
        fname.update()
        lname.update()
        phone.update()
        shop.update()
        update_clear_button_state()

    def update_clear_button_state():
        if fname.value or lname.value or phone.value != "+7" or shop.value:
            clear_button.disabled = False
        else:
            clear_button.disabled = True
        clear_button.update()

    # Создание элементов интерфейса
    title = ft.Text(value="Форма регистрации на Flet",
                    style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD))
    fname = ft.TextField(label="Фамилия", width=300, on_change=on_name_change)
    lname = ft.TextField(label="Имя", width=300, on_change=on_name_change)
    phone = ft.TextField(label="Номер телефона (11 цифр)", width=300, value="+7", on_change=on_phone_change)

    shop = ft.Dropdown(
        options=[
            ft.dropdown.Option("Магазин1"),
            ft.dropdown.Option("Магазин2"),
            ft.dropdown.Option("Магазин3"),
            ft.dropdown.Option("Магазин4"),
            ft.dropdown.Option("Магазин5"),
            ft.dropdown.Option("Магазин6"),
            ft.dropdown.Option("Магазин7"),
            ft.dropdown.Option("Магазин8"),
            ft.dropdown.Option("Магазин9"),
            ft.dropdown.Option("Магазин10"),
            ft.dropdown.Option("Магазин11"),
        ],
        width=300
    )

    error_msg = ft.Text(value="")

    submit_button = ft.ElevatedButton(text="Регистрация", on_click=on_submit)
    clear_button = ft.ElevatedButton(text="Очистить поля", on_click=clear_fields, disabled=True)

    registration_success_message = ft.Text(
        value="Регистрация успешно завершена!",
        visible=True,
        style=ft.TextStyle(size=18),
        weight=ft.FontWeight.BOLD,
        color=ft.colors.GREEN,
        text_align=ft.TextAlign.CENTER  # Центрирование текста
    )

    # Создание контейнера с фоном и центровкой
    form_container = ft.Container(
        content=ft.Column(
            [
                title,  # Добавление заголовка
                fname,
                lname,
                phone,
                shop,
                error_msg,
                ft.Row([submit_button], alignment=ft.MainAxisAlignment.CENTER),  # Ранее добавленная кнопка регистрации
                ft.Row([clear_button], alignment=ft.MainAxisAlignment.CENTER)  # Отдельная строка для кнопки очистки
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=50,
        bgcolor=ft.colors.LIGHT_BLUE_50,
        border_radius=ft.border_radius.all(8),
        alignment=ft.Alignment(0.0, 0.0),
        width=400,
        visible=True
    )

    # Кнопка "Назад", которая вернет нас к форме регистрации
    back_button = ft.ElevatedButton(
        content=ft.Text("🔙 Назад к форме регистрации", size=14, text_align=ft.TextAlign.CENTER),
        width=250,
        height=50,
        on_click=back_to_form,
    )

    # Создание контейнера для сообщения об успешной регистрации и кнопок
    success_container = ft.Container(
        content=ft.Column(
            [
                registration_success_message,
                back_button,  # Добавляем кнопку назад
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=50,
        bgcolor=ft.colors.LIGHT_BLUE_50,
        border_radius=ft.border_radius.all(8),
        alignment=ft.Alignment(0.0, 0.0),
        width=400,
        visible=False
    )

    # Основной контейнер, который будет обновляться
    main_container = ft.Container(
        content=ft.Stack(
            [
                form_container,
                success_container
            ],
            fit=ft.StackFit.PASS_THROUGH
        ),
        bgcolor=ft.colors.LIGHT_BLUE_50,
        border_radius=ft.border_radius.all(8),
        alignment=ft.Alignment(0.0, 0.0),
        width=400,
        padding=20
    )

    page.add(main_container)

# Запуск приложения
ft.app(target=main)
