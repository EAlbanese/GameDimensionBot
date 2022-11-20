import configparser
import os

import discord
from discord import Button, Embed, EmbedField, Member, Option, OptionChoice

import database

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config.get('Bot', 'Token')
DEBUG_GUILDS = None if config.get('Bot', 'DebugGuilds') == "" else list(
    map(lambda id: int(id), config.get('Bot', 'DebugGuilds').split(',')))

bot = discord.Bot(debug_guild=DEBUG_GUILDS)
db = database.Database("database.db")

db.create_tables()


@bot.event
async def on_ready():
    print(f'{bot.user} is connected')


# Moderation commands
@bot.slash_command(description="Shows information about the user")
async def modlogs(interaction: discord.ApplicationContext, member: Option(Member, 'Select the user')):
    embed = Embed(
        title=f'Modlogs for {member.display_name}#{member.discriminator}'
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f'UID: {member.id}')
    penalties = db.get_penalties_by_user(
        interaction.guild_id, interaction.user.id)
    if len(penalties) == 0:
        embed.add_field(name='No logs found', value='User is good')
    for penalty in penalties:
        embed.add_field(
            name=f'Case {penalty[0]}', value=f'**Type:** {penalty[1]}\n**Moderator:** <@{penalty[4]}>\n**Reason:** {penalty[5]}')
    await interaction.respond(embed=embed, ephemeral=True)


@bot.slash_command(description="Punish a user")
async def punish(
        interaction: discord.ApplicationContext,
        member: Option(Member, 'Select the user'),
        type: Option(str, 'The type of punishment', choices=[
            OptionChoice(name='warn', value='1'),
            OptionChoice(name='timeout', value='2'),
            OptionChoice(name='kick', value='3'),
            OptionChoice(name='ban', value='4'),
        ]),
        reason: Option(str, 'The reason for the punishment', max_length=100),
        duration: Option(str, 'The duration of the punishment', required=False)):

    db.create_penalty(
        interaction.guild_id,
        type,
        member.id,
        interaction.author.id,
        reason
    )

    await interaction.respond(f'<@{member.id}> received punishment {type} with reason `{reason}`' + ((' for ' + duration) if duration is not None else ''), ephemeral=True)


# Welcomer
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1038812807216496640)
    await channel.send(f'Hey <@{member.user.id}>, welcome to **Game Dimension**!')

# Information category Embeds


@bot.slash_command(description="Introduction")
async def introduction(interaction: discord.ApplicationContext):
    embed = Embed(
        title=f'Introduction',
        description='Welcome to Game Dimension <:pikachu_love:1042727900996173884> \n \n We are a community server where you can have fun with your friends.',
        fields=[
            EmbedField(
                name='Rules', value=f'Before you can start to have fun on our server, you have to accept our rules, click here <#1038812962598699008>'),
            EmbedField(name='Announcements', value=f'These following three channels will be one of the most important if you will be active on the server. The <#1038813102185123922> channel is there to be informed about the latest updates of the server, such as new roles, new channels or new team members. \n In the <#1038813117179756544> we will announce events, giveaways, tournaments or other announcements that we will do with you as a community. \n Last but not least comes the <#1038813153447919688>, if you are interested in patch-notes about your games, you will find all relevant info here. Last but not least comes the <There is a separate role for each channel, so if you are interested, pick the role and you will always be informed.'),
            EmbedField(
                name='Selfroles', value=f'If you want, you can now check out our <#1038813219420110869> channel to choose your own roles. These give your profile that certain something'),
            EmbedField(
                name='Support', value=f'We ask you to choose a **Support language** in the <#1038813219420110869> , so that you can better communicate with the team. We offer an English and a German team.'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1043197337499078716/1043197379123363901/4273a4704084d68cd6475fe20ce291fc329a5d5ea75c415352c0c355a5f00c8f.gif'),
    embed.set_image(url='https://media.discordapp.net/attachments/1043197337499078716/1043197378737492060/e343da6ee754a06c2f6a946cdc049d74fa773510d8dd8b3641e6bd72f6f58dd1.png')
    await interaction.respond("Created introduction embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@bot.slash_command(description="Rules")
async def rules(interaction: discord.ApplicationContext):
    embed = Embed(
        title=f'Rules',
        description='By joining the Game Dimension server you accept all the rules below. If someone does not follow the rules, please report it to <@&1038814047270866974> or <@&1038821661224484995> and they will check it.',
        fields=[
            EmbedField(
                name='1) Be respectful', value=f'Be respectful, friendly and welcoming to all members on the server to make the server a pleasant experience for all. Insults, discrimination, bullying, or inappropriate Reactions are grounds for a permanent ban.'),
            EmbedField(name='2) Harassment', value=f'Refrain from any form of harassment. We do not allow racism, homophobia, transphobia, sexism, or discriminatory comments of any kind. (This includes harassment through direct messages).'),
            EmbedField(
                name='3) Advertising', value=f'Do not advertise your/other Discord servers or any type of unsolicited advertising (including direct messages).'),
            EmbedField(
                name='4) Streaming of paid streaming services prohibited', value=f'Streaming paid streaming services is forbidden and will be punished with a warning.'),
            EmbedField(
                name='5) Use channels for their intended purpose', value=f'Please use the channels for the intended purpose. Use the channel <#1038812094344200212> for normal talking, etc.'),
            EmbedField(
                name='6) Use Self-Roles correctly', value=f'Using inappropriate self-roles is considered trolling and will be penalized with a timeout.'),
            EmbedField(
                name='7) No NSFW content allowed', value=f'Do not post explicit content (NSFW). This includes any sexual topics, actions or intentions in the text and voice channels as well as direct messages.'),
            EmbedField(
                name='8) No spamming', value=f'Please do not spam emojis or spam messages in channels. This will result in an immediate mute. 3 times, and then you will be kicked. Spamming consists of sending the same messages over and over again.'),
            EmbedField(
                name='9) Staff', value=f'Listen to the rankers when they say something. If you don\'t agree with the decision, you can write to me or another member and tell us what you think.'),
            EmbedField(
                name='10) Terms of use', value=f'Terms of use and guidelines: \n Riot Terms of Use: https://www.riotgames.com/en/terms-of-service \n Discord terms of use: https://discordapp.com/terms \n Discord guidleines: https://discord.com/guidelines'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1043197337499078716/1043197379123363901/4273a4704084d68cd6475fe20ce291fc329a5d5ea75c415352c0c355a5f00c8f.gif'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@bot.slash_command(description="Team")
async def team(interaction: discord.ApplicationContext):
    embed = Embed(
        title=f'Game DImension Team',
        fields=[
            EmbedField(
                name='Owner', value=f'『✦』<@480523441439506443> english/german speaking \n『✦』<@479537494384181248> english/german speaking'),
            EmbedField(name='Administrator',
                       value=f'『✦』<@187599309070401541> english/german speaking'),
            EmbedField(
                name='Head Manager', value=f'『✦』<@91665388970311782> english/german speaking \n :incoming_envelope: Is searched german speaking (0/1)'),
            EmbedField(
                name='Manager', value=f'『✦』<@880829080524685402> english speaking \n 『✦』<@1023325930044784680> english speaking \n 『✦』<@805504937567322122> german speaking \n :incoming_envelope: Is searched german speaking (0/1)'),
            EmbedField(
                name='Head Moderator', value=f':incoming_envelope: Is searched english speaking (0/1) \n :incoming_envelope: Is searched german speaking (0/1)'),
            EmbedField(
                name='Moderator', value=f'『✦』<@704020919365926983> english speaking \n :incoming_envelope: Is searched english speaking (1/2) \n :incoming_envelope: Is searched german speaking (0/2)'),
            EmbedField(
                name='Test-Supporter / Supporter', value=f'『✦』<@465349397803171841> english speaking \n 『✦』<@694143135101616168> english speaking \n 『✦』<@854034741934161971> english speaking \n 『✦』<@763433366875013151> english speaking \n :incoming_envelope: Is searched german speaking (0/3)'),
            EmbedField(
                name='Content Creator', value=f'『✦』<@612664092741730344> \n 『✦』<@485148322609496074>'),
            EmbedField(
                name='Designer', value=f':incoming_envelope: Is searched english/german speaking (0/2) \n \n \n If you need help, feel free to open a <#1038810882349736056> and our staff will take care of your request. \n \n If you want to apply, you can apply under <#1038810904822808726> and get a chance to join the team.'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1043197337499078716/1043197379123363901/4273a4704084d68cd6475fe20ce291fc329a5d5ea75c415352c0c355a5f00c8f.gif'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


# Ticket System
# @bot.slash_command(description="ticket-en")
# async def ticketenglish(interaction: discord.ApplicationContext):
#     embed = Embed(
#         title=f'Support Ticket',
#         description='If you have a concern, feel free to open one of the following tickets. A team member will be with you in no time.',
#     )
#     button = Button(
#         emoji=':no_entry_sign:',
#         label='Report a User',
#         style='primary'
#     )
#     await interaction.respond("Created rules embed", ephemeral=True)
#     await interaction.channel.send(embed=embed, button=button)


bot.run(TOKEN)
db.connection.close()
