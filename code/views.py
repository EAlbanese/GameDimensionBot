from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed


class TicketCreateView(ui.View):
    @ui.button(emoji="🚫", label="Report a User", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @ui.button(emoji="🆘", label="Support", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @ui.button(emoji="🛠️", label="Bot Problems", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")


class MyModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(label="Short Input"))
        self.add_item(ui.InputText(
            label="Long Input", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])
