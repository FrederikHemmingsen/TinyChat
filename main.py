import os
import discord
import openai
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
 
    # OPEN_AI Parameters
    response = openai.Completion.create(
    engine="gpt-3.5-turbo",
    prompt=f"{message.content}",
    max_tokens=1024,
    temperature=0.5,
    )

  # Send the response as a message
  await message.channel.send(response.choices[0].text)


#Go live stupid
client.run(TOKEN)


