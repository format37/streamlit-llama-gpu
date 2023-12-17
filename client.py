# -*- coding: utf-8 -*-
import requests
import json

API_URL = "http://localhost:8501" 

def chat(text):
    data = {'text': text}
    response = requests.post(f"{API_URL}/chat", json=data)
    content = json.loads(response.content)
    return content["response"]

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        bot_response = chat(user_input)
        print(f"\nBot: {bot_response}")

if __name__ == '__main__':
    main()
