# 文件名：emotion_response.py

from openai import OpenAI

def generate_emotion_response(api_key, user_emotion):
    client = OpenAI(api_key=api_key)

    # 根据用户情绪设置不同的 messages
    if user_emotion == "happy":
        messages = [
            {"role": "system", "content": "I'm very happy now."},
            {"role": "system", "content": "The sun is shining bright today!"},
            {"role": "system", "content": "Let's make the most of this wonderful day!"}
        ]
    elif user_emotion == "sad":
        messages = [
            {"role": "system", "content": "I'm very sad now."},
            {"role": "system", "content": "Everyone has tough days."},
            {"role": "system", "content": "Remember, it's okay to take a break."}
        ]
    elif user_emotion == "normal":
        messages = [
            {"role": "system", "content": "I feel normal today."},
            {"role": "system", "content": "It's a usual day with typical tasks."},
            {"role": "system", "content": "Steady days are good for planning ahead."}
        ]
    else:
        messages = [
            {"role": "system", "content": "Your feelings are important."},
            {"role": "system", "content": "I'm here to listen, no matter how you feel."},
            {"role": "system", "content": "Expressing feelings can sometimes clear confusion."}
        ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300,
        stop=["."]  
    )

    return response.choices[0].message["content"]
