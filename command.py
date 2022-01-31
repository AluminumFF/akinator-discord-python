@client.command(aliases=["aki"])
async def akinator(ctx):
    aki = Akinator()
    first = await ctx.send("Processing...")
    q = await aki.start_game()
    skirt = aki.step

    game_embed = discord.Embed(title=f"**AkiNaTor!**", description=q, color=discord.Color.blurple())
    game_embed.set_footer(text=f"Wait for Hiro to add reactions before you give your response.")

    option_map = {'✅': 'y', '❌':'n', '🤷‍♂️':'p', '😕':'pn', '⁉️': 'i'}
    """You can pick any emojis for the responses, I just chose what seemed to make sense.
      '✅' -> YES, '❌'-> NO, '🤷‍♂️'-> PROBABLY YES, '😕'-> PROBABLY NO, '⁉️'->IDK, '😔'-> force end game, '◀️'-> previous question"""
      
    def option_check(reaction, user):   #a check function which takes the user's response
            return user==ctx.author and reaction.emoji in ['✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔', '◀️']
    count = 0 
    while aki.progression <= 100:    #this is aki's certainty level on an answer, per say. 80 seems to be a good number.
        if count == 0:
            await first.delete()      #deleting the message which said "Processing.."
            count += 1
            
        game_message = await ctx.send(embed=game_embed)
           

        for emoji in ['✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔', '◀️']:
            await game_message.add_reaction(emoji)

        option, _ = await client.wait_for('reaction_add', check=option_check, timeout=360)     #taking user's response
        if option.emoji == '😔':
            embed=discord.Embed(description="**Game Ended!**", color=0x00ffff)
            return await game_message.edit(embed=embed)
        async with ctx.channel.typing():
            if option.emoji == '◀️': 
                try:
                    q = await aki.back()
                except:   #excepting trying-to-go-beyond-first-question error
                    pass
                #editing embed for next question
                game_embed = discord.Embed(title=f"**AkiNaTor**", description=q, color=discord.Color.blurple())
                continue
            else:
                q = await aki.answer(option_map[option.emoji])
                #editing embed for next question
                game_embed = discord.Embed(title=f"**AkiNaTor!**", description=q, color=discord.Color.blurple())
                continue

    await aki.win()

    result_embed = discord.Embed(title="My guess....", colour=discord.Color.dark_blue())
    result_embed.add_field(name=f"My first guess is **{aki.first_guess['name']}**", value=aki.first_guess['description'], inline=False)
    result_embed.set_footer(text="Was I right? Add the reaction accordingly.")
    result_embed.set_image(url=aki.first_guess['absolute_picture_path'])
    result_message = await ctx.send(embed=result_embed)
    for emoji in ['✅', '❌']:
        await result_message.add_reaction(emoji)

    option, _ = await client.wait_for('reaction_add', check=option_check, timeout=120)
    if option.emoji ==  '✅':
        final_embed = discord.Embed(title="I'm A Genius", color=discord.Color.green())
    elif option.emoji == '❌':
        final_embed = discord.Embed(title="Oof", description="Maybe try again?", color=discord.Color.red())   
       #this does not restart/continue a game from where it was left off, but you can program that in if you like.
       
    return await ctx.send(embed=final_embed)
