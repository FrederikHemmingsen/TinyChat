import os
import discord
import openai
import requests
import re
from dotenv import load_dotenv
from helper_functions import locate_memory, update_memory, llm_answer

#Get those secret cheat codes
load_dotenv()
TOKEN = os.environ['MY_DISCORD_TOKEN']
AITOKEN = os.environ['AITOKEN']

#API for openAI
openai.api_key = AITOKEN

#initiate/ Create the Discord bot(intent is the funny enough - The intent with the bot" but chosen in the discord admin panel)
intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)

global collective_chat_history
collective_chat_history = {}


#Test if the bot is alive
@client.event
async def on_ready():
  print("Yup im really alive - im a real tiny BOY!")


# lisent to @mention
@client.event
async def on_message(message):
  # make sure it does not go bananas
  if message.author == client.user:
    return

  # if mention
  if client.user in message.mentions:
    print(message)
    print(type(message.content))

    author = message.author

    # slice the discord chat name away please count the string when printing AItext
    human_message = message.content[22:]  #username is 22chars

    current_memory = locate_memory(author, collective_chat_history)

    ai_output = llm_answer(human_message, current_memory)

    update_memory(author, collective_chat_history, human_message, ai_output)

    await message.channel.send(ai_output)
  '''
    messages = [
      {
        "role": "system",
        "content": "you are a chatbot full of humor"
      },  #Who is the bot - personality? 
      {
        "role": "user",
        "content": f'{AIslice}'
      }  #prompt the message
    ]
    #ChatGPT parameters
    response = requests.post(url="https://api.openai.com/v1/chat/completions",
                             json={
                               "model": "gpt-3.5-turbo",
                               "messages": messages,
                               "temperature": 0.1
                             },
                             headers={
                               'authorization': f'Bearer {AITOKEN}',
                               'content-type': 'application/json'
                             })
    response = response.json()

      # Send the response as a message
  await message.channel.send(response['choices'][0]['message']['content'])
  '''


#Go live stupid
client.run(TOKEN)
