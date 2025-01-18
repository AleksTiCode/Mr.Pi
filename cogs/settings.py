import disnake
from disnake.ext import commands
import sqlite3

class Settings(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name='settings', description='Настройка бота')
    @commands.has_guild_permissions(administrator=True)
    async def set(self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role, report_channel: disnake.TextChannel, logs_channel: disnake.TextChannel, invite_url: str):
            role_id = role.id
            channel_id = report_channel.id
            log_channel_id = logs_channel.id
            
            conn = sqlite3.connect('MrPi.db')
            db = conn.cursor()
            db.execute('INSERT OR REPLACE INTO servers (guild_id,  role_id, channel_id, log_id, invite) VALUES (?,?,?,?,?)', (inter.guild.id, role_id, channel_id, log_channel_id, invite_url))
            conn.commit()
            conn.close()
      
            embed_own = disnake.Embed(
                title='Значения успешно добавлены',
                description='Теперь на сервере можно пользоваться слеш-командоми бота',
                color=disnake.Color.from_rgb(255,255,255))
            await inter.response.send_message(embed=embed_own, ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(Settings(bot))