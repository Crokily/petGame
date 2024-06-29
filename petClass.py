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
            return "健康"
        elif 10 < self.health <= 30:
            return "生病"
        else:
            return "死亡"

    def get_happiness_status(self):
        if self.happiness > 30:
            return "开心"
        elif 10 < self.happiness <= 30:
            return "一般"
        else:
            return "不开心"

    def get_status_message(self):
        health_status = self.get_health_status()
        happiness_status = self.get_happiness_status()

        if health_status == "生病":
            return "你的宠物生病了，请注意吃更多的健康食物来帮助它恢复。"
        elif health_status == "死亡":
            return "很遗憾，你的宠物因为不健康的饮食习惯已经死亡。请重新开始并尝试更健康的饮食。"
        elif happiness_status == "开心":
            return "你的宠物非常开心，继续保持健康的饮食习惯！"
        else:
            return "你的宠物状态一般，请继续关注它的饮食。"
        
    def get_All(self):
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
    # 这里应该调用GPT API来识别食物并给出评分
    # 为了演示，我们用随机数模拟
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
