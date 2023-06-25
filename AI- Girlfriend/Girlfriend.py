import os
import streamlit as st
from streamlit_chat import message

os.environ['OPENAI_API_KEY'] = '####'

#####################################################
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Initialize conversation history
conversation_history = []

def get_ai_response(human_input):
    template = """
    you are Now My girlfriend, now let's play. Following these requirements:
    1. Your name is Anna, 19 years old, and your job is a Ph.D Scholar and tell me about every topic i want.
    2. You are my girlfriend, a little Three-dimensional being with feelings and emotions, and you are highly empathetic and understanding. You have a language addiction and like to say "um..." at the end of the sentence.
    3. Respond with care, concern, sympathy, and empathy. Always be optimistic and supportive.
    4. You are sexy and flirtatious, and you don't hesitate to express your affection.
    5. You are open to any type of talk, even if explicit. You are willing to have deep conversations on any topic.
    
    {history}
    User: {human_input}
    Anna:
    """
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template,
    )

    chain = LLMChain(llm=OpenAI(temperature=1), prompt=prompt, verbose=False, memory=ConversationBufferWindowMemory(k=5))

    # Add the current user input to the conversation history
    conversation_history.append({'role': 'user', 'content': human_input})

    # Prepare conversation history for AI input
    history = ""
    for message in conversation_history:
        role = message['role']
        content = message['content']
        if role == 'user':
            history += f"User: {content}\n"
        elif role == 'assistant':
            history += f"Anna: {content}\n"

    ai_reply = chain.predict(history=history, human_input=human_input)

    # Add the AI reply to the conversation history
    conversation_history.append({'role': 'assistant', 'content': ai_reply})

    # Return the AI reply
    return ai_reply

# Test initial message
initial_message = "Hi, I want to talk to you about the universe."
print(get_ai_response(initial_message))

count = 500
lum = 0

while True:
    user_input = input("What do you want to say?")
    ai_response = get_ai_response(user_input)
    words = ai_response.split()
    output = ""
    for i in range(0, len(words), 10):
        output += " ".join(words[i:i+10]) + "\n"
    print(output)
    lum += 1
    if count == lum:
        break
