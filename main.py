import flet as ft
import random
import database as db
import webbrowser

# --- ТҮСТЕР ПАЛИТРАСЫ ---
THEME_COLOR = ft.Colors.INDIGO
LIGHT_BG = "#F3F4F6"
LIGHT_CARD = "#FFFFFF"
LIGHT_TEXT = "#1F2937"
DARK_BG = "#111827"
DARK_CARD = "#1F2937"
DARK_TEXT = "#F9FAFB"
SECONDARY_TEXT = "#6B7280"

# --- МОТИВАЦИЯЛЫҚ СӨЗДЕР ---
QUOTES = [
    "«Оқу инемен құдық қазғандай.»",
    "«Білімді мыңды жығар, білекті бірді жығар.»",
    "«Еңбек етсең ерінбей, тояды қарның тіленбей.» – Абай",
    "«Армансыз адам – қанатсыз құспен тең.»",
    "«Бүгінгі еңбек – ертеңгі жеміс.»",
    "«Талапты ерге нұр жауар.»"
]

# --- АНЫҚТАМАЛЫҚ ДЕРЕКТЕР ---
HISTORY_DATES = [
    {"date": "Б.з.б. 1 мыңжылдық", "event": "Сақтардың өмір сүрген уақыты"},
    {"date": "552 жыл", "event": "Түрік қағанатының құрылуы"},
    {"date": "751 жыл", "event": "Атлах (Талас) шайқасы"},
    {"date": "1206 жыл", "event": "Шыңғыс ханның ұлы хан болып сайлануы"},
    {"date": "1465 жыл", "event": "Қазақ хандығының құрылуы"},
    {"date": "1723-1727 жылдар", "event": "«Ақтабан шұбырынды, Алқакөл сұлама»"},
    {"date": "1837-1847 жылдар", "event": "Кенесары Қасымұлы бастаған көтеріліс"},
    {"date": "1991 жыл 16 желтоқсан", "event": "Қазақстанның Тәуелсіздігін жариялауы"},
]

MATH_FORMULAS = [
    {"name": "Пифагор теоремасы", "formula": "a² + b² = c²"},
    {"name": "Шеңбердің ауданы", "formula": "S = πr²"},
    {"name": "Шеңбердің ұзындығы", "formula": "C = 2πr"},
    {"name": "Тіктөртбұрыш ауданы", "formula": "S = a × b"},
    {"name": "Трапеция ауданы", "formula": "S = (a + b) / 2 × h"},
    {"name": "Арифметикалық прогрессия", "formula": "an = a1 + (n-1)d"},
    {"name": "Геометриялық прогрессия", "formula": "bn = b1 × q^(n-1)"},
]

def main(page: ft.Page):
    db.init_db()

    page.title = "№63 Қ.Сатбаев ҰБТ"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=THEME_COLOR)
    page.bgcolor = LIGHT_BG
    page.window_width = 400
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {
        "user": None,
        "current_subject": None,
        "questions": [],
        "current_index": 0,
        "score": 0,
        "answers_log": []
    }

    # --- UI Helpers ---
    def get_bg_color(): return DARK_BG if page.theme_mode == ft.ThemeMode.DARK else LIGHT_BG
    def get_card_color(): return DARK_CARD if page.theme_mode == ft.ThemeMode.DARK else LIGHT_CARD
    def get_text_color(): return DARK_TEXT if page.theme_mode == ft.ThemeMode.DARK else LIGHT_TEXT

    def create_card(content, padding=20):
        return ft.Container(
            content=content,
            padding=padding,
            bgcolor=get_card_color(),
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=15, spread_radius=1, color=ft.Colors.with_opacity(0.1, "black"), offset=ft.Offset(0, 4)),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.bgcolor = get_bg_color()
        e.control.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        if state["user"]:
            if state["user"]["role"] == "teacher": show_teacher_menu()
            else: show_student_menu()
        else: show_login_screen()
        page.update()

    # --- 1. LOGIN ---
    def show_login_screen():
        page.clean(); page.bgcolor = get_bg_color()
        username = ft.TextField(label="Логин", width=280, border_radius=12, prefix_icon=ft.Icons.PERSON_OUTLINE)
        password = ft.TextField(label="Құпия сөз", width=280, password=True, can_reveal_password=True, border_radius=12, prefix_icon=ft.Icons.LOCK_OUTLINE)
        error_text = ft.Text("", color="red", size=12)

        def login_click(e):
            user = db.login_user(username.value, password.value)
            if user:
                state["user"] = user
                if user["role"] == "teacher": show_teacher_menu()
                else: show_student_menu()
            else: error_text.value = "Қате логин немесе құпия сөз!"; page.update()

        content = ft.Column([
            ft.Icon(ft.Icons.SCHOOL_ROUNDED, size=60, color=THEME_COLOR),
            ft.Text("Қош келдіңіз!", size=26, weight="bold", color=get_text_color()),
            ft.Text("№63 Қ.Сатбаев ҰБТ-ға дайындық бағдарламасы", color=SECONDARY_TEXT, text_align="center", size=12),
            ft.Divider(height=20, color="transparent"),
            username, password, error_text,
            ft.Container(height=10),
            ft.FilledButton("КІРУ", width=280, height=50, on_click=login_click),
            ft.TextButton("Тіркелу", on_click=lambda e: show_register_screen())
        ], horizontal_alignment="center", spacing=10)
        page.add(ft.Container(content=create_card(content, padding=40), alignment=ft.Alignment(0, 0), expand=True))

    def show_register_screen():
        page.clean(); page.bgcolor = get_bg_color()
        full_name = ft.TextField(label="Аты-жөніңіз", width=280, border_radius=12)
        username = ft.TextField(label="Логин", width=280, border_radius=12)
        password = ft.TextField(label="Құпия сөз", width=280, password=True, border_radius=12)
        error_text = ft.Text("", color="red", size=12)

        def register_click(e):
            if not all([username.value, full_name.value, password.value]): error_text.value = "Барлық өрісті толтырыңыз!"; page.update(); return
            if db.register_user(username.value, full_name.value, password.value):
                user = db.login_user(username.value, password.value)
                state["user"] = user
                show_student_menu()
            else: error_text.value = "Бұл логин бос емес!"; page.update()

        content = ft.Column([
            ft.Text("Тіркелу", size=24, weight="bold", color=get_text_color()),
            full_name, username, password, error_text,
            ft.Container(height=10),
            ft.FilledButton("ТІРКЕЛУ", width=280, height=50, on_click=register_click),
            ft.TextButton("Кері қайту", on_click=lambda e: show_login_screen())
        ], horizontal_alignment="center", spacing=10)
        page.add(ft.Container(content=create_card(content), alignment=ft.Alignment(0, 0), expand=True))

    # --- 2. STUDENT MENU ---
    def show_student_menu():
        page.clean(); page.bgcolor = get_bg_color()
        random_quote = random.choice(QUOTES)

        header = ft.Row([
            ft.Row([
                ft.CircleAvatar(content=ft.Text(state['user']['full_name'][0], size=20, weight="bold"), bgcolor=THEME_COLOR, radius=20),
                ft.Column([ft.Text(f"Сәлем,", size=12, color=SECONDARY_TEXT), ft.Text(f"{state['user']['full_name']}", size=16, weight="bold", color=get_text_color())], spacing=2)
            ]),
            ft.Row([ft.IconButton(ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE, on_click=toggle_theme), ft.IconButton(ft.Icons.LOGOUT_ROUNDED, on_click=lambda e: show_login_screen(), icon_color="red")])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        def create_btn(text, icon, color, action):
            return ft.Container(
                content=ft.Row([ft.Container(content=ft.Icon(icon, color="white", size=24), bgcolor=color, padding=10, border_radius=10), ft.Text(text, size=16, weight="w600", color=get_text_color())], spacing=15),
                padding=15, bgcolor=get_card_color(), border_radius=15, border=ft.Border.all(1, ft.Colors.GREY_800 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_200), on_click=action, ink=True 
            )

        motivation_card = ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.YELLOW_600), ft.Text("Күннің сөзі", weight="bold", color=get_text_color())]),
                ft.Text(random_quote, italic=True, size=14, color=SECONDARY_TEXT, text_align="center")
            ], horizontal_alignment="center"),
            padding=15, bgcolor=get_card_color(), border_radius=15,
            border=ft.Border.all(1, ft.Colors.GREY_300 if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.GREY_700)
        )

        page.add(ft.Column([
            ft.Container(content=header, padding=ft.Padding(bottom=5)),
            motivation_card,
            ft.Divider(height=10, color="transparent"),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=ft.Colors.BLUE_400, size=30),
                    ft.Column([ft.Text("Менің профилім", weight="bold", color=get_text_color()), ft.Text("Статистика және баптаулар", size=12, color=SECONDARY_TEXT)], spacing=2),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=SECONDARY_TEXT)
                ], alignment="spaceBetween"),
                padding=15, bgcolor=get_card_color(), border_radius=15, border=ft.Border.all(1, ft.Colors.GREY_800 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_200), on_click=lambda e: show_profile_screen(), ink=True
            ),
            ft.Divider(height=10, color="transparent"),
            ft.Text("Тест тапсыру", size=18, weight="bold", color=get_text_color()),
            create_btn("Қазақстан тарихы", ft.Icons.HISTORY_EDU, ft.Colors.BLUE_500, lambda e: start_test_prep("Қазақстан тарихы")),
            create_btn("Мат. сауаттылық", ft.Icons.CALCULATE_OUTLINED, ft.Colors.ORANGE_500, lambda e: start_test_prep("Математикалық сауаттылық")),
            create_btn("Оқу сауаттылығы", ft.Icons.MENU_BOOK_ROUNDED, ft.Colors.GREEN_500, lambda e: start_test_prep("Оқу сауаттылығы")),
            ft.Divider(height=5, color="transparent"),
            create_btn("Анықтамалық", ft.Icons.MENU_BOOK, ft.Colors.TEAL_400, lambda e: show_reference_screen()),
            ft.Container(height=5),
            create_btn("Пайдалы ресурстар", ft.Icons.LINK, ft.Colors.CYAN_500, lambda e: show_resources_screen()),
            ft.Container(height=5),
            create_btn("Нәтижелер тарихы", ft.Icons.BAR_CHART_ROUNDED, ft.Colors.PURPLE_500, lambda e: show_my_results()),
        ], spacing=10))

    def start_test_prep(subj): state["current_subject"] = subj; show_settings_menu()

    # --- ЖАҢАРТЫЛҒАН: АНЫҚТАМАЛЫҚ ЭКРАНЫ (TABS-сыз, Батырмалармен) ---
    def show_reference_screen():
        page.clean(); page.bgcolor = get_bg_color()
        
        # Тізім контейнері
        content_column = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        def load_history(e=None):
            # Түймелердің түсін өзгерту
            btn_history.style = ft.ButtonStyle(bgcolor=THEME_COLOR, color="white")
            btn_math.style = ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT, color=get_text_color())
            
            content_column.controls.clear()
            for item in HISTORY_DATES:
                content_column.controls.append(ft.Container(
                    content=ft.Column([
                        ft.Text(item['date'], weight="bold", color=THEME_COLOR, size=16),
                        ft.Text(item['event'], color=get_text_color())
                    ]),
                    padding=10, bgcolor=get_card_color(), border_radius=10, border=ft.Border.all(1, ft.Colors.GREY_300)
                ))
            page.update()

        def load_math(e=None):
            # Түймелердің түсін өзгерту
            btn_math.style = ft.ButtonStyle(bgcolor=ft.Colors.ORANGE, color="white")
            btn_history.style = ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT, color=get_text_color())
            
            content_column.controls.clear()
            for item in MATH_FORMULAS:
                content_column.controls.append(ft.Container(
                    content=ft.Row([
                        ft.Text(item['name'], expand=True, color=get_text_color()),
                        ft.Container(content=ft.Text(item['formula'], weight="bold", color="white"), bgcolor=ft.Colors.ORANGE_400, padding=5, border_radius=5)
                    ], alignment="spaceBetween"),
                    padding=10, bgcolor=get_card_color(), border_radius=10, border=ft.Border.all(1, ft.Colors.GREY_300)
                ))
            page.update()

        # Батырмалар
        btn_history = ft.FilledButton("Тарих даталары", on_click=load_history, expand=True)
        btn_math = ft.FilledButton("Мат. формулалар", on_click=load_math, expand=True) # Басында Filled емес, Outlined сияқты жасаймыз

        # Бастапқы жүктеу
        load_history()

        page.add(ft.Column([
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_student_menu()), ft.Text("Анықтамалық", size=20, weight="bold", color=get_text_color())]),
            ft.Row([btn_history, btn_math], spacing=10),
            content_column
        ], expand=True))

    # --- 3. TEST PROCESS ---
    def show_settings_menu():
        page.clean(); page.bgcolor = get_bg_color()
        dd_count = ft.Dropdown(label="Сұрақ саны", options=[ft.dropdown.Option("5"), ft.dropdown.Option("10"), ft.dropdown.Option("20")], value="5", width=280, border_radius=12)
        def start(e):
            state["questions"] = db.get_questions_by_subject(state["current_subject"], limit=int(dd_count.value))
            if not state["questions"]: page.snack_bar = ft.SnackBar(ft.Text("Сұрақ жоқ!")); page.snack_bar.open=True; page.update(); return
            state["score"] = 0; state["current_index"] = 0; state["answers_log"] = []
            load_question_screen()
        content = ft.Column([ft.Icon(ft.Icons.QUIZ_ROUNDED, size=50, color=THEME_COLOR), ft.Text("Тест баптаулары", size=22, weight="bold", color=get_text_color()), ft.Text(f"{state['current_subject']}", color=SECONDARY_TEXT), ft.Divider(), dd_count, ft.Container(height=20), ft.FilledButton("БАСТАУ", on_click=start, width=280, height=50)], horizontal_alignment="center")
        page.add(ft.Column([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_student_menu()), create_card(content, padding=30)]))

    def load_question_screen():
        if state["current_index"] >= len(state["questions"]): show_result_screen(); return
        page.clean(); page.bgcolor = get_bg_color()
        idx = state["current_index"]; total = len(state["questions"])
        data = state["questions"][idx]; opts = data["opts"].copy(); random.shuffle(opts)

        progress_circles = []
        for i in range(total):
            color = ft.Colors.GREY_300 
            if i < len(state["answers_log"]): color = ft.Colors.GREEN if state["answers_log"][i]["is_correct"] else ft.Colors.RED
            elif i == idx: color = THEME_COLOR 
            progress_circles.append(ft.Container(width=10, height=10, border_radius=5, bgcolor=color))
        
        btn_next = ft.FilledButton("Келесі", icon=ft.Icons.ARROW_FORWARD, width=320, height=50, on_click=lambda e: next_q(), visible=False)
        options_container = ft.Column(spacing=10)

        def check_answer(e):
            clicked = e.control; selected = clicked.data; correct = data["a"]; is_correct = (selected == correct)
            state["answers_log"].append({"question": data["q"], "your_answer": selected, "correct_answer": correct, "explanation": data["expl"], "is_correct": is_correct})
            for c in options_container.controls:
                c.on_click = None 
                if c.data == correct: c.bgcolor = ft.Colors.GREEN_100; c.border = ft.Border.all(2, ft.Colors.GREEN); c.content.controls[1].color = ft.Colors.BLACK
                elif c.data == selected: c.bgcolor = ft.Colors.RED_100; c.border = ft.Border.all(2, ft.Colors.RED); c.content.controls[1].color = ft.Colors.BLACK
                c.update()
            if is_correct: state["score"] += 1
            btn_next.visible = True; btn_next.update()

        for opt in opts:
            options_container.controls.append(ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.CIRCLE_OUTLINED, size=16, color=THEME_COLOR), ft.Text(opt, size=16, expand=True, color=get_text_color())], alignment="start"),
                padding=15, bgcolor=get_card_color(), width=320, border_radius=12,
                border=ft.Border.all(2, ft.Colors.GREY_600 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_200), on_click=check_answer, data=opt, ink=True
            ))

        page.add(ft.Column([
            ft.Text(f"Сұрақ {idx + 1}/{total}", weight="bold", color=get_text_color()),
            ft.Row(progress_circles, alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            ft.Container(height=10),
            ft.Container(content=ft.Text(data["q"], size=18, weight="bold", text_align="center", color=get_text_color()), padding=20, bgcolor=get_card_color(), width=320, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, "black"))),
            ft.Container(height=10), options_container, ft.Container(height=10), btn_next, ft.Container(height=20)
        ], scroll=ft.ScrollMode.AUTO, horizontal_alignment="center", expand=True))

    def next_q(): state["current_index"] += 1; load_question_screen()

    def show_resources_screen():
        page.clean(); page.bgcolor = get_bg_color()
        def open_url(url): webbrowser.open(url)
        def resource_card(title, desc, url, icon, color):
            return ft.Container(
                content=ft.Row([ft.Container(content=ft.Icon(icon, color="white"), bgcolor=color, padding=10, border_radius=10), ft.Column([ft.Text(title, weight="bold", color=get_text_color()), ft.Text(desc, size=12, color=SECONDARY_TEXT, width=200, overflow=ft.TextOverflow.ELLIPSIS)], expand=True), ft.IconButton(ft.Icons.OPEN_IN_NEW, on_click=lambda e: open_url(url))], alignment="spaceBetween"),
                padding=15, bgcolor=get_card_color(), border_radius=12, border=ft.Border.all(1, ft.Colors.GREY_300 if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.GREY_700), on_click=lambda e: open_url(url), ink=True
            )
        page.add(ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_student_menu()), ft.Text("Пайдалы ресурстар", size=20, weight="bold", color=get_text_color())]), ft.ListView([resource_card("Ұлттық тестілеу орталығы", "Ресми сайт, байқау сынақтары", "https://testcenter.kz/", ft.Icons.PUBLIC, ft.Colors.BLUE), resource_card("Daryn.online", "Видеосабақтар және ҰБТ курстары", "https://daryn.online/", ft.Icons.PLAY_CIRCLE_FILLED, ft.Colors.ORANGE), resource_card("Kitap.kz", "Қазақ әдебиеті және тарихы", "https://kitap.kz/", ft.Icons.BOOK, ft.Colors.GREEN), resource_card("BilimLand", "Барлық пәндер бойынша сабақтар", "https://bilimland.kz/", ft.Icons.SCHOOL, ft.Colors.PURPLE)], spacing=10, expand=True)], expand=True))

    def show_profile_screen():
        page.clean(); page.bgcolor = get_bg_color()
        total_tests, avg_score = db.get_user_stats(state['user']['id'])
        level = "Бастаушы"; level_color = ft.Colors.GREY
        if total_tests > 5: level = "Студент"; level_color = ft.Colors.BLUE
        if total_tests > 20: level = "Маман"; level_color = ft.Colors.ORANGE
        if total_tests > 50: level = "Профессор"; level_color = ft.Colors.PURPLE
        profile_card = ft.Column([ft.CircleAvatar(content=ft.Text(state['user']['full_name'][0], size=40, weight="bold"), bgcolor=THEME_COLOR, radius=50), ft.Text(state['user']['full_name'], size=22, weight="bold", color=get_text_color()), ft.Container(content=ft.Text(level, color="white", size=12, weight="bold"), bgcolor=level_color, padding=ft.Padding(left=10, top=5, right=10, bottom=5), border_radius=10), ft.Divider(), ft.Row([ft.Column([ft.Text(str(total_tests), size=20, weight="bold", color=get_text_color()), ft.Text("Тест саны", size=12, color=SECONDARY_TEXT)], horizontal_alignment="center"), ft.Container(width=1, height=40, bgcolor=SECONDARY_TEXT), ft.Column([ft.Text(f"{int(avg_score)}%", size=20, weight="bold", color=ft.Colors.GREEN if avg_score > 70 else ft.Colors.ORANGE), ft.Text("Орташа бал", size=12, color=SECONDARY_TEXT)], horizontal_alignment="center")], alignment="spaceEvenly", width=300)], horizontal_alignment="center", spacing=10)
        
        # Қатені түзету: Функция анықталды
        def go_to_change_password(e):
            show_change_password_screen()

        settings_col = ft.Column([ft.Text("Баптаулар", weight="bold", color=get_text_color()), ft.Container(content=ft.Row([ft.Icon(ft.Icons.LOCK_RESET, color=THEME_COLOR), ft.Text("Құпия сөзді өзгерту", color=get_text_color(), expand=True), ft.Icon(ft.Icons.CHEVRON_RIGHT, color=SECONDARY_TEXT)]), padding=15, bgcolor=get_card_color(), border_radius=12, on_click=go_to_change_password, ink=True)])
        page.add(ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_student_menu()), ft.Text("Профиль", size=20, weight="bold", color=get_text_color())]), create_card(profile_card, padding=30), settings_col], spacing=20))

    def show_result_screen():
        page.clean(); page.bgcolor = get_bg_color()
        db.save_result(state["user"]["id"], state["current_subject"], state["score"], len(state["questions"]))
        score = state["score"]; total = len(state["questions"]); percent = int((score/total) * 100) if total > 0 else 0
        color = ft.Colors.GREEN if percent >= 80 else (ft.Colors.ORANGE if percent >= 50 else ft.Colors.RED)
        content = ft.Column([ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, size=80, color=color), ft.Text("Тамаша!" if percent >= 80 else "Жақсы!", size=28, weight="bold", color=color), ft.Text(f"{score} / {total}", size=40, weight="bold", color=get_text_color()), ft.ProgressBar(value=percent/100, color=color, bgcolor=ft.Colors.GREY_200, height=10), ft.Text(f"{percent}%", weight="bold", color=get_text_color()), ft.Container(height=20), ft.FilledButton("Қатемен жұмыс", icon=ft.Icons.ASSIGNMENT_LATE, width=250, on_click=lambda e: show_mistakes_screen(), style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400)), ft.FilledButton("Мәзірге оралу", width=250, on_click=lambda e: show_student_menu())], horizontal_alignment="center", spacing=10)
        page.add(ft.Container(content=create_card(content, padding=40), alignment=ft.Alignment(0, 0), expand=True))

    def show_mistakes_screen():
        page.clean(); page.bgcolor = get_bg_color()
        lv = ft.ListView(expand=True, spacing=15, padding=10)
        for item in state["answers_log"]:
            is_cor = item['is_correct']; icon = ft.Icons.CHECK_CIRCLE if is_cor else ft.Icons.CANCEL; color = ft.Colors.GREEN if is_cor else ft.Colors.RED
            expl_content = ft.Column([ft.Divider(), ft.Text(f"Дұрыс жауап: {item['correct_answer']}", color=ft.Colors.GREEN, weight="bold"), ft.Text(f"Түсіндірме: {item['explanation']}", italic=True, size=12, color=get_text_color())]) if not is_cor else ft.Container()
            card = ft.Container(content=ft.Column([ft.Row([ft.Icon(icon, color=color), ft.Text("Дұрыс" if is_cor else "Қате", color=color, weight="bold")]), ft.Text(item['question'], weight="bold", size=16, color=get_text_color()), ft.Text(f"Сіздің жауап: {item['your_answer']}", color=color), expl_content]), padding=15, bgcolor=get_card_color(), border_radius=12, border=ft.Border.all(1, color), shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.with_opacity(0.1, "black")))
            lv.controls.append(card)
        page.add(ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_student_menu()), ft.Text("Қатемен жұмыс", size=20, weight="bold", color=get_text_color())]), lv], expand=True))

    def show_change_password_screen():
        page.clean(); page.bgcolor = get_bg_color()
        
        # ҚАТЕНІ ТҮЗЕТУ: Функция осында анықталды
        def back_action(e):
            if state["user"]["role"] == "student": show_student_menu()
            else: show_teacher_menu()

        old_pass = ft.TextField(label="Ескі құпия сөз", width=300, password=True, can_reveal_password=True, border_radius=12, prefix_icon=ft.Icons.LOCK_OPEN)
        new_pass = ft.TextField(label="Жаңа құпия сөз", width=300, password=True, can_reveal_password=True, border_radius=12, prefix_icon=ft.Icons.LOCK_OUTLINE)
        confirm_pass = ft.TextField(label="Құпия сөзді қайталаңыз", width=300, password=True, can_reveal_password=True, border_radius=12, prefix_icon=ft.Icons.LOCK_RESET)
        
        def save(e):
            if not all([old_pass.value, new_pass.value, confirm_pass.value]): page.snack_bar = ft.SnackBar(ft.Text("Толықтырыңыз!")); page.snack_bar.open=True; page.update(); return
            if old_pass.value != state["user"]["password"]: page.snack_bar = ft.SnackBar(ft.Text("Ескі пароль қате!")); page.snack_bar.open=True; page.update(); return
            if new_pass.value != confirm_pass.value: page.snack_bar = ft.SnackBar(ft.Text("Парольдер сәйкес емес!")); page.snack_bar.open=True; page.update(); return
            if db.change_password(state["user"]["id"], new_pass.value):
                state["user"] = db.login_user(state["user"]["username"], new_pass.value)
                page.snack_bar = ft.SnackBar(ft.Text("Пароль жаңартылды! ✅"), bgcolor="green"); page.snack_bar.open=True; old_pass.value=""; new_pass.value=""; confirm_pass.value=""; page.update()
                import time; time.sleep(0.5)
                if state["user"]["role"] == "teacher": show_teacher_menu()
                else: show_student_menu()
        
        content = ft.Column([ft.Icon(ft.Icons.MANAGE_ACCOUNTS, size=50, color=THEME_COLOR), ft.Text("Парольді жаңарту", size=22, weight="bold", color=get_text_color()), ft.Divider(), old_pass, new_pass, confirm_pass, ft.Container(height=10), ft.FilledButton("САҚТАУ", width=300, height=50, on_click=save)], horizontal_alignment="center", spacing=15)
        page.add(ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=back_action), ft.Text("Баптаулар", size=20, weight="bold", color=get_text_color())]), create_card(content, padding=30)]))

    def show_teacher_menu():
        page.clean(); page.bgcolor = get_bg_color()
        def menu_btn(title, icon, color, action): return ft.Container(content=ft.Column([ft.Icon(icon, size=40, color="white"), ft.Text(title, color="white", weight="bold", size=14, text_align="center")], alignment="center", horizontal_alignment="center"), width=150, height=150, bgcolor=color, border_radius=25, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.2, "black")), on_click=action, ink=True)
        top_bar = ft.Row([ft.Text("ҰСТАЗ ПАНЕЛІ", size=20, weight="bold", color=THEME_COLOR), ft.Row([ft.IconButton(ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE, on_click=toggle_theme), ft.IconButton(ft.Icons.LOGOUT, on_click=lambda e: show_login_screen(), icon_color="red")])], alignment="spaceBetween")
        page.add(ft.Column([top_bar, ft.Divider(), ft.Row([menu_btn("Сұрақ қосу", ft.Icons.ADD_TASK, ft.Colors.INDIGO_400, lambda e: show_add_question_screen()), menu_btn("Рейтинг", ft.Icons.LEADERBOARD, ft.Colors.TEAL_400, lambda e: show_leaderboard_screen())], alignment="center"), ft.Container(height=10), ft.Row([menu_btn("Сұрақтарды өшіру", ft.Icons.DELETE_FOREVER, ft.Colors.RED_400, lambda e: show_delete_questions_screen())], alignment="center")], spacing=15, horizontal_alignment="center"))

    def show_delete_questions_screen():
        page.clean(); page.bgcolor = get_bg_color()
        questions = db.get_all_questions_for_teacher(); lv = ft.ListView(expand=True, spacing=10, padding=10)
        def delete_click(q_id, card_ref):
            if db.delete_question(q_id): lv.controls.remove(card_ref); page.update(); page.snack_bar = ft.SnackBar(ft.Text("Өшірілді"), bgcolor="red"); page.snack_bar.open=True; page.update()
        if not questions: lv.controls.append(ft.Text("Сұрақтар жоқ", italic=True, color=get_text_color()))
        else:
            for q in questions:
                card = ft.Container(content=ft.Row([ft.Column([ft.Text(q['subject'], size=12, color=SECONDARY_TEXT, weight="bold"), ft.Text(q['question'], size=14, weight="w500", color=get_text_color(), overflow=ft.TextOverflow.ELLIPSIS, width=250)], expand=True), ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, qid=q['id']: delete_click(qid, e.control.parent.parent.parent))]), padding=10, bgcolor=get_card_color(), border_radius=10, border=ft.Border.all(1, ft.Colors.GREY_300))
                lv.controls.append(card)
        page.add(ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_teacher_menu()), ft.Text("Сұрақтарды өшіру", size=20, weight="bold", color=get_text_color())]), lv], expand=True))

    def show_my_results():
        page.clean(); page.bgcolor = get_bg_color()
        results = db.get_my_results(state['user']['id']); lv = ft.ListView(expand=True, spacing=10, padding=10)
        if not results: lv.controls.append(ft.Text("Нәтиже жоқ", italic=True, color=get_text_color()))
        else:
            for r in results:
                percent = int((r['score'] / r['total']) * 100)
                if percent >= 80: badge_color = ft.Colors.GREEN
                elif percent >= 50: badge_color = ft.Colors.ORANGE
                else: badge_color = ft.Colors.RED
                lv.controls.append(ft.Container(content=ft.Row([ft.Column([ft.Text(f"{r['subject']}", weight="bold", color=get_text_color()), ft.Text(f"{r['date']}", size=12, color=SECONDARY_TEXT)]), ft.Container(content=ft.Text(f"{r['score']} / {r['total']}", color="white", size=14, weight="bold"), bgcolor=badge_color, padding=ft.Padding(left=12, top=6, right=12, bottom=6), border_radius=8)], alignment="spaceBetween"), padding=15, bgcolor=get_card_color(), border_radius=12, border=ft.Border.all(1, ft.Colors.GREY_600 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_300), shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.with_opacity(0.05, "black"))))
        page.add(ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_student_menu()), ft.Text("Нәтижелер", size=20, weight="bold", color=get_text_color())]), lv], expand=True))

    def show_leaderboard_screen():
        page.clean()
        page.bgcolor = get_bg_color()
        leaders = db.get_leaderboard_general()
        lv = ft.ListView(expand=True, spacing=10, padding=15)

        if not leaders:
            lv.controls.append(ft.Container(content=ft.Text("Әзірге нәтижелер жоқ", italic=True, color=SECONDARY_TEXT), alignment=ft.Alignment(0, 0), padding=20))
        else:
            for i, row in enumerate(leaders):
                rank = i + 1
                
                # ТҮЗЕТІЛГЕН ЖЕР: 1-3 орындарға ИКОНКА, қалғанына САН қоямыз
                if rank == 1:
                    rank_color = "#FFD700"
                    rank_content = ft.Icon(ft.Icons.WORKSPACE_PREMIUM, color="white", size=20)
                elif rank == 2:
                    rank_color = "#C0C0C0"
                    rank_content = ft.Icon(ft.Icons.LOOKS_TWO, color="white", size=20)
                elif rank == 3:
                    rank_color = "#CD7F32"
                    rank_content = ft.Icon(ft.Icons.LOOKS_3, color="white", size=20)
                else:
                    rank_color = ft.Colors.BLUE_GREY_200
                    # Мына жерде Icon емес, Text (Сан) қоямыз
                    rank_content = ft.Text(str(rank), color="white", weight="bold", size=16)

                def score_badge(icon, val, color):
                    return ft.Container(
                        content=ft.Row([ft.Icon(icon, size=14, color="white"), ft.Text(str(int(val)), size=12, color="white", weight="bold")], spacing=3, alignment="center"),
                        bgcolor=color, padding=5, border_radius=8, width=60, height=25
                    )

                card_content = ft.Row([
                    ft.Container(
                        content=rank_content, # <--- Иконка немесе Сан
                        bgcolor=rank_color, width=40, height=40, border_radius=20, alignment=ft.Alignment(0, 0),
                        shadow=ft.BoxShadow(blur_radius=5, color=rank_color)
                    ),
                    ft.Column([
                        ft.Text(row['full_name'], weight="bold", size=16, color=get_text_color()),
                        ft.Row([
                            score_badge(ft.Icons.HISTORY_EDU, row['history'], ft.Colors.BLUE_400),
                            score_badge(ft.Icons.CALCULATE, row['math'], ft.Colors.ORANGE_400),
                            score_badge(ft.Icons.MENU_BOOK, row['reading'], ft.Colors.GREEN_400)
                        ])
                    ], expand=True, spacing=5),
                    ft.Column([
                        ft.Text("Жалпы", size=10, color=SECONDARY_TEXT),
                        ft.Text(f"{int(row['total_score'])}", weight="bold", size=20, color=THEME_COLOR)
                    ], horizontal_alignment="center")
                ], alignment="spaceBetween")

                lv.controls.append(ft.Container(
                    content=card_content,
                    padding=15, bgcolor=get_card_color(), border_radius=15,
                    border=ft.Border.all(2, rank_color if rank <= 3 else ft.Colors.TRANSPARENT),
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, "black")),
                    animate_scale=ft.Animation(300, "easeOut")
                ))

        page.add(ft.Column([
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_teacher_menu() if state['user']['role'] == 'teacher' else show_student_menu()), ft.Text("Үздік оқушылар", size=24, weight="bold", color=get_text_color())]),
            ft.Container(content=ft.Row([ft.Text("Тар: Тарих", size=12, color=SECONDARY_TEXT), ft.Text("Мат: Математика", size=12, color=SECONDARY_TEXT), ft.Text("Оқу: Оқу сауат.", size=12, color=SECONDARY_TEXT)], alignment="center", spacing=20), padding=5),
            lv
        ], expand=True))
    def show_add_question_screen():
        page.clean()
        page.bgcolor = get_bg_color()
        subject_dd = ft.Dropdown(label="Пән", options=[ft.dropdown.Option("Қазақстан тарихы"), ft.dropdown.Option("Математикалық сауаттылық"), ft.dropdown.Option("Оқу сауаттылығы")], width=300)
        q_text = ft.TextField(label="Сұрақ", multiline=True, width=300)
        opt1 = ft.TextField(label="Дұрыс жауап", width=300, prefix_icon=ft.Icons.CHECK)
        opt2, opt3, opt4 = ft.TextField(label="Нұсқа 2", width=300), ft.TextField(label="Нұсқа 3", width=300), ft.TextField(label="Нұсқа 4", width=300)
        expl_text = ft.TextField(label="Түсіндірме (қате жауап үшін)", multiline=True, width=300, icon=ft.Icons.INFO)
        
        def save_q(e):
            if not all([subject_dd.value, q_text.value, opt1.value, opt2.value]): return
            db.add_question(subject_dd.value, q_text.value, [opt1.value, opt2.value, opt3.value, opt4.value], opt1.value, expl_text.value)
            page.snack_bar = ft.SnackBar(ft.Text("Сақталды! ✅"), bgcolor="green"); page.snack_bar.open=True; page.update()
            q_text.value = ""; opt1.value = ""; opt2.value = ""; opt3.value = ""; opt4.value = ""; expl_text.value = ""

        page.add(ft.Column([ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_teacher_menu()), ft.Text("Сұрақ қосу", size=20, weight="bold", color=get_text_color())]), 
                           ft.Column([subject_dd, q_text, opt1, opt2, opt3, opt4, expl_text, ft.FilledButton("САҚТАУ", on_click=save_q, width=300)], spacing=10)], scroll=ft.ScrollMode.AUTO))

    show_login_screen()

if __name__ == "__main__":
    ft.run(main)
