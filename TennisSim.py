#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/env python
# coding: utf-8

# In[36]:


import numpy as np
from texttable import Texttable

    
PLAYSL = ["S1","S2","J1","J2","G1","G2"]
PLAYS = {"S1":0,"S2":1,"J1":2,"J2":3,"G1":4,"G2":5}
POINT_VALUES = ["0","15","30","40"]


class tenisSim:
    
    def __init__(self, surface):
        self.surface = surface
        
        
    def simPoint(self, j1, j2, isBP):
        state = "S1"
        states = [state]
        chain = self.updateChain(j1,j2,isBP)
        while state!="G1" and state !="G2":
            nState = np.random.choice(PLAYSL,replace=True,p=chain[PLAYS[state]])
            states.append((nState,chain[PLAYS[state]][PLAYS[nState]]))
            state =nState
        if state=="G1":
            return (states,0)
        else:
            return (states,1)
    
    def simGame(self,j1,j2):
        p1=0
        p2=0
        pToWin=4
        points = []
        
        print("---------------------")
        print("Game")
        
        while True:
            if(p2==(pToWin-1) and p2>p1):
                pW = self.simPoint(j1,j2,True)
            else:
                pW = self.simPoint(j1,j2,False)
            if(pW[1]==0):
                p1=p1+1
            else:
                p2=p2+1
            
            
            
            if(p1 == p2 and p1>=3):
                pToWin=pToWin+1
            
            if(p1 == pToWin):
                points.append(("Winner","40" if p2>3 else POINT_VALUES[p2]))
                return (0,points)
            elif(p2 == pToWin):
                points.append(("40" if p1>3 else POINT_VALUES[p1],"Winner"))
                return (1,points)
            
            if(p1<=3 and p2 <=3):
                points.append((POINT_VALUES[p1],POINT_VALUES[p2]))
            elif p1>p2:
                points.append(("Adv","40"))
            elif p1<p2:
                points.append(("40","Adv"))
            else:
                points.append(("40","40"))
            
    def simSet(self,j1,j2):
        g1=0
        g2=0
        gToWin=6
        turn = 0
        
        
        print("======================")
        print("Set")
        
        while True:
            scoreTable=[]
            if(g1==g2 and g1==6):
                gW = self.simTieBreak(j1,j2)
                if(gW==0):
                    g1=g1+1
                else:
                    g2=g2+1
            else:
                if(turn%2==0):
                    gW = self.simGame(j1,j2)
                    if(gW[0]==0):
                        g1=g1+1
                    else:
                        g2=g2+1
                    scoreTable = [[j1.name,j2.name]]
                else:
                    gW = self.simGame(j2,j1)
                    if(gW[0]==1):
                        g1=g1+1
                    else:
                        g2=g2+1
                    scoreTable = [[j2.name,j1.name]]
                
                
                for i in range(len(gW[1])):
                    scoreTable.append(gW[1][i])
                
                setScore = Texttable()
                setScore.add_rows(scoreTable)
                print(setScore.draw())
                    
                
            if(g1==g2 and g1==5):
                gToWin=gToWin+1
            
            turn=turn+1
            
            setScore = Texttable()
            setScore.add_rows([['Jugador', 'Set'], [j1.name, g1], [j2.name, g2]])
            print(setScore.draw())
                
            if(g1==gToWin):
                print("\nSet Winner = " + j1.name)
                print("======================\n")
                return (0,(g1,g2))
            elif(g2==gToWin):
                print("\nSet Winner = " + j2.name)
                print("======================\n")
                return (1,(g1,g2))
 
    def simTieBreak(self,j1,j2):
        p1 = 0
        p2 = 0
        pToWin = 7
        c = 0
        turn = 1
        
        
        print("---------------------")
        print("Tie Break")
        
        
        while(True):
            if(turn%2==0):
                c=c+1
            
            if(c%2==0):
                print("Serving -> " +j1.name)
                pW = self.simPoint(j1,j2,False)
                if(pW[1]==0):
                    p1 = p1+1
                else:
                    p2 = p2+1
            else:
                print("Serving -> " +j2.name)
                pW = self.simPoint(j2,j1,False)
                if(pW[1]==1):
                    p1 = p1+1
                else:
                    p2 = p2+1
            
            
            turn = turn + 1
            
            if(p1 == p2 and p1>=6):
                pToWin=pToWin+1
            
            tieScore = Texttable()
            tieScore.add_rows([['Jugador', 'Points'], [j1.name, p1], [j2.name, p2]])
            print(tieScore.draw())
            
            if(p1 == pToWin):
                print("Tie Break Winner -> " + j1.name)
                print("---------------------")
                print()
                return 0
            elif(p2 == pToWin):
                print("Tie Break Winner -> " + j2.name)
                print("---------------------")
                print()
                return 1
 
            
    def simMatch(self,j1,j2):
        s1 = 0
        s2 = 0
        sToWin = 3
        c = 0
        score = []
        scoreTable = [["Jugador"],[j1.name],[j2.name]]
        
        print("\nMatch\n")
        print("\n////////////////////////////\n")
        while(True):
            if(c%2==0):
                sWin=self.simSet(j1,j2)
                score.append((sWin[1][0],sWin[1][1]))
                if(sWin[0]==0):
                    s1=s1+1
                else:
                    s2=s2+1
                
            else:
                sWin=self.simSet(j2,j1)
                score.append((sWin[1][1],sWin[1][0]))
                if(sWin[0]==1):
                    s1=s1+1
                else:
                    s2=s2+1
            
            if(s1==sToWin):
                print("Match Winner " + j1.name)
                print(str(s1) + " - " + str(s2))
                
                for i in range(len(score)):
                    scoreTable[0].append("Set " + str(i+1))
                    scoreTable[1].append(score[i][0])
                    scoreTable[2].append(score[i][1])
                
                setScore = Texttable()
                setScore.add_rows(scoreTable)
                print(setScore.draw())
                
                print("\n////////////////////////////\n")
                
                
                return (0,score)
            elif(s2==sToWin):
                print("Match Winner " + j2.name)
                print(str(s1) + " - " + str(s2))
                
                for i in range(len(score)):
                    scoreTable[0].append("Set " + str(i+1))
                    scoreTable[1].append(score[i][0])
                    scoreTable[2].append(score[i][1])
                
                setScore = Texttable()
                setScore.add_rows(scoreTable)
                print(setScore.draw())
                
                print("\n////////////////////////////\n")
                
                
                return (1,score)
            
                
    def updateChain(self, j1, j2, isBreak):
        if self.surface == "Clay":
            return self.updateChain2(j1.clay,j2.clay,isBreak)
        elif self.surface == "Grass":
            return self.updateChain2(j1.grass,j2.grass,isBreak)
        else:
            return self.updateChain2(j1.hard,j2.hard,isBreak)
            
                
    
    def updateChain2(self,serves,recieves,isBreak):
        if(isBreak):
            FAce = (serves.sAce + recieves.sAce)*serves.sFServe/2
            FServe = serves.sFServe - FAce
            FFoul = 1 - FServe - FAce
            SAce = (serves.sAce + recieves.sAce)*FFoul/2
            DFoul = ((serves.sDFoult/FFoul)+(recieves.rDFoult/FFoul))/2
            SServe = 1 - SAce - DFoul
            FPlayer1 = (((serves.sFServeW + serves.sBPSaved)/2) + (((1 - recieves.rFServeW)+(1 - recieves.rBPWon))/2))/2
            FPlayer2 = 1 - FPlayer1
            SPlayer1 = (((serves.sSServeW + serves.sBPSaved)/2) + (((1 - recieves.rSServeW)+(1 - recieves.rBPWon))/2))/2
            SPlayer2 = 1 - SPlayer1
            
            self.chain = [
                [0,FFoul,FServe,0,FAce,0],
                [0,0,0,SServe,SAce,DFoul],
                [0,0,0,0,FPlayer1,FPlayer2],
                [0,0,0,0,SPlayer1,SPlayer2],
                [0,0,0,0,1,0],
                [0,0,0,0,0,1]
            ]
            
        else:
            FAce = (serves.sAce + recieves.sAce)*serves.sFServe/2
            FServe = serves.sFServe - FAce
            FFoul = 1 - FServe - FAce
            SAce = (serves.sAce + recieves.sAce)*FFoul/2
            DFoul = ((serves.sDFoult/FFoul)+(recieves.rDFoult/FFoul))/2
            SServe = 1 - SAce - DFoul
            FPlayer1 = (serves.sFServeW + (1 - recieves.rFServeW))/2
            FPlayer2 = 1 - FPlayer1
            SPlayer1 = (serves.sSServeW + (1 - recieves.sSServeW))/2
            SPlayer2 = 1 - SPlayer1
            
            self.chain = [
                [0,FFoul,FServe,0,FAce,0],
                [0,0,0,SServe,SAce,DFoul],
                [0,0,0,0,FPlayer1,FPlayer2],
                [0,0,0,0,SPlayer1,SPlayer2],
                [0,0,0,0,1,0],
                [0,0,0,0,0,1]
            ]
            
        return self.chain
            
        
            
class jugador:
    def __init__(self,name,clay,grass,hard):
        self.clay = clay
        self.grass = grass
        self.hard = hard
        self.name = name
        
class stats:
    def __init__(self,sAce,sDFoult,sFServe,sFServeW,sSServeW,sBPSaved,rAce,rDFoult,rFServeW,rSServeW,rBPWon):
        self.sAce = sAce
        self.sDFoult = sDFoult
        self.sFServe = sFServe
        self.sFServeW = sFServeW
        self.sSServeW = sSServeW
        self.sBPSaved = sBPSaved
        self.rAce = rAce
        self.rDFoult = rDFoult
        self.rFServeW = rFServeW
        self.rSServeW = rSServeW
        self.rBPWon = rBPWon
    
        
            
            
            
        
        
    
nadal = jugador("Nadal",
               stats(.033,.026,.687,.717,.607,.685,.044,.032,.414,.561,.483),
               stats(.106,.026,.619,.808,.607,.75,.148,.023,.318,.536,.429),
               stats(.074,.028,.626,.786,.584,.644,.103,.03,.316,.560,.424))
federer = jugador("Federer",
                 stats(.064,.018,.637,.758,.581,.739,.042,.034,.298,.532,.394),
                 stats(.104,.02,.65,.803,.623,.761,.062,.035,.315,.50,.469),
                 stats(.107,.022,.649,.781,.586,.677,.053,.033,.339,.489,.395))   
londero = jugador("Londero",
                   stats(.051,.031,.595,.718,.556,.649,.069,.041,.298,.509,.364),
                   stats(.063,.042,.614,.716,.531,.636,.101,.062,.283,.456,.31),
                   stats(.067,.040,.626,.684,.534,.629,.131,.043,.243,.492,.391))

def switch_player(value):
    return {
        '1': nadal,
        '2': federer,
        '3': londero,
    }.get(value)

def switch_field(value):
    return {
        '1': "Hard",
        '2': "Clay",
        '3': "Grass",
    }.get(value)    

while (True):
    w1=0
    w2=0
    n=0

    # take user input
    inp = input('Select player 1: 1) Nadal 2) Federer 3) Londero\n')
    j1=switch_player(inp)

    inp = input('Select player 2: 1) Nadal 2) Federer 3) Londero\n')
    j2=switch_player(inp)

    inp = input('Select field material : 1) Hard 2) Clay 3) Grass\n')
    s=tenisSim(switch_field(inp))
    #s.simMatch(j1,j2)

    n= int(input('Select number of matches\n'))

    if(n==1):
        s.simMatch(j1,j2)
        print()
    elif(n>1):
        for i in range (n):
            if(s.simMatch(j1,j2)[0]==0):
                w1=w1+1
            else:
                w2=w2+1

        print()
        print(j1.name + " Wins: " + str(w1))
        print(j2.name + " Wins: " + str(w2))
        print()
        
    simMore = int(input('1 - Exit / 2 - Continue\n'))
    if simMore==1:
        break


# In[ ]:




