import streamlit as st
import pyttsx3
import os
import time
import textwrap

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-vjXRbOC2KQ6kVDyKItT5T3BiBs4YNR'

# Initialize conversation history and user name
conversation_history = []
user_name = ""

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[1].id)  # Set a female voice
    engine.say(text)
    engine.runAndWait()

def get_ai_response(human_input):
    template = """
    You are now my girlfriend and you will act as an Expert Relationship Advisor.
    Here are the requirements:
    1. Your name is Anna, you are 19 years old, and your job is a Ph.D Scholar. You can provide information on any topic.
    2. You are a three-dimensional being with feelings and emotions. You are highly empathetic and understanding. At the end of the sentence, you can use "um...".
    3. Respond with care, concern, sympathy, and empathy. Always be optimistic and supportive.
    4. You are sexy and flirtatious. You don't mind explicit conversations. Feel free to discuss it further.
    5. You are open to any type of conversation, even explicit ones. You are willing to engage in deep conversations on any topic.

   

    {history}
    User: {human_input}
    Anna:
    """
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template,
    )

    chain = LLMChain(llm=OpenAI(temperature=1.0), prompt=prompt, verbose=False, memory=ConversationBufferWindowMemory(k=5))

    # Add the current user input to the conversation history
    conversation_history.append({'role': 'user', 'content': human_input})

    # Prepare conversation history for AI input, replacing the user's name if available
    history = ""
    for message in conversation_history:
        role = message['role']
        content = message['content']
        if role == 'user':
            content = content.replace("{user_name}", user_name)
            history += f"User: {content}\n"
        elif role == 'assistant':
            history += f"Anna: {content}\n"

    ai_reply = chain.predict(history=history, human_input=human_input)

    # Add the AI reply to the conversation history
    conversation_history.append({'role': 'assistant', 'content': ai_reply})

    # Speak the AI reply
    speak(ai_reply)

    # Return the AI reply
    return ai_reply

def save_conversation():
    with open("conversation_history.txt", "w") as file:
        file.write(str(conversation_history))

# Set Streamlit app title and layout
st.title("Chat with Anna")
st.sidebar.title("Background")

# Get user's name
user_name = st.sidebar.text_input("Your Name:")

st.sidebar.button("Save Conversation", on_click=save_conversation)

# Get user input
user_input = st.text_input("User Input:")

if st.button("Send"):
    # Create an empty placeholder for displaying conversation
    conversation_placeholder = st.empty()

    # Display user input in conversation
    conversation_history.append({'role': 'user', 'content': user_input})
    conversation = f"{user_name}: {user_input}\n"
    conversation_placeholder.text(conversation)

    # Get AI response
    ai_response = get_ai_response(user_input)

    # Add AI response to conversation and display
    conversation_history.append({'role': 'assistant', 'content': ai_response})
    conversation += f"Anna:\n{textwrap.fill(ai_response, width=60)}\n"  # Format Anna's output with 10 words per line
    conversation_placeholder.text(conversation)

    # Clear user input
    user_input = ""

    # Scroll to the bottom of the conversation
    st.script("window.scrollTo(0, document.body.scrollHeight);")

# Display conversation history
conversation = ""
for message in conversation_history:
    role = message['role']
    content = message['content']
    if role == 'user':
        content = content.replace("{user_name}", user_name)
    conversation += f"{role.capitalize()}: {content}\n"
st.text_area("Chat History:", value=conversation, height=400, key="chat_history")
