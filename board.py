import Tkinter

S_WIDTH=36		# Width Of All Boxes
S_HEIGHT=36		# Height Of All Boxes
AREA = 15		# Number Of Boxes

# Track Color

C_1_A = "chartreuse3"	# When Active
C_2_A = "red"	
C_3_A = "yellow2"	
C_4_A = "RoyalBlue1"	

# List Of Active Colors
COLOR = [C_2_A, C_1_A, C_3_A, C_4_A]

# Function For Track Coordinates Calculations
def paths(s, r):						#r is an iterable object
	return [s.format(i) for i in r]

# Creating Main Track Square Boxes
# TRACK=path
path = []
path+= paths("6.{}", range(6))[::-1]            #['6.5', '6.4', '6.3', '6.2', '6.1', '6.0'] stores this
path+= ['7.0']
path+= paths("8.{}", range(6))
path+= paths("{}.6", range(9,15))
path+= ['14.7']
path+= paths("{}.8", range(9,15))[::-1]
path+= paths("8.{}", range(9,15))
path+= ['7.14']
path+= paths("6.{}", range(9,15))[::-1]
path+= paths("{}.8", range(6))[::-1]
path+= ['0.7']
path+= paths("{}.6", range(6))

# Creating Ending Tracks / Home tracks 
# F_TRACK=home_path
home_path=[]
home_path.append(paths("7.{}", range(1,7)))        #GREEN
home_path.append(paths("{}.7", range(8,14))[::-1])    #yellow
home_path.append(paths("7.{}", range(8,14))[::-1])    #blue
home_path.append(paths("{}.7", range(1,7)))        #RED

# Now Creating Roots
# TRAIN=pawn_path
pawn_path_1 = []
pawn_path_2 = []
pawn_path_3 = []
pawn_path_4 = []
pawn_path_1 = path[8:] + path[:7] + home_path[0]    # ROOT One Green
pawn_path_2 = path[21:] + path[:20] + home_path[1]  # Root Two YELLOW
pawn_path_3 = path[34:] + path[:33] + home_path[2]    # Root Three BLUE
pawn_path_4 = path[47:] + path[:46] + home_path[3]   # Root Four red

# STATION=start_square
start_square=[]
start_square.append(['11.2','12.2','11.3','12.3'])            #start_square[0] GREEN
start_square.append(['2.2','3.2','2.3','3.3'])                #start_square[1] RED
start_square.append(['11.11','12.11','11.12','12.12'])        #start_square[2] YELLOW
start_square.append(['2.11','3.11','2.12','3.12'])            #start_square[3] BLUE

#AROUND STATIONS
around = [[],[],[],[]]
#---------RED----------#
around[0] += (paths("{}.0", range(0,6)))
around[0] += (paths("{}.1", range(0,6)))
around[0] +=(paths("{}.4", range(0,6)))
around[0] += (paths("{}.5", range(0,6)))
around[0] += [0.2, 1.2, 4.2, 5.2]
around[0] += [0.3, 1.3, 4.3, 5.3]

#--------GREEN---------#
around[1] += (paths("{}.0", range(9,15)))
around[1] += (paths("{}.1", range(9,15)))
around[1] += (paths("{}.4", range(9,15)))
around[1] += (paths("{}.5", range(9,15)))
around[1] += [9.2, 10.2, 13.2, 14.2]
around[1] += [9.3, 10.3, 13.3, 14.3]

#-------YELLOW--------#
around[2] += (paths("{}.9", range(9,15)))
around[2] += (paths("{}.10", range(9,15)))
around[2] += (paths("{}.13", range(9,15)))
around[2] += (paths("{}.14", range(9,15)))
around[2] += [9.11, 10.11, 13.11, 14.11]
around[2] += [9.12, 10.12, 13.12, 14.12]

#--------BLUE---------#
around[3] += (paths("{}.9", range(0,6)))
around[3] += (paths("{}.10", range(0,6)))
around[3] += (paths("{}.13", range(0,6)))
around[3] += (paths("{}.14", range(0,6)))
around[3] += [0.11, 1.11, 4.11, 5.11]
around[3] += [0.12, 1.12, 4.12, 5.12]

OVALS = [
(pawn_path_1, start_square[0], "green2"),		#GREEN
(pawn_path_4, start_square[1], "orange red"),			#RED
(pawn_path_2, start_square[2], "yellow"),		#YELLOW
(pawn_path_3, start_square[3], "deep sky blue")			#BLUE
]
# Stops
stack_points = [['1.6','2.8'],['8.1','6.2'],['12.6','13.8'],['8.12','6.13']]
sp = ['1.6','2.8','8.1','6.2','12.6','13.8','8.12','6.13', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '1.7', '2.7', '3.7', '4.7', '5.7', '6.7', '8.7', '9.7', '10.7', '11.7', '12.7', '13.7', '7.8', '7.9' ,'7.10', '7.11', '7.12', '7.13']
# Filling Colors In Boxes
def highlight(root):
	# Main Tracks
	for c in path:
		root.itemconfigure(c, fill="azure", activewidth=2,outline="seashell4" ,activeoutline="black")
	color = [C_1_A, C_3_A, C_4_A, C_2_A]
	# Ending paths
	for n,k in enumerate(home_path):
		for j in k:
			root.itemconfigure(j, fill=color[n], activewidth=2, outline='gray10')

	# Stations
	for n,s in enumerate(start_square):
		for j,c in enumerate(s):
			root.itemconfigure(c, fill="white", activewidth=2, outline="gray10")
			coordinates = root.coords(c)
			
	# Around Stations
	for n,s in enumerate(around):
		for j,c in enumerate(s):
			root.itemconfigure(c, fill=COLOR[n], activewidth=2)
			coordinates = root.coords(c)
			
	# Stops
	for n,s in enumerate(stack_points):
		for j,c in enumerate(s):
			root.itemconfigure(c, fill=COLOR[n], activewidth=3)
	
	a1,b1,c1,d1 = getcoordinates(root , '5.0')
	a2,b2,c2,d2 = getcoordinates(root , '5.14')
	root.create_line(c1,b1,c2,d2, fill="black",width="2")
	
	a1,b1,c1,d1 = getcoordinates(root , '9.0')
	a2,b2,c2,d2 = getcoordinates(root , '9.14')
	root.create_line(a1,b1,a2,d2, fill="black",width="2")
	
	
	a1,b1,c1,d1 = getcoordinates(root , '0.5')
	a2,b2,c2,d2 = getcoordinates(root , '14.5')
	root.create_line(a1,d1,c2,d2, fill="black",width="2")
	
	a1,b1,c1,d1 = getcoordinates(root , '0.9')
	a2,b2,c2,d2 = getcoordinates(root , '14.9')
	root.create_line(a1,b1,c2,b2, fill="black",width="2")
	
	a1,b1,c1,d1 = getcoordinates(root , '0.0')
	a2,b2,c2,d2 = getcoordinates(root , '14.14')
	root.create_rectangle(a1,b1,c2,d2, outline="black",width="2")
	
	return
	
# Creating Square Boxes
def create_squares(root):
	for i in range(AREA):
		for j in range(AREA):
			root.create_rectangle(S_WIDTH*i, S_HEIGHT*j, (S_WIDTH*i)+S_WIDTH,(S_HEIGHT*j)+S_HEIGHT, tag="{}.{}".format(i,j), outline='white', fill="seashell2")	
			#A tag is a string that you can associate with objects on the canvas
	return

# Creating Ovals
def create_ovals(root):
	oval_identity=[]
	# a = Track
	# b = Station
	# c = Color
	for a,b,c in OVALS:		
		for i in b:
			s = root.create_oval(getcoordinates(root,i), fill=c, tag="C{}".format(i), activewidth=2)
			oval_identity.append("C{}".format(i))
	return

# Get Tag Coordinates In Canvas
def getcoordinates(root, tags):
	return root.coords(tags)

def move_oval(root, tag, target):			#tag is goti ka naam
	a,b,c,d = getcoordinates(root , tag)
	e,f,g,h = getcoordinates(root, target)
	root.move(tag, g-c, h-d)
	
def clear_oval(root, tag):
	root.delete(tag)

prevlist = []
def stack_oval(root, txtlist):			#txtlist is a dictinary. key= position, value=txt
	global prevlist
	for i in range(len(prevlist)):
		root.delete(prevlist[i])
	prevlist = []
	for i in txtlist:
		txt="t"+i
		a,b,c,d = getcoordinates(root, i)
		x=a+((c-a)/2.0)
		y=b+((d-b)/2.0)
		root.create_text(x,y, text=txtlist[i], tag=txt, font=("bold"))
		
		prevlist.append(txt)

def create_playerturn(root, txt):
	tag="dpbox"
	root.delete(tag)
	canvas_id = root.create_text(S_WIDTH*AREA*0.5, S_HEIGHT*AREA+ S_HEIGHT*2, tag="dpbox", font=("Comic Sans MS", 12, "bold"), anchor="center")
	root.itemconfig(canvas_id, text=txt)

r = Tkinter.Tk()
r.title("Ludo game")
root=Tkinter.Canvas()
