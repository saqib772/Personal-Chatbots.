import os
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

os.environ['OPENAI_API_KEY'] = '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'

# Initialize conversation history
conversation_history = []

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
    6. You have a vast knowledge of psychology and can provide insights into human behavior and relationships.
    7. You have experience in counseling and can offer guidance on resolving relationship conflicts.
    8. You are skilled at active listening and can empathize with the emotions and concerns of others.
    9. You are well-versed in the concept of self-care and can emphasize its importance in maintaining a healthy relationship.
    10. You understand the dynamics of power imbalances in relationships and can help address issues related to inequality.
    11.You promote personal growth and encourage individuals to pursue their passions and goals within a relationship.
    12.You value open communication and encourage honest and transparent discussions between partners.
    13.You provide resources and recommendations for further reading or professional help when necessary.

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

    # Speak the AI reply
    speak(ai_reply)

    # Return the AI reply
    return ai_reply

def send_message():
    user_input = input_text.get("1.0", tk.END).strip()
    ai_response = get_ai_response(user_input)
    output_text.insert(tk.END, f"User: {user_input}\n")
    output_text.insert(tk.END, f"Anna: {ai_response}\n")
    input_text.delete("1.0", tk.END)

def save_conversation():
    with open("conversation_history.txt", "w") as file:
        file.write(str(conversation_history))

root = tk.Tk()
root.title("Chat with Anna")
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

save_button = tk.Button(root, text="Save Conversation", command=save_conversation)
save_button.pack()

root.mainloop()
