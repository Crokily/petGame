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

class PetApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        # Top bar with status bars
        status_layout = GridLayout(cols=4, size_hint=(1, 0.1))
        statuses = ['HUNGER', 'ENERGY', 'HAPPY', 'HEALTH']
        for status in statuses:
            status_layout.add_widget(Label(text=status, font_size=14))
            status_layout.add_widget(ProgressBar(max=100, value=10))  # Example with a filled bar at 50%
        main_layout.add_widget(status_layout)

        # Center area with the pet image
        pet_layout = FloatLayout(size_hint=(1, 0.8))
        self.pet_image = Image(source='/Users/yangtiechui/Downloads/kaola.png', size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        pet_layout.add_widget(self.pet_image)
        main_layout.add_widget(pet_layout)

        # Initial position of the pet
        self.pet_x = 0.5
        self.pet_y = 0.5

        # Bottom bar with buttons
        button_layout = GridLayout(cols=2, size_hint=(1, 0.1))
        buttons = ['Take Photos', 'Exercise']
        for button in buttons:
            button_layout.add_widget(Button(text=button, font_size=14))
        main_layout.add_widget(button_layout)

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

        # Schedule the update of pet's position
        Clock.schedule_interval(self.update_position, 1.0 / 60.0)  # Update 60 times per second

        return main_layout

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

if __name__ == "__main__":
    PetApp().run()
