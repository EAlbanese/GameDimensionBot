import configparser
import math
from datetime import datetime

import database as database
from discord import (ApplicationContext, Bot, Embed,
                     EmbedField, Member, Option, Permissions, Button, PartialEmoji, Game, File, Intents)
from enums import PunishmentType
from pytimeparse.timeparse import timeparse
from views import SupportTicketCreateView, AddminTicketCreatView, ReportUserModal, SupportModal, BotProblemsModal
from PIL import Image, ImageDraw, ImageFont
# import requests
import io

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config.get('Bot', 'Token')
DEBUG_GUILDS = None if config.get('Bot', 'DebugGuilds') == "" else list(
    map(lambda id: int(id), config.get('Bot', 'DebugGuilds').split(',')))

intents = Intents.default()
intents.members = True
bot = Bot(debug_guild=DEBUG_GUILDS, intents=intents)
db = database.Database("bot.db")

db.create_tables()


@bot.event
async def on_ready():
    print(f'{bot.user} is connected')
    await bot.change_presence(activity=Game('in another Dimension'))


# Moderation commands
@bot.slash_command(description="Shows information about the user", default_member_permissions=Permissions.none())
async def modlogs(interaction: ApplicationContext, member: Option(Member, 'Select the user')):
    embed = Embed(
        title=f'Modlogs for {member.display_name}#{member.discriminator}')
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f'UID: {member.id}')
    penalties = db.get_penalties_by_user(
        interaction.guild_id, member.id)
    if len(penalties) == 0:
        embed.add_field(name='No logs found', value='User is good')
    for penalty in penalties:
        embed.add_field(
            name=f'⚖️ Case {penalty[0]}',
            value=f'**Type:** {PunishmentType(penalty[1]).name}\n**Moderator:** <@{penalty[4]}>\n**Reason:** {penalty[5]}',
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
                name='Reason',
                value=reason
            )
        ]
    )
    if punishment_end.timestamp() > datetime.now().timestamp():
        embed.add_field(
            name='End', value=f'<t:{math.ceil(punishment_end.timestamp())}:R>')

    await interaction.respond(embed=embed, ephemeral=True)


@bot.slash_command(description="Warn a user")
async def warn(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'The reason for the warn', max_length=100)
):
    await punish(interaction, PunishmentType.WARN, interaction.guild_id, member, interaction.author.id, reason)


@bot.slash_command(description="Timeout a user", default_member_permissions=Permissions.none())
async def timeout(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'The reason for the timeout', max_length=100),
    duration: Option(str, 'The duration for the timeout', max_length=10)
):
    punishment_end = parse_duration_end(duration)
    try:
        await member.timeout(punishment_end, reason=reason)
    except:
        return await interaction.respond('Looks like I don\'t have timeout permissions.')

    await punish(interaction, PunishmentType.TIMEOUT, interaction.guild_id, member, interaction.author.id, reason, punishment_end)


@bot.slash_command(description="Kick a user", default_member_permissions=Permissions.none())
async def kick(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'The reason for the kick', max_length=100)
):
    try:
        await member.kick(reason=reason)
    except:
        return await interaction.respond('Looks like I don\'t have kick permissions.')

    await punish(interaction, PunishmentType.KICK, interaction.guild_id, member, interaction.author.id, reason)


@bot.slash_command(description="Ban a user", default_member_permissions=Permissions.none())
async def ban(
    interaction: ApplicationContext,
    member: Option(Member, 'Select the user'),
    reason: Option(str, 'The reason for the ban', max_length=100),
    duration: Option(str, 'The duration for the ban', max_length=10)
):
    punishment_end = parse_duration_end(duration)
    try:
        await member.ban(reason=reason, delete_message_days=7)
    except:
        return await interaction.respond('Looks like I don\'t have ban permissions.')

    await punish(interaction, PunishmentType.BAN, interaction.guild_id, member, interaction.author.id, reason, punishment_end)
# Welcomer


@bot.event
async def on_member_join(member):
    print("FUCK MY LIFE")
    channel = bot.get_channel(1038812807216496640)
    await channel.send(f'Hey <@{member.user.id}>, welcome to **Game Dimension**!')

# Information category Embeds


@ bot.slash_command(description="Introduction EN")
async def introductionen(interaction: ApplicationContext):
    embed = Embed(
        title=f'Introduction',
        description='Welcome to Game Dimension <:pikachu_love:1042727900996173884> \n \n We are a community server where you can have fun with your friends.',
        fields=[
            EmbedField(
                name='Rules',
                value=f'Before you can start to have fun on our server, you have to accept our rules, click here <#1038812962598699008>'
            ),
            EmbedField(
                name='Announcements',
                value=f'These following three channels will be one of the most important if you will be active on the server. The <#1038813102185123922> channel is there to be informed about the latest updates of the server, such as new roles, new channels or new team members. \n In the <#1038813117179756544> we will announce events, giveaways, tournaments or other announcements that we will do with you as a community. \n Last but not least comes the <#1038813153447919688>, if you are interested in patch-notes about your games, you will find all relevant info here. Last but not least comes the <There is a separate role for each channel, so if you are interested, pick the role and you will always be informed.'
            ),
            EmbedField(
                name='Selfroles',
                value=f'If you want, you can now check out our <#1038813219420110869> channel to choose your own roles. These give your profile that certain something'
            ),
            EmbedField(
                name='Language',
                value=f'In the config channel, you can select the server language. If you realize you would rather be with the English or German community, you can change your role at any time. Just go to the <#1067140820681109575> channel.'
            ),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358552289290/GameDimension_Profile_pic.png?width=616&height=616'),
    embed.set_image(
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358325813289/GameDimension_Banner.png?width=1095&height=616')
    await interaction.respond("Created introduction embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@ bot.slash_command(description="Introduction DE")
async def introductionde(interaction: ApplicationContext):
    embed = Embed(
        title=f'Einführung',
        description='Willkommen auf Game Dimension <:pikachu_love:1042727900996173884> \n \n Wir sind ein Community-Server, wo du mit deinen Freunden Spaß haben kannst.',
        fields=[
            EmbedField(
                name='Regeln',
                value=f'Bevor du anfangen kannst, auf unserem Server Spaß zu haben, musst du unsere Regeln akzeptieren, klicke hier <#1067025598574235648>'
            ),
            EmbedField(
                name='Ankündigungen',
                value=f'Die folgenden drei Channels sind mit die wichtigsten, wenn ihr auf dem Server aktiv seid. Der <#1067026210250559498> Kanal ist dazu da, um über die neuesten Updates des Servers informiert zu werden, wie zum Beispiel neue Rollen, neue Kanäle oder neue Teammitglieder. \n Im <#1038813117179756544> werden wir Events, Giveaways, Turniere oder andere Ankündigungen ankündigen, die wir mit euch als Community machen werden. \n Last but not least kommt die <#1038813153447919688>, wenn ihr an Patch-Notes zu euren Spielen interessiert seid, findet ihr hier alle relevanten Infos. Zu guter Letzt kommt noch der <#10131579198>. Für jeden Kanal gibt es eine eigene Rolle, wenn ihr also Interesse habt, wählt die Rolle und ihr werdet immer informiert.'
            ),
            EmbedField(
                name='Selfroles',
                value=f'Wenn du möchtest, kannst du dir jetzt in unserem <#1038813219420110869>-Kanal deine eigenen Rollen aussuchen. Diese geben deinem Profil das gewisse Etwas'
            ),
            EmbedField(
                name='Sprache',
                value=f'Im config Channel, kannst du die Server Sprache auswählen. Wenn du merkst, du möchtest lieber mit der Englischen oder Deutschen Community sein, dann kannst du deine Rolle jederzeit ändern. Geh dafür einfach in den <#1067140820681109575> Channel.'
            ),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358552289290/GameDimension_Profile_pic.png?width=616&height=616'),
    embed.set_image(
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358325813289/GameDimension_Banner.png?width=1095&height=616')
    await interaction.respond("Created introduction embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@ bot.slash_command(description="Rules EN")
async def rulesen(interaction: ApplicationContext):
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
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358552289290/GameDimension_Profile_pic.png?width=616&height=616'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@bot.slash_command(description="Rules DE")
async def rulesde(interaction: ApplicationContext):
    embed = Embed(
        title=f'Regelwerk',
        description='Mit dem Beitritt zum Game Dimension Server akzeptierst du alle unten stehenden Regeln. Wenn sich jemand nicht an die Regeln hält, melde es bitte an <@&1038814047270866974> oder <@&1038821661224484995> und sie werden es überprüfen.',
        fields=[
            EmbedField(
                name='1) Sei respektvoll', value=f'Sei respektvoll, freundlich und einladend zu allen Mitgliedern auf dem Server, um den Server zu einer angenehmen Erfahrung für alle zu machen. Beleidigungen, Diskriminierung, Mobbing oder unangemessene Reaktionen sind Gründe für einen permanenten Bann.'),
            EmbedField(name='2) Belästigung', value=f'Unterlasse jegliche Form der Belästigung. Wir dulden keinen Rassismus, keine Homophobie, keine Transphobie, keinen Sexismus und keine diskriminierenden Kommentare jeglicher Art. (Dies gilt auch für Belästigungen durch Direktnachrichten).'),
            EmbedField(
                name='3) Werbung', value=f'Mache keine Werbung für deinen/andere Discord-Server oder jede Art von unaufgeforderter Werbung (einschließlich Direktnachrichten).'),
            EmbedField(
                name='4) Streaming von kostenpflichtigen Streaming-Diensten verboten', value=f'Das Streaming von kostenpflichtigen Streaming-Diensten ist verboten und wird mit einer Verwarnung geahndet.'),
            EmbedField(
                name='5) Kanäle für den vorgesehenen Zweck nutzen', value=f'Bitte verwende die Kanäle für den vorgesehenen Zweck. Verwende den Kanal <#1067028493881311292> für normale Gespräche usw.'),
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
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358552289290/GameDimension_Profile_pic.png?width=616&height=616'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@ bot.slash_command(description="Team EN")
async def teamen(interaction: ApplicationContext):
    embed = Embed(
        title=f'Game Dimension Staff',
        fields=[
            EmbedField(
                name='Owner', value=f'『✦』<@480523441439506443> \n『✦』<@479537494384181248>'),
            EmbedField(name='Administrator',
                       value=f'『✦』<@187599309070401541>'),
            # EmbedField(
            #     name='Head Manager', value=f'『✦』<@91665388970311782>'),
            EmbedField(
                name='Manager', value=f'『✦』<@704020919365926983>'),
            EmbedField(
                name='Head Moderator', value=f':incoming_envelope: Is searched (0/1)'),
            EmbedField(
                name='Moderator', value=f'『✦』<@465349397803171841> \n 『✦』<@520696535311188000> \n '),
            EmbedField(
                name='Test-Supporter / Supporter', value=f'『✦』<@694143135101616168> \n 『✦』<@880829080524685402> \n 『✦』<@854034741934161971>'),
            EmbedField(
                name='Content Creator', value=f'『✦』<@612664092741730344> \n 『✦』<@485148322609496074>'),
            EmbedField(
                name='Designer', value=f'『✦』<@353887773088022539> \n \n \n If you need help, feel free to open a <#1038810882349736056> and our staff will take care of your request. \n \n If you want to apply, you can apply under <#1038810904822808726> and get a chance to join the team.'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358552289290/GameDimension_Profile_pic.png?width=616&height=616'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)


@ bot.slash_command(description="Team DE")
async def teamde(interaction: ApplicationContext):
    embed = Embed(
        title=f'Game Dimension Team',
        fields=[
            EmbedField(
                name='Owner', value=f'『✦』<@480523441439506443> \n『✦』<@479537494384181248>'),
            EmbedField(name='Administrator',
                       value=f'『✦』<@187599309070401541>'),
            # EmbedField(
            #     name='Head Manager', value=f'『✦』<@91665388970311782>'),
            EmbedField(
                name='Manager', value=f':incoming_envelope: Is searched (0/1)'),
            EmbedField(
                name='Head Moderator', value=f':incoming_envelope: Is searched (0/1)'),
            EmbedField(
                name='Moderator', value=f'『✦』<@520696535311188000> \n '),
            EmbedField(
                name='Test-Supporter / Supporter', value=f':incoming_envelope: Is searched (0/1)'),
            EmbedField(
                name='Content Creator', value=f':incoming_envelope: Is searched (0/1)'),
            EmbedField(
                name='Designer', value=f':incoming_envelope: Is searched (0/1) \n \n \n Wenn du Hilfe brauchst, kannst du eine <#1067027312308133978> eröffnen und unsere Mitarbeiter werden sich um dein Anliegen kümmern. \n \n Wenn Sie sich bewerben möchten, können Sie sich unter <#1067027382285910026> bewerben und erhalten eine Chance, dem Team beizutreten.'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358552289290/GameDimension_Profile_pic.png?width=616&height=616'),
    await interaction.respond("Created rules embed", ephemeral=True)
    await interaction.channel.send(embed=embed)

# Temp channel Bot "How to use" embed


@ bot.slash_command(description="Instructions to manage your voice call")
async def tempbotinstructions(interaction: ApplicationContext):
    embed = Embed(
        title=f'Instructions to manage your voice call',
        description='Welcome this is our voice channel management bot. You can manage your channel with the buttons above.',
        fields=[
            EmbedField(
                name='1. Example', value=f'Click the lock icon to close your channel from everyone.'),
            EmbedField(
                name='2. Example', value=f'Click pen icon to rename the channel to your activity or set it to your liking.'),
            EmbedField(
                name='3. Example', value=f'Click the crown icon to claim the channel if the owner left the call.'),
            EmbedField(
                name='4. Example', value=f'Click the ban button to ban someone from your voice call.'),
        ],
    )
    embed.set_thumbnail(
        url='https://media.discordapp.net/attachments/1038809022310129765/1068437358552289290/GameDimension_Profile_pic.png?width=616&height=616'),
    await interaction.respond("Instructions to manage your voice call", ephemeral=True)
    await interaction.channel.send(embed=embed)


# Ticket System
@bot.slash_command(description="supportticket")
async def supportticket(interaction: ApplicationContext):
    embed = Embed(
        title=f'Support Ticket',
        description='If you need help, feel free to open one of the following tickets. A team member will be with you in no time.',
    )
    await interaction.respond("Created ticket embed", ephemeral=True)
    await interaction.channel.send(embed=embed, view=SupportTicketCreateView())


@bot.slash_command(description="adminticket")
async def adminticket(interaction: ApplicationContext):
    embed = Embed(
        title=f'Admin Ticket',
        description='If you need help, feel free to open one of the following tickets. A team admin will be with you in no time.',
    )
    await interaction.respond("Created ticket embed", ephemeral=True)
    await interaction.channel.send(embed=embed, view=AddminTicketCreatView())


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


bot.run(TOKEN)
db.connection.close()
