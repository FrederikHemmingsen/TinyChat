import os
import discord
import openai
import requests
import re
from dotenv import load_dotenv

#Get those secret cheat codes
load_dotenv()
TOKEN = os.getenv("MY_DISCORD_TOKEN")
AITOKEN = os.getenv("MY_OPENAI_TOKEN")

#API for openAI
openai.api_key = AITOKEN

#initiate/ Create the Discord bot(intent is the funny enough - The intent with the bot" but chosen in the discord admin panel)
intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)

#Test if the bot is alive
@client.event
async def on_ready():
    print("Yup im really alive - im a MOFO BOY!")

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

    # slice the discord chat name away please count the string when printing AItext
    AIslice = message.content[22:]
    print(AIslice)

    messages = [
            {"role": "system", "content": "you are a chatbot full of humor"},
            {"role": "user", "content": f'{AIslice}'}
        ]

    response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            
            json = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.1},
            headers= {
                'authorization': f'Bearer {AITOKEN}',
                'content-type': 'application/json'}
                )
    response = response.json()

  # Send the response as a message
  await message.channel.send(response['choices'][0]['message']['content']) 
 
#Go live stupid
client.run(TOKEN)


