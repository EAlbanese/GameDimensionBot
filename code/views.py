from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, Client, ChannelType
import database as database
import datetime

client = Client()
db = database.Database("bot.db")


class variableManager(ui.View):
    threadID = 0

# Ticket System


class TicketManageView(ui.View):
    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button,  interaction: Interaction):
        channel = await interaction.guild.fetch_channel(1072486758157135922)

        threadId = db.get_ticket_thread_id()
        thread = interaction.guild.get_thread(threadId)

        ticketId = db.get_ticket_id(threadId)
        ticketinfo = db.get_ticket_info(ticketId)
        ticketClosedBy = interaction.user.display_name
        memberName = interaction.guild.get_member(ticketinfo[2])
        moderatorName = interaction.guild.get_member(ticketinfo[3])

        embed = Embed(title=f"🔒 Ticket wurde geschlossen")
        embed.add_field(name="🎫 Ticket ID",
                        value=f'{ticketinfo[0]} \n\n **🎫 Thread ID** \n {ticketinfo[1]} \n\n **👤 Ticket geöffnet von** \n {memberName} \n\n **✅ Ticket geclaimt von** \n {moderatorName} \n\n **🔒 Ticket geschlossen von** \n {ticketClosedBy}')

        await channel.send(embed=embed, view=TicketLogsView())
        await thread.edit(archived=True, locked=True)
        await interaction.response.defer()


class TicketLogsView(ui.View):
    @ui.button(label="🔓 Ticket erneut öffnen", style=ButtonStyle.primary)
    async def reopenTicket(self, button,  interaction: Interaction):
        threadId = db.get_ticket_thread_id()
        thread = interaction.guild.get_thread(threadId)

        await thread.edit(archived=False, locked=False)
        await interaction.response.send_message(f"<#{thread.id}> Ticket wurde wieder geöffnet", ephemeral=True)


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Wo benötigst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Anliegen", description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Wo benötigst du Hilfe?",
                        value=self.children[0].value)
        channel = await interaction.guild.fetch_channel(1072473811162771486)

        create_date = datetime.datetime.now()
        print(create_date)
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(create_date.timestamp())

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{1072489048515559506}>", embed=embed, view=TicketManageView())


class TeamComplaintModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Was für eine Team Beschwerde hast du?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Team Beschwerde",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Was für eine Team Beschwerde hast du?",
                        value=self.children[0].value)
        channel = await interaction.guild.fetch_channel(1072473811162771486)
        manager = interaction.guild.get_role(1072487643255951360)
        admin = interaction.guild.get_role(1072487454101209148)
        owner = interaction.guild.get_role(1072487003632971838)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(create_date)

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{manager.id}> <@&{admin.id}> <@&{owner.id}>", embed=embed, view=TicketManageView())


class BewerbungModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Als was möchtest du dich bewerben?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Bewerbung",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Als was möchtest du dich bewerben?", value=self.children[0].value)

        channel = await interaction.guild.fetch_channel(1072473811162771486)
        adminrole = interaction.guild.get_role(1072489048515559506)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(create_date)

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())


class ReportUserModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Welchen Spieler möchtest du melden?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Spieler Melden",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Welchen Spieler möchtest du melden?", value=self.children[0].value)

        channel = await interaction.guild.fetch_channel(1072479021008429066)
        adminrole = interaction.guild.get_role(1072489048515559506)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(create_date)

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())


class MinecraftSupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Wo brauchst du auf dem Minecraft Server Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Minecraft Hilfe",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Wo brauchst du auf dem Minecraft Server Hilfe?", value=self.children[0].value)

        channel = await interaction.guild.fetch_channel(1072479021008429066)
        adminrole = interaction.guild.get_role(1072489048515559506)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(create_date)

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())


class SupportTicketCreateView(ui.View):
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
