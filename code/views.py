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
        embed = Embed(title="Modal Results", description="test")
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
        # await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView()) <-- Am ende das benutzen
        await ticketchannel.send(f"<@{interaction.user.id}>", embed=embed, view=TicketManageView())


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Where do you need help?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Modal Results")
        embed.add_field(name="Where do you need help?",
                        value=self.children[0].value)
        await interaction.response.send_message(embeds=[embed])


class BotProblemsModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="What bot problem do you have?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Modal Results")
        embed.add_field(name="What bot problem do you have?",
                        value=self.children[0].value)
        await interaction.response.send_message(embeds=[embed])


class TicketCreateView(ui.View):
    @ ui.button(emoji="🚫", label="Report a User", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(ReportUserModal(title="User Report"))

    @ ui.button(emoji="🆘", label="Support", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Support"))

    @ ui.button(emoji="🛠️", label="Bot Problems", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(BotProblemsModal(title="Bot Problems"))
