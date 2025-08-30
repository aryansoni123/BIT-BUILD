from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.app import App


class TeacherDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=get_color_from_hex("#f0f4f8ff"))
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        self.class_id_label = Label(
            text="Teacher Dashboard",
            font_size=26,
            markup=True,
            color=get_color_from_hex("#22223bff"),
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "top": 0.92}
        )
        self.add_widget(self.class_id_label)

        self.qr_image = KivyImage(
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "top": 0.75}
        )
        self.add_widget(self.qr_image)

        gen_btn = Button(
            text="Generate QR",
            font_size=20,
            size_hint=(None, None),
            size=(320, 60),
            pos_hint={"center_x": 0.5, "top": 0.55},
            background_color=get_color_from_hex("#488155ff"),
            color=get_color_from_hex("#ffffffff"),
            bold=True,
            background_normal=""
        )
        gen_btn.bind(on_press=lambda inst: App.get_running_app().generate_qr_current_class())
        self.add_widget(gen_btn)

        view_attendance_btn = Button(
            text="View Attendance",
            font_size=20,
            size_hint=(None, None),
            size=(320, 60),
            pos_hint={"center_x": 0.5, "top": 0.42},
            background_color=get_color_from_hex("#488155ff"),
            color=get_color_from_hex("#ffffffff"),
            bold=True,
            background_normal=""
        )
        view_attendance_btn.bind(on_press=lambda inst: App.get_running_app().show_teacher_attendance_screen())
        self.add_widget(view_attendance_btn)

        back_btn = Button(
            text="Logout",
            font_size=20,
            size_hint=(None, None),
            size=(320, 60),
            pos_hint={"center_x": 0.5, "top": 0.29},
            background_color=get_color_from_hex("#adb5bdff"),
            color=get_color_from_hex("#22223bff"),
            bold=True,
            background_normal=""
        )
        back_btn.bind(on_press=lambda inst: App.get_running_app().logout_to_login())
        self.add_widget(back_btn)

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
