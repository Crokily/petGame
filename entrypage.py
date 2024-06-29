from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.graphics import Color, RoundedRectangle, Triangle
from kivy.uix.screenmanager import ScreenManager, Screen
from petClass import Pet, create_pet, update_pet, get_pet_status

class EntryScreen(Screen):
    def __init__(self, **kwargs):
        super(EntryScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=(10, 10))
        self.question_label = Label(text="Enter food:", font_size=14)
        self.food_input = TextInput(multiline=False)
        self.food_input.bind(on_text_validate=self.on_enter_text_validate)
        layout.add_widget(self.question_label)
        layout.add_widget(self.food_input)
        self.add_widget(layout)

    def on_enter_text_validate(self, instance):
        food = self.food_input.text
        if food.lower() == 'exit':
            App.get_running_app().stop()
        else:
            self.manager.current = 'maininterface'

class MainInterface(Screen):
    def __init__(self, **kwargs):
        super(MainInterface, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        # Top bar with status bars
        status_layout = GridLayout(cols=4, size_hint=(1, 0.1), spacing=10, padding=[20, 10, 20, 10])
        
        # 创建进度条变量
        self.hunger_bar = ProgressBar(max=100, value=50)
        self.energy_bar = ProgressBar(max=100, value=50)
        self.happy_bar = ProgressBar(max=100, value=50)
        self.health_bar = ProgressBar(max=100, value=50)
        
        statuses = [
            ('HUNGER', self.hunger_bar),
            ('ENERGY', self.energy_bar),
            ('HAPPY', self.happy_bar),
            ('HEALTH', self.health_bar)
        ]
        
        for status, bar in statuses:
            status_layout.add_widget(Label(text=status, font_size=14, size_hint_x=None, width=80))
            status_layout.add_widget(bar)
        
        main_layout.add_widget(status_layout)

        # Center area with the pet image
        pet_layout = FloatLayout(size_hint=(1, 0.8))
        self.pet_image = Image(source='/mnt/data/image.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        pet_layout.add_widget(self.pet_image)
        main_layout.add_widget(pet_layout)

        # Initial position of the pet
        self.pet_x = 0.5
        self.pet_y = 0.5

        # Bottom bar with buttons
        button_layout = GridLayout(cols=2, size_hint=(1, 0.1), spacing=10, padding=[20, 10, 20, 10])
        
        take_photo_button = Button(text='Take Photos', font_size=14)
        take_photo_button.bind(on_press=self.take_photo)
        
        button_layout.add_widget(take_photo_button)
        button_layout.add_widget(Button(text='Exercise', font_size=14))
        
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

        # 创建一个新宠物
        self.pet = create_pet("Koala")

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

        # Schedule the update of pet's position and status
        Clock.schedule_interval(self.update_position, 1.0 / 60.0)  # Update 60 times per second
        Clock.schedule_interval(self.update_status, 1.0)  # Update status every second

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

    def update_status(self, dt):
        # 从后端获取最新的宠物状态
        status = get_pet_status(self.pet)
        
        # 更新进度条的值
        self.hunger_bar.value = status['health']
        self.energy_bar.value = status['energy']
        self.happy_bar.value = status['happiness']
        self.health_bar.value = status['growth']

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

class PetApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EntryScreen(name='entry'))
        sm.add_widget(MainInterface(name='maininterface'))
        return sm

if __name__ == "__main__":
    PetApp().run()
