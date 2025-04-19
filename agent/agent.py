import openai
from prompt import NO_VALUE_PROMPT
import os
from dotenv import load_dotenv
from search_vdb import search

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "chroma"
openai.api_key = OPENAI_API_KEY      
class Agent:
  def __init__(self):
     self.sys_msg = NO_VALUE_PROMPT
     self.history = []
     self.history.append({
       "role":"system",
       "content":self.sys_msg
       })
  
  def respond(self, message):

    context = search(message, CHROMA_PATH)
    if context:
      message = f"this is the customer's message, respond in it's language and ignore the context language:{message}\n\n[context: {context}]"
      self.history.append({"role":"user", "content":message})
    else:
      self.history.append({
      "role":"user",
      "content":message
    })
    completion = openai.chat.completions.create(
    model="gpt-4o",
    messages=self.history)
    response_message = completion.choices[0].message.content
    # ✅ Append assistant response once
    self.history.append({"role": "assistant", "content": response_message})
    return response_message

#search("ما هو تأثير الفساد الأقتصادي", CHROMA_PATH)
# search("How are you?", CHROMA_PATH)
agent = Agent()
print(agent.respond("hi, how are you?"))