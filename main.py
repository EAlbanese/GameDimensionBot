import os

import discord
from dotenv import load_dotenv
from discord import Embed, EmbedField, Option, Member

load_dotenv()
TOKEN = 'MTA0MjQzMDcxMTk4ODIzMjIxMg.GQ0P7W.KMhE3oCVkvBtiFXbE08xAPNIpdKBOGAdju4h4g'

bot = discord.Bot(debug_guilds=['1038123472007737375'])


@bot.event
async def on_ready():
    print(f'{bot.user} is connected')


@bot.slash_command(description="Shows information about the user")
async def modlogs(interaction: discord.ApplicationContext, member: Option(Member, 'Select the user')):
    embed = Embed(
        title=f'Modlogs for {member.display_name}#{member.discriminator}',
        fields=[
            EmbedField(
                name='Name', value=f'{member.display_name}#{member.discriminator}'),
            EmbedField(name='User Id', value=f'{member.id}'),
        ],
    )
    embed.set_thumbnail(url=member.display_avatar.url),
    await interaction.respond(embed=embed, ephemeral=True)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1038812807216496640)
    await channel.send(f'Hey <@{member.user.id}>, welcome to **Game Dimension**!')


@bot.slash_command(description="Introduction")
async def introduction(interaction: discord.ApplicationContext):
    embed = Embed(
        title=f'Introduction',
        description='Welcome to Game Dimension <:pikachu_love:1042727900996173884> \n \n We are a community server where you can have fun with your friends.',
        fields=[
            EmbedField(
                name='Rules', value=f'Before you can start to have fun on our server, you have to accept our rules, click here <#1038812962598699008>'),
            EmbedField(name='User Id', value=f'{member.id}'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1043197337499078716/1043197378737492060/e343da6ee754a06c2f6a946cdc049d74fa773510d8dd8b3641e6bd72f6f58dd1.png'),
    embed.set_image(url='https://media.discordapp.net/attachments/1043197337499078716/1043197379123363901/4273a4704084d68cd6475fe20ce291fc329a5d5ea75c415352c0c355a5f00c8f.gif')
    await interaction.respond(embed=embed, ephemeral=True)

bot.run(TOKEN)
