import coc

from discord.ext import commands
from beautifultable import BeautifulTable

ROYALS_TAG = "#9Y82QPU0"
enemy_log_hidden_status = False

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="warlog")
    async def get_war_log(self, ctx):
        
        war_log = []
        
        temp_warlog = await self.bot.coc.get_warlog(ROYALS_TAG)
        i = 0
        while i < 7:
            war_log.append(temp_warlog[i])
            i += 1

        wincnt = 0
        losecnt = 0
        table = BeautifulTable()
        table.column_headers = ["Win/Lose", "Enemy"]

        # iterate over the wars
        for war in war_log:
            table.append_row([war.result, war.opponent.name])
            
            if war.result == "win":
                wincnt += 1
            else:
                losecnt += 1

        table.set_style(BeautifulTable.STYLE_COMPACT)
        print(f"wins: {wincnt}")
        print(f"loses: {losecnt}")

        await ctx.send(table)

def setup(bot):
    bot.add_cog(General(bot))
