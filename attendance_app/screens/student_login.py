from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.app import App


class StudentLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex("#f0f4f8ff"))
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        self.heading = Label(
            text="[b]Student Login[/b]",
            markup=True,
            font_size=26,
            color=get_color_from_hex("#22223bff"),
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "top": 0.92}
        )
        self.add_widget(self.heading)

        self.label_user = Label(
            text="User ID:",
            size_hint=(None, None),
            size=(120, 30),
            color=get_color_from_hex("#22223bff"),
            pos_hint={"center_x": 0.5, "top": 0.80}
        )
        self.add_widget(self.label_user)

        self.user_id_input = TextInput(
            multiline=False,
            size_hint=(None, None),
            size=(280, 40),
            background_color=get_color_from_hex("#e0e1ddff"),
            foreground_color=get_color_from_hex("#22223bff"),
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        self.add_widget(self.user_id_input)

        self.label_pass = Label(
            text="Password:",
            size_hint=(None, None),
            size=(120, 30),
            color=get_color_from_hex("#22223bff"),
            pos_hint={"center_x": 0.5, "top": 0.70}
        )
        self.add_widget(self.label_pass)

        self.password_input = TextInput(
            password=True,
            multiline=False,
            size_hint=(None, None),
            size=(280, 40),
            background_color=get_color_from_hex("#e0e1ddff"),
            foreground_color=get_color_from_hex("#22223bff"),
            pos_hint={"center_x": 0.5, "top": 0.65}
        )
        self.add_widget(self.password_input)

        self.login_btn = Button(
            text="Login",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "top": 0.55},
            background_color=get_color_from_hex("#4ea8deff"),
            color=get_color_from_hex("#ffffffff"),
            bold=True,
            background_normal=""
        )
        self.login_btn.bind(on_press=self.attempt_login)
        self.add_widget(self.login_btn)

        self.back_btn = Button(
            text="Back",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "top": 0.45},
            background_color=get_color_from_hex("#adb5bdff"),
            color=get_color_from_hex("#22223bff"),
            bold=True,
            background_normal=""
        )
        self.back_btn.bind(on_press=lambda inst: App.get_running_app().go_to_screen("login"))
        self.add_widget(self.back_btn)

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def attempt_login(self, instance):
        user_id = self.user_id_input.text.strip()
        password = self.password_input.text.strip()
        App.get_running_app().validate_login("Student", user_id, password)
