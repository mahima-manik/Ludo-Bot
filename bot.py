import copy
from board import *

count=4 
gamemode = 0
graphics = 0
pid =0
self_color = ''
opp_color = ''
def initialization(gm, gph, player):
    global gamemode, pid, self_color, opp_color, graphics
    gamemode = gm
    pid = player
    graphics = gph
    if gamemode==0:
        if pid==1:
            self_color='Red'
            opp_color='Yellow'
        else:
            self_color='Yellow'
            opp_color='Red'
    else:
        if pid==1:
            self_color='Blue'
            opp_color='Green'
        else:
            self_color='Green'
            opp_color='Blue'
	if graphics==1:
		txt="You are: "+self_color+", Player: "+str(pid-1)
		player_color(root, txt)
	


daf_dict={(True, True, True):7, (True, False, True):6, (False, True, True):5, (True, True, False):4, (True, False, False):3, (False, True, False):2, (False, False, True):1, (False, False, False):0}
        
tokenID= {
"C2.2": "R3", "C2.3": "R2", "C3.2": "R1", "C3.3": "R0", "C11.2": "G3", "C11.3": "G2", "C12.2": "G1", "C12.3": "G0", "C11.11": "Y3", "C11.12": "Y2", "C12.11": "Y1", "C12.12": "Y0", "C2.11": "B3", "C2.12": "B2", "C3.11": "B1", "C3.12": "B0"
}
tokenIDrev= {"R3": "C2.2", "R2": "C2.3", "R1" : "C3.2","R0": "C3.3", "G3": "C11.2", "G2": "C11.3", "G1": "C12.2", "G0": "C12.3", "Y3": "C11.11", "Y2": "C11.12", "Y1": "C12.11", "Y0": "C12.12", "B3": "C2.11", "B2": "C2.12", "B1": "C3.11", "B0": "C3.12"}

pawns = { "Red": { "C2.2": "2.2", "C2.3": "2.3", "C3.2": "3.2", "C3.3": "3.3" },
            "Green": { "C11.2": "11.2", "C11.3": "11.3", "C12.2": "12.2", "C12.3": "12.3" },
            "Yellow": { "C11.11": "11.11", "C11.12": "11.12", "C12.11": "12.11", "C12.12": "12.12" },
            "Blue": { "C2.11": "2.11", "C2.12": "2.12", "C3.11": "3.11", "C3.12": "3.12" }}
            
temp_pawns = copy.deepcopy(pawns)
color_path = { "Red" : pawn_path_4, "Green" : pawn_path_1, "Yellow" : pawn_path_2, "Blue" : pawn_path_3 }


def cut_pawn():
    global pawns
    for p1 in pawns[self_color]:
        for p2 in pawns[opp_color]:
            if(pawns[self_color][p1] == pawns[opp_color][p2]) and (pawns[opp_color][p2] not in sp):
                pawns[opp_color][p2] = p2[1:] 
                if graphics==1:
                    move_oval(root, p2, p2[1:])

def stack_pawn():
    revdict={}
    for i in pawns[self_color]:
        if pawns[self_color][i] not in revdict:
            revdict[pawns[self_color][i]]=[i]
        else:
            revdict[pawns[self_color][i]].append(i)
    for i in pawns[opp_color]:
        if pawns[opp_color][i] not in revdict:
            revdict[pawns[opp_color][i]]=[i]
        else:
            revdict[pawns[opp_color][i]].append(i)
    for k, v in revdict.items():
         if len(v)<=1:
             del revdict[k]
    for i in revdict:
        text=""
        for k in revdict[i]:
            text=text+tokenID[k][:1]
        revdict[i]=text
    stack_oval(root, revdict)
	

def own_cut_pawn():
    global pawns
    for p1 in pawns[self_color]:
        for p2 in pawns[opp_color]:
            if(pawns[self_color][p1] == pawns[opp_color][p2]) and (pawns[self_color][p1] not in sp):
                pawns[self_color][p1] = p1[1:] 
                if graphics==1:
                    move_oval(root, p1, p1[1:])


def search_start_finish(pos):
    for i in range(4): #no. of lists in start_square=4
        if pos in start_square[i]:
            return True
    for i in range(4):#no.of lists in home_path=4
        if pos in home_path[i]:
            return True
    return False
     

def distance(self_pos, opp_pos):# pos is of the form 2.3
    if search_start_finish(self_pos) or search_start_finish(opp_pos):
        return -100
    else:
        distance = path.index(opp_pos)-path.index(self_pos)
        return distance%52

def isDefensive(piece, which_pawns): #piece is of the form "C2.11" , which_pawns = 0, then pawns, else temp_pawns
    global self_color, opp_color, pawns
    d=[]
    if (which_pawns == 0): 
        current_pos = pawns[self_color][piece]
        for i in pawns[opp_color].values():
            d.append(distance(current_pos, i))
    
    elif (which_pawns == 1):
        current_pos = temp_pawns[self_color][piece]
        for i in temp_pawns[opp_color].values():
            d.append(distance(current_pos, i))
    if current_pos in sp:
    	return False
    a=[]
    for i in range(len(d)):
        a.append((d[i] >= 43) and (d[i] != -100))
    x=False
    for i in range(len(a)):
        x=(x or a[i])
    return x
        
    
def isAggressive(piece, dice):#piece is of form C2.3
    global self_color, opp_color, pawns
    current_pos = pawns[self_color][piece]
    d=[]
    for i in pawns[opp_color].values():
        d.append(distance(current_pos, i))
    a=[]
    for i in range(len(d)):
        a.append( (dice<=d[i]) and (d[i]<=9))
    x=False
    for i in range(len(a)):
        x=(x or a[i])
    return x
        
def isFast(piece):#piece is of form C2.3
    global self_color, opp_color, pawns
    current_pos = pawns[self_color][piece]
    for i in range(4): #no. of lists in start_square=4
        if current_pos in start_square[i]:
            return False
    d={}
    ppath=color_path[self_color]
    for p in pawns[self_color]:
        if search_start_finish(pawns[self_color][p]):
            d[p]=-1
        else:
            d[p]=ppath.index(pawns[self_color][p])
    if piece==max(d, key=d.get):
        return True
    d.pop(max(d, key=d.get))
    maxm=max(d, key=d.get)
    if piece==max(d, key=d.get):
        return True
    else:
        return False
        
def get_daf(piece, dice): #piece is of form C2.3
    global self_color, opp_color, pawns
    current_pos = pawns[self_color][piece]
    for i in range(4):#no.of lists in home_path=4
        if current_pos in start_square[i]:
            return 0        
    d = isDefensive(piece, 0)
    a = isAggressive(piece, dice)
    f = isFast(piece)
    return daf_dict[(d,a,f)]
    
    
def count_not_defensive():
    dcount=0
    for p in temp_pawns[self_color]:
        if isDefensive(p, 1):
            dcount+=1
    return len(temp_pawns[self_color])-dcount
    
def count_open():
    ocount=0
    for p in temp_pawns[self_color]:
        pos = temp_pawns[self_color][p]
        for i in range(4):                  #no. of lists in start_square=4
            if pos in start_square[i]:
                ocount+=1
                break
    return len(temp_pawns[self_color])-ocount
    
def count_opp_not_opened():
    oppcount=0
    for p in temp_pawns[opp_color]:
        pos = temp_pawns[opp_color][p]
        for i in range(4):                  #no. of lists in start_square=4
            if pos in start_square[i]:
                oppcount+=1
                break
    return oppcount
    
def count_own_home():
    return 4-len(temp_pawns[self_color])
  
    
def get_winprob():
    c1=count_not_defensive()
    c2=count_open()
    c3=count_opp_not_opened()
    c4=count_own_home()
    value=0.4*c4 + 0.3 *c1 + 0.2*c3 + 0.1*c2
    return value/4.0

def move_opponent(piece, dice):
    global pawns
    path_list=color_path[opp_color]
    #open a piece 
    for i in range(4): 
        if pawns[opp_color][piece] in start_square[i]:
            if dice==6 or dice==1:
                pawns[opp_color][piece]=path_list[0]
                if graphics==1:
                    move_oval(root, piece, path_list[0])
                return (tokenID[piece]+'_'+str(dice)).rstrip()
            else:
                return ('NA').rstrip()
    #piece is already opened
    start = path_list.index(pawns[opp_color][piece])
    target=start+dice
    
    if target == 56:
        pawns[opp_color].pop(piece)
        if graphics==1:
            clear_oval(root,piece)
        return (tokenID[piece]+'_'+str(dice)).rstrip()
    elif target > 56:
        return ('NA').rstrip()              #need 3 for home but got 5
    else:                                       # a normal move
        for p1 in pawns[opp_color]:
            if (p1 != piece) and (pawns[opp_color][p1]==path_list[target]) and (path_list[target] not in sp):
                return -1
        pawns[opp_color][piece]=path_list[target]
        if graphics==1:
            move_oval(root, piece, path_list[target])
        return (tokenID[piece]+'_'+str(dice)).rstrip()

def temp_moves(piece, dice):
    global self_color, opp_color, count, temp_pawns, pawns
    path_list=color_path[self_color]
    #open a piece 
    for i in range(4): 
        if temp_pawns[self_color][piece] in start_square[i]:
            if dice==6 or dice==1:
                temp_pawns[self_color][piece]=path_list[0]
                return 0
            else:
                return -1
    #piece is already opened
    start = path_list.index(temp_pawns[self_color][piece])
    target = start + dice
    if target == 56:      #send a piece home
        temp_pawns[self_color].pop(piece)
        return 0
    elif target > 56:
        return -1           #need 3 for home but got 5
    else:                   # a normal move
        for p1 in temp_pawns[self_color]:
            if (p1 != piece) and (temp_pawns[self_color][p1]==path_list[target]) and (path_list[target] not in sp):
                return -1
        temp_pawns[self_color][piece]=path_list[target]
        return 0

    
def move(piece, dice, color):   #dice=1 dice move, if r0 has to move both 6 and 4, call move() two times , piece is of the form 'C2.3'
    global count, pawns
    path_list=color_path[color]
    #open a piece 
    for i in range(4): 
        if pawns[color][piece] in start_square[i]:
            if dice==6 or dice==1:
                pawns[color][piece]=path_list[0]
                if graphics==1:
                    move_oval(root, piece, path_list[0])
                return (tokenID[piece]+'_'+str(dice)).rstrip()
            else:
                return ('NA').rstrip()
    #piece is already opened
    start = path_list.index(pawns[color][piece])
    target=start+dice
    
    if target == 56:
        count-=1
        pawns[color].pop(piece)
        if graphics==1:
            clear_oval(root,piece)
        return (tokenID[piece]+'_'+str(dice)).rstrip()
    elif target > 56:
        return ('NA').rstrip()            #need 3 for home but got 5
    else:                                 # a normal move
        for p1 in pawns[color]:
            if (p1 != piece) and (pawns[color][p1]==path_list[target]) and (path_list[target] not in sp):
                return -1
        pawns[color][piece]=path_list[target]
        if graphics==1:
            move_oval(root, piece, path_list[target])
        return (tokenID[piece]+'_'+str(dice)).rstrip()

def select_pawn(dice):
    global temp_pawns, pawns
    temp_pawns = copy.deepcopy(pawns)
    
    daf={}
    for p in temp_pawns[self_color]:
        daf[p] = get_daf(p, dice)           #p is of form C2.3
    
    winprob = {}
    temp_pawns_2= {}
    temp_pawns_2=copy.deepcopy(temp_pawns[self_color])         #storing its own positions
        
    for p in temp_pawns_2:
        if (temp_moves(p, dice) == -1):
            winprob[p]=-1
        else:                           #valid move
            winprob[p] = get_winprob()
        
        temp_pawns = copy.deepcopy(pawns)
    
    for d in daf:
        x=daf[d]/7.0
        daf[d]=round(x,2)
    
    final = {}
    for i in temp_pawns_2:
        if winprob[i]==-1 or daf[i]==-1:
            final[i] = -1
        else:
            final[i] = 0.6*winprob[i] + 0.4 * daf[i]
    
    maxm = max(final, key=final.get)   
    if final[maxm] ==-1: 
        return 'NA'
    else:
        return maxm
    
                
def one_dice(dice):
    global pawns
    p = select_pawn(dice)
    if p == 'NA':
        return 'NA'
    else:    
        x = move(p, dice, self_color)
        if x == -1:
            return 'NA'
        cut_pawn()
        return x
    
def max_leaf3(piece, dice_list):
    global pawns, temp_pawns
    winprob = {}
    daf={}
    first_piece={}
    second_piece = {}
    third_piece = {}
    #----------------Branch A: D1 D2 D3 = (6, 6, D3), on the same piece-------------------#
    daf['A'] = get_daf(piece, dice_list[0])           #p is of form C2.3
    
    temp_pawns = copy.deepcopy(pawns)
    
    if (temp_moves(piece, dice_list[0]) == 0):
        first_piece['A']=(piece, dice_list[0])
        winprob['A'] = get_winprob()
        if piece not in temp_pawns[self_color]:
            winprob['A'] = get_winprob()
        else:                                       #ghar nai gaya
            if (temp_moves(piece, dice_list[1]) == 0):
                second_piece['A']=(piece, dice_list[1])
                winprob['A'] = get_winprob()
                if piece not in temp_pawns[self_color]:
                    winprob['A'] = get_winprob()
                else:                                    #ghar nai gaya
                    if (temp_moves(piece, dice_list[2]) == 0):
                        third_piece['A']=(piece, dice_list[2])
                        winprob['A'] = get_winprob()
                      
            else:
                if (temp_moves(piece, dice_list[2]) == 0):
                    third_piece['A']=(piece, dice_list[2])
                    winprob['A'] = get_winprob()
    else:
        temp_pawns = copy.deepcopy(pawns)
        if (temp_moves(piece, dice_list[1]) == 0):
            second_piece['A']=(piece, dice_list[1])
            winprob['A'] = get_winprob()
            if piece not in temp_pawns[self_color]:
                winprob['A'] = get_winprob()
            else:                                    #ghar nai gaya
                if (temp_moves(piece, dice_list[2]) == 0):
                    third_piece['A']=(piece, dice_list[2])
                    winprob['A'] = get_winprob()
                    
        else:
            if (temp_moves(piece, dice_list[2]) == 0):
                third_piece['A']=(piece, dice_list[2])
                winprob['A'] = get_winprob()
            else:
                winprob['A'] = -1
    
    #----------------Branch B: D1 D2 D3 = (D3, 6, 6), on the same piece-------------------#
    daf['B'] = get_daf(piece, dice_list[2])           #p is of form C2.3
    
    temp_pawns = copy.deepcopy(pawns)
    if (temp_moves(piece, dice_list[2]) == 0):
        first_piece['B']=(piece, dice_list[2])
        winprob['B'] = get_winprob()
        if piece not in temp_pawns[self_color]:
            winprob['B'] = get_winprob()
        else:                                       #ghar nai gaya
            if (temp_moves(piece, dice_list[1]) == 0):
                second_piece['B']=(piece, dice_list[1])
                winprob['B'] = get_winprob()
                if piece not in temp_pawns[self_color]:
                    winprob['B'] = get_winprob()
                else:                                    #ghar nai gaya
                    if (temp_moves(piece, dice_list[0]) == 0):
                        third_piece['B']=(piece, dice_list[0])
                        winprob['B'] = get_winprob()
                      
            else:
                if (temp_moves(piece, dice_list[0]) == 0):
                    third_piece['B']=(piece, dice_list[0])
                    winprob['B'] = get_winprob()
    else:
        temp_pawns = copy.deepcopy(pawns)
        if (temp_moves(piece, dice_list[1]) == 0):
            second_piece['B']=(piece, dice_list[1])
            winprob['B'] = get_winprob()
            if piece not in temp_pawns[self_color]:
                winprob['B'] = get_winprob()
            else:                                    #ghar nai gaya
                if (temp_moves(piece, dice_list[0]) == 0):
                    third_piece['B']=(piece, dice_list[0])
                    winprob['B'] = get_winprob()
                    
        else:
            if (temp_moves(piece, dice_list[0]) == 0):
                third_piece['B']=(piece, dice_list[0])
                winprob['B'] = get_winprob()
            else:
                winprob['B'] = -1
    
    
    #----------------Branch C: D1 D2 D3 = (6, D3, 6), on the same piece-------------------#
    daf['C'] = get_daf(piece, dice_list[1])           #p is of form C2.3
    
    temp_pawns = copy.deepcopy(pawns)
    if (temp_moves(piece, dice_list[1]) == 0):
        first_piece['C']=(piece, dice_list[1])
        winprob['C'] = get_winprob()
        if piece not in temp_pawns[self_color]:
            winprob['C'] = get_winprob()
        else:                                       #ghar nai gaya
            if (temp_moves(piece, dice_list[2]) == 0):
                second_piece['C']=(piece, dice_list[2])
                winprob['C'] = get_winprob()
                if piece not in temp_pawns[self_color]:
                    winprob['C'] = get_winprob()
                else:                                    #ghar nai gaya
                    if (temp_moves(piece, dice_list[0]) == 0):
                        third_piece['C']=(piece, dice_list[0])
                        winprob['C'] = get_winprob()
                      
            else:
                if (temp_moves(piece, dice_list[0]) == 0):
                    third_piece['C']=(piece, dice_list[0])
                    winprob['C'] = get_winprob()
    else:
        temp_pawns = copy.deepcopy(pawns)
        if (temp_moves(piece, dice_list[2]) == 0):
            second_piece['C']=(piece, dice_list[2])
            winprob['C'] = get_winprob()
            if piece not in temp_pawns[self_color]:
                winprob['C'] = get_winprob()
            else:                                    #ghar nai gaya
                if (temp_moves(piece, dice_list[0]) == 0):
                    third_piece['C']=(piece, dice_list[0])
                    winprob['C'] = get_winprob()
                    
        else:
            if (temp_moves(piece, dice_list[0]) == 0):
                third_piece['C']=(piece, dice_list[0])
                winprob['C'] = get_winprob()
            else:
                winprob['C'] = -1
    
    
    #----------------Branch DEF: (D3, 6) on a sigle piece and 6 on the different piece-------------------#
    
    daf['D'] = daf['E'] = daf['F'] = get_daf(piece, dice_list[2])           #p is of form C2.3
    winprob['D'] =winprob['E']=winprob['F']= -1
    x = 'C'
    temp_pawns = copy.deepcopy(pawns)
    
    if (temp_moves(piece, dice_list[2]) == 0):          #first move successful
        first_piece['D'] = first_piece['E'] = first_piece['F']=(piece, dice_list[2])
        winprob['D'] = winprob['E'] = winprob['F'] = get_winprob()
        if piece not in temp_pawns[self_color]:         #first piece went home
            temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
            for i in temp_pawns_x[self_color]:  
                if i != piece:
                    if (temp_moves(i, dice_list[0]) == 0):      #third move successful
                        third_piece[chr(ord(x)+1)]=(i, dice_list[0])
                        winprob[chr(ord(x)+1)] = get_winprob()
                    x = chr(ord(x)+1)
                temp_pawns = copy.deepcopy(temp_pawns_x)
            
        else:                                            #first piece did not go home
            if(temp_moves(piece, dice_list[1]) == 0):    #checking for second move success
                second_piece['D'] = second_piece['E'] = second_piece['F'] = (piece, dice_list[1])
                winprob['D'] = winprob['E'] = winprob['F'] = get_winprob()
                temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
                
                for i in temp_pawns_x[self_color]:      
                    if i != piece:
                        if (temp_moves(i, dice_list[0]) == 0):  
                            third_piece[chr(ord(x)+1)] = (i, dice_list[0])    
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
            else:                                        #second move invalid
                temp_pawns_x = copy.deepcopy(temp_pawns) #checking for third move on 2nd piece
                for i in temp_pawns_x[self_color]:
                    if i != piece:
                        if (temp_moves(i, dice_list[0]) == 0):
                            third_piece[chr(ord(x)+1)]=(i, dice_list[0]) 
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
    else:                                               # first move was invalid
        if(temp_moves(piece, dice_list[1]) == 0):       #second move valid
                second_piece['D'] = second_piece['E'] = second_piece['F'] = (piece, dice_list[1]) 
                winprob['D'] = winprob['E'] = winprob['F'] = get_winprob()
                
                temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
                for i in temp_pawns_x[self_color]:
                    if i != piece:
                        if (temp_moves(i, dice_list[0]) == 0):
                            third_piece[chr(ord(x)+1)]=(i, dice_list[0])
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
        else:                                           #second move invalid
            temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
            for i in temp_pawns_x[self_color]:
                if i != piece:
                    if (temp_moves(i, dice_list[0]) == 0):
                        third_piece[chr(ord(x)+1)]=(i, dice_list[0]) 
                        winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    else:
                        winprob[chr(ord(x)+1)] = -1
                        x = chr(ord(x)+1)
                temp_pawns = copy.deepcopy(temp_pawns_x)

    #----------------Branch GHI: (6, D3) on a sigle piece and 6 on the different piece (1, 2, 0)-------------------#
    
    daf['G'] = daf['H'] = daf['I'] = get_daf(piece, dice_list[1])           #p is of form C2.3
    winprob['G'] = winprob['H'] = winprob['I'] = -1
    x = 'F'
    temp_pawns = copy.deepcopy(pawns)
    
    if (temp_moves(piece, dice_list[1]) == 0):          #first move successful
        first_piece['G'] = first_piece['H'] = first_piece['I'] = (piece, dice_list[1]) 
        winprob['G'] = winprob['H'] = winprob['I'] = get_winprob()
        if piece not in temp_pawns[self_color]:         #first piece went home
            temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
            for i in temp_pawns_x[self_color]:  
                if i != piece:
                    if (temp_moves(i, dice_list[0]) == 0):      #third move successful
                        third_piece[chr(ord(x)+1)]=(i, dice_list[0]) 
                        winprob[chr(ord(x)+1)] = get_winprob()
                    x = chr(ord(x)+1)
                temp_pawns = copy.deepcopy(temp_pawns_x)
            
        else:                                            #first piece did not go home
            if(temp_moves(piece, dice_list[2]) == 0):    #checking for second move success
                second_piece['G'] = second_piece['H']= second_piece['I']= (piece, dice_list[2]) 
                winprob['G'] = winprob['H'] = winprob['I'] = get_winprob()
                
                temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
                for i in temp_pawns_x[self_color]:      
                    if i != piece:
                        if (temp_moves(i, dice_list[0]) == 0):
                            third_piece[chr(ord(x)+1)]=(i, dice_list[0])       
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
            else:                                        #second move invalid
                temp_pawns_x = copy.deepcopy(temp_pawns) #checking for third move on 2nd piece
                for i in temp_pawns_x[self_color]:
                    if i != piece:
                        if (temp_moves(i, dice_list[0]) == 0):
                            third_piece[chr(ord(x)+1)]=(i, dice_list[0]) 
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
    else:                                               # first move was invalid
        if(temp_moves(piece, dice_list[2]) == 0):       #second move valid
                second_piece['G'] = second_piece['H']= second_piece['I']= (piece, dice_list[2]) 
                winprob['G'] = winprob['H'] = winprob['I'] = get_winprob()
                temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
                
                for i in temp_pawns_x[self_color]:
                    if i != piece:
                        if (temp_moves(i, dice_list[0]) == 0):
                            third_piece[chr(ord(x)+1)]=(i, dice_list[0]) 
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
        else:                                           #second move invalid
            temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
            for i in temp_pawns_x[self_color]:
                if i != piece:
                    if (temp_moves(i, dice_list[0]) == 0):
                        third_piece[chr(ord(x)+1)]=(i, dice_list[0]) 
                        winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    else:
                        winprob[chr(ord(x)+1)] = -1
                        x = chr(ord(x)+1)
                temp_pawns = copy.deepcopy(temp_pawns_x)


    #----------------Branch JKL: (6, 6) on a sigle piece and D3 on the different piece (0, 1, 2) -------------------#
    
    daf['J'] = daf['K'] = daf['L'] = get_daf(piece, dice_list[0])           #p is of form C2.3
    winprob['J'] = winprob['K'] = winprob['L'] = -1
    x = 'I'
    temp_pawns = copy.deepcopy(pawns)
    
    if (temp_moves(piece, dice_list[0]) == 0):          #first move successful
        first_piece['J']=first_piece['K']=first_piece['L']=(piece, dice_list[0]) 
        winprob['J'] = winprob['K'] = winprob['L'] = get_winprob()
        if piece not in temp_pawns[self_color]:         #first piece went home
            temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
            for i in temp_pawns_x[self_color]:  
                if i != piece:
                    if (temp_moves(i, dice_list[2]) == 0):      #third move successful
                        third_piece[chr(ord(x)+1)]=(i, dice_list[2]) 
                        winprob[chr(ord(x)+1)] = get_winprob()
                    x = chr(ord(x)+1)
                temp_pawns = copy.deepcopy(temp_pawns_x)
            
        else:                                            #first piece did not go home
            if(temp_moves(piece, dice_list[1]) == 0):    #checking for second move success
                second_piece['J']=second_piece['K']=second_piece['L']=(piece, dice_list[1]) 
                winprob['J'] = winprob['K'] = winprob['L'] = get_winprob()
                temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
                
                for i in temp_pawns_x[self_color]:      
                    if i != piece:
                        if (temp_moves(i, dice_list[2]) == 0): 
                            third_piece[chr(ord(x)+1)]=(i, dice_list[2]) 
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
            else:                                        #second move invalid
                temp_pawns_x = copy.deepcopy(temp_pawns) #checking for third move on 2nd piece
                for i in temp_pawns_x[self_color]:
                    if i != piece:
                        if (temp_moves(i, dice_list[2]) == 0):
                            third_piece[chr(ord(x)+1)]=(i, dice_list[2]) 
                            winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    temp_pawns = copy.deepcopy(temp_pawns_x)
    else:                                               # first move was invalid
        if(temp_moves(piece, dice_list[1]) == 0):       #second move valid
            second_piece['J']=second_piece['K']=second_piece['L']=(piece, dice_list[1]) 
            winprob['J'] = winprob['K'] = winprob['L'] = get_winprob()
            temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
            for i in temp_pawns_x[self_color]:
                if i != piece:
                    if (temp_moves(i, dice_list[2]) == 0):
                        third_piece[chr(ord(x)+1)]=(i, dice_list[2]) 
                        winprob[chr(ord(x)+1)] = get_winprob()
                    x = chr(ord(x)+1)
                temp_pawns = copy.deepcopy(temp_pawns_x)
        else:                                           #second move invalid
            temp_pawns_x = copy.deepcopy(temp_pawns)    #checking for third move on 2nd piece
            for i in temp_pawns_x[self_color]:
                if i != piece:
                    if (temp_moves(i, dice_list[2]) == 0):
                        third_piece[chr(ord(x)+1)]=(i, dice_list[2]) 
                        winprob[chr(ord(x)+1)] = get_winprob()
                        x = chr(ord(x)+1)
                    else:
                        winprob[chr(ord(x)+1)] = -1
                        x = chr(ord(x)+1)
                temp_pawns = copy.deepcopy(temp_pawns_x)

        
    #----------------Branch M: (6, 6, D3) on all different piece. Current piece will move 6-------------------#
    
    daf['M'] = get_daf(piece, dice_list[0])           #p is of form C2.3
    winprob['M'] = -1
    temp_pawns = copy.deepcopy(pawns)
    ret_list={}
    if (temp_moves(piece, dice_list[0]) == 0):
        first_piece['M'] = (piece, dice_list[0]) 
        temp_pawns_x = copy.deepcopy(temp_pawns)
        winprob['M'] = get_winprob()
        for i in temp_pawns_x[self_color]:
            if i != piece:
                x = max_leaf(i, dice_list[1:], 1)
                if x!='NA':
                    ret_list[i]=x
        if ret_list:
            maxm=max(ret_list, key=ret_list.get)
            winprob['M']=ret_list[maxm][0]
            second_piece['M']= (ret_list[maxm][1][0], ret_list[maxm][1][1])
            if len(ret_list[maxm])>2:
                third_piece['M']= (ret_list[maxm][2][0], ret_list[maxm][2][1])
        temp_pawns = copy.deepcopy(temp_pawns_x)
        ret_list = {}
    else:
        winprob['M']=-1 
        for i in temp_pawns_x[self_color]:
            if i != piece:
               x = max_leaf(i, dice_list[1:], 1)
               if x!='NA':
                    ret_list[i]=x
        if ret_list:
            maxm=max(ret_list, key=ret_list.get)
            winprob['M']=ret_list[maxm][0]
            second_piece['M']= (ret_list[maxm][1][0], ret_list[maxm][1][1])
            if len(ret_list[maxm])>2:
                third_piece['M']= (ret_list[maxm][2][0], ret_list[maxm][2][1])
        temp_pawns = copy.deepcopy(temp_pawns_x)
        ret_list = {}
            
    #----------------Branch N: (D3, 6, 6) on all different piece. Current piece will move 6-------------------#
    daf['N'] = get_daf(piece, dice_list[2])           #p is of form C2.3
    winprob['N'] = -1
    temp_pawns = copy.deepcopy(pawns)
    ret_list={}
    if (temp_moves(piece, dice_list[2]) == 0):
        first_piece['N']=(piece, dice_list[2])
        temp_pawns_x = copy.deepcopy(temp_pawns)
        winprob['N'] = get_winprob()
        for i in temp_pawns_x[self_color]:
            if i != piece:
                x = max_leaf(i, dice_list[:2], 1)
                if x!='NA':
                    ret_list[i]=x
        if ret_list:
            maxm=max(ret_list, key=ret_list.get)
            winprob['N']=ret_list[maxm][0]
            second_piece['N']= (ret_list[maxm][1][0], ret_list[maxm][1][1])
            if len(ret_list[maxm])>2:
                third_piece['N']= (ret_list[maxm][2][0], ret_list[maxm][2][1])
        temp_pawns = copy.deepcopy(temp_pawns_x)
        ret_list = {}
    else:
        winprob['N']=-1 
        for i in temp_pawns_x[self_color]:
            if i != piece:
               x = max_leaf(i, dice_list[:2], 1)
               if x!='NA':
                    ret_list[i]=x
        if ret_list:
            maxm=max(ret_list, key=ret_list.get)
            winprob['N']=ret_list[maxm][0]
            second_piece['N']= (ret_list[maxm][1][0], ret_list[maxm][1][1])
            if len(ret_list[maxm])>2:
                third_piece['N']= (ret_list[maxm][2][0], ret_list[maxm][2][1])
        temp_pawns = copy.deepcopy(temp_pawns_x)
        ret_list = {}
                
    for d in daf:
        x=daf[d]/7.0
        daf[d]=round(x,2)

    temp_pawns = copy.deepcopy(pawns)
    
    util3 = []
    util2 = []
    util1 = [] 
    util0 = []
    
    for i in range(ord('A'), ord('O')):
        if (chr(i) in first_piece):
            if (chr(i) in second_piece):
                if (chr(i) in third_piece):
                    util3.append(chr(i))
                else:
                    util2.append(chr(i))
            else:
                if (chr(i) in third_piece):
                    util2.append(chr(i))
                else:
                    util1.append(chr(i))
        else:
            if (chr(i) in second_piece):
                if (chr(i) in third_piece):
                    util2.append(chr(i))
                else:
                    util1.append(chr(i))
            else:
                if (chr(i) in third_piece):
                    util1.append(chr(i))
                else:
                    util0.append(chr(i))
    
    final = {}
    if util3:
        for i in util3:
            if winprob[i] == -1 or daf[i] == -1:
                final[i] = -1
            else:
                final[i] = round((0.6*winprob[i] + 0.4 * daf[i]), 2)
        
        maxm=max(final, key=final.get)
        
        if winprob[maxm] == -1:
            return 'NA'
        else:
            output_list = []
            output_list.append(final[maxm])
            output_list.append(first_piece[maxm])
            output_list.append(second_piece[maxm])
            output_list.append(third_piece[maxm])
            return output_list    
    
    elif util2:
        for i in util2:
            if winprob[i] == -1 or daf[i] == -1:
                final[i] = -1
            else:
                final[i] = round((0.6*winprob[i] + 0.4 * daf[i]), 2)
        
        maxm=max(final, key=final.get)
        if winprob[maxm] == -1:
            return 'NA'
        else:
            output_list = []
            output_list.append(final[maxm])
            if maxm in first_piece:
                output_list.append(first_piece[maxm])
            if maxm in second_piece:
                output_list.append(second_piece[maxm])
            if maxm in third_piece:
                output_list.append(third_piece[maxm])
            return output_list

    elif util1:
        for i in util1:
            if winprob[i] == -1 or daf[i] == -1:
                final[i] = -1
            else:
                final[i] = round((0.6*winprob[i] + 0.4 * daf[i]), 2)
        
        maxm=max(final, key=final.get)
        if winprob[maxm] == -1:
            return 'NA'
        else:
            output_list = []
            output_list.append(final[maxm])
            if maxm in first_piece:
                output_list.append(first_piece[maxm])
            if maxm in second_piece:
                output_list.append(second_piece[maxm])
            if maxm in third_piece:
                output_list.append(third_piece[maxm])
            return output_list

    elif util0:
        return 'NA'
    
         
def max_leaf(piece, dice_list, d_flag):                         #takes as parameter the index of which goti and the dice list
    global pawns, temp_pawns
    winprob = {}
    daf={}
    second_piece = {}
    first_piece = {}
    temp_pawns_2 = copy.deepcopy(temp_pawns)
    
    #----------------Branch A: D1 D2, on the same piece-------------------#
    daf['A'] = get_daf(piece, dice_list[0])           #p is of form C2.3
    
    if d_flag==0:
        temp_pawns = copy.deepcopy(pawns)
    
    if (temp_moves(piece, dice_list[0]) == 0):          #piece move valid on dice[0]
        first_piece['A']=(piece, dice_list[0])
        if piece not in temp_pawns[self_color]:         #piece went home on dice[0]
            winprob['A'] = get_winprob()         
        else:
            winprob['A'] = get_winprob()
            if (temp_moves(piece, dice_list[1]) == 0):            #piece was valid on dice[0] and did not go home, so moved on dice[1]
                second_piece['A']=(piece, dice_list[1])
                winprob['A'] = get_winprob()
    else:
        if d_flag==0:
            temp_pawns = copy.deepcopy(pawns)
        else:
            temp_pawns = copy.deepcopy(temp_pawns_2)
            
        if (temp_moves(piece, dice_list[1]) == 0):
            second_piece['A']=(piece, dice_list[1])
            winprob['A'] = get_winprob()           
        else:                                           #both the moves were invalid
            winprob['A'] = -1
    
    #----------------Branch H: D2 D1, on the same piece-------------------#
    daf['H'] = get_daf(piece, dice_list[1])           #p is of form C2.3
    
    if(d_flag==0):
        temp_pawns = copy.deepcopy(pawns)
    else:
        temp_pawns = copy.deepcopy(temp_pawns_2)
        
    if (temp_moves(piece, dice_list[1]) == 0):          #piece move valid on dice[0]
        first_piece['H']=(piece, dice_list[1])
        if piece not in temp_pawns[self_color]:         #piece went home on dice[0]
            winprob['H'] = get_winprob()         
        else:
            winprob['H'] = get_winprob()
            if (temp_moves(piece, dice_list[0]) == 0):            #piece was valid on dice[0] and did not go home, so moved on dice[1]
                second_piece['H']=(piece, dice_list[0])
                winprob['H'] = get_winprob()
    else:
        if d_flag==0:
            temp_pawns = copy.deepcopy(pawns)
        else:
            temp_pawns = copy.deepcopy(temp_pawns_2)
            
        if (temp_moves(piece, dice_list[0]) == 0):
            second_piece['H']=(piece, dice_list[0])
            winprob['H'] = get_winprob()           
        else:                                           #both the moves were invalid
            winprob['H'] = -1        
    
    #----------------Branch BCD: D1 D2, on the different piece-------------------#
    
    daf['B'] = daf['C'] = daf['D'] = get_daf(piece, dice_list[0])           #p is of form C2.3
    winprob['B'] = winprob['C'] = winprob['D']= -1
    x = 'A'
    if(d_flag==0):
        temp_pawns = copy.deepcopy(pawns)
    else:
        temp_pawns = copy.deepcopy(temp_pawns_2)
    
    if (temp_moves(piece, dice_list[0]) == 0):          #piece move valid on dice[0]
        first_piece['B']=first_piece['C']=first_piece['D']=(piece, dice_list[0])
        temp_pawns_x = copy.deepcopy(temp_pawns)
        winprob['B'] = winprob['C'] = winprob['D'] = get_winprob()
        for i in temp_pawns_x[self_color]:
            if i != piece:
                if (temp_moves(i, dice_list[1]) == 0):
                    second_piece[chr(ord(x)+1)] = (i, dice_list[1])
                    winprob[chr(ord(x)+1)] = get_winprob()
                x = chr(ord(x)+1)
            temp_pawns = copy.deepcopy(temp_pawns_x)        
            
    else:
        if d_flag==0:
            temp_pawns = copy.deepcopy(pawns)
        else:
            temp_pawns = copy.deepcopy(temp_pawns_2)
        temp_pawns_x = copy.deepcopy(temp_pawns)
        for i in temp_pawns_x[self_color]:
            if i != piece:
                if (temp_moves(i, dice_list[1]) == 0):
                    second_piece[chr(ord(x)+1)] =(i, dice_list[1])
                    winprob[chr(ord(x)+1)] = get_winprob()
                    x = chr(ord(x)+1)
                else:
                    winprob[chr(ord(x)+1)] = -1
                    x = chr(ord(x)+1)
            temp_pawns = copy.deepcopy(temp_pawns_x)     
        
    #----------------Branch EFG: D2 D1, on the different piece-------------------#
    
    daf['E'] = daf['F'] = daf['G'] = get_daf(piece, dice_list[1])           #p is of form C2.3
    winprob['E'] =winprob['F']=winprob['G']= -1
    x = 'D'
    if(d_flag==0):
        temp_pawns = copy.deepcopy(pawns)
    else:
        temp_pawns = copy.deepcopy(temp_pawns_2)
        
    if (temp_moves(piece, dice_list[1]) == 0):
        first_piece['E'] =first_piece['F']=first_piece['G']=(piece, dice_list[1])
        temp_pawns_x = copy.deepcopy(temp_pawns)
        winprob['E'] = winprob['F'] = winprob['G'] = get_winprob()
        for i in temp_pawns_x[self_color]:
            if i != piece:
                if (temp_moves(i, dice_list[0]) == 0):
                    second_piece[chr(ord(x)+1)] =(i, dice_list[0])
                    winprob[chr(ord(x)+1)] = get_winprob()
                x = chr(ord(x)+1)
            temp_pawns = copy.deepcopy(temp_pawns_x)
    else:
        if d_flag==0:
            temp_pawns = copy.deepcopy(pawns)
        else:
            temp_pawns = copy.deepcopy(temp_pawns_2)
        
        temp_pawns_x = copy.deepcopy(temp_pawns)
        for i in temp_pawns_x[self_color]:
            if i != piece:
                if (temp_moves(i, dice_list[0]) == 0):
                    second_piece[chr(ord(x)+1)] =(i, dice_list[0])
                    winprob[chr(ord(x)+1)] = get_winprob()
                    x = chr(ord(x)+1)
                else:
                    winprob[chr(ord(x)+1)] = -1
                    x = chr(ord(x)+1)
            temp_pawns = copy.deepcopy(temp_pawns_x)
        
    for d in daf:
        x=daf[d]/7.0
        daf[d]=round(x,2)
    
    if(d_flag==0):
        temp_pawns = copy.deepcopy(pawns)
    else:
        temp_pawns = copy.deepcopy(temp_pawns_2)
    
    util2 = []
    util1 = [] 
    util0 = []
    for i in range(ord('A'), ord('I')):
        if (chr(i) in first_piece):
            if (chr(i) in second_piece):
                util2.append(chr(i))
            else:
                util1.append(chr(i))
        else:
            if (chr(i) in second_piece):
                util1.append(chr(i))
            else:
                util0.append(chr(i))
    
    final = {}
    if util2:
        for i in util2:
            if winprob[i] == -1 or daf[i] == -1:
                final[i] = -1
            else:
                final[i] = round((0.6*winprob[i] + 0.4 * daf[i]), 2)
        
        maxm=max(final, key=final.get)
        
        if winprob[maxm] == -1:
            return 'NA'
        else:
            output_list = []
            if d_flag==0:
                output_list.append(final[maxm])
            else:
                output_list.append(winprob[maxm])    
            
            output_list.append(first_piece[maxm])
            output_list.append(second_piece[maxm])
            return output_list    
    
    elif util1:
        for i in util1:
            if winprob[i] == -1 or daf[i] == -1:
                final[i] = -1
            else:
                final[i] = round((0.6*winprob[i] + 0.4 * daf[i]), 2)
        
        maxm=max(final, key=final.get)
        if winprob[maxm] == -1:
            return 'NA'
        else:
            output_list = []
            if d_flag==0:
                output_list.append(final[maxm])
            else:
                output_list.append(winprob[maxm])    
            
            if maxm in first_piece:
                output_list.append(first_piece[maxm])
            if maxm in second_piece:
                output_list.append(second_piece[maxm])
            return output_list

    elif util0:
        return 'NA'
    
def two_dice(dice):
    global pawns
    trees={}
    util2 = {}
    util1 = {} 
    for i in pawns[self_color]:
        x = max_leaf(i, dice, 0)              # max leaf will return [max_leaf_value, (pawn1,dice1), (pawn2, dice2)]
        if x != 'NA':
            if len(x)==3:
                util2[i]=x
            elif len(x)==2:
                util1[i]=x
                
    if util2:
        maxm = max(util2, key=util2.get)
        m=[]
        for t in range(1, 3):
            m.append(move(util2[maxm][t][0], util2[maxm][t][1], self_color))
            cut_pawn()
        return m    
    if util1:
        maxm = max(util1, key=util1.get)
        m=[]
        m.append(move(util1[maxm][1][0], util1[maxm][1][1], self_color))
        cut_pawn()
        return m    
    else:
        return ['NA']
    
def three_dice(dice):
    global pawns
    trees = {}
    util3 = {}
    util2 = {}
    util1 = {} 
    for i in pawns[self_color]:
        x=max_leaf3(i, dice)              # max_leaf3 will return [max_leaf_value, (pawn1,dice1), (pawn2, dice2),  (pawn3, dice3)]
        if x!='NA':
            if len(x)==4:
                util3[i]=x
            elif len(x)==3:
                util2[i]=x
            elif len(x)==2:
                util1[i]=x
                         
    if util3:
        maxm=max(util3, key=util3.get)
        m=[]
        for t in range(1, 4):
            m.append(move(util3[maxm][t][0], util3[maxm][t][1], self_color))
            cut_pawn()
        return m
    if util2:
        maxm=max(util2, key=util2.get)
        m=[]
        for t in range(1, 3):
            m.append(move(util2[maxm][t][0], util2[maxm][t][1], self_color))
            cut_pawn()
        return m
    if util1:
        maxm=max(util1, key=util1.get)
        m=[]
        m.append(move(util1[maxm][1][0], util1[maxm][1][1], self_color))
        cut_pawn()
        return m  
    else:
        return ['NA']
