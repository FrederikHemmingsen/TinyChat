from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from dotenv import load_dotenv
import os
import openai

load_dotenv()
TOKEN = os.environ['MY_DISCORD_TOKEN']
AITOKEN = os.environ['AITOKEN']

#API for openAI
openai.api_key = AITOKEN

def locate_memory(author:str, collective_chat_history:dict) -> ConversationBufferMemory:

  if author in collective_chat_history:
    memory = collective_chat_history[author]
    
  if author not in collective_chat_history:
    memory = ConversationBufferMemory(memory_key="chat_history")

    collective_chat_history[author] = memory

  return memory

def update_memory(author:str, collective_chat_history:dict, human_input:str, ai_output:str) -> dict:

  memory = locate_memory(author, collective_chat_history)
  memory.chat_memory.add_user_message(human_input)
  memory.chat_memory.add_ai_message(ai_output)

  collective_chat_history[author] = memory

  return collective_chat_history
  
def llm_answer(human_input, stored_memory):

  template = """You are a chatbot having a conversation with a human.

    {chat_history}
    Human: {human_input}
    Chatbot:"""

  prompt = PromptTemplate(
      input_variables=["chat_history", "human_input"], 
      template=template
  )
  memory = stored_memory

  llm_chain = LLMChain(
      llm=OpenAI(openai_api_key=AITOKEN), 
      prompt=prompt, 
      verbose=True, 
      memory=memory
  )

  return llm_chain.predict(human_input=human_input)
