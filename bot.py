import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_URL = 'http://localhost:8000'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!critique'):
        try:
            parts = message.content.split(' ')
            url = parts[1]
            rating = int(parts[2])
            review = ' '.join(parts[3:])
            user_id = str(message.author.id)
            username = str(message.author.name)

            payload = {
                'url': url,
                'rating': rating,
                'review': review,
                'user_id': user_id,
                'username': username
            }
            response = requests.post(f'{API_URL}/review', json=payload)
            if response.status_code == 200:
                message_text = response.json()['message']
                await message.channel.send(message_text)
            else:
                await message.channel.send(f'Erreur : {response.json()["error"]}')
        except Exception as e:
            await message.channel.send(f'Erreur : {str(e)}')

    if message.content.startswith('!hasard'):
        try:
            url = message.content.split(' ')[1]
            payload = {'url': url}
            response = requests.post(f'{API_URL}/random_review', json=payload)
            if response.status_code == 200:
                review = response.json()['review']
                title = response.json()['title']
                await message.channel.send(f'Une critique au pif de {title} : \n\n{review}')
            else:
                await message.channel.send(f'Erreur : {response.json()["error"]}')
        except Exception as e:
            await message.channel.send(f'Erreur : {str(e)}')
            
    if message.content.startswith('!list'):
        try:
            url = message.content.split(' ')[1]
            payload = {'url': url}
            response = requests.post(f'{API_URL}/list_reviews', json=payload)
            if response.status_code == 200:
                reviews = response.json()['reviews']
                if reviews:
                    list_message = '\n'.join([f"ID {review['id']} : {review['username']} a collé {review['rating']} à {review['title']} " for review in reviews])
                    await message.channel.send(f'Liste des notes :\n{list_message}')
                else:
                    await message.channel.send('Je trouve rien.')
            else:
                await message.channel.send(f'Erreur : {response.json()["error"]}')
        except Exception as e:
            await message.channel.send(f'Erreur : {str(e)}')

    if message.content.startswith('!del'):
        try:
            critique_id = message.content.split(' ')[1]
            response = requests.delete(f'{API_URL}/delete/{critique_id}')
            if response.status_code == 200:
                await message.channel.send('Critique supprimée.')
            else:
                await message.channel.send(f'Erreur : {response.json()["error"]}')
        except Exception as e:
            await message.channel.send(f'Erreur : {str(e)}')

client.run(DISCORD_BOT_TOKEN)
