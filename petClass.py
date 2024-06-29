import random
from datetime import datetime, timedelta
import time
import json
import os

class Pet:
    def __init__(self, name):
        self.name = name
        self.health = 50
        self.energy = 50
        self.happiness = 50
        self.growth = 10
        self.food_uploads = 0
        self.last_upload_date = None
        self.last_interaction_time = 0

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
    
    def initiate_mood_interaction(self):
        """开始心情互动"""
        current_time = time.time()
        if not hasattr(self, 'last_interaction_time') or current_time - self.last_interaction_time > 300:  # 5分钟间隔
            self.last_interaction_time = current_time
            return True
        return False

    def ask_mood(self):
        """询问主人的心情"""
        return "小主人，今天心情如何呀？\n😊 - 好\n😐 - 正常\n😢 - 坏"

    def respond_to_mood(self, mood):
        """根据主人的心情做出回应"""
        if mood == "好":
            return self.generate_response("positive")
        elif mood == "正常":
            return self.generate_response("neutral")
        elif mood == "坏":
            return self.generate_response("negative")
        else:
            return "对不起，我不太明白。能再说一次吗？"

    def generate_response(self, mood_type):
        """生成回应（这里用固定的回复代替API调用）"""
        responses = {
            "positive": [
                f"太好了！{self.name}也为你感到高兴呢！",
                f"听到你心情不错，{self.name}也开心起来了！",
                "阳光灿烂的心情最适合你了！"
            ],
            "neutral": [
                f"{self.name}陪着你，希望能让你的心情变得更好！",
                "平静的心情也不错，要不要和我玩个游戏？",
                "普普通通的一天，也有它的美好之处哦！"
            ],
            "negative": [
                f"{self.name}在这里陪着你，别难过了好吗？",
                "每个人都会有不开心的时候，让我们一起度过这个难关吧！",
                "不开心的时候吃点好吃的怎么样？我可以推荐一些健康食品哦！"
            ]
        }
        return random.choice(responses[mood_type])

    def to_dict(self):
        """将宠物对象转换为字典"""
        return {
            "name": self.name,
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
        """从字典创建宠物对象"""
        pet = cls(data["name"])
        pet.health = data["health"]
        pet.energy = data["energy"]
        pet.happiness = data["happiness"]
        pet.growth = data["growth"]
        pet.food_uploads = data["food_uploads"]
        pet.last_upload_date = datetime.fromisoformat(data["last_upload_date"]) if data["last_upload_date"] else None
        pet.last_interaction_time = data["last_interaction_time"]
        return pet

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

def get_pet_status(pet):
    return pet.get_All()

def pet_mood_interaction(pet):
    """处理宠物心情互动的功能"""
    if pet.initiate_mood_interaction():
        question = pet.ask_mood()
        return {
            "interaction_started": True,
            "question": question
        }
    return {"interaction_started": False}

def process_mood_response(pet, mood):
    """处理用户对心情问题的回答"""
    response = pet.respond_to_mood(mood)
    return {
        "pet_response": response
    }

def save_pet(pet, filename="pet_data.json"):
    """保存宠物数据到JSON文件"""
    with open(filename, "w") as f:
        json.dump(pet.to_dict(), f)

def load_pet(filename="pet_data.json"):
    """从JSON文件加载宠物数据"""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return Pet.from_dict(data)
    return None