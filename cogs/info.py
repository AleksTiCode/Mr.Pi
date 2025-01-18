import disnake
from disnake.ext import commands

class Info(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name='info', description='Информация о боте')
    async def infobot(self, inter: disnake.ApplicationCommandInteraction):
        embed_info = disnake.Embed(
            title='Info Mr.Pi bot',
            description='**V: 1.2.0**\nХозяин и создатель: Kat Dev\nКод бота на GitHub: [тык](https://github.com/AleksTiGit/Report-Discord-Bot)\nСервер поддержки: [тык](https://discord.com/invite/nHD8bpdvR4)',
            color=disnake.Color.from_rgb(255,255,255))
        await inter.response.send_message(embed=embed_info)

def setup(bot: commands.InteractionBot):
    bot.add_cog(Info(bot))