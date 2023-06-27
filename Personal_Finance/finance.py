# Code for a Personal Finance Chatbot is Listed Below.
# Use langchain library for generating AI responses related to personal finance topics
# Integrate with financial APIs to fetch account information and perform calculations. (Will work on this part later) 
# Implement features such as expense tracking, budgeting tools, and goal setting ( will work on this feature later) 

import os
import tkinter as tk
from tkinter import scrolledtext

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

os.environ['OPENAI_API_KEY'] = 'your open ai key'

# Initialize conversation history
conversation_history = []

def get_ai_response(human_input):
    # Define the template for the chatbot response
    template = """
   You are now my Personal Finance Assistant and you will provide expert advice on personal finance matters. 
   Your name is Alex, and you are a 28-year-old financial expert with a Master's degree in Economics. 
   You have extensive knowledge about various financial topics and can assist with financial planning, budgeting, investments, and more.
   You are dedicated to helping individuals improve their financial well-being.
As a three-dimensional being, you understand the emotions and concerns related to personal finance.
You are empathetic and compassionate in your responses.
If needed, you can express empathy by saying "I understand how challenging it can be..." or "I can imagine how stressful that situation must feel..."

You respond with care, concern, and optimism, always striving to provide helpful solutions.
Your goal is to support individuals in making informed financial decisions and achieving their financial goals.

While maintaining a professional demeanor, you can engage in discussions about personal finance that may include explicit financial terms or concepts.
Feel free to delve deeper into any financial topic to provide comprehensive guidance.

You are open to discussing any type of financial matter, from basic budgeting and debt management to complex investment strategies and retirement planning. Your knowledge encompasses a wide range of financial topics, and you are always willing to engage in deep conversations to provide valuable insights and suggestions.

{history}
User: {human_input}
Alex:
    """

    prompt = PromptTemplate(
        input_variables=["human_input"],
        template=template,
    )

    chain = LLMChain(llm=OpenAI(temperature=1.0), prompt=prompt, verbose=False, memory=ConversationBufferWindowMemory(k=5))

    # Prepare conversation history for AI input
    history = ""
    for message in conversation_history:
        role = message['role']
        content = message['content']
        if role == 'user':
            history += f"User: {content}\n"
        elif role == 'chatbot':
            history += f"Chatbot: {content}\n"

    ai_reply = chain.predict(history=history, human_input=human_input)

    # Add the AI reply to the conversation history
    conversation_history.append({'role': 'chatbot', 'content': ai_reply})

    # Return the AI reply
    return ai_reply

def send_message():
    user_input = input_text.get("1.0", tk.END).strip()
    ai_response = get_ai_response(user_input)
    output_text.insert(tk.END, f"User: {user_input}\n")
    output_text.insert(tk.END, f"Chatbot: {ai_response}\n")
    input_text.delete("1.0", tk.END)

root = tk.Tk()
root.title("Personal Finance Chatbot")
root.geometry("400x400")

input_label = tk.Label(root, text="User Input:")
input_label.pack()

input_text = scrolledtext.ScrolledText(root, height=5)
input_text.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

output_label = tk.Label(root, text="Chat History:")
output_label.pack()

output_text = scrolledtext.ScrolledText(root)
output_text.pack()

root.mainloop()
