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
        ourWarLog = []
        enemyWarLog = []
        ourLoseCnt = 0
        enemyLoseCnt = 0
        enemy_tag = ""

        if currentWar.state == "notinWar":
            await ctx.send("Royals is not in war")
            return
        elif currentWar.state == "inWar" or currentWar.state == "preparation":
            enemyTag = currentWar.opponent.tag
            enemyInfo = await self.bot.coc.get_clan(enemyTag)

            if "FWA" in enemyInfo.description:
        
                tempWarLogUs = await self.bot.coc.get_warlog(ROYALS_TAG)
                tempWarLogEnemy = await self.bot.coc.get_warlog(enemyTag)

                parentTable = BeautifulTable()
                warLogTableUs = BeautifulTable()
                warLogTableEnemy = BeautifulTable()
                parentTable.column_headers = ["Jesters Royals", currentWar.opponent.name]

                # Us calculations
                i = 0
                while i < 7:
                    ourWarLog.append(tempWarLogUs[i])
                    i += 1

                for war in ourWarLog:
                    warLogTableUs.append_row([war.result, war.opponent.name])
                    if war.result == "lose":
                        ourLoseCnt += 1

                # Enemy calculations
                i = 0
                while i < 7:
                    enemyWarLog.append(tempWarLogEnemy[i])
                    i += 1

                for war in enemyWarLog:
                    warLogTableEnemy.append_row([war.result, war.opponent.name])
                    if war.result == "lose":
                        enemyLoseCnt += 1
                
                parentTable.append_row([warLogTableUs, warLogTableEnemy])
                await ctx.send(parentTable)

                # Display winner base on lose count
                if ourLoseCnt > enemyLoseCnt:
                    await ctx.send("Congrats an FWA Clan!! Royals is winning their war with {0}".format(currentWar.opponent.name))
                    return
                elif ourLoseCnt < enemyLoseCnt:
                    await ctx.send("Congrats an FWA Clan!! Royals is losing their war with {0}".format(currentWar.opponent.name))
                    return
                else:
                    await ctx.send("Congrats an FWA Clan!! Your lose counts are the same")
                    return
            else:
                await ctx.send("Sorry! Enemy Clan is not FWA")
                return
        
def setup(bot):
    bot.add_cog(General(bot))
