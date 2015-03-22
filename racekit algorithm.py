########################
##                    ##
##     Luke Melo      ##
##   Racer Tool Kit   ##
##  Random Algorithm  ##
##    Melo Classic    ##
##                    ##
########################

import random

###
open_heats = {}
junior_heats = {}

## new rider library is a library seeing if there in juniors and their scores
new_rider_library = {}

## heat_dict is the final correct heat database
heat_dict = {}

## rider library for number/person combinations
rider_library = {}

## listof rounds 
rbn_rounds = []

######################################################################

def bracket_gen(power):
    if power == 1:
        return [[1,2]]
    elif power == 2:
        return [[1,4],[3,2]]
    base_list = map(lambda x: x+1 ,range(2**power))[:2**power / 2]
    c_down = 2**power
    index = 0
    for i in base_list:
        base_list[index] = [i,c_down-index]
        index+=1
    rnd = []
    index_front = 0
    index_end = -1
    for i in base_list:
        rnd = rnd + [[base_list[index_front],base_list[index_end]]]
        index_front+=1
        index_end-=1
    rnd = rnd[:len(rnd)/2]        
    index_front = 0
    index_end = -1
    for i in rnd:
        rnd[index_front] += rnd[index_end]
        index_front+=1
        index_end-=1
    rnd = rnd[:len(rnd)/2]
    while len(rnd) != 1:
        index = 0
        middle = len(rnd)/2
        for i in rnd[:middle]:
            rnd[index] += rnd[index+middle]
            index+=1
        rnd = rnd[:middle]       
    rnd = rnd[0]
    n_rnd = []
    for i in rnd:
        n_rnd+=i
    return n_rnd

######################################################################

def bracket_32(rl,bl,category,num):
    f=file('bracket export '+ category + str(num) + '.csv', 'w')
    wlist=[]
    index=0
    bval = 0
    wlist+=['\r\r']
    for i in bl:
        if not(new_rider_library.has_key(i-1)):
            wlist+=['BYE\r']
            bval+=1
            if bval == 2:
                wlist+=['\r\r']
                bval = 0
        else:
            wlist+=['(' + str(rl[i-1]) + ') ' + \
                    new_rider_library[(rl[i-1])][0] + '\r']
            bval+=1
            if bval == 2:
                wlist+=['\r\r']
                bval = 0
        index+=1
    f.writelines(wlist)
    f.close

######################################################################

def bracket_export(rl,exp,category):
    bl = bracket_gen(exp)
    if len(bl) <= 32:
        bracket_32(rl,bl,category,1)
    else:
        rls = []
        index = 0
        end = 32
        while end <= len(rl):
            rls+=[rl[index:end]]
            index+=32
            end+=32
        bls = []
        index = 0
        end = 32
        while end <= len(bl):
            bls+=[bl[index:end]]
            index+=32
            end+=32
        l=range((len(bl)/32))
        index = 0
        for i in l:
            bracket_32(rl,bls[index],category,index+1)
            index+=1

######################################################################

def round_robin_import():
    global new_rider_library
    global open_heats
    global junior_heats
    race_data_csv = 'round robin race data.csv'
    try:
        f=file(race_data_csv, 'r')
        csv= f.readlines()
        f.close
    except:
        print "Dude you're blowing it. Get your shit together or give the computer to Luke!"
    index = 0
    for i in csv:
        csv[index]=i.split("\r\n")[0]
        index +=1
    csv=csv[1:]
    index = 0
    for i in csv:
        csv[index] = i.split(',')
        index+=1
    for i in csv:
        new_rider_library[int(i[0])].append(int(i[-1]))
    for i in new_rider_library:
        if new_rider_library[i][1] == 'Y':
            if junior_heats.has_key(new_rider_library[i][-1]):
                junior_heats[new_rider_library[i][-1]] += [i]
            else:
                junior_heats[new_rider_library[i][-1]] = [i]
    for i in new_rider_library:
        if open_heats.has_key(new_rider_library[i][-1]):
            open_heats[new_rider_library[i][-1]] += [i] 
        else:
            open_heats[new_rider_library[i][-1]] = [i]
    ol = []
    for i in open_heats:
        rlist_final = []
        rlist = open_heats[i]
        while len(rlist)>1:
            pick=random.randint(0,len(rlist)-1)
            rlist_final.append(rlist[pick])
            rlist.pop(pick)
        rlist_final.append(rlist[0])
        ol = rlist_final + ol
    f1=file('open qualifying results.csv', 'w')
    f1.writelines(['Qualifying Position,','Rider #,','Name\r'])
    wlist = range(1,len(ol)+1)
    index = 0
    for i in wlist:
        wlist[index] = str(index+1) + ',' + '(' + str(ol[index]) + ')' + ',' \
             + rider_library[str(ol[index])] + ',\r'
        index+=1
    f1.writelines(wlist)
    f1.close
    jl = []
    for i in junior_heats:
        rlist_final = []
        rlist = junior_heats[i]
        while len(rlist)>1:
            pick=random.randint(0,len(rlist)-1)
            rlist_final.append(rlist[pick])
            rlist.pop(pick)
        rlist_final.append(rlist[0])
        jl = rlist_final + jl
    f2=file('juniors qualifying results.csv', 'w')
    f2.writelines(['Qualifying Position,','Rider #,','Name\r'])
    wlist = range(1,len(jl)+1)
    index = 0
    for i in wlist:
        wlist[index] = str(index+1) + ',' + '(' + str(jl[index]) + ')' + ',' \
             + rider_library[str(jl[index])] + ',\r'
        index+=1
    f2.writelines(wlist)
    f2.close
    power = 1
    while not(2**power >= len(ol)):
        power += 1
    bracket_export(ol,power,'open')
    power = 1
    while not(2**power >= len(jl)):
        power += 1
    bracket_export(jl,power,'jr')
    

######################################################################

def transpose(m):
    mT=[]
    for i in m[0]:
        mT.append([i])
    for row in m[1:]:
        index=0
        for n in row:
            mT[index].append(n)
            index += 1    
    return mT

######################################################################

def heat_gen(n_riders):
    global heat_dict
    x = n_riders
    rider_list = range(x + x%2)
    n_rounds=int(raw_input('How many rounds? [>0]:'))
    if n_rounds == 0:
        return None
    if heat_dict == {}:
        for i in rider_list:
            heat_dict[i] = []
    index = 0
    ## match_possible is a possible heat lineup pending duplicate races
    match_possible = {}
    while n_rounds > index:
        magic_hat = range(x)        
        while magic_hat != []:
            ld1=random.randint(0,len(magic_hat)-1)
            ld2=random.randint(0,len(magic_hat)-1)
            if ld1 != ld2:
                draw1 = magic_hat[ld1]
                draw2 = magic_hat[ld2]
                match_possible[draw1] = draw2
                match_possible[draw2] = draw1
                if ld1>ld2:
                    magic_hat.pop(ld1)
                    magic_hat.pop(ld2)
                else:
                    magic_hat.pop(ld2)
                    magic_hat.pop(ld1)
        check = True
        for i in match_possible:
            if match_possible[i] in heat_dict[i]:
                check = False
        if check:
            index+=1
            for i in match_possible:
                (heat_dict[i]).append(match_possible[i])
        match_possible={}
        f=file('raw rider matchups.dict', 'w')
        f.writelines(str(heat_dict))
        f.close
    return heat_dict

######################################################################

def round_robin_shuffle():
    global heat_dict
    global rider_library
    global rbn_rounds
    index_max = len(heat_dict[0])
    index = 0
    n_previous = 0
    while index != index_max:
        if len(rbn_rounds) > index:
            index +=1
            n_previous +=1
        else:
            rbn_rounds.append([])
            for i in heat_dict:
                (rbn_rounds[index]).append([i,(heat_dict[i])[index]])
            index +=1
    heat_indx = 0
    for heat in rbn_rounds:
        heats_new = []
        for pair in heat:
            if pair[0] < pair[1]:
                heats_new.append([pair[0],pair[1]])
        rbn_rounds[heat_indx] = heats_new
        heat_indx+=1
    heat_index = n_previous
    for heat in rbn_rounds[heat_index:]:
        shuffled = [heat[0]]
        for pair in heat[1:]:            
            shuffled.insert(random.randint(0,len(shuffled)-1),pair)
        rbn_rounds[heat_index] = shuffled
        heat_index +=1
    rbn_rounds = transpose(rbn_rounds)
    f0=file('raw heats.array', 'w')
    f0.writelines(str(rbn_rounds))
    f0.close
    f=file('round robin heats info.csv','w')
    f.writelines(map(lambda x: "Heat #" + str(x+1) + ",", \
                                range(len(heat_dict[0]))))
    f.writelines('\r')    
    for heat_num in rbn_rounds:
        for i in heat_num:           
            f.writelines(['(',str(i[0]),') ',rider_library[str(i[0])],' vs. ', \
                         '(',str(i[1]),') ',rider_library[str(i[1])],","])
        f.writelines(['\r'])
    f.close
    rbn_rounds = transpose(rbn_rounds)
    
######################################################################

def signup_import():
    global rider_library
    global heat_dict
    global new_rider_library
    rider_lst_csv = 'Rider List.csv'
    try:
        f=file(rider_lst_csv, 'r')
        csv= f.readlines()
        f.close
    except:
        print "Dude you're blowing it. Get your shit together or give the computer to Luke!"
    for i in csv:
        csv=i.split("\r")
    index = 0
    while index < len(csv):
        csv[index] = (csv[index]).split(',')
        index+=1
    for i in csv[1:]:
        rider_library[i[1]] = i[0]
    if len(rider_library)%2 != 0:
        rider_library[str(len(rider_library))] = 'Patrick Switzer'
    heat_gen(len(rider_library))
    write_lst = []
    f2=file('round robin racer info.csv','w')
    f2.writelines(['Racer #,','Racer,'])
    f2.writelines(map(lambda x: "Heat #" + str(x+1) + ",", \
                                range(len(heat_dict[0]))))
    f2.writelines('\r')
    for i in heat_dict:
        f2.writelines([str(i),",",rider_library[str(i)],","])
        max_in = len(heat_dict[i])-1
        index = 0
        while index != max_in:
            f2.writelines([rider_library[str(heat_dict[i][index])], ","])
            index+=1
        f2.writelines([rider_library[str(heat_dict[i][max_in])],"\r"])
    f2.close    
    f3=file('round robin race data.csv', 'w')
    f3.writelines(['Racer #,','Racer,'])
    f3.writelines(map(lambda x: "Heat #" + str(x+1) + ",", \
                                range(len(heat_dict[0]))))
    f3.writelines(['Total Wins:','\r'])
    for i in heat_dict:
        f3.writelines([str(i),",",rider_library[str(i)],","])
        f3.writelines('\r')
    f3.close()        
    round_robin_shuffle()
    try:
        f=file(rider_lst_csv, 'r')
        csv= f.readlines()
        f.close
    except:
        print "Dude you're blowing it. Get your shit together or give the computer to Luke!"
    for i in csv:
        csv=i.split("\r")
    index = 0
    while index < len(csv):
        csv[index] = (csv[index]).split(',')
        index+=1
    for i in csv[1:]:
        new_rider_library[int(i[1])] = [i[0],i[2]]
    if len(new_rider_library)%2 != 0:
        new_rider_library[len(new_rider_library)] = ['Patrick Switzer','N']
    
######################################################################