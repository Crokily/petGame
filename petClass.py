import random
from datetime import datetime, timedelta

class Pet:
    def __init__(self, name):
        self.name = name
        self.health = 50
        self.energy = 50
        self.happiness = 50
        self.growth = 10
        self.food_uploads = 0
        self.last_upload_date = None

    def update_attributes(self, score):
        if 8 <= score <= 10:
            self.health += 10
            self.energy += 10
            self.happiness += 10
            self.growth += 3
        elif 5 <= score < 8:
            self.health += 5
            self.energy += 5
            self.happiness += 5
            self.growth += 2
        elif 3 <= score < 5:
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

    def get_health_status(self):
        if self.health > 30:
            return "Healthy"
        elif 10 < self.health <= 30:
            return "Sick"
        else:
            return "Dead"

    def get_happiness_status(self):
        if self.happiness > 30:
            return "Happy"
        elif 10 < self.happiness <= 30:
            return "Neutral"
        else:
            return "Unhappy"

    def get_status_message(self):
        health_status = self.get_health_status()
        happiness_status = self.get_happiness_status()

        if health_status == "Sick":
            return "Your pet is sick, please provide more healthy food to help it recover."
        elif health_status == "Dead":
            return "Unfortunately, your pet has died due to unhealthy eating habits. Please start over and try healthier options."
        elif happiness_status == "Happy":
            return "Your pet is very happy, keep up the good diet!"
        else:
            return "Your pet is in a neutral state, please continue to monitor its diet."
        
    def get_all(self):
        return {
            "name": self.name,
            "health": self.health,
            "energy": self.energy,
            "happiness": self.happiness,
            "growth": self.growth,
            "health_status": self.get_health_status(),
            "happiness_status": self.get_happiness_status(),
            "status_message": self.get_status_message(),
            "food_score": 0,
            "combined_score": 0
        }

def create_pet(name):
    return Pet(name)

def calculate_food_score(food_name):
    # Placeholder for GPT API call to identify food and give a score
    return random.uniform(0, 10)

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

def update_pet(pet, food_name):
    food_score = calculate_food_score(food_name)
    frequency_score = calculate_upload_frequency_score(pet)
    combined_score = 0.7 * food_score + 0.3 * frequency_score
    pet.update_attributes(combined_score)
    return {
        "name": pet.name,
        "health": pet.health,
        "energy": pet.energy,
        "happiness": pet.happiness,
        "growth": pet.growth,
        "health_status": pet.get_health_status(),
        "happiness_status": pet.get_happiness_status(),
        "status_message": pet.get_status_message(),
        "food_score": food_score,
        "combined_score": combined_score
    }

def get_pet_status(pet):
    return pet.get_all()
