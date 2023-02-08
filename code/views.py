from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite


# Ticket System

class TicketManageView(ui.View):
    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        staffrole = interaction.guild.get_role(1072489048515559506)
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return
        embed = Embed(title="Ticket Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um dein Ticket.")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar
        await interaction.response.send_message(embed=embed)


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Wo benötigst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Anliegen",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Wo benötigst du Hilfe?", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1072486549909930036)
        staffrole = interaction.guild.get_role(1072489048515559506)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


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
        category = await interaction.guild.fetch_channel(1072486549909930036)
        staffrole = interaction.guild.get_role(1072489048515559506)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


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

        category = await interaction.guild.fetch_channel(1072486549909930036)
        adminrole = interaction.guild.get_role(1072489048515559506)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


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

        category = await interaction.guild.fetch_channel(1072486549909930036)
        adminrole = interaction.guild.get_role(1072489048515559506)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


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

        category = await interaction.guild.fetch_channel(1072486549909930036)
        adminrole = interaction.guild.get_role(1072489048515559506)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


class SupportTicketCreateView(ui.View):
    @ ui.button(emoji="🆘", label="Anliegen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Anliegen"))

    @ ui.button(emoji="📩", label="Team Beschwerde", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(TeamComplaintModal(title="Team Beschwerde"))

    @ ui.button(emoji="📝", label="Bewerbung", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(BewerbungModal(title="Bewerbung"))


class MinecraftTicketCreateView(ui.View):
    @ ui.button(emoji="⛔", label="Spieler Melden", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(ReportUserModal(title="Spieler Melden"))

    @ ui.button(emoji="🆘", label="Minecraft Hilfe", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(MinecraftSupportModal(title="Minecraft Hilfe"))
