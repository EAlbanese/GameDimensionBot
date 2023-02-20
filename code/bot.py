import configparser
import math
from datetime import datetime

import database as database
from discord import (ApplicationContext, Bot, Embed,
                     EmbedField, Member, Option, Permissions, Button, PartialEmoji, Game, File, Intents)
from enums import PunishmentType
from pytimeparse.timeparse import timeparse
from views import SupportTicketCreateView, MinecraftTicketCreateView, ReportUserModal, SupportModal, BugReportCreateView, SuggestionView
from PIL import Image, ImageDraw, ImageFont
# import requests
import io
import logging

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config.get('Bot', 'Token')
DEBUG_GUILDS = None if config.get('Bot', 'DebugGuilds') == "" else list(
    map(lambda id: int(id), config.get('Bot', 'DebugGuilds').split(',')))

intents = Intents.default()
intents.members = True
bot = Bot(debug_guild=DEBUG_GUILDS, intents=intents)
db = database.Database("bot.db")

# db.drop_db()
db.create_moderation_table()
db.create_ticket_table()

# logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():
    print(f'{bot.user} is connected')
    await bot.change_presence(activity=Game(''))


# Moderation commands
@bot.slash_command(description="Shows information about the user", default_member_permissions=Permissions.none())
async def modlogs(interaction: ApplicationContext, member: Option(Member, 'Select the user')):
    embed = Embed(
        title=f'Modlogs über {member.display_name}#{member.discriminator}')
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f'UID: {member.id}')
    penalties = db.get_penalties_by_user(
        interaction.guild_id, member.id)
    if len(penalties) == 0:
        embed.add_field(name='Keine Logs gefunden',
                        value='Member fällt nicht auf')
    for penalty in penalties:
        embed.add_field(
            name=f'⚖️ Case {penalty[0]}',
            value=f'**Type:** {PunishmentType(penalty[1]).name}\n**Moderator:** <@{penalty[4]}>\n**Grund:** {penalty[5]}',
            inline=False
        )
    await interaction.respond(embed=embed, ephemeral=True)


def parse_duration_end(duration_string):
    seconds = timeparse(duration_string)
    return datetime.fromtimestamp(datetime.now().timestamp() + seconds)


async def punish(interaction: ApplicationContext, type: PunishmentType, guild_id: int, member: Member, mod_id: int, reason: str, punishment_end: datetime = datetime.now()):
    db.create_penalty(type.value, guild_id, member.id, mod_id, reason)

    embed = Embed(
        title=f'Created {type.name} for {member.display_name}#{member.discriminator}',
        fields=[
            EmbedField(
                name='Grund',
                value=reason
            )
        ]
    )
    if punishment_end.timestamp() > datetime.now().timestamp():
        embed.add_field(
            name='End', value=f'<t:{math.ceil(punishment_end.timestamp())}:R>')

    await interaction.respond(embed=embed, ephemeral=True)


@bot.slash_command(description="Member warnen")
async def warn(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'Grund für den Warn', max_length=100)
):
    await punish(interaction, PunishmentType.WARN, interaction.guild_id, member, interaction.author.id, reason)


@bot.slash_command(description="Member timouten", default_member_permissions=Permissions.none())
async def timeout(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'Grund für den Timeout', max_length=100),
    duration: Option(str, 'Dauer des Timoutes', max_length=10)
):
    punishment_end = parse_duration_end(duration)
    try:
        await member.timeout(punishment_end, reason=reason)
    except:
        return await interaction.respond('Sieht so aus als hätte ich keine Berechtigungen um den Member zu timeouten.')

    await punish(interaction, PunishmentType.TIMEOUT, interaction.guild_id, member, interaction.author.id, reason, punishment_end)


@bot.slash_command(description="Member kicken", default_member_permissions=Permissions.none())
async def kick(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'Grund für den Kick', max_length=100)
):
    try:
        await member.kick(reason=reason)
    except:
        return await interaction.respond('Sieht so aus als hätte ich keine Berechtigungen um den Member zu kicken.')

    await punish(interaction, PunishmentType.KICK, interaction.guild_id, member, interaction.author.id, reason)


@bot.slash_command(description="Member bannen", default_member_permissions=Permissions.none())
async def ban(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'Grund für den Bann', max_length=100),
    duration: Option(str, 'Dauer des Bannes', max_length=10)
):
    punishment_end = parse_duration_end(duration)
    try:
        await member.ban(reason=reason, delete_message_days=7)
    except:
        return await interaction.respond('Sieht so aus als hätte ich keine Berechtigungen um den Member zu bannen.')

    await punish(interaction, PunishmentType.BAN, interaction.guild_id, member, interaction.author.id, reason, punishment_end)
# Welcomer


@bot.event
async def on_member_join(member):
    print("FUCK MY LIFE")
    channel = bot.get_channel(1038812807216496640)
    await channel.send(f'Hey <@{member.user.id}>, willkommen auf **Game Town**!')

# Information category Embeds


@ bot.slash_command(description="Einführung")
async def introduction(interaction: ApplicationContext):
    embed = Embed(
        title=f'Einführung',
        description='Willkommen auf Game Town <:pikachu_love:1042727900996173884> \n \n Wir sind ein Community-Server, wo du mit deinen Freunden Spaß haben kannst.',
        fields=[
            EmbedField(
                name='Regeln',
                value=f'Bevor du anfangen kannst, auf unserem Server Spaß zu haben, musst du unsere Regeln akzeptieren, klicke hier <#1072470606706126848>'
            ),
            EmbedField(
                name='Ankündigungen',
                value=f'In dem <#1072470253491200090> Channel werden wir Giveaways, Events und Updates verkünden. Wenn du dich für eins der folgenden Ankündigungen interessierst, dann such dir die passende Rolle dazu aus, damit du nichts verpasst.'
            ),
            EmbedField(
                name='Chats',
                value=f'Im <#1072478704724344873> kannst du dich mit deinen Freunden unterhalten und Spass haben. Falls du leute suchst, mit denen du spielen möchtest, dann Frag im <#1072480036915007530> nach ob wer lust hat.'
            ),
            EmbedField(
                name='Booster',
                value=f'Wir freuen uns über jegliche Unterstützung von dir. Falls du den Server geboostet hast, kannst du ein <#1072473811162771486> und du hast das Anrecht auf eine custom Rolle nach deiner Wahl.'
            ),
            EmbedField(
                name='Support',
                value=f'Falls du Fragen oder Hilfe brauchst kannst du jederzeit ein Ticket im <#1072473811162771486> Channel erstellen. Unser Team wird sich um dich kümmern.'
            ),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1019566455601238017/1072935031779102871/LogoV1.jpg?width=616&height=616')
    await interaction.respond("Created introduction embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@bot.slash_command(description="Regelwerk")
async def rules(interaction: ApplicationContext):
    embed = Embed(
        title=f'Regelwerk',
        description='Mit dem Beitritt zum Game Town Server akzeptierst du alle unten stehenden Regeln. Wenn sich jemand nicht an die Regeln hält, melde dies bitte an unser <@&1072489048515559506> und wir werden es überprüfen.',
        fields=[
            EmbedField(
                name='1) Sei respektvoll', value=f'Sei respektvoll, freundlich und einladend zu allen Mitgliedern auf dem Server, um den Server zu einer angenehmen Erfahrung für alle zu machen. Beleidigungen, Diskriminierung, Mobbing oder unangemessene Reaktionen sind Gründe für einen permanenten Bann.'),
            EmbedField(name='2) Belästigung', value=f'Unterlasse jegliche Form der Belästigung. Wir dulden keinen Rassismus, keine Homophobie, keine Transphobie, keinen Sexismus und keine diskriminierenden Kommentare jeglicher Art. (Dies gilt auch für Belästigungen durch Direktnachrichten).'),
            EmbedField(
                name='3) Werbung', value=f'Mache keine Werbung für deinen/andere Discord-Server oder jede Art von unaufgeforderter Werbung (einschließlich Direktnachrichten).'),
            EmbedField(
                name='4) Streaming von kostenpflichtigen Streaming-Diensten verboten', value=f'Das Streaming von kostenpflichtigen Streaming-Diensten ist verboten und wird mit einer Verwarnung geahndet.'),
            EmbedField(
                name='5) Kanäle für den vorgesehenen Zweck nutzen', value=f'Bitte verwende die Kanäle für den vorgesehenen Zweck. Verwende den Kanal <#1072478704724344873> für normale Gespräche usw.'),
            EmbedField(
                name='6) Eigene Rollen richtig verwenden', value=f'Die Verwendung unangemessener Selbstrollen gilt als Trolling und wird mit einer Zeitüberschreitung geahndet.'),
            EmbedField(
                name='7) Keine NSFW-Inhalte erlaubt', value=f'Poste keine expliziten Inhalte (NSFW). Dazu gehören alle sexuellen Themen, Handlungen oder Absichten in den Text- und Sprachkanälen sowie in Direktnachrichten.'),
            EmbedField(
                name='8) Kein Spamming', value=f'Bitte spame keine Emojis oder Spam-Nachrichten in Kanälen. Dies wird zu einer sofortigen Stummschaltung führen. Wenn ihr 3 Mal spammt, werdet ihr gekickt. Spamming besteht darin, die gleichen Nachrichten immer wieder zu senden.'),
            EmbedField(
                name='9) Team', value=f'Höre auf die Teammitglieder, wenn sie etwas sagen. Wenn du mit der Entscheidung nicht einverstanden bist, kannst du  die Owner oder einem anderen Mitglied schreiben und uns deine Meinung sagen.'),
            EmbedField(
                name='10) Terms of use', value=f'Terms of use and guidelines: \n Riot Terms of Use: https://www.riotgames.com/en/terms-of-service \n Discord terms of use: https://discordapp.com/terms \n Discord guidleines: https://discord.com/guidelines'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1019566455601238017/1072935031779102871/LogoV1.jpg?width=616&height=616'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@ bot.slash_command(description="Team")
async def team(interaction: ApplicationContext):
    embed = Embed(
        title=f'Game Town Team',
        fields=[
            EmbedField(
                name='Owner', value=f'⟫<@479537494384181248> \n⟫<@187599309070401541>'),
            EmbedField(name='Administrator',
                       value=f'Nicht besetzt'),
            EmbedField(
                name='Head Manager', value=f'Nicht besetzt'),
            EmbedField(
                name='Manager', value=f'Nicht besetzt'),
            EmbedField(
                name='Head Moderator', value=f'Nicht besetzt'),
            EmbedField(
                name='Moderator', value=f'Nicht besetzt'),
            EmbedField(
                name='Test-Supporter / Supporter', value=f'Nicht besetzt'),
            EmbedField(
                name='Content Creator', value=f'Nicht besetzt'),
            EmbedField(
                name='Designer', value=f'Nicht besetzt \n \n \n Wenn du Hilfe brauchst, kannst du eine <#1072473811162771486> eröffnen und unsere Mitarbeiter werden sich um dein Anliegen kümmern.'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1019566455601238017/1072935031779102871/LogoV1.jpg?width=616&height=616'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)

# Ticket System


@bot.slash_command(description="Server Support")
async def supportticket(interaction: ApplicationContext):
    embed = Embed(
        title=f'Support Ticket',
        description='Falls du Hilfe brauchst, jemanden aus dem Team melden oder dich Bewerben möchtest, dann öffne eines der folgenden Tickets. Ein Teammitglied wird in kürze bei dir sein. \n \n ⛔ Für das missbrauchen des Ticket-Systems gibt es Verwarnungen.',
    )
    await interaction.respond("Created ticket embed", ephemeral=True)
    await interaction.channel.send(embed=embed, view=SupportTicketCreateView())


@bot.slash_command(description="Minecraft Support")
async def minecraftticket(interaction: ApplicationContext):
    embed = Embed(
        title=f'Minecraft Support Ticket',
        description='Falls du Hilfe auf dem Minecraft Server brauchst oder jemanden melden, dann öffne eines der folgenden Tickets. Ein Teammitglied wird in kürze bei dir sein. \n \n ⛔ Für das missbrauchen des Ticket-Systems gibt es Verwarnungen.',
    )
    await interaction.respond("Created ticket embed", ephemeral=True)
    await interaction.channel.send(embed=embed, view=MinecraftTicketCreateView())


@bot.slash_command(description="test")
async def test(interaction: ApplicationContext):
    await interaction.response.send_message("Fuck you")
    # Open the background image
    bg_img = Image.open("resources/bg.png")

    # Create an ImageDraw object
    draw = ImageDraw.Draw(bg_img)

    # Define the font and font size
    font = ImageFont.truetype("resources/font.ttf", 80)

    text = f"Username#0000 just joined the server"

    # Draw the text on the background
    draw.text((bg_img.width/2-draw.textlength(text, font=font)/2, bg_img.height-325), text,
              font=font, fill=(255, 255, 255))

    # Open the image you want to add
    avatar_request = requests.get(
        f"{interaction.user.display_avatar.url}")
    avatar_img = Image.open(io.BytesIO(avatar_request.content))
    img_pos = (int(bg_img.width/2-avatar_img.width/2), 150)

    # Paste the image on the background
    bg_img.paste(avatar_img, img_pos)

    # Save the final image
    buf = io.BytesIO()
    bg_img.save(buf, format='PNG')
    buf.seek(0)
    await interaction.channel.send(files=[File(buf, "welcome.png")])


# Help


@bot.slash_command(description="Game Town Command-Liste")
async def help(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hilfe',
        description='Hier findest du alle Commands, welche der Bot kann und wie du diese ausführen kannst.',
    )
    embed.add_field(name="Bug melden", value="Mit ``/bugreport`` kannst du einen Bug melden. Ich bitte dich, sobald du einen Fehler oder Bug gefunden hast, den zu melden!", inline=False)
    embed.add_field(name="Verbesserungsvorschläge",
                    value="Mit ``/suggestion`` kannst du mir Verbesserungsvorschläge mitteilen. Ich freue mich über jegliches Feedback von euch.", inline=False)
    embed.add_field(name="Sonstige Hilfe",
                    value="Du kannst mir auch jederzeit via Discord DM --> **Draixon#1999** ein Feedback geben oder Fragen über den Bot stellen.", inline=False)

    await interaction.respond("Hilfe ist unterwegs!", ephemeral=True)
    await interaction.channel.send(embed=embed)


# Bug report
@bot.slash_command(description="Bug reporten")
async def bugreport(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hast du einen Bug gefunden?',
        description='Falls du einen Bug gefunden hast, bitte ich dich den genau zu beschreiben.',
    )
    await interaction.respond("Danke für das melden!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=BugReportCreateView())


# Suggestion
@bot.slash_command(description="Verbesserungsvorschlag")
async def suggestion(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hast du einen Verbesserungsvorschlag?',
        description='Falls du einen Verbesserungsvorschlag hast, kannst du mir diesen jederzeit mitteilen.',
    )
    await interaction.respond("Danke für den Vorschlag!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=SuggestionView())


# Autoroles
memberrole = 1072489393228628048
customtitlerole = 1072490631164870746
leveltitlerole = 1072491006546673724
aboutmerole = 1072489315973738578
pingtitlerole = 1072491189435105310
mcinforole = 1072572623092990022
boostertitlerole = 1072490552563617883


@bot.event
async def on_member_join(member):
    # Get the special role by ID
    member_role = member.guild.get_role(memberrole)
    customtitle_role = member.guild.get_role(customtitlerole)
    leveltitle_role = member.guild.get_role(leveltitlerole)
    aboutme_role = member.guild.get_role(aboutmerole)
    pingtitle_role = member.guild.get_role(pingtitlerole)
    mcinfo_role = member.guild.get_role(mcinforole)
    boostertitle_role = member.guild.get_role(boostertitlerole)

    # Give the member the special role
    await member.add_roles(member_role, customtitle_role, leveltitle_role, aboutme_role, pingtitle_role, mcinfo_role, boostertitle_role)


bot.run(TOKEN)
db.connection.close()
