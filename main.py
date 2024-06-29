# Main.py

from petClass import Pet, create_pet, update_pet

def main():
    # 创建一个新宠物
    pet_name = input("请为您的宠物起一个名字：")
    pet = create_pet(pet_name)
    print(f"欢迎您的新宠物 {pet.name}!")

    while True:
        # 模拟用户输入食物
        food = input("请输入您给宠物的食物（输入'退出'结束）：")
        if food.lower() == '退出':
            break

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