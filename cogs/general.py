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
        
        warLog = []
        
        tempWarLog = await self.bot.coc.get_warlog(ROYALS_TAG)
        i = 0
        while i < 7:
            warLog.append(tempWarLog[i])
            i += 1

        losecnt = 0
        table = BeautifulTable()
        table.column_headers = ["Win/Lose", "Enemy"]

        # iterate over the wars
        for war in warLog:
            table.append_row([war.result, war.opponent.name])
            
            if war.result == "lose":
                losecnt += 1

        table.set_style(BeautifulTable.STYLE_COMPACT)
        print(f"loses: {losecnt}")

        await ctx.send(table)

    @commands.command(name="whowins")
    async def who_wins(self, ctx):
        currentWar = await self.bot.coc.get_clan_war(ROYALS_TAG)
        ourResults = []
        enemyResults = []
        ourLoseCnt = 0
        enemyLoseCnt = 0
        enemy_tag = ""

        if currentWar.state == "notinWar":
            await ctx.send("Royals is not in war")
            return
        elif currentWar.state == "inWar" or currentWar.state == "preparation":
            enemy_tag = currentWar.opponent.tag
        
            tempWarLogUs = await self.bot.coc.get_warlog(ROYALS_TAG)
            tempWarLogEnemy = await self.bot.coc.get_warlog(enemy_tag)

            i = 0
            while i < 7:
                ourResults.append(tempWarLogUs[i].result)
                i += 1

            for result in ourResults:
                if result == "lose":
                    ourLoseCnt += 1

            i = 0
            while i < 7:
                enemyResults.append(tempWarLogEnemy[i].result)
                i += 1

            for result in enemyResults:
                if result == "lose":
                    enemyLoseCnt += 1

            if ourLoseCnt > enemyLoseCnt:
                await ctx.send("Royals is winning their war with {0}".format(currentWar.opponent.name))
            elif ourLoseCnt < enemyLoseCnt:
                await ctx.send("Royals is losing their war with {0}".format(currentWar.opponent.name))
            else:
                await ctx.send("Your lose counts are the same")
        
def setup(bot):
    bot.add_cog(General(bot))
