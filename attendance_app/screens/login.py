from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.app import App


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex("#8F9198FF"))
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        self.heading = Label(
            text="[b]Attendance System[/b]",
            markup=True,
            font_size=32,
            color=get_color_from_hex("#FFFFFFFF"),
            size_hint=(None, None),
            size=(400, 60),
            pos_hint={"center_x": 0.5, "top": 0.92}
        )
        self.add_widget(self.heading)

        self.btn_student = Button(
            text="Student Login",
            font_size=20,
            size_hint=(None, None),
            size=(320, 60),
            pos_hint={"center_x": 0.5, "top": 0.75},
            background_color=get_color_from_hex("#62AFE2FF"),
            color=get_color_from_hex("#ffffffff"),
            bold=True,
            background_normal=""
        )
        self.btn_student.bind(on_press=lambda inst: App.get_running_app().go_to_screen("student_login"))
        self.add_widget(self.btn_student)

        self.btn_teacher = Button(
            text="Teacher Login",
            font_size=20,
            size_hint=(None, None),
            size=(320, 60),
            pos_hint={"center_x": 0.5, "top": 0.62},
            background_color=get_color_from_hex("#488155ff"),
            color=get_color_from_hex("#ffffffff"),
            bold=True,
            background_normal=""
        )
        self.btn_teacher.bind(on_press=lambda inst: App.get_running_app().go_to_screen("teacher_login"))
        self.add_widget(self.btn_teacher)

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
