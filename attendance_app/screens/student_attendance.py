import pandas as pd
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

from utils.helpers import CSV_FILE


class StudentAttendanceScreen(Screen):
    """
    Screen to display a single student's attendance as two-column grid (subject, value)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.title_label = Label(text="Attendance", font_size=20, size_hint=(1, 0.1))
        layout.add_widget(self.title_label)

        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.grid = GridLayout(cols=2, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        layout.add_widget(self.scroll)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=lambda inst: App.get_running_app().go_to_screen("student_dashboard"))
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def populate_for_student(self, student_name):
        """Read CSV, find the row and populate subject/value pairs."""
        self.grid.clear_widgets()
        try:
            df = pd.read_csv(CSV_FILE)
            if student_name not in df["Name"].values:
                App.get_running_app().popup("Error", "Attendance record not found!")
                return
            student_attendance = df[df["Name"] == student_name].drop(columns=["Name"])
            subjects = list(student_attendance.columns)
            values = student_attendance.iloc[0].values
            for s, v in zip(subjects, values):
                self.grid.add_widget(Label(text=str(s)))
                self.grid.add_widget(Label(text=str(v)))
            self.title_label.text = f"Attendance - {student_name}"
        except Exception as e:
            App.get_running_app().popup("Error", f"Failed to load attendance: {e}")
