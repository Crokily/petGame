import base64
import requests
import re
import json

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading or encoding image: {e}")
        return None

def make_request(image_path, text_content):
    api_key = ""
    base64_image = encode_image(image_path)
    if base64_image is None:
        raise ValueError("Failed to encode image.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_content},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 300,
        #"stop": ['}']
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        # 提取并返回响应中的content部分
        messages = response_data['choices'][0]['message']['content'] if 'choices' in response_data and len(response_data['choices']) > 0 else None
        return messages
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_food_information(text):
    # 使用正则表达式匹配foodname和score
    pattern = r'"foodname":\s*"([^"]+)",\s*"score":\s*(\d+)'
    matches = re.finditer(pattern, text, re.MULTILINE)

    results = []
    for match in matches:
        # 将匹配的字符串转换为JSON对象
        try:
            food_info = {
                "foodname": match.group(1),
                "score": int(match.group(2))
            }
            results.append(food_info)
        except ValueError:
            continue  # 如果转换失败，跳过这个匹配

    if results:
        return json.dumps(results, indent=4)  # 返回格式化的JSON字符串
    else:
        return None  # 如果没有匹配项，返回None

# Example usage:
image_path = "morethanone.jpg"
text_content = """
        You need to identify the food items in an image and evaluate their healthiness based on a food scoring algorithm/
        You'll score each food item uploaded without providing specific data, instead using standard nutritional information of similar dishes for calculations/
        If an image contains multiple food items, you need to score each one individually/
        score is the calculated number/
        score ranges from 0 to 100/
        Output structured JSON object, conforming to the following TypeScript：
        FoodInformation {
        foodname: string;
        score: number
        }



                Here's the content of the food scoring algorithm:
                Scoring Standards
                1. Calories (kcal) - Lower calorie content is usually considered healthier.
                2. Fat (grams) - Foods with lower fat content are generally healthier, especially those with low saturated and trans fats.
                3. Fiber (grams) - High-fiber foods are usually healthier.
                4. Sugar (grams) - Foods with low sugar content are usually healthier.
                5. Protein (grams) - Protein is essential for a healthy diet.
                6. Sodium (mg) - Foods with low sodium content are usually healthier.

                Scoring Algorithm
                We can assign a weight to each indicator based on its importance to health. Then, normalize the values of each indicator to fairly compare different foods.
                Pseudocode for the Algorithm:
                1. Normalize each indicator for each food:
                - For calories, fat, sugar, and sodium: `Standard score = 100 - (value / max value × 100)`
                - For fiber and protein: `Standard score = (value / max value × 100)`
                2. Calculate the total score:
                - `Total score = (Calories standard score × 0.15) + (Fat standard score × 0.25) + (Fiber standard score × 0.20) + (Sugar standard score × 0.20) + (Protein standard score × 0.10) + (Sodium standard score × 0.10)`
          """

text = make_request(image_path, text_content)
result=extract_food_information(text)
print(result)
