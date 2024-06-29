from kivy.uix.popup import Popup
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
from kivy.uix.camera import Camera
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.graphics.transformation import Matrix
from kivy.uix.scatter import Scatter
from kivy.core.text import LabelBase

import shutil

from petClass import create_pet, update_pet, save_pet, load_pet, get_pet_status
from gpt.gptemotion import generate_emotion_response

class PetApp(App):
    def init_pet(self):
        # Try to load existing pet data
        self.pet = load_pet()
        print(self.pet)

    def build(self):
        LabelBase.register(name="seguiemj", 
                           fn_regular="font\seguiemj.ttf")
        main_layout = BoxLayout(orientation='vertical')

        # Top bar with status bars
        status_layout = GridLayout(cols=4, size_hint=(1, 0.1), spacing=10, padding=[20, 10, 20, 10])
        
        # Create progress bars for different statuses
        self.hunger_bar = ProgressBar(max=100, value=50)
        self.hunger_label = Label(text="50", size_hint_x=None, width=40)
        
        self.energy_bar = ProgressBar(max=100, value=50)
        self.energy_label = Label(text="50", size_hint_x=None, width=40)
        
        self.happy_bar = ProgressBar(max=100, value=50)
        self.happy_label = Label(text="50", size_hint_x=None, width=40)
        
        self.health_bar = ProgressBar(max=100, value=50)
        self.health_label = Label(text="50", size_hint_x=None, width=40)
        
        statuses = [
            ('HEALTH', self.hunger_bar, self.hunger_label),
            ('ENERGY', self.energy_bar, self.energy_label),
            ('HAPPY', self.happy_bar, self.happy_label),
            ('GROWTH', self.health_bar, self.health_label)
        ]
        
        for status, bar, label in statuses:
            box = BoxLayout(orientation='horizontal', spacing=10)
            box.add_widget(Label(text=status, font_size=14, size_hint_x=None, width=80))
            box.add_widget(bar)
            box.add_widget(label)
            status_layout.add_widget(box)
        
        main_layout.add_widget(status_layout)

        # Label for pet name
        self.pet_name_label = Label(text="Pet's name: ", font_size=18, size_hint=(1, 0.1))
        main_layout.add_widget(self.pet_name_label)

        # Center area with the pet image and background image
        pet_layout = FloatLayout(size_hint=(1, 0.6))

        # Add background image
        self.background_image = Image(source='assests\\background.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        pet_layout.add_widget(self.background_image, index=0)  # Add background image at the bottom

        self.pet_image = Image(source='kaola.png', size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        pet_layout.add_widget(self.pet_image)
        main_layout.add_widget(pet_layout)

        # Initial position of the pet
        self.pet_x = 0.5
        self.pet_y = 0.5

        # Bottom bar with buttons
        button_layout = GridLayout(cols=3, size_hint=(1, 0.1), spacing=10, padding=[20, 10, 20, 10])
        
        self.take_photo_button = Button(text='Take Photos', font_size=14)
        self.take_photo_button.bind(on_press=self.open_take_photo_popup)
        
        self.upload_photo_button = Button(text='Upload Photos', font_size=14)
        self.upload_photo_button.bind(on_press=self.open_upload_photo_popup)
        
        self.exercise_button = Button(text='Mood', font_size=14)
        self.exercise_button.bind(on_press=self.show_exercise_buttons)

        button_layout.add_widget(self.take_photo_button)
        button_layout.add_widget(self.upload_photo_button)
        button_layout.add_widget(self.exercise_button)
        
        main_layout.add_widget(button_layout)

        # Initialize pet
        self.pet = None

        self.exercise_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=100, padding=[20, 10, 20, 10])
        self.button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)

        self.happy_button = Button(text="😃", size_hint=(1, None), height=40, font_name="seguiemj")
        self.good_button = Button(text="🙂", size_hint=(1, None), height=40, font_name="seguiemj")
        self.bad_button = Button(text="😞", size_hint=(1, None), height=40, font_name="seguiemj")

        self.happy_button.bind(on_press=lambda instance: self.submit_exercise("happy"))
        self.good_button.bind(on_press=lambda instance: self.submit_exercise("normal"))
        self.bad_button.bind(on_press=lambda instance: self.submit_exercise("sad"))

        self.button_layout.add_widget(self.happy_button)
        self.button_layout.add_widget(self.good_button)
        self.button_layout.add_widget(self.bad_button)

        self.mood_label = Label(text="How are you feeling now?", size_hint=(1, None), height=40, font_size=18, halign='center', valign='middle')

        self.exercise_layout.add_widget(self.button_layout)
        self.exercise_layout.add_widget(self.mood_label)

        # hide the layout
        self.exercise_layout.opacity = 0

        main_layout.add_widget(self.exercise_layout)

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

        # Initialize pet
        self.init_pet()
        print(self.pet)
        if self.pet is None:
            Clock.schedule_once(self.show_pet_selection_popup, 0.5)

        # Schedule the update of pet's position and status
        Clock.schedule_interval(self.update_position, 1.0 / 60.0)  # Update 60 times per second
        Clock.schedule_interval(self.update_status, 1.0)  # Update status every second
        # Clock.schedule_interval(self.random_move_pet, 1.0)  # Random move pet every second

        return main_layout

    def show_pet_selection_popup(self, dt):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text="Select a pet")
        pet_selection_layout = GridLayout(cols=4, spacing=10)

        # Add pet selection buttons
        pet_images = ['pet/kaola.png', 'pet/tuotuo.png', 'pet/whitecat.png', 'pet/kapibala.png']
        for pet_image in pet_images:
            btn = Button(background_normal=pet_image, size_hint=(None, None), size=(100, 100))
            btn.bind(on_press=lambda instance, img=pet_image: self.select_pet(img))
            pet_selection_layout.add_widget(btn)
        
        layout.add_widget(label)
        layout.add_widget(pet_selection_layout)

        self.popup = Popup(title="Select a pet", content=layout, size_hint=(0.8, 0.8), auto_dismiss=False)
        self.popup.open()

    def select_pet(self, pet_image):
        self.selected_pet_image = pet_image
        self.show_name_input_popup()

    def show_name_input_popup(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text="Enter your pet's name:")
        self.name_input = TextInput(multiline=False)
        submit_button = Button(text="Confirm")
        submit_button.bind(on_press=self.set_pet_name)

        layout.add_widget(label)
        layout.add_widget(self.name_input)
        layout.add_widget(submit_button)

        self.popup.dismiss()
        self.popup = Popup(title="Pet's name", content=layout, size_hint=(0.8, 0.4), auto_dismiss=False)
        self.popup.open()

    def set_pet_name(self, instance):
        pet_name = self.name_input.text.strip()
        if pet_name:
            self.pet = create_pet(pet_name,img=self.selected_pet_image)
            self.pet_name_label.text = f"Pet's name: {pet_name}"
            self.pet_image.source = self.selected_pet_image
            self.popup.dismiss()
        else:
            print("Please enter a valid name")
            pass

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
        if self.pet:
            # Get the latest status of the pet from the backend
            status = get_pet_status(self.pet)
            
            # Update the value of progress bars and text of labels
            self.hunger_bar.value = status['health']
            self.hunger_label.text = str(status['health'])
            
            self.energy_bar.value = status['energy']
            self.energy_label.text = str(status['energy'])
            
            self.happy_bar.value = status['happiness']
            self.happy_label.text = str(status['happiness'])
            
            self.health_bar.value = status['growth']
            self.health_label.text = str(status['growth'])

            self.pet_name_label.text = f"Pet's name: {self.pet.name}"
            self.pet_image.source = self.pet.img

            if self.pet.health < 10:
                self.handle_pet_death()

    def open_take_photo_popup(self, instance):
        # Open the camera view
        camera_layout = BoxLayout(orientation='vertical')
        self.camera = Camera(play=True, resolution=(640, 480), size_hint=(1, 0.8))
        camera_layout.add_widget(self.camera)
        
        self.camera_transform = Matrix().rotate(3.14159, 0, 0, 1)  # Rotate the camera view by 180 degrees
        
        btn_layout = BoxLayout(size_hint=(1, 0.2))
        capture_button = Button(text='Capture', size_hint=(1, 1))
        capture_button.bind(on_press=self.capture_photo)
        btn_layout.add_widget(capture_button)
        camera_layout.add_widget(btn_layout)

        self.popup = Popup(title='Take a Photo', content=camera_layout, size_hint=(1, 1))
        self.popup.open()

    def capture_photo(self, instance):
        # Save the captured image
        self.camera.export_to_png("captured_image.png")
        update_pet(self.pet, "captured_image.png")
        self.popup.dismiss()

    def open_upload_photo_popup(self, instance):
        filechooser_layout = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserIconView(size_hint=(1, 0.8))
        filechooser_layout.add_widget(self.filechooser)
        
        btn_layout = BoxLayout(size_hint=(1, 0.2))
        select_button = Button(text='Select', size_hint=(1, 1))
        select_button.bind(on_press=self.upload_photo)
        btn_layout.add_widget(select_button)
        filechooser_layout.add_widget(btn_layout)

        self.popup = Popup(title='Upload a Photo', content=filechooser_layout, size_hint=(1, 1))
        self.popup.open()

    def upload_photo(self, instance):
        selected = self.filechooser.selection
        if selected:
            shutil.copy(selected[0], "uploaded_image.png")
            update_pet(self.pet, "uploaded_image.png")
            self.popup.dismiss()

    def show_exercise_buttons(self, instance):
        self.exercise_layout.opacity = 1

    def submit_exercise(self, mood):
        print(f"Selected mood: {mood}")
        response = generate_emotion_response(mood)
        self.mood_label.text = response
        Clock.schedule_once(self.hide_exercise_buttons, 10)

    def hide_exercise_buttons(self, dt):
        self.exercise_layout.opacity = 0

    def handle_pet_death(self):
        # Hide the buttons
        self.take_photo_button.opacity = 0
        self.upload_photo_button.opacity = 0
        self.exercise_button.opacity = 0

        # Disable the buttons to prevent any interactions
        self.take_photo_button.disabled = True
        self.upload_photo_button.disabled = True
        self.exercise_button.disabled = True

        # You can also add a message or change the pet image to indicate death
        self.pet_name_label.text = f"{self.pet.name} has passed away..."
        self.pet.img = 'assests\\tomb.png'
        self.pet_image.source = self.pet.img

        # Optionally, you can show a popup to inform the user
        popup = Popup(title='Game Over',
                      content=Label(text=f"{self.pet.name} has passed away..."),
                      size_hint=(0.6, 0.4))
        popup.open()


    def on_stop(self):
        # This method is called when the application is closing
        if self.pet:
            save_pet(self.pet)
            print(f"Pet data saved for {self.pet.name}")

if __name__ == "__main__":
    PetApp().run()
