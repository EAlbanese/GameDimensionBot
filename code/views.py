from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite


class TicketManageView(ui.View):
    @ui.button(label="Close Ticket", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        staffrole = interaction.guild.get_role(1038821661224484995)
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ No permissions!", ephemeral=True)
            return
        embed = Embed(title="Ticket status changed: We're on it!",
                      description=f"<@{interaction.user.id}> is taking care of your ticket.")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar
        await interaction.response.send_message(embed=embed)


class ReportUserModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Which user and why do you want to report him", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="User Report",
                      description="✅ Thank you for contacting support. Our team will take good care of your concern.")
        embed.add_field(
            name="Which user and why do you want to report him", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1038810106260901899)
        staffrole = interaction.guild.get_role(1038821661224484995)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Where do you need help?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Support", description="✅ Thank you for contacting support. Our team will take good care of your concern.")
        embed.add_field(name="Where do you need help?",
                        value=self.children[0].value)
        category = await interaction.guild.fetch_channel(1038810106260901899)
        staffrole = interaction.guild.get_role(1038821661224484995)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


class BotProblemsModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="What bot problem do you have?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Bot Problems",
                      description="✅ Thank you for contacting support. Our team will take good care of your concern.")
        embed.add_field(name="What bot problem do you have?",
                        value=self.children[0].value)
        category = await interaction.guild.fetch_channel(1038810106260901899)
        staffrole = interaction.guild.get_role(1038821661224484995)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


class ApplicationModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="For what role you want to apply?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Application",
                      description="✅ Thank you for applying to join our team. Our staff will take care of your application.")
        embed.add_field(
            name="For what role you want to apply?", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1038810106260901899)
        adminrole = interaction.guild.get_role(1038814047270866974)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


class StreamerModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="What platform are you streaming on?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Streamer",
                      description="✅ Thank you for supporting us through your streams. Our team will take care of this ticket.")
        embed.add_field(
            name="What platform are you streaming on?", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1038810106260901899)
        adminrole = interaction.guild.get_role(1038814047270866974)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


class StaffComplaintModal(ui.Modal):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Who from team do you want to report?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Staff complaint",
                      description="✅ Thank you for creating a ticket and reporting someone on staff. We are sorry and our admins will do the best they can. ")
        embed.add_field(
            name="Who from team do you want to report?", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1038810106260901899)
        adminrole = interaction.guild.get_role(1038814047270866974)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


class SupportTicketCreateView(ui.View):
    @ ui.button(emoji="🚫", label="Report a User", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(ReportUserModal(title="User Report"))

    @ ui.button(emoji="🆘", label="Support", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Support"))

    @ ui.button(emoji="🛠️", label="Bot Problems", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(BotProblemsModal(title="Bot Problems"))


class AddminTicketCreatView(ui.View):
    @ ui.button(emoji="📝", label="Application", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(ReportUserModal(title="Application"))

    @ ui.button(emoji="🎥", label="Streamer", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Streamer"))

    @ ui.button(emoji="⛔", label="Team complaint", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(BotProblemsModal(title="Team complaint"))
