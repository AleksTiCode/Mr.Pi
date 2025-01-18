import disnake
from disnake.ext import commands
import sqlite3
from app import bot

class Report(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name='report', description='Подать жалобу')
    async def report(inter: disnake.ApplicationCommandInteraction, link: str):
        try:    
            conn = sqlite3.connect('MrPi.db')
            bd = conn.cursor()
            bd.execute('SELECT role_id, channel_id FROM servers WHERE guild_id = ?', (inter.guild.id,))
            bd_par = bd.fetchone()
            role_id = bd_par[0]
            rep_channel = bd_par[1]
            conn.close()


            embed_chat = disnake.Embed(
                title='Репорт отправлен',
                description='Стафф ближайшем времени накажет нарушителя',
                color=disnake.Color.from_rgb(0, 77, 255))
        

            embed_report = disnake.Embed(title = 'Репорт',
                          description =f'[Ссылка на сообщение нарушителя]({link})\n<@&{int(role_id)}> примите меры',
                          color=disnake.Color.from_rgb(255,0,0))
    
            await inter.send(embed=embed_chat, ephemeral=True)
            channel = bot.get_channel(int(rep_channel))
            await channel.send(embed=embed_report)
        except Exception:
            embed_TE = disnake.Embed(
                title='Не удалось(',
                description='Для того, чтобы использовать бота администратор сервера должен его настроить.\nЕсли же бот настроен, то значит в его настройке есть ошибка.\nЕсли же бот настроен правильно, то это может быть связано с тем, что бот не имеет доступа к каналу репортов\nТакже проверьте разоешения бота: с версии 1.1.2 для бота требуется разрешение "администратор"\nСообщите администратору об этом!',
                color=disnake.Color.from_rgb(255,0,0))
            await inter.send(embed=embed_TE, ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(Report(bot))