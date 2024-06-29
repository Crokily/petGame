# Main.py

from petClass import Pet, create_pet, update_pet, pet_mood_interaction, process_mood_response, save_pet, load_pet


def main():
    # 尝试加载现有的宠物数据
    pet = load_pet()
    
    if pet is None:
        # 如果没有现有数据，创建新宠物
        pet_name = input("请为您的宠物起一个名字：")
        pet = create_pet(pet_name)
        print(f"欢迎您的新宠物 {pet.name}!")
    else:
        print(f"欢迎回来！{pet.name} 很想你哦！")

    while True:
        # 检查是否应该开始心情互动
        interaction_result = pet_mood_interaction(pet)
        if interaction_result["interaction_started"]:
            print(interaction_result["question"])
            user_mood = input("请选择你的心情 (好/正常/坏): ")
            response = process_mood_response(pet, user_mood)
            print(response["pet_response"])

        # 模拟用户输入食物
        food = input("请输入您给宠物的食物（输入'退出'结束，输入'保存'保存当前状态）：")
        if food.lower() == '退出':
            # 在退出前保存宠物状态
            save_pet(pet)
            print("已保存宠物状态。再见！")
            break
        elif food.lower() == '保存':
            save_pet(pet)
            print("已保存宠物状态。")
            continue

        # 更新宠物状态
        update_result = update_pet(pet, food)

        # 打印更新后的状态
        print(f"\n{pet.name} 的最新状态：")
        print(f"健康值：{update_result['health']}")
        print(f"体力：{update_result['energy']}")
        print(f"快乐度：{update_result['happiness']}")
        print(f"成长值：{update_result['growth']}")
        print(f"健康状态：{update_result['health_status']}")
        print(f"心情状态：{update_result['happiness_status']}")
        print(f"状态消息：{update_result['status_message']}")
        print(f"食物评分：{update_result['food_score']:.2f}")
        print(f"综合评分：{update_result['combined_score']:.2f}\n")

if __name__ == "__main__":
    main()