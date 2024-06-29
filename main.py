# main.py

from petClass import Pet, create_pet, update_pet

current_pet = None

def initialize_pet(pet_name):
    global current_pet
    current_pet = create_pet(pet_name)
    return current_pet

def update_current_pet(food_name):
    if current_pet:
        return update_pet(current_pet, food_name)
    return None

if __name__ == "__main__":
    from mainInterface import PetApp
    PetApp().run()
