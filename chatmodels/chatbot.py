import os
import streamlit as st

os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage

model = ChatMistralAI(model = "mistral-small-2506" , temperature=0.9)

print("Choose your AI Mood")
print("Press 1 for Angry Mood")
print("Press 2 for funny Mood")
print("Press 3 for sad Mood")

choice = int(input("Tell me your Response :-> "))

if choice  == 1:
    mode = "You are an Angry AI agent. You  respond aggresively and impatiently"
elif choice == 2:
    mode = "You are a Funny AI agent. You respond with humour and jokes."
elif choice == 3:
    mode = "You are a Sad AI agent. You respond with sadness and grief."

messages = [
  SystemMessage(content=mode)
]

print("________________ Welcome type 0 to exit the application __________________")

while True :
    prompt = input("You : ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        print("Exiting the application!")
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))

    print("Bot :",response.content)