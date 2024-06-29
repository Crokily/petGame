from openai import OpenAI

api_key = ''

client = OpenAI(api_key=api_key)

user_emotion = input("Please enter your emotion (happy, normal, sad): ")#把这块改成接口

if user_emotion == "happy":
    messages = [
        {"role": "system", "contenhat": "I'm very happy now."},
        {"role": "system", "content": "The sun is shining bright today!"},
        {"role": "system", "content": "Let's make the most of this wonderful day!"}
    ]
elif user_emotion == "sad":
    messages = [
        {"role": "system", "content": "I'm very sad now."},
        {"role": "user", "content": "It's been a tough day."},
        {"role": "assistant", "content": "I'm here to help. What can I do to make your day better?"}
    ]
elif user_emotion == "normal":
    messages = [
        {"role": "system", "content": "I feel normal today."},
        {"role": "user", "content": "Just another regular day."},
        {"role": "assistant", "content": "Let's make the best out of this day!"}
    ]
else:
    messages = [
        {"role": "system", "content": "Your feelings are important."},
        {"role": "user", "content": "I'm not sure how I feel."},
        {"role": "assistant", "content": "Take your time. I'm here whenever you need to talk."}
    ]

response = client.chat.completions.create(
  model="gpt-4o",
  messages= messages,
  max_tokens=300,
  stop=["."]  
)
print(response.choices[0].message.content)

