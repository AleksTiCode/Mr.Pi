import disnake
from disnake.ext import commands
from app import bot
import sqlite3

class Unmute(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
    
    @commands.slash_command(name='unmute', description='Снять мьют с участника')
    @commands.has_guild_permissions(moderate_members=True)
    async def untimeout(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):   
        try:    
            conn = sqlite3.connect('MrPi.db')
            bd = conn.cursor()
            bd.execute('SELECT log_id, invite FROM servers WHERE guild_id = ?', (inter.guild.id,))
            bd_par = bd.fetchone()
            log_channel = bd_par[0]
            invite = bd_par[1]
            conn.close()

            invite = await bot.fetch_invite(invite)
     
            embed_unmute = disnake.Embed(
                title='Произошло снятие мьюта!!!',
                description=f'У {member.mention} сняли мьют.\nНадеемся, он исправился)',
                color=disnake.Color.from_rgb(0, 77, 255))
            embed_unmute_ls = disnake.Embed(
                title=f'Вас размьютили на сервере {invite.guild.name}',
                description=f'Надеемся, вы исправились)',
                color=disnake.Color.from_rgb(0, 77, 255))
        
            channel = bot.get_channel(int(log_channel))

            await inter.send(content=f'_Успешно\nУчастник {member.mention} размьючен_', ephemeral=True)
            await channel.send(embed=embed_unmute)

            await member.timeout(reason=None, until=None)
            
            try:
                await member.send(embed=embed_unmute_ls)
            except disnake.HTTPException:
                 pass
        except Exception:
            embed_TE = disnake.Embed(
                title='Не удалось(',
                description='Для того, чтобы использовать бота администратор сервера должен его настроить.\nЕсли же бот настроен, то значит в его настройке есть ошибка.\nЕсли же бот настроен правильно, то это может быть связано с тем, что бот не имеет доступа к каналу логов, либо роль бота ниже роли участника, которого надо размьютить\nТакже проверьте разоешения бота: с версии 1.1.2 для бота требуется разрешение "администратор"\nСообщите администратору об этом!',
                color=disnake.Color.from_rgb(255,0,0))
            await inter.send(embed=embed_TE, ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(Unmute(bot))