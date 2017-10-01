import sys, time
from bot import *
from board import *

graphics=1
tl = sys.stdin.readline().strip()
tl1 = int(tl.split(' ')[1])     #time limit
pid = int(tl.split(' ')[0])     #player id
gm = int(tl.split(' ')[2])      #game mode
graphics = 1- (int(tl.split(' ')[3]))



if graphics==1:
	Tkinter.Canvas.__init__(root, r, width=S_WIDTH*AREA, height=S_HEIGHT*AREA)
	create_squares(root)
	fill_colors(root)
	root.configure(width=S_WIDTH*AREA, height=S_HEIGHT*AREA+S_HEIGHT*2)
	root.pack(side="top", expand=True, fill="both")
	create_ovals(root)
	
initialization(gm, graphics, pid)

init_flag = False

REPEAT = False                  #no repeat initially

while True:

    if REPEAT == False:
        sys.stdout.flush()
        if pid == 2 and init_flag == False:     
            init_flag = True
            dice = sys.stdin.readline().strip()             #reading the move of the opponent team
            if graphics==1:
				create_playerturn(root, dice)
            move_opp = sys.stdin.readline().strip()
            opp_move=move_opp.strip().split('<next>')
            for i in opp_move:
                if i!='NA':
                    x = i.split('_')
                    move_opponent(tokenIDrev[x[0]],int(x[1]))
        dice=[]
        sys.stdout.write('<THROW>\n')
        sys.stdout.flush()
        dice_string = sys.stdin.readline().strip()         #Master returns the value of the dice move
        if graphics==1:
           	create_playerturn(root, dice_string)
        if (dice_string=='YOU ROLLED 3 SIXES, AND THUS A DUCK'):
            dice.append(0)
            dice.append(0)
            dice.append(0)
        else:
            dice_list_string = dice_string[11:].split()
            for i in range(len(dice_list_string)):
                dice.append(int(dice_list_string[i]))
        
        if len(dice)<3:
            for i in range(3-len(dice)):
                dice.append(0)
        if (dice[0]!=0):
            if (dice[1]!=0):
                if (dice[2]!=0):                #dice=[6 6 x]
                    x = three_dice(dice)
                    if x[0]=='NA':
                        sys.stdout.write('NA\n')
                    else:
                        st=x[0]
                        for i in range(1,len(x)):
                            st=st+'<next>'+x[i]
                        sys.stdout.write(st + '\n')    
                else:                           #dice=[6 x]
                    #two_dice(dice)
                    x = two_dice(dice[:2])
                    if x[0]=='NA':
                        sys.stdout.write('NA\n')
                    else:
                        st=x[0]
                        if len(x)>1:
                            st=st+'<next>'+x[1]
                        sys.stdout.write(st + '\n')
            else:                               #dice=[x]
                x1=one_dice(dice[0])
                if x1=='NA':
                    sys.stdout.write('NA\n')
                else:
                    sys.stdout.write(str(x1)+'\n')
        else:
            sys.stdout.write('NA\n')
        cut_pawn()
        if graphics==1:
            stack_pawn()
        sys.stdout.flush()
    else:
        REPEAT = False
    if graphics==1:
		r.update_idletasks()
		r.update()   
    dice = sys.stdin.readline().strip()         #Waiting for opponent's dice
    if graphics==1:
		create_playerturn(root, dice)
    if dice != 'REPEAT':                        # if dice==repeat, then our REPEAT turn
        sys.stderr.write('bot_msg_dice: ' + dice + '\n')
        move_opp = sys.stdin.readline().strip()
        sys.stderr.write('bot_msg_move: ' + move_opp + '\n')
        opp_move = move_opp.strip().split('<next>')
   
        if opp_move[-1] == 'REPEAT':#next move is also of opponent
            REPEAT = True
            del opp_move[-1]
        if 'NA' not in opp_move:
            for i in opp_move:
                x = i.split('_')
                move_opponent( tokenIDrev[x[0]], int(x[1]) )
                own_cut_pawn()
                if graphics==1:
                    stack_pawn()
    if graphics==1:
		r.update_idletasks()
		r.update()
            
    time.sleep(1)
