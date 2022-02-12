from csv import DictWriter

headersCSV = ['level', 'total_xp', 'id', 'username', 'discriminator', 'avatar', 'message_count', 'XP/LEVEL', 'level_requirement']
dict={'level':'1','id':'yes'}
with open('mee6data(Formated test).csv', 'a', newline='') as f_object:
    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
    dictwriter_object.writerow(dict)
    # Close the file object
    f_object.close()

bot = True

if bot == False: #not a bot
    
    
    if newUser: #new user means id is not in csv
        x = 1
        #level 1, total xp add random xp between 15-25, id, username and discrimator from id,
        #avatar from id, message 1, xp = total xp, level_requirement = 100, percentage = total / 100, last message = time.now

    if newMessage: #no message sent in the current minute
        #update last_message time

        #give random amount of xp and update total and XP/Level
        

        if levelUp: #if xp is higher than level requirement
            #reset xp to xp minus old level requirement
            x = 1
            #update level requirement

        #update percent total / level requirement

        if roleReward: #level meets roleReward requirement
            #give role
            x = 1
            

