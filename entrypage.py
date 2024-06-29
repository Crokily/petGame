from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

class EntryScreen(Screen):
    def __init__(self, **kwargs):
        super(EntryScreen, self).__init__(**kwargs)
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)
        self.build_ui()

    def build_ui(self):
        # Add background image
        background = Image(source='/Users/julian/Desktop/Course/hackathon/petGame/4.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.main_layout.add_widget(background)

        layout = BoxLayout(orientation='vertical', padding=(10, 10), size_hint=(None, None), size=(300, 200), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.question_label = Label(text="Enter Name:", font_size=50)
        self.name_input = TextInput(multiline=False)
        self.name_input.bind(on_text_validate=self.on_enter_text_validate)
        layout.add_widget(self.question_label)
        layout.add_widget(self.name_input)
        self.main_layout.add_widget(layout)

    def on_enter_text_validate(self, instance):
        pet_name = self.name_input.text
        self.manager.get_screen('maininterface').initialize_pet(pet_name)
        self.manager.current = 'maininterface'
