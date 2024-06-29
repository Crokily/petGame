from datetime import datetime
import json
import os

from gpt.gpt import get_food_scores

class Pet:
    def __init__(self, name,img):
        self.name = name
        self.img = img
        self.health = 50
        self.energy = 50
        self.happiness = 50
        self.growth = 10
        self.food_uploads = 0
        self.last_upload_date = None
        self.last_interaction_time = 0

    def update_attributes(self, score):
        if 80 <= score <= 100:
            self.health += 10
            self.energy += 10
            self.happiness += 10
            self.growth += 3
        elif 50 <= score < 80:
            self.health += 5
            self.energy += 5
            self.happiness += 5
            self.growth += 2
        elif 30 <= score < 50:
            self.health += 3
            self.energy += 3
            self.happiness += 3
            self.growth += 1
        else:
            self.health -= 5
            self.energy -= 5
            self.happiness -= 5
            self.growth -= 1

        self.health = max(0, min(100, self.health))
        self.energy = max(0, min(100, self.energy))
        self.happiness = max(0, min(100, self.happiness))
        self.growth = max(0, min(100, self.growth))
        
    def get_All(self):
        return {
            "name": self.name,
            "img": self.img,
            "health": self.health,
            "energy": self.energy,
            "happiness": self.happiness,
            "growth": self.growth,
            "food_score": 0,
            "combined_score": 0
        }

    def to_dict(self):
        # save the pet data to a dictionary
        return {
            "name": self.name,
            "img": self.img,
            "health": self.health,
            "energy": self.energy,
            "happiness": self.happiness,
            "growth": self.growth,
            "food_uploads": self.food_uploads,
            "last_upload_date": self.last_upload_date.isoformat() if self.last_upload_date else None,
            "last_interaction_time": self.last_interaction_time
        }
    
    @classmethod
    def from_dict(cls, data):
        # Create a pet object from a dictionary
        pet = cls(data["name"],data["img"])
        pet.health = data["health"]
        pet.energy = data["energy"]
        pet.happiness = data["happiness"]
        pet.growth = data["growth"]
        pet.food_uploads = data["food_uploads"]
        pet.last_upload_date = datetime.fromisoformat(data["last_upload_date"]) if data["last_upload_date"] else None
        pet.last_interaction_time = data["last_interaction_time"]
        return pet

def create_pet(name,img):
    return Pet(name,img)

def calculate_food_score(food_img):
    result = get_food_scores(food_img)
    return result

def calculate_upload_frequency_score(pet):
    today = datetime.now().date()
    if pet.last_upload_date is None or pet.last_upload_date != today:
        pet.food_uploads = 1
        pet.last_upload_date = today
    else:
        pet.food_uploads += 1

    if pet.food_uploads > 3:
        return 5
    elif 2 <= pet.food_uploads <= 3:
        return 3
    elif pet.food_uploads == 1:
        return 1
    else:
        return 0

def update_pet(pet, food_img):
    food_score = calculate_food_score(food_img)
    print(f"Food score:{food_score:.2f}")
    frequency_score = calculate_upload_frequency_score(pet)
    combined_score = 0.7 * food_score + 0.3 * frequency_score
    print(f"Combined_score:{combined_score:.2f}")
    pet.update_attributes(combined_score)
    return {
        "name": pet.name,
        "img": pet.img,
        "health": pet.health,
        "energy": pet.energy,
        "happiness": pet.happiness,
        "growth": pet.growth,
        "food_score": food_score,
        "combined_score": combined_score
    }

def get_pet_status(pet):
    return pet.get_All()

def save_pet(pet, filename="pet_data.json"):
    # save the pet data to a JSON file
    with open(filename, "w") as f:
        json.dump(pet.to_dict(), f)

def load_pet(filename="pet_data.json"):
    # load the pet data from a JSON file
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return Pet.from_dict(data)
    return None