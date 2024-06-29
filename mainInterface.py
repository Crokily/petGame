from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.core.audio import SoundLoader  # Import SoundLoader

from entrypage import EntryScreen
from main import initialize_pet, update_current_pet

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.pet_name = ""
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)
        self.jump_sound = SoundLoader.load('/Users/julian/Desktop/Course/hackathon/petGame/1.mp3')  # Load the jump sound

    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.main_layout.clear_widgets()

        # Top bar with status bars
        status_layout = GridLayout(cols=4, size_hint=(1, 0.1), pos_hint={'top': 1})
        statuses = ['HUNGER', 'ENERGY', 'HAPPINESS', 'HEALTH']
        self.status_labels = {}
        for status in statuses:
            label = Label(text=f"{status}: 50", font_size=14)
            status_layout.add_widget(label)
            progress_bar = ProgressBar(max=100, value=50)
            status_layout.add_widget(progress_bar)
            self.status_labels[status] = (label, progress_bar)
        self.main_layout.add_widget(status_layout)

        # Add background image
        background = Image(source='/Users/julian/Desktop/Course/hackathon/petGame/2.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 0.9), pos_hint={'center_x': 0.5, 'y': 0})
        self.main_layout.add_widget(background)

        # Center area with the pet image
        self.pet_image = Image(source='/Users/julian/Desktop/Course/hackathon/petGame/10.png', size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.main_layout.add_widget(self.pet_image)

        # Initial position of the pet
        self.pet_x = 0.5
        self.pet_y = 0.5

        # Bottom bar with buttons
        button_layout = GridLayout(cols=2, size_hint=(1, 0.1), pos_hint={'y': 0})
        take_photo_button = Button(text='Take Photos', font_size=14)
        exercise_button = Button(text='Exercise', font_size=14)
        take_photo_button.bind(on_press=self.take_photo)
        exercise_button.bind(on_press=self.jump)
        button_layout.add_widget(take_photo_button)
        button_layout.add_widget(exercise_button)
        self.main_layout.add_widget(button_layout)

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

        # Schedule the update of pet's position
        Clock.schedule_interval(self.update_position, 1.0 / 60.0)  # Update 60 times per second

    def initialize_pet(self, pet_name):
        self.pet_name = pet_name
        print(f"Initializing pet with name: {pet_name}")
        initialize_pet(pet_name)

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 273:  # Up arrow key
            self.pet_y += 0.02
        elif key == 274:  # Down arrow key
            self.pet_y -= 0.02
        elif key == 276:  # Left arrow key
            self.pet_x -= 0.02
        elif key == 275:  # Right arrow key
            self.pet_x += 0.02

    def update_position(self, dt):
        self.pet_image.pos_hint = {'center_x': self.pet_x, 'center_y': self.pet_y}

    def update_statuses(self, food):
        update_result = update_current_pet(food)
        if update_result:
            # Update status bars
            self.status_labels['HUNGER'][0].text = f"HUNGER: {update_result['health']}"
            self.status_labels['HUNGER'][1].value = update_result['health']
            self.status_labels['ENERGY'][0].text = f"ENERGY: {update_result['energy']}"
            self.status_labels['ENERGY'][1].value = update_result['energy']
            self.status_labels['HAPPINESS'][0].text = f"HAPPINESS: {update_result['happiness']}"
            self.status_labels['HAPPINESS'][1].value = update_result['happiness']
            self.status_labels['HEALTH'][0].text = f"HEALTH: {update_result['growth']}"
            self.status_labels['HEALTH'][1].value = update_result['growth']

    def take_photo(self, instance):
        # 打开拍照界面
        camera_layout = BoxLayout(orientation='vertical')
        self.camera = Camera(play=True, resolution=(640, 480), size_hint=(1, 0.8))
        camera_layout.add_widget(self.camera)

        btn_layout = BoxLayout(size_hint=(1, 0.2))
        capture_button = Button(text='Capture', size_hint=(1, 1))
        capture_button.bind(on_press=self.capture)
        btn_layout.add_widget(capture_button)
        camera_layout.add_widget(btn_layout)

        self.popup = Popup(title='Take a Photo', content=camera_layout, size_hint=(1, 1))
        self.popup.open()

    def capture(self, instance):
        # 保存照片
        self.camera.export_to_png("captured_image.png")
        self.popup.dismiss()
        # 这里你可以实现上传照片的逻辑，例如上传到服务器或处理图像

    def jump(self, instance):
        # 播放跳跃音效
        if self.jump_sound:
            self.jump_sound.play()

        # Create an animation to simulate the jump
        jump_up = Animation(pos_hint={'center_y': self.pet_y + 0.2}, duration=0.2)
        jump_down = Animation(pos_hint={'center_y': self.pet_y}, duration=0.2)
        jump_sequence = jump_up + jump_down
        jump_sequence.start(self.pet_image)


class PetApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EntryScreen(name='entry'))
        sm.add_widget(MainScreen(name='maininterface'))
        return sm

if __name__ == "__main__":
    PetApp().run()
