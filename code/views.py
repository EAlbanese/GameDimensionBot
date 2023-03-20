from discord import SelectOption, ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, Client, ChannelType
import database as database
import datetime

client = Client()
db = database.Database("bot.db")


class variableManager(ui.View):
    threadID = 0

# Ticket System


class TicketManageView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button,  interaction: Interaction):
        ticketlogs = await interaction.guild.fetch_channel(1072486758157135922)

        ticketId = db.get_ticket_id_by_channel_id(
            interaction.message.channel.id)
        ticketinfo = db.get_ticket_info(ticketId)
        ticketClosedBy = interaction.guild.get_member(interaction.user.id)
        memberName = interaction.guild.get_member(ticketinfo[2])
        moderatorName = interaction.guild.get_member(ticketinfo[3])

        if ticketinfo[3] is None:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return

        if ticketinfo[3] is interaction.user.id:
            await interaction.response.send_message("⛔ Das Ticket kann nur durch den claimer dieses Ticket geschlossen werden.", ephemeral=True)
            return

        embed = Embed(title=f"🔒 Ticket wurde geschlossen")
        embed.add_field(name="🎫 Ticket ID",
                        value=f'{ticketinfo[0]}', inline=False)
        embed.add_field(name="🎫 Channel ID",
                        value=f'{ticketinfo[1]}', inline=False)
        embed.add_field(name="👤 Ticket geöffnet von",
                        value=f'{memberName}', inline=False)
        embed.add_field(name="✅ Ticket geclaimt von",
                        value=f'{moderatorName}', inline=False)
        embed.add_field(name="🔒 Ticket geschlossen von",
                        value=f'{ticketClosedBy}', inline=False)

        await ticketlogs.send(embed=embed)
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction: Interaction):
        staffrole = interaction.guild.get_role(1072489048515559506)
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return
        embed = Embed(title="Ticket Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um dein Ticket")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar

        ticketId = db.get_ticket_id_by_channel_id(
            interaction.message.channel.id)
        ticketinfo = db.get_ticket_info(ticketId)
        db.update_claimed_ticket(interaction.user.id, ticketinfo[1])

        await interaction.response.send_message(embed=embed)


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Wo benötigst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Anliegen", description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Wo benötigst du Hilfe?",
                        value=self.children[0].value)
        category = await interaction.guild.fetch_channel(1075698931205427262)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id,
                         round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        staffrole = interaction.guild.get_role(1072489048515559506)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{staffrole.id}>", embed=embed, view=TicketManageView())


class TeamComplaintModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Was für eine Team Beschwerde hast du?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Team Beschwerde",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Was für eine Team Beschwerde hast du?",
                        value=self.children[0].value)
        category = await interaction.guild.fetch_channel(1075698931205427262)
        adminrole = interaction.guild.get_role(1075709143207387160)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())


class BewerbungModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Als was möchtest du dich bewerben?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Bewerbung",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Als was möchtest du dich bewerben?", value=self.children[0].value)

        formembed = Embed(title="Bewerbung einreichen",
                          description="Wir bitten dich das folgenden Formular auszufüllen, damit unser Team sich deine Bewerbung anschauen kann.")
        formembed.add_field(
            name='Google Forms:', value='[Bewerbungs Formular](https://forms.gle/mt5sfLnahoHdm3pv6)')
        category = await interaction.guild.fetch_channel(1075698931205427262)
        adminrole = interaction.guild.get_role(1075709143207387160)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())
        await ticketchannel.send(embed=formembed)


class ReportUserModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Welchen Spieler möchtest du melden?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Spieler Melden",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Welchen Spieler möchtest du melden?", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1075698931205427262)
        adminrole = interaction.guild.get_role(1075709143207387160)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())


class MinecraftSupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Wo auf dem Server brauchst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Minecraft Hilfe",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Wo auf dem Server brauchst du Hilfe?", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1075698931205427262)
        adminrole = interaction.guild.get_role(1075709143207387160)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())


class SupportTicketCreateView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ ui.button(emoji="🆘", label="Anliegen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Anliegen"))

    @ ui.button(emoji="📩", label="Team Beschwerde", style=ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(TeamComplaintModal(title="Team Beschwerde"))

    @ ui.button(emoji="📝", label="Bewerbung", style=ButtonStyle.success)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(BewerbungModal(title="Bewerbung"))


class MinecraftTicketCreateView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ ui.button(emoji="⛔", label="Spieler Melden", style=ButtonStyle.danger)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(ReportUserModal(title="Spieler Melden"))

    @ ui.button(emoji="🆘", label="Minecraft Hilfe", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(MinecraftSupportModal(title="Minecraft Hilfe"))


# Bug report
class BugReportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Dein Username (Username#0000)", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Bug Titel", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Wie oft ist das aufgetreten?", style=InputTextStyle.long))
        self.add_item(ui.InputText(
            label="Beschreibe dein Vorgehen bis zum Bug", style=InputTextStyle.short))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="❗ Neuer Bug-Report ❗")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Bug Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Beschreibe dein Vorgehen bis zum Bug", value=self.children[2].value, inline=False)
        embed.add_field(
            name="Wie oft ist das aufgetreten?", value=self.children[3].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"✅ Bug wurde erfolgreich gemeldet. Vielen Dank ❤️", ephemeral=True)
        await draixon.send(embed=embed)


class BugReportCreateView(ui.View):
    @ui.button(emoji="🗑️", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="📬", label="Bug melden", style=ButtonStyle.success)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(BugReportModal(title="Bug melden"))


# Suggestion
class SuggestionModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Dein Username (Username#0000)", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Verbesserungsvorschlag Titel", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Was kann ich verbesser?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="🛠️ Neuer Verbesserungsvorschlag 🛠️")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Verbesserungsvorschlag Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Was kann ich verbesser?", value=self.children[2].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"✅ Vorschlag wurde erfolgreich eingereicht. Vielen Dank ❤️", ephemeral=True)
        await draixon.send(embed=embed)


class SuggestionView(ui.View):
    @ui.button(emoji="🗑️", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="📬", label="Vorschlag erstellen", style=ButtonStyle.success)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(SuggestionModal(title="Vorschlag erstellen"))


# Entbannungsantrag

class AppealManageView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Antrag schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button,  interaction: Interaction):
        appeallogs = await interaction.guild.fetch_channel(1081255325476323458)

        appealId = db.get_appeal_id_by_channel_id(
            interaction.message.channel.id)
        appealinfo = db.get_appeal_info(appealId)
        appealClosedBy = interaction.guild.get_member(interaction.user.id)
        memberName = interaction.guild.get_member(appealinfo[2])
        moderatorName = interaction.guild.get_member(appealinfo[3])

        embed = Embed(title=f"🔒 Entbannungsantrag wurde geschlossen")
        embed.add_field(name="🎫 Antrag ID",
                        value=f'{appealinfo[0]}', inline=False)
        embed.add_field(name="🎫 Channel ID",
                        value=f'{appealinfo[1]}', inline=False)
        embed.add_field(name="👤 Antrag geöffnet von",
                        value=f'{memberName}', inline=False)
        embed.add_field(name="✅ Antrag geclaimt von",
                        value=f'{moderatorName}', inline=False)
        embed.add_field(name="🔒 Antrag geschlossen von",
                        value=f'{appealClosedBy}', inline=False)

        await appeallogs.send(embed=embed)
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Antrag", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction: Interaction):
        staffrole = interaction.guild.get_role(1081267406325948446)
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return

        appealId = db.get_appeal_id_by_channel_id(
            interaction.message.channel.id)
        appealinfo = db.get_appeal_info(appealId)
        db.update_claimed_appeal(interaction.user.display_name, appealinfo[1])

        embed = Embed(title="Antrag Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um deinen Antrag")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar

        appealId = db.get_appeal_id_by_channel_id(
            interaction.message.channel.id)
        appealinfo = db.get_appeal_info(appealId)
        db.update_claimed_appeal(interaction.user.id, appealinfo[1])

        await interaction.response.send_message(embed=embed)


class BanappealModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Dein Username (Username#0000)", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Wieso bist du auf unserem Discord Server?", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Wieso möchtest du entbannt werden?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="📬 Entbannungantrag 📬")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Wieso bist du auf unserem Discord Server?", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Entbannungsantrag", value=self.children[2].value + "\n\n ✅ Unser Team wird sich in kürze darum kümmern!", inline=False)

        category = await interaction.guild.fetch_channel(1081265979398570095)
        staffrole = interaction.guild.get_role(1081267406325948446)

        create_date = datetime.datetime.now()
        db.create_appeal(interaction.user.id, round(create_date.timestamp()))
        count = db.get_appeal_id(round(create_date.timestamp()))

        appealchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })

        db.update_appeal(appealchannel.id, count)

        await interaction.response.send_message(f"Entbannungsantrag eröffnet in <#{appealchannel.id}>", ephemeral=True)
        await appealchannel.send(f"<@{interaction.user.id}> <@&{staffrole.id}>", embed=embed, view=AppealManageView())


class BannappealView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(emoji="📬", label="Entbannungsantrag", style=ButtonStyle.primary)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(BanappealModal(title="Entbannungsantrag schreiben"))


# Ticket Unban Server
class UnbanTicketManageView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button,  interaction: Interaction):
        ticketlogs = await interaction.guild.fetch_channel(1081255258119995482)

        ticketId = db.get_ticket_id_by_channel_id(
            interaction.message.channel.id)
        ticketinfo = db.get_ticket_info(ticketId)
        ticketClosedBy = interaction.guild.get_member(interaction.user.id)
        memberName = interaction.guild.get_member(ticketinfo[2])
        moderatorName = interaction.guild.get_member(ticketinfo[3])

        embed = Embed(title=f"🔒 Ticket wurde geschlossen")
        embed.add_field(name="🎫 Ticket ID",
                        value=f'{ticketinfo[0]}', inline=False)
        embed.add_field(name="🎫 Channel ID",
                        value=f'{ticketinfo[1]}', inline=False)
        embed.add_field(name="👤 Ticket geöffnet von",
                        value=f'{memberName}', inline=False)
        embed.add_field(name="✅ Ticket geclaimt von",
                        value=f'{moderatorName}', inline=False)
        embed.add_field(name="🔒 Ticket geschlossen von",
                        value=f'{ticketClosedBy}', inline=False)

        await ticketlogs.send(embed=embed)
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction: Interaction):
        staffrole = interaction.guild.get_role(1081267406325948446)
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return
        embed = Embed(title="Ticket Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um dein Ticket")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar

        ticketId = db.get_ticket_id_by_channel_id(
            interaction.message.channel.id)
        ticketinfo = db.get_ticket_info(ticketId)
        db.update_claimed_ticket(interaction.user.id, ticketinfo[1])

        await interaction.response.send_message(embed=embed)


class UnbanSupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Wo benötigst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Anliegen", description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Wo benötigst du Hilfe?",
                        value=self.children[0].value)
        category = await interaction.guild.fetch_channel(1081265751064850553)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id,
                         round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        staffrole = interaction.guild.get_role(1081267406325948446)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{staffrole.id}>", embed=embed, view=UnbanTicketManageView())


class UnbanSupportTicketCreateView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ ui.button(emoji="📩", label="Anliegen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(UnbanSupportModal(title="Anliegen"))


# Booster Rollen Dropdown
class BoosterRolesView(ui.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

    @ui.select(
        placeholder="Suche dir eine Booster Rolle aus",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label="🤍",
                value='1'
            ),
            SelectOption(
                label="💙",
                value='2'
            ),
            SelectOption(
                label="🖤",
                value='3'
            ),
            SelectOption(
                label="🧡",
                value='4'
            ),
            SelectOption(
                label="💛",
                value='5'
            ),
            SelectOption(
                label="💜",
                value='6'
            ),
        ]
    )
    async def select_callback(self, select, interaction: Interaction):
        await interaction.response.defer()
        snowwhite = interaction.guild.get_role(1085473900730777610)
        iceblue = interaction.guild.get_role(1085474000421007360)
        blacksoul = interaction.guild.get_role(1085474119711211520)
        orange = interaction.guild.get_role(1085474235679522826)
        gelb = interaction.guild.get_role(1085474425249480724)
        pink = interaction.guild.get_role(1085474511853453352)
        if select.values[0] == "1":
            if iceblue in interaction.user.roles or blacksoul in interaction.user.roles or orange in interaction.user.roles or gelb in interaction.user.roles or pink in interaction.user.roles:
                await interaction.user.remove_roles(iceblue)
                await interaction.user.remove_roles(blacksoul)
                await interaction.user.remove_roles(orange)
                await interaction.user.remove_roles(gelb)
                await interaction.user.remove_roles(pink)
                await interaction.user.add_roles(snowwhite)
                await interaction.followup.send(f"✅ Du hast die <@&1085473900730777610> Rolle erhalten.", ephemeral=True)
        if select.values[0] == "2":
            if snowwhite in interaction.user.roles or blacksoul in interaction.user.roles or orange in interaction.user.roles or gelb in interaction.user.roles or pink in interaction.user.roles:
                await interaction.user.remove_roles(snowwhite)
                await interaction.user.remove_roles(blacksoul)
                await interaction.user.remove_roles(orange)
                await interaction.user.remove_roles(gelb)
                await interaction.user.remove_roles(pink)
                await interaction.user.add_roles(iceblue)
                await interaction.followup.send(f"✅ Du hast die <@&1085474000421007360> Rolle erhalten.", ephemeral=True)
        if select.values[0] == "3":
            if snowwhite in interaction.user.roles or iceblue in interaction.user.roles or iceblue in interaction.user.roles or gelb in interaction.user.roles or pink in interaction.user.roles:
                await interaction.user.remove_roles(snowwhite)
                await interaction.user.remove_roles(iceblue)
                await interaction.user.remove_roles(orange)
                await interaction.user.remove_roles(gelb)
                await interaction.user.remove_roles(pink)
                await interaction.user.add_roles(blacksoul)
                await interaction.followup.send(f"✅ Du hast die <@&1085474119711211520> Rolle erhalten.", ephemeral=True)
        if select.values[0] == "4":
            if snowwhite in interaction.user.roles or blacksoul in interaction.user.roles or iceblue in interaction.user.roles or gelb in interaction.user.roles or pink in interaction.user.roles:
                await interaction.user.remove_roles(snowwhite)
                await interaction.user.remove_roles(blacksoul)
                await interaction.user.remove_roles(iceblue)
                await interaction.user.remove_roles(gelb)
                await interaction.user.remove_roles(pink)
                await interaction.user.add_roles(orange)
                await interaction.followup.send(f"✅ Du hast die <@&1085474235679522826> Rolle erhalten.", ephemeral=True)
        if select.values[0] == "5":
            if snowwhite in interaction.user.roles or blacksoul in interaction.user.roles or orange in interaction.user.roles or iceblue in interaction.user.roles or pink in interaction.user.roles:
                await interaction.user.remove_roles(snowwhite)
                await interaction.user.remove_roles(blacksoul)
                await interaction.user.remove_roles(orange)
                await interaction.user.remove_roles(iceblue)
                await interaction.user.remove_roles(pink)
                await interaction.user.add_roles(gelb)
                await interaction.followup.send(f"✅ Du hast die <@&1085474425249480724> Rolle erhalten.", ephemeral=True)
        if select.values[0] == "6":
            if snowwhite in interaction.user.roles or blacksoul in interaction.user.roles or orange in interaction.user.roles or gelb in interaction.user.roles or iceblue in interaction.user.roles:
                await interaction.user.remove_roles(snowwhite)
                await interaction.user.remove_roles(blacksoul)
                await interaction.user.remove_roles(orange)
                await interaction.user.remove_roles(gelb)
                await interaction.user.remove_roles(iceblue)
                await interaction.user.add_roles(pink)
                await interaction.followup.send(f"✅ Du hast die <@&1085474511853453352> Rolle erhalten.", ephemeral=True)
