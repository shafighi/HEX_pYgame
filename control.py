## Francisco Rivera - franr.com.ar/hex |
## ------------------------------------/

# import os
import random
from threading import Thread
import pygame
import copy

# constantes
RUN = True
LONG = 20
YELLOW = (255, 231, 0)  #yellow
YELLOW_C = (255, 255, 50)
BLUE = (0, 127, 245) #blue
BLUE_C = (50, 177, 255)
WHITE = (255,255,255)
BLACK = (0,0,0)
current_player_color = BLUE_C
player = BLUE
FLAG = 0


lastBlueValue=0
max_depth=0

# change player
def change_player():
    global player
    global current_player_color

    if player == BLUE:
        player = YELLOW
        current_player_color = YELLOW_C
    else:
        player = BLUE
        current_player_color = BLUE_C


class Font: #source

    def __init__(self):
        pygame.font.init()
        self.Font = pygame.font.Font("cubicfive10.ttf", 20)

    def render(self, texto):
        return self.Font.render(texto, False, BLACK)


class Hexagon:

    def __init__(self, screen, x, y, id, BLUE_p, BLUE_f, YELLOW_p, YELLOW_f):
        self.screen = screen    #parde
        self.d = LONG
        self.color = WHITE
        self.marked = False #marked
        self.id = id
        self.BLUE_p = BLUE_p
        self.BLUE_f = BLUE_f
        self.YELLOW_p = YELLOW_p
        self.YELLOW_f = YELLOW_f

        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.d/2 - 4, self.y - self.d, self.d + 8, self.d*2)

    def draw(self): #draw
        pl = [(self.x - self.d, self.y),
              (self.x - self.d/2, self.y - self.d),
              (self.x + self.d/2, self.y - self.d),
              (self.x + self.d, self.y),
              (self.x + self.d/2, self.y + self.d),
              (self.x - self.d/2, self.y + self.d)]
        pygame.draw.polygon(self.screen, self.color, pl)
        pygame.draw.polygon(self.screen, (100,100,100), pl, 3)
        # pygame.draw.rect(self.screen, BLACK, self.rect)
    def evaluationOneBlue(self,h):
        mini = 10000
        maxi = 0
        maxPathBlue =-1
        blueValue=0
        BluePathRow=-1
        if (bluePathes[0][0]==0):
            if(h.id>50 and h.id<55) or (h.id>61 and h.id<66) or (h.id>72 and h.id<77):
                if(1>maxPathBlue):
                    maxPathBlue=1
                    BluePathRow=0
            else:
                if(0>maxPathBlue):
                    maxPathBlue=0
                    BluePathRow=0
        else:
            for i in range (0, len(bluePathes)):
                nowStateListCopy = copy.deepcopy(bluePathes[i])
                for j in nowStateListCopy:# mishe ino negah darim ke har dafe hesab nakonim
                    if (j<mini):
                        mini=j
                    if (j>maxi):
                        maxi=j
         
                if (h.id==mini-1) or (h.id==maxi+1) or (h.id==mini-2) or (h.id==maxi+2) :
                    nowStateListCopy.append(h.id)
                    last = nowStateListCopy[0]
                    #for item in nowStateListCopy:
                        #if(item == last+10 or 
                    if(len(nowStateListCopy)>maxPathBlue):
                        maxPathBlue=len(nowStateListCopy)+1
                        BluePathRow=i
                else:
                    maxPathBlue=0
        if(BluePathRow==-1):
            bluePathes.append([h.id])
        else:
            if(BluePathRow==0 and bluePathes[BluePathRow]==0):
                bluePathes[BluePathRow][0] = h.id
            else:
                bluePathes[BluePathRow].append(h.id)
        blueValue =  maxPathBlue
        return blueValue
    def update(self, x, y, p):
        c = self.rect.collidepoint(x, y)
        if c:
            if p and self.color == current_player_color:
                self.mark() #mark(50, 177, 255)
                #if (current_player_color==(50, 177, 255)):
                    #lastBlueValue = self.evaluationOneBlue(self)
                change_player()
                return 1
            return 2
        return 0
   
    def mark(self):
        self.color = player
        self.marked = True

    def focus(self):    #focus
        if not self.marked:
            self.color = current_player_color

    def blur(self): #blur
        if not self.marked:
            self.color = WHITE


class Board:    #board

    def __init__(self, screen):
        self.screen = screen
        self.initiate()
        self.targetH = None

    def initiate(self): #start
        self.hexas = {}
        self.foco = None    #focus
        self.id = 0
        dx = LONG
        dy = LONG*11
        # Board
        for i in range(11):
            for e in range(11):
                x = dx + LONG*(e + i)*1.5
                y = dy + LONG*(i - e)
                self.id += 1
                azp, azf, amp, amf = self.border(self.id)
                self.hexas[self.id] = Hexagon(self.screen, x, y, self.id, azp, azf, amp, amf)
        self.opp = Opponent()

    def border(self, id):   #edge

        if id == 1:
            return True, False, True, False

        elif id == 11:
            return False, True, True, False

        elif id == 111:
            return True, False, False, True

        elif id == 121:
            return False, True, False, True

        elif id % 11 == 1:
            return True, False, False, False

        elif id > 1 and id < 11:
            return False, False, True, False

        elif (id % 11) == 0:
            return False, True, False, False

        elif (id - 110) > 1 and (id - 110) < 11:
            return False, False, False, True

        else:
            return False, False, False, False


    def draw(self):
        global FLAG

        opp = self.opp

        pygame.draw.rect(self.screen, YELLOW, (0, 0, LONG*11*1.5, LONG*11))
        pygame.draw.rect(self.screen, BLUE, (LONG*11*1.5, 0, LONG*11*1.5*2, LONG*11))
        pygame.draw.rect(self.screen, BLUE, (0, LONG*11, LONG*11*1.5, LONG*11))
        pygame.draw.rect(self.screen, YELLOW, (LONG*11*1.5, LONG*11, LONG*11*1.5, LONG*11))
        x, y = pygame.mouse.get_pos()
        if FLAG==0:
            click = pygame.event.wait().type == pygame.MOUSEBUTTONDOWN
        if FLAG == 2:
            FLAG = 0
            x = 0
            y = 0
            click = False
        win = None  #win

        if player == BLUE:

                for h in self.hexas.values():

                    r = h.update(x, y, click)
                    if r:

                        if r == 1:

                            self.foco = None
                            win = self.resolver(h.id)

                        elif r == 2:

                            if self.foco and self.foco != h:

                                self.foco.blur()
                            self.foco = h
                    if self.foco:

                        self.foco.focus()
                    h.draw()
        elif player == YELLOW:

            if FLAG != 1:
                h = opp.getTargetHex(self.hexas)
                self.targetH = h
            else:
                h = self.targetH

            r = h.update(h.x, h.y, True)

            if r:
                if r == 1:

                    self.foco = None
                    win = self.resolver(h.id)

                    FLAG = 2
                elif r == 2:

                    FLAG = 1
                    if self.foco and self.foco != h:
                        self.foco.blur()
                    self.foco = h
                if self.foco:
                    
                    self.foco.focus()
                h.draw()
        return win

    def resolver(self, id):
        viewed = []
        color = self.hexas[id].color
        chain = [h for h in self.around(id, color, viewed)] #chain
        if self.beginning(chain, color) and self.end(chain, color):
            return color
        return None

    def around(self, id, color, viewed):    #around
        # returns ids of Hexagons of the same color around one
        if self.border(id)[0] == True:
            pos = 0, -10, -11, 1, 11
        elif self.border(id)[1] == True:
            pos = 0, -11, -1, 11, 10
        else:
            pos = 0, -10, -11, 1, -1, 11, 10
        alr = [self.hexas[id+i].id for i in pos if (self.hexas.has_key(id+i) and (id+i not in viewed))]
        chain = [self.hexas[h].id for h in alr if (self.hexas[h].color == color)]
        viewed.extend(chain)
        for i in chain:
            self.around(i, color, viewed)
        return viewed   #viewed

    def beginning(self, chain, color):  #principle
        if color == BLUE:
            for c in chain:
                if self.hexas[c].BLUE_p:
                    return True
        else:
            for c in chain:
                if self.hexas[c].YELLOW_p:
                    return True
        return False

    def end(self, chain, color):
        if color == BLUE:
            for c in chain:
                if self.hexas[c].BLUE_f:
                    return True
        else:
            for c in chain:
                if self.hexas[c].YELLOW_f:
                    return True
        return False

class Opponent:#the functions here are just samples
    def __init__(self): #constructor, use the pattern "self.variable" to define class attributes. you can access them later by the same syntax.
        self.cloneHexas = {}

    def printall(self, hexas):
        for h in hexas.values():
            print (h.color)
            print (h.marked)
            print (h.id)

    def printHex(self, h):
        print (h.color)
        print (h.marked)
        print (h.id)

    def getSimpleCloneForModel(self, hexas): # I thought you may have problems with cloning a dictionary, you see how python is easy?
        return copy.deepcopy(hexas)

    def setHexColor(self, h, color): #you can use a function like this for setting colors
        h.marked = True
        h.color = color
        
    def evaluation(self):
        bluePathes = [[[0],0,0]]
        yellowPathes = [[[0],0,0]]
        linkedYellowPath = [[[-1],100000,0,0]]
        linkedBluePath = [[[-1],100000,0,0]]
        bluePathesCopy = bluePathes
        yellowPathesCopy = yellowPathes
        linkedYellowPathCopy = linkedYellowPath
        linkedBluePathCopy = linkedBluePath
        return bluePathesCopy,yellowPathesCopy,linkedBluePathCopy,linkedYellowPathCopy
    
    def constructStateOfNode(self,hexa ,nowState,h,color):
        flag=-1
        if(nowState[color][0][0][0]==0):
            flag=1
            nowState[color][0][0][0]=h.id
            nowState[color][0][1]=h.id
            nowState[color][0][2]=h.id
        else:            
            whichList=-1
            for i in range (0, len(nowState[color])):
                mini = nowState[color][i][1]
                maxi = nowState[color][i][2]
                if(color==1):
                    if ((h.id==mini-11) or (h.id==maxi+11) or (h.id%11!=1 and (h.id==mini-10)) or (h.id%11!=0 and (h.id==maxi+10))):

                        flag=1
                        whichList=i
                        nowState[color][i][0].append(h.id)
                        if(h.id<mini):
                            nowState[color][i][1]=h.id
                        else:
                            nowState[color][i][2]=h.id
                if(color==0):
                    if (h.id==mini-1 and h.id%11!=0) or (h.id==maxi+1 and h.id%11!=1) or (h.id%11!=1 and h.id==mini-10) or (h.id%11!=0 and h.id==maxi+10):
                        flag=1
                        whichList=i
                        nowState[color][i][0].append(h.id)
                        if((h.id%11)<(mini%11)):
                            nowState[color][i][1]=h.id
                        else:
                            nowState[color][i][2]=h.id
            if(flag==-1):
                nowState[color].append([[h.id],h.id,h.id])
                whichList=len(nowState[color])-1
            self.makeLinks(hexa,nowState,h,color,whichList)
    
    def makeLinks(self,hexa,nowState,h,color,whichList):
        
        for listNum in range (0, len(nowState[color])):
            listNumFound=-1
            whichListFound=-1
            flag=-1
            if (color==1):
                if(h.id>11 and h.id<110):
                    ifC = ((h.id%11!=1 and h.id==nowState[color][listNum][1]-21 and (hexa[h.id+11].marked==False or hexa[h.id+10].marked==False) ) or (h.id%11!=0 and h.id==nowState[color][listNum][2]+21 and( hexa[h.id-11].marked==False or hexa[h.id-10].marked==False ))) 
                elif(h.id>11):
                    ifC = ((h.id%11!=1 and h.id==nowState[color][listNum][1]-21 and (hexa[h.id+11].marked==False or hexa[h.id+10].marked==False) ) or(h.id%11!=0 and h.id==nowState[color][listNum][2]+21)) 
                elif(h.id<112):
                    ifC = ((h.id%11!=1 and h.id==nowState[color][listNum][1]-21 ) or (h.id%11!=0 and h.id==nowState[color][listNum][2]+21 and (hexa[h.id-11].marked==False or hexa[h.id-10].marked==False) )) 
                else:
                    ifC = ((h.id%11!=1 and h.id==nowState[color][listNum][1]-21 ) or (h.id%11!=0 and h.id==nowState[color][listNum][2]+21 )) 
            if (color==0):
                if(h.id>11 and h.id<110):
                    ifC = ((h.id%11!=0 and h.id==nowState[color][listNum][1]-12 and (hexa[h.id-11].marked==False or hexa[h.id-1].marked==False) ) or ( h.id%11!=0 and h.id%11!=10 and h.id==nowState[color][listNum][1]+9 and (hexa[h.id+11].marked==False or hexa[h.id-1].marked==False) ) or (h.id%11!=1 and h.id%11!=2 and  h.id==nowState[color][listNum][2]-9 and (hexa[h.id-10].marked==False or hexa[h.id+1].marked==False) ) or ( h.id==nowState[color][listNum][2]+12 and (hexa[h.id+10].marked==False or hexa[h.id+1].marked==False) )) 
                elif(h.id>11):
                    ifC = ((h.id%11!=0 and h.id==nowState[color][listNum][1]-12 and (hexa[h.id-11].marked==False or hexa[h.id-1].marked==False) ) or ( h.id%11!=0 and h.id%11!=10 and h.id==nowState[color][listNum][1]+9  ) or (h.id%11!=1 and h.id%11!=2 and  h.id==nowState[color][listNum][2]-9 ) or ( h.id==nowState[color][listNum][2]+12 )) 
                elif(h.id<110):
                    ifC = ((h.id%11!=0 and h.id==nowState[color][listNum][1]-12  ) or (h.id%11!=0 and  h.id==nowState[color][listNum][1]+9  ) or (h.id%11!=1 and h.id%11!=2 and h.id==nowState[color][listNum][2]-9  ) or ( h.id==nowState[color][listNum][2]+12 and (hexa[h.id+10].marked==False or hexa[h.id+1].marked==False) )) 
                else:
                    ifC = ((h.id%11!=0 and h.id==nowState[color][listNum][1]-12  ) or (h.id%11!=0 and h.id==nowState[color][listNum][1]+9  ) or (h.id%11!=1 and h.id%11!=2 and  h.id==nowState[color][listNum][2]-9  ) or ( h.id==nowState[color][listNum][2]+12 )) 
            for linkNum in range (0, len(nowState[color+2])):
                if(listNum in nowState[color+2][linkNum][0])==True:
                    listNumFound=linkNum
                if(whichList in nowState[color+2][linkNum][0])==True:
                    whichListFound=linkNum
            if(ifC) :
                flag=1
                if(listNumFound==-1 and whichListFound==-1):
                    #make a new link
                    self.modifyLinks(nowState,color,whichList,listNum,listNumFound,whichListFound,"NEWLINK")

                if(listNumFound!=-1 and whichListFound==-1):
                    #add to link1
                    self.modifyLinks(nowState,color,whichList,listNum,listNumFound,whichListFound,"ADDTOLINK1")

                if(listNumFound==-1 and whichListFound!=-1):
                    #add to link2
                    self.modifyLinks(nowState,color,whichList,listNum,listNumFound,whichListFound,"ADDTOLINK1")

                if(listNumFound!=-1 and whichListFound!=-1):
                    #merg two link
                    self.modifyLinks(nowState,color,whichList,listNum,listNumFound,whichListFound,"MERG2LINK")
            if(flag==-1):
                if (color==1):
                    mini=nowState[color+2][linkNum][1]
                    maxi=nowState[color+2][linkNum][2]
                    if ((h.id==mini-11) or (h.id==maxi+11) or (h.id%11!=1 and (h.id==mini-10)) or (h.id%11!=0 and (h.id==maxi+10))):
                        nowState[color+2][linkNum][1]= min (h.id,nowState[color+2][linkNum][1])
                        nowState[color+2][linkNum][2]= max (h.id,nowState[color+2][linkNum][2])
                if (color==0):
                    mini=nowState[color][linkNum][1]
                    maxi=nowState[color][linkNum][2]
                    if (h.id==mini-1 and h.id%11!=0) or (h.id==maxi+1 and h.id%11!=1):
                        if(h.id%11<nowState[color+2][linkNum][1]%11):
                            nowState[color+2][listNum][1]=h.id
                        if(h.id>nowState[color+2][linkNum][2]):
                            nowState[color+2][listNum][2]= h.id      
    def modifyLinks(self, nowState,color,whichList,listNum,listNumFound,whichListFound,job):
        if(job=="NEWLINK"):
            if(nowState[color][listNum][1]%11 < nowState[color][whichList][1]%11):
                mini=nowState[color][listNum][1]
            else:
                mini=nowState[color][whichList][1]
            if(nowState[color][listNum][2]%11 < nowState[color][whichList][2]%11):
                maxi=nowState[color][whichList][2]
            else :
                maxi=nowState[color][listNum][2]
                
            nowState[color+2].append([[whichList,listNum],mini,maxi,len(nowState[color][whichList][0])+len(nowState[color][listNum][0])+1])   

        if(job=="ADDTOLINK1"):
            nowState[color+2][listNumFound][0].append(whichList)
            if(nowState[color+2][listNumFound][1]%11 < nowState[color][whichList][1]%11):
                mini=nowState[color+2][listNumFound][1]
            else :
                mini= nowState[color][whichList][1]
                
            if(nowState[color+2][listNumFound][2]%11 < nowState[color][whichList][2]%11):
                maxi=nowState[color][whichList][2]
            else:
                maxi=nowState[color+2][listNumFound][2]
                
            nowState[color+2][listNumFound][1]=mini
            nowState[color+2][listNumFound][2]=maxi
            nowState[color+2][listNumFound][3]=nowState[color+2][listNumFound][3]+len(nowState[color][whichList][0])+1

        if(job=="ADDTOLINK2"):
            if(nowState[color+2][whichListFound][1]%11 < nowState[color][listNum][1]%11):
                mini=nowState[color+2][whichListFound][1]
            else :
                mini= nowState[color][listNum][1]
                
            if(nowState[color+2][whichListFound][1]%11 < nowState[color][listNum][1]%11):
                maxi=nowState[color][listNum][1]
            else:
                maxi=nowState[color+2][whichListFound][1]
            
            nowState[color+2][whichListFound][0].append(listNum)
            nowState[color+2][whichListFound][1]=mini
            nowState[color+2][whichListFound][2]=maxi
            nowState[color+2][whichListFound][3]=nowState[color+2][whichListFound][3]+len(nowState[color][listNum][0])+1        

        if(job=="MERG2LINK"):
            if(nowState[color+2][listNumFound][1]%11 < nowState[color+2][whichListFound][1]%11):
                mini=nowState[color+2][listNumFound][1]
            else :
                mini= nowState[color+2][whichListFound][1]
                
            if(nowState[color+2][listNumFound][1]%11 < nowState[color+2][whichListFound][1]%11):
                maxi=nowState[color+2][whichListFound][1]
            else:
                maxi=nowState[color+2][listNumFound][1]
            
            nowState[color+2][whichListFound][0].append(nowState[color+2][listNumFound][0])
            nowState[color+2][listNumFound][1]=mini
            nowState[color+2][listNumFound][2]=maxi
            nowState[color+2][listNumFound][3]=nowState[color+2][listNumFound][3]+nowState[color+2][whichListFound][3]+1
            nowState[color+2][listNumFound]=[[0],0,0,0]

    def testLinks(self,hexa, nowState,h,color,whichList):

        Value=0
        for listNum in range (0, len(nowState[color])):
            listNumFound=-1
            whichListFound=-1
            ifC=(h.id%11!=1 and h.id==nowState[color][listNum][1]-21 ) or (h.id%11!=0 and h.id==nowState[color][listNum][2]+21)
            if(h.id-11>1 and h.id+11<120 ):
                ifC=(h.id%11!=1 and h.id==nowState[color][listNum][1]-21 and hexa[h.id+11].marked!=True and hexa[h.id+10].marked!=True) or (h.id%11!=0 and h.id==nowState[color][listNum][2]+21 and hexa[h.id-11].marked!=True and hexa[h.id-10].marked!=True)
            elif h.id-11>1 :
                ifC=(h.id%11!=1 and h.id==nowState[color][listNum][1]-21 and hexa[h.id+11].marked!=True and hexa[h.id+10].marked!=True)or (h.id%11!=0 and h.id==nowState[color][listNum][2]+21)
            elif h.id+11<120 :
                ifC =(h.id%11!=0 and h.id==nowState[color][listNum][2]+21 and hexa[h.id-11].marked!=True and hexa[h.id-10].marked!=True)or (h.id%11!=1 and h.id==nowState[color][listNum][1]-21 )
            if ifC:
                for linkNum in range (0, len(nowState[color+2])):
                    if(listNum in nowState[color+2][linkNum][0])==True:
                        listNumFound=linkNum
                    if(whichList in nowState[color+2][linkNum][0])==True:
                        whichListFound=linkNum
                wl=0
                if(whichList==len(nowState[color])):
                    wl = 1
                else :
                    wl = len(nowState[color][whichList])
                if(listNumFound==-1 and whichListFound==-1):
                    #make a new link
                    Value = len(nowState[color][listNum][0])+wl+1

                if(listNumFound!=-1 and whichListFound==-1):
                    #add to link1
                    Value = nowState[2+color][listNumFound][3]+wl+1
                    
                if(listNumFound==-1 and whichListFound!=-1):
                    #add to link2
                    Value = nowState[2+color][whichListFound][3]+len(nowState[color][listNum][0])+1

                if(listNumFound!=-1 and whichListFound!=-1):
                    #merg two link
                    Value = nowState[2+color][whichListFound][3]+nowState[2+color][listNumFound][3]+1
        return Value

    def stateOfNode(self,hexa, nowState,h,color):

        flag=-1
        whichList=-1
        Value=-1
        if(nowState[color][0][0][0]==0):
            whichList=0
            flag= 1
            if(nowState[1-color][0][0][0]!=0):
                hd=nowState[1-color][0][0][0]
                if(hd>47 and hd<50) or (hd>58 and hd<61) or (hd>69 and hd<72) or (hd>36 and hd<39):
                    if(h.id==hd-8):
                        Value=max(Value,2)
                elif(hd>=50 and hd<53) or (hd>=61 and hd<64) or (hd>=72 and hd<75) or (hd>=39 and hd<42):
                    if(h.id==hd+8):
                        Value=max(Value,2)
                elif(hd%11<5 and hd<50 ):
                    if(h.id==nowState[1-color][0][0][0]+16 ):
                        Value=max(Value,1)
                elif(hd%11<5 and hd>50 ):
                    if(h.id==nowState[1-color][0][0][0]-16):
                        Value=max(Value,1)
                elif(hd%11>5 and hd<50 ):
                    if(h.id==nowState[1-color][0][0][0]+8 ):
                        Value=max(Value,1)
                elif(hd%11>5 and hd>50 ):
                    if( h.id==nowState[1-color][0][0][0]-16):
                        Value=max(Value,1)
                else:
                    Value=0
            else:
                if(h.id>47 and h.id<52) or (h.id>58 and h.id<63) or (h.id>69 and h.id<74) or (h.id>36 and h.id<41):
                    Value=1

        else:
            for i in range (0, len(nowState[color])):
                mini = nowState[color][i][1]
                maxi = nowState[color][i][2]
                if(color==1):
                    if ((h.id==mini-11) or (h.id==maxi+11) or (h.id%11!=1 and (h.id==mini-10)) or (h.id%11!=0 and (h.id==maxi+10))):
                        for listItem in nowState[2+color]:
                            if((i) in listItem[0])==True:
                                Value = max(Value,listItem[3]+1)
                                if((h.id==mini-11) or (h.id==maxi+10)):
                                    co=BLUE
                                    if(color==0):
                                        co=YELLOW
                                    if(h.id+1<122):
                                        if(hexa[h.id+1].marked==True and hexa[h.id+1].color==co):
                                            Value +=7
        
                                if((h.id==mini-10) or (h.id==maxi+11)):
                                    co=BLUE
                                    if(color==0):
                                        co=YELLOW
                                    if(h.id-1>0):
                                        if(hexa[h.id-1].marked==True and hexa[h.id-1].color==co):
                                            Value +=7
                if((h.id==mini-11 ) or (h.id==maxi+10 and h.id%11!=0)):
                    co=BLUE
                    if(color==0):
                        co=YELLOW
                    if(h.id<121):
                        if(hexa[h.id+1].marked==True and hexa[h.id+1].color==co):
                            Value +=len(nowState[color][i][0])+5
        
                if((h.id==mini-10 and h.id%11!=1 ) or (h.id==maxi+11)):
                    co=BLUE
                    if(color==0):
                        co=YELLOW
                    if(h.id-1>0):
                        if(hexa[h.id-1].marked==True and hexa[h.id-1].color==co):
                            Value +=len(nowState[color][i][0])+5

                        flag= 1
                        whichList=i
                        Value = max(Value,len(nowState[color][i][0])) 

                if(color==0):
                    if (h.id==mini-1 and h.id%11!=0) or (h.id==maxi+1 and h.id%11!=1): #or (h.id%11!=1 and h.id==mini-10) or (h.id%11!=0 and h.id==maxi+10):
                        for listItem in nowState[2+color]:
                            if((i) in listItem[0])==True:
                                Value = max(Value,listItem[3]+1)
                                ifC=False
                                if(h.id>11 and h.id<120):
                                    ifC= (h.id==mini-11)or (h.id==maxi+1)
                                elif(h.id>11):
                                    ifC= (h.id==mini-11)
                                elif(h.id<120):
                                    ifC= (h.id==mini+1)
                                    
                                if(ifC):
                                    co=BLUE
                                    if(color==1):
                                        co=YELLOW
                                    if(h.id+10<122):
                                        if(hexa[h.id+10].marked==True and hexa[h.id+10].color==co):
                                            Value +=7

                                if(h.id>1 and h.id<111):
                                    ifC= (h.id==mini+11)or (h.id==maxi-1)
                                elif(h.id>1):
                                    ifC= (h.id==mini-1)
                                elif(h.id<111):
                                    ifC= (h.id==mini+11)
                                    
                                if((h.id==mini-1) or (h.id==maxi+11)):
                                    co=BLUE
                                    if(color==1):
                                        co=YELLOW
                                    if(h.id-10>0):
                                        if(hexa[h.id-10].marked==True and hexa[h.id-10].color==co):
                                            Value +=7
                        flag= 1
                        whichList=i
                        Value = max(Value,len(nowState[color][i][0]))

            if(flag==-1):
                whichList=len(nowState[color])
                Value = max(Value,0)
                
            Value = max(self.testLinks(hexa,nowState,h,color,whichList),Value)
        otherPath=-1
        path=-1
        link=-1
        for i in range (0, len(nowState[1-color])):
            if(otherPath<len(nowState[1-color][i][0])):
                otherPath=len(nowState[1-color][i][0])
                path=i
        if(otherPath==1):
            otherPath=0
            hd=nowState[1-color][path][0][0]
            if(hd>47 and hd<52) or (hd>58 and hd<63) or (hd>69 and hd<74) or (hd>36 and hd<41):
                otherPath=1
        if(otherPath>3 and color==1):
            if((h.id==nowState[1-color][path][1]-1 and h.id%11!=0) or (h.id==nowState[1-color][path][2]+1 and h.id%11!=1)):
                Value=max(Value,otherPath+2)

        if(otherPath>3 and color==0):
            if((h.id==nowState[1-color][path][1]-10 and h.id%11!=1) or (h.id==nowState[1-color][path][2]+10 and h.id%11!=0) or (h.id==nowState[1-color][path][1]-11) or (h.id==nowState[1-color][path][2]+11)):
                Value=max(Value,otherPath+2)

        if(otherPath>6 and color==1):####
            if((h.id==nowState[1-color][path][1]-1 and h.id%11!=0) or (h.id==nowState[1-color][path][2]+1 and h.id%11!=1)):
                Value=max(Value,otherPath+4)

        if(otherPath>6 and color==0):
            if((h.id==nowState[1-color][path][1]-10 and h.id%11!=1) or (h.id==nowState[1-color][path][2]+10 and h.id%11!=0) or (h.id==nowState[1-color][path][1]-11) or (h.id==nowState[1-color][path][2]+11)):
                Value=max(Value,otherPath+4)
                
        for item in range (0, len(nowState[3-color])):
            if(otherPath<nowState[3-color][item][3]):
                otherPath=nowState[3-color][item][3]
                link =item
                
        if(otherPath>3 and color==0 and link!=-1):
            if((h.id==nowState[3-color][link][1]-11 ) or (h.id==nowState[3-color][link][1]+10 and h.id%11!=0) or (h.id==nowState[3-color][link][2]-10 and h.id%11!=1) or h.id==nowState[3-color][link][2]+11):
                Value=max(Value,nowState[3-color][link][3]+3)

        if(otherPath>3 and color==1 and link!=-1):
            if((h.id==nowState[3-color][link][1]-1 and h.id%11!=0) or (h.id==nowState[3-color][link][2]+1 and h.id%11!=1)):
                Value=max(Value,nowState[3-color][link][3]+3)

        if(otherPath>6 and color==0 and link!=-1):
            if((h.id==nowState[3-color][link][1]-11) or (h.id==nowState[3-color][link][1]+10 and h.id%11!=0) or (h.id==nowState[3-color][link][2]-10 and h.id%11!=1) or h.id==nowState[3-color][link][2]+11):
                Value=max(Value,nowState[3-color][link][3]+5)

        if(otherPath>6 and color==1 and link!=-1):
            if((h.id==nowState[3-color][link][1]-1 and h.id%11!=0) or (h.id==nowState[3-color][link][2]+1 and h.id%11!=1)):
                Value=max(Value,nowState[3-color][link][3]+5)

        if(h.id>11 and h.id<110):
            if(color==0):
                co=YELLOW
            else:
                co=BLUE
            if(color==1):    
                if((hexa[h.id+1].color==co and hexa[h.id-10].color==co and hexa[h.id-11].color==co) or (hexa[h.id-1].color==co and hexa[h.id-10].color==co and hexa[h.id-11].color==co) or (hexa[h.id+1].color==co and hexa[h.id+10].color==co and hexa[h.id+11].color==co) or (hexa[h.id-11].color==co and hexa[h.id+10].color==co and hexa[h.id+11].color==co)):
                    Value=0
            else:
                if((hexa[h.id-1].color==co and hexa[h.id-11].color==co and hexa[h.id+10].color==co) or (hexa[h.id+11].color==co and hexa[h.id+1].color==co and hexa[h.id-10].color==co)):
                    Value=0

        if(color==1):
            return Value-otherPath
        else :
            return otherPath-Value


    def evalList(self,hexas,color):
        values = {}
        hexasDict = {}
        for h in hexas.values():
            if not h.marked :
                h.marked = True
                if(color==1):
                    h.color = YELLOW
                else:
                    h.color= BLUE
                hexasDict[h] = (copy.deepcopy(hexas))
                h.color = WHITE
                h.marked = False
        return hexasDict
    def evalLeaf(self,color,hexaDict):
        values = {}
        colori=-1
        nowState=self.evaluation()
        value=0
        pathRow=0
        nowState=self.evaluation()
        for item in hexaDict.values():
            if item.marked :
                if(item.color==YELLOW):
                    colori=1
                else :
                    colori=0
                self.constructStateOfNode(hexaDict,nowState,item,colori)
        for h in hexaDict.values():
            if not h.marked:
                temp = copy.deepcopy(nowState)
                value = (self.stateOfNode(hexaDict,temp,h,color))
                values[h] = (value)#,copy.deepcopy(nowState),pathRow)
                    
        nowState=[]
        return values
    
    def min_max(self,MinOrMax,hexas,nowState,depth):
        hexasCopy = hexas#copy.deepcopy(hexas)
        hexasDict = {}
        if(depth<=max_depth-1):
            hexasDict = self.evalList(hexasCopy,MinOrMax)
        if MinOrMax==0 :
            Min = 1000
            listM={}
            if(depth>=max_depth-1):
                values = self.evalLeaf(MinOrMax,hexasCopy)
                for hh in values :
                    if(Min==1000):
                        Min=hh
                    elif values[hh]<values[Min] :
                        Min = hh

                return values[Min],Min

            else:
                counter =0
                for hl in hexasDict:
                    listM[hl]=(self.min_max(1,hexasDict[hl],[[0]],depth+1))
                mmin = (1000,-1)                    
                for temp in listM:
                    if listM[temp][0]<mmin[0]:
                        mmin = listM[temp]
                return mmin,temp
            
        if MinOrMax==1 :
            Max=-1000
            listM={}
            if(depth>=max_depth-1):
                values = self.evalLeaf(MinOrMax,hexasCopy)
                for hh in values :
                    if(Max==-1000):
                        Max = hh
                    elif values[hh]>values[Max] :
                        Max = hh
                return values[Max],Max
                   
            else :
                counter =0
                hmax=0
                for hl in hexasDict:
                    listM[hl]=(self.min_max(0,hexasDict[hl],[[0]],depth+1))
                mmax = (-1000,-1)                    
                for temp in listM:
                    if listM[temp][0]>mmax[0]:
                        mmax = listM[temp]
                        hmax=temp
                return mmax,hmax

    def Hex(self, hexas):  #this is: your main function, you must return a hex, here is a simple example
        nowState = (self.evaluation())
        m,Temp = self.min_max(1,hexas,nowState,0)
        Temp.color = YELLOW
        hexas[Temp.id].color = YELLOW
        return Temp
            
    def getTargetHex(self,hexas):
        return self.Hex(hexas)
        
        
class screen:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hex")
        self.clock = pygame.time.Clock()
        # os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.screen = pygame.display.set_mode((LONG*32, LONG*11*2))
        self.t = Board(self.screen)
        self.win = True
        self.color = None
        self.Font = Font()
        self.main()

    def main(self):
        global RUN
        while RUN:


            self.screen.fill(BLUE_C)
            # mostramos
            pygame.event.pump()
            if not self.win:
                color = self.t.draw()
                if color:
                    self.win = True
                    self.color = color
            else:
                self.winner()
            pygame.display.update()
            if not self.update():
                RUN = False
                break
            self.clock.tick(40)
        pygame.quit()



    def winner(self):   #winner
        if self.color == BLUE:
            color = "BLUE"
        else:
            color = "YELLOW"

        if self.color:
            r1 = self.Font.render("winner: " + color)
        r2 = self.Font.render("[i] initiate")
        r3 = self.Font.render("[Esc] exit")

        if self.color:
            self.screen.blit(r1, (200,50))
        self.screen.blit(r2, (200,200))
        self.screen.blit(r3, (200,250))

    def update(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_ESCAPE]:
            return False
        elif k[pygame.K_i]:
            self.win = False
            self.t.initiate()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
        return True

screen()
