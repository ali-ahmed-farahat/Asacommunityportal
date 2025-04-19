import openai
from agent.prompt import NO_VALUE_PROMPT
import os
from dotenv import load_dotenv
from agent.search_vdb import search

# Load environment variables
load_dotenv()

# Get API key and verify it's loaded
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY

CHROMA_PATH = "chroma"

class Agent:
    def __init__(self):
        self.sys_msg = NO_VALUE_PROMPT
        self.history = []
        self.history.append({
            "role": "system",
            "content": self.sys_msg
        })
        self.client = client  # Store the client instance

    def respond(self, message):
        context = search(message, CHROMA_PATH)
        if context:
            message = f"this is the customer's message, respond in it's language and ignore the context language:{message}\n\n[context: {context}]"
            self.history.append({"role": "user", "content": message})
        else:
            self.history.append({
                "role": "user",
                "content": message
            })
        
        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.history
        )
        response_message = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": response_message})
        return response_message

#search("ما هو تأثير الفساد الأقتصادي", CHROMA_PATH)
# search("How are you?", CHROMA_PATH)
# agent = Agent()
# print(agent.respond("من هو رئيس الجهاز المركزي للمجاسبات"))