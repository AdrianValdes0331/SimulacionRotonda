import agentpy as ap
import random
import json
import time
import os

#from numpy import empty

recorrido = []
parameters = {
    'carros': 1,
    'peatones': 1,
    'steps': 50,
    'size': 19
}
# Usar marcadore para cambiar direccion de giro
#Funciones Generales
def matriz():
    tablero = [
                                                                                       
        #X 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19   # Y
        ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'], # 0
        ['x',  0,  0,  0,  0,  0,'x',  2,  2,'x','x',  0,  0,'x',  0,  0,  0,  0,  0,'x'], # 1
        ['x',  0,  0,  0,  0,  0,'x',  0,  0,'x','x',  0,  0,'x',  0,  0,  0,  0,  0,'x'], # 2
        ['x',  0,  0,'*',  1,  0,  9,  0,  0,  9,  9,  0,  0,  9,  0,  0,'*',  0,  0,'x'], # 3
        ['x',  0,  0,  0,  0,  0,'x',  0,  0,'x','x',  0,  0,'x',  0,  0,  1,  0,  0,'x'], # 4
        ['x',  0,  0,  0,  0,  0,'x',  0,  0,'x','x',  0,  0,'x',  0,  0,  0,  0,  0,'x'], # 5
        ['x','x','x',  9,'x','x','l',  0,  0,'x','x',  0,  0,'u','x','x',  9,'x','x','x'], # 6
        ['x',  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,'x'], # 7
        ['x',  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,'x'], # 8
        ['x','x','x',  9,'x','x','x',  0,  0,'u','r',  0,  0,'x','x','x',  9,'x','x','x'], # 9
        ['x','x','x',  9,'x','x','x',  0,  0,'l','d',  0,  0,'x','x','x',  9,'x','x','x'], # 10
        ['x',  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,'x'], # 11
        ['x',  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,'x'], # 12
        ['x','x','x',  9,'x','x','d',  0,  0,'x','x',  0,  0,'r','x','x',  9,'x','x','x'], # 13
        ['x',  0,  0,  0,  0,  0,'x',  0,  0,'x','x',  0,  0,'x',  0,  0,  0,  0,  0,'x'], # 14
        ['x',  0,  0,  1,  0,  0,'x',  0,  0,'x','x',  0,  0,'x',  0,  0,  0,  0,  0,'x'], # 15
        ['x',  0,  0,'*',  0,  0,  9,  0,  0,  9,  9,  0,  0,  9,  0,  1,'*',  0,  0,'x'], # 16
        ['x',  0,  0,  0,  0,  0,'x',  0,  0,'x','x',  0,  0,'x',  0,  0,  0,  0,  0,'x'], # 17
        ['x',  0,  0,  0,  0,  0,'x',  0,  0,'x','x',  2,  2,'x',  0,  0,  0,  0,  0,'x'], # 18
        ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x']  # 19
    ]
    return tablero
#Barrera para autos
def pared(ypos, xpos, tablero):
    if tablero[ypos][xpos] != 'x' and  tablero[ypos][xpos] != 1 and tablero[ypos][xpos] != 9 and tablero[ypos][xpos] != 2:
        return(True)
    return(False)

#Barrera para peatones
def malla(ypos, xpos, tablero):
    if tablero[ypos][xpos] != '*' and tablero[ypos][xpos] != 1:    
        return(True)
    return(False)

#Lord Supremo, king Controller
def controladorM(x, xpos, ypos, tablero, condicion, val):
    if x == 0:
        if condicion(ypos-1, xpos, tablero):
            ypos = ypos - 1
            tablero[ypos][xpos] = tablero[ypos][xpos] + val
            tablero[ypos+1][xpos] = tablero[ypos+1][xpos] - val
            despliega_Tablero(tablero)
        else:
            print("error")
    elif x == 1:
        if condicion(ypos, xpos-1, tablero):
            xpos = xpos - 1
            tablero[ypos][xpos] = tablero[ypos][xpos] + val
            tablero[ypos][xpos+1] = tablero[ypos][xpos+1] - val
            despliega_Tablero(tablero)
        else:
            print("error")
    elif x == 2:
        if condicion(ypos+1, xpos, tablero):
            ypos = ypos + 1
            tablero[ypos][xpos] = tablero[ypos][xpos] + val
            tablero[ypos-1][xpos] = tablero[ypos-1][xpos] - val
            despliega_Tablero(tablero)
        else:
            print("error")
    elif x == 3:
        if condicion(ypos, xpos+1, tablero):
            xpos = xpos + 1
            tablero[ypos][xpos] = tablero[ypos][xpos] + val
            tablero[ypos][xpos-1] = tablero[ypos][xpos-1] - val
            despliega_Tablero(tablero)
        else:
            print("error")
    else:
        print("error")

def despliega_Tablero(matriz):
    print()
    for ren in range(len(matriz)):
        for col in range(len(matriz)):
            print(matriz[ren][col], end=" ")
        print()

#Agentes y Modelos
class Carro(ap.Agent):

    def setup(self):
        self.grid = self.model.grid
        self.dic1 = []
        self.dic2 = []
        self.dic3 = []
        self.dic4 = []
        self.dic5 = []
        self.dic6 = []
        self.dic7 = []
        self.dic8 = []
        #Posicion inicial Vehiculos
        #leftRight
        self.LRxpos = 1
        self.LRypos = 12
        self.LRval = 0
        self.LRxpos2 = 1
        self.LRypos2 = 11
        self.LRval2 = 0
        #downUp
        self.DUxpos = 12
        self.DUypos = 18
        self.DUval = 0
        self.DUxpos2 = 11
        self.DUypos2 = 18
        self.DUval2 = 0
        #upDown
        self.UDxpos = 7
        self.UDypos = 1
        self.UDval = 0
        self.UDxpos2 = 8
        self.UDypos2 = 1
        self.UDval2 = 0
        #rightLeft
        self.RLxpos = 18
        self.RLypos = 7
        self.RLval = 0
        self.RLxpos2 = 18
        self.RLypos2 = 8
        self.RLval2 = 0

    #Decide a donde se mueve el carro
    def accelera(self, pos):

        val = 2
        direccion = random.randint(0,0)
        #downUp
        if direccion == 0 and pared(self.DUypos-1, self.DUxpos, pos):
            #Vueta Corta
             if self.DUval == 0:
                if pos[self.DUypos+1][self.DUxpos+1] == 'r':
                    controladorM(3, self.DUxpos, self.DUypos, pos, pared, val)
                    self.DUxpos = self.DUxpos + 1   
                    self.DUval = 1
                else:
                    controladorM(0, self.DUxpos, self.DUypos, pos, pared, val)
                    self.DUypos = self.DUypos - 1
             else:
                controladorM(3, self.DUxpos, self.DUypos, pos, pared, val)
                self.DUxpos = self.DUxpos + 1   

        if direccion == 0 and pared(self.DUypos2-1, self.DUxpos2, pos):
            #Vueta Larga
             if self.DUval2 == 0:
                if pos[self.DUypos2+1][self.DUxpos2-1] == 'r':
                    controladorM(1, self.DUxpos2, self.DUypos2, pos, pared, val)
                    self.DUxpos2 = self.DUxpos2 - 1   
                    self.DUval2 = 1
                else:
                    controladorM(0, self.DUxpos2, self.DUypos2, pos, pared, val)
                    self.DUypos2 = self.DUypos2 - 1
             else:
                controladorM(1, self.DUxpos2, self.DUypos2, pos, pared, val)
                self.DUxpos2 = self.DUxpos2 - 1  

        #rightLeft
        if direccion == 0 and pared(self.RLypos, self.RLxpos-1, pos):
            #Vueta Corta
            if self.RLval == 0:
                if pos[self.RLypos-1][self.RLxpos+1] == 'u':
                    controladorM(0, self.RLxpos, self.RLypos, pos, pared, val)
                    self.RLypos = self.RLypos - 1   
                    self.RLval = 1
                else:
                    controladorM(1, self.RLxpos, self.RLypos, pos, pared, val)
                    self.RLxpos = self.RLxpos - 1
            else:
                controladorM(0, self.RLxpos, self.RLypos, pos, pared, val)
                self.RLypos = self.RLypos - 1   

        if direccion == 0 and pared(self.RLypos2, self.RLxpos2-1, pos):
            #Vueta Larga
            if self.RLval2 == 0:
                if pos[self.RLypos2+1][self.RLxpos2+1] == 'u':
                    controladorM(2, self.RLxpos2, self.RLypos2, pos, pared, val)
                    self.RLypos2 = self.RLypos2 + 1   
                    self.RLval2 = 1
                else:
                    controladorM(1, self.RLxpos2, self.RLypos2, pos, pared, val)
                    self.RLxpos2 = self.RLxpos2 - 1
            else:
                controladorM(2, self.RLxpos2, self.RLypos2, pos, pared, val)
                self.RLypos2 = self.RLypos2 + 1 

        #upDown
        if direccion == 0 and pared(self.UDypos+1, self.UDxpos, pos):
            #Vueta Corta
            if self.UDval == 0:
                if pos[self.UDypos-1][self.UDxpos-1] == 'l':
                    controladorM(1, self.UDxpos, self.UDypos, pos, pared, val)
                    self.UDxpos = self.UDxpos - 1   
                    self.UDval = 1
                else:
                    controladorM(2, self.UDxpos, self.UDypos, pos, pared, val)
                    self.UDypos = self.UDypos + 1
            else:
                controladorM(1, self.UDxpos, self.UDypos, pos, pared, val)
                self.UDxpos = self.UDxpos - 1

        if direccion == 0 and pared(self.UDypos2+1, self.UDxpos2, pos):
            #Vueta Larga
            if self.UDval2 == 0:
                if pos[self.UDypos2-1][self.UDxpos2+1] == 'l':
                    controladorM(3, self.UDxpos2, self.UDypos2, pos, pared, val)
                    self.UDxpos2 = self.UDxpos2 + 1   
                    self.UDval2 = 1
                else:
                    controladorM(2, self.UDxpos2, self.UDypos2, pos, pared, val)
                    self.UDypos2 = self.UDypos2 + 1
            else:
                controladorM(3, self.UDxpos2, self.UDypos2, pos, pared, val)
                self.UDxpos2 = self.UDxpos2 + 1  
      
        #leftRight
        if direccion == 0 and pared(self.LRypos, self.LRxpos+1, pos):
            #Vueta Corta
            if self.LRval == 0:
                if pos[self.LRypos+1][self.LRxpos-1] == 'd':
                    controladorM(2, self.LRxpos, self.LRypos, pos, pared, val)
                    self.LRypos = self.LRypos + 1
                    self.LRval = 1
                else:
                    controladorM(3, self.LRxpos, self.LRypos, pos, pared, val)
                    self.LRxpos = self.LRxpos + 1     
            else:
                controladorM(2, self.LRxpos, self.LRypos, pos, pared, val)
                self.LRypos = self.LRypos + 1
                
        if direccion == 0 and pared(self.LRypos2, self.LRxpos2+1, pos):
            #Vueta Larga
            if self.LRval2 == 0:
                if pos[self.LRypos2-1][self.LRxpos2-1] == 'd':
                    controladorM(0, self.LRxpos2, self.LRypos2, pos, pared, val)
                    self.LRypos2 = self.LRypos2 - 1
                    self.LRval2 = 1
                else:
                    controladorM(3, self.LRxpos2, self.LRypos2, pos, pared, val)
                    self.LRxpos2 = self.LRxpos2 + 1     
            else:
                controladorM(0, self.LRxpos2, self.LRypos2, pos, pared, val)
                self.LRypos2 = self.LRypos2 - 1

        yxPosVals =  [self.LRypos,  self.LRxpos], [self.DUypos, self.DUxpos], [self.UDypos, self.UDxpos], [self.RLypos, self.RLxpos]                
        self.record("Car #1   Car #2   Car #3   Car #4", yxPosVals)
        #Start Left turn down
        x1 = str(self.LRypos)
        y1 = str(self.LRxpos)
        ans1 = x1 + ', ' + y1
        self.dic1.append(ans1)
        #Start left turn up
        x2 = str(self.LRypos2)
        y2 = str(self.LRxpos2)
        ans2 = x2 + ', ' + y2
        self.dic2.append(ans2)
        #Start Down turn right
        x3 = str(self.DUypos)
        y3 = str(self.DUxpos)
        ans3 = x3 + ', ' + y3
        self.dic3.append(ans3)
        #Start Down turn left
        x4 = str(self.DUypos2)
        y4 = str(self.DUxpos2)
        ans4 = x4 + ', ' + y4
        self.dic4.append(ans4)
        #Start up turn left
        x5 = str(self.UDypos)
        y5 = str(self.UDxpos)
        ans5 = x5 + ', ' + y5
        self.dic5.append(ans5)
        #Start Up turn right
        x6 = str(self.UDypos2)
        y6 = str(self.UDxpos2)
        ans6 = x6 + ', ' + y6
        self.dic6.append(ans6)
        #Start Right turn up
        x7 = str(self.RLypos)
        y7 = str(self.RLxpos)
        ans7 = x7 + ', ' + y7
        self.dic7.append(ans7)
        #Start Right turn up
        x8 = str(self.RLypos2)
        y8 = str(self.RLxpos2)
        ans8 = x8 + ', ' + y8
        self.dic8.append(ans8)

    def printt(self, pos):
        #carro1 = "{carros: " + "[" + "{" + 'coord' + ': ' + str(self.dic1) + "}"
        #carro2 = "{" + 'coord' + ': ' + str(self.dic2) + "}"
        #carro3 = "{" + 'coord' + ': ' + str(self.dic3) + "}"
        #carro4 = "{" + 'coord' + ': ' + str(self.dic4) + "}"
        #carro5 = "{" + 'coord' + ': ' + str(self.dic5) + "}"
        #carro6 = "{" + 'coord' + ': ' + str(self.dic6) + "}"
        #carro7 = "{" + 'coord' + ': ' + str(self.dic7) + "}"
        #carro8 = "{" + 'coord' + ': ' + str(self.dic8) + "}" + "]" + "}"
        with open('carross.json', 'a') as f:
            json.dump([self.dic1, self.dic2, self.dic3, self.dic4, self.dic5, self.dic6, self.dic7, self.dic8], f)
            #(carro1, carro2, carro3, carro4, carro5, carro6, carro7, carro8), f) #self.dic3, self.dic4, self.dic5, self.dic6, self.dic7, self.dic8], f)

class Peaton(ap.Agent):

    def setup(self):
        self.dic1 = []
        self.dic2 = []
        self.dic3 = []
        self.dic4 = []
        self.grid = self.model.grid
        #Posicion inicial Peatones
        #downLeftUp
        self.DLUxpos = 3
        self.DLUypos = 15
        #upRightRight
        self.URRxpos = 4
        self.URRypos = 3
        #UpRightDown
        self.URDxpos = 16
        self.URDypos = 4
        #downRightLeft
        self.DRLxpos = 15
        self.DRLypos = 16

    #Decide a donde se mueve el Peaton
    def camina(self, pos):

        val = 1
        direccion = random.randint(0,0)
        #downLeftUp
        if direccion == 0 and malla(self.DLUypos-1, self.DLUxpos, pos):
            controladorM(0, self.DLUxpos, self.DLUypos, pos, malla, val)
            self.DLUypos = self.DLUypos - 1
        #downRightLeft
        if direccion == 0 and malla(self.DRLypos, self.DRLxpos-1, pos):
            controladorM(1, self.DRLxpos, self.DRLypos, pos, malla, val)
            self.DRLxpos = self.DRLxpos - 1
        #UpRightDown
        if direccion == 0 and malla(self.URDypos+1, self.URDxpos, pos):
            controladorM(2, self.URDxpos, self.URDypos, pos, malla, val)
            self.URDypos = self.URDypos + 1
        #upRightRight
        if direccion == 0 and malla(self.URRypos, self.URRxpos+1, pos):
            controladorM(3, self.URRxpos, self.URRypos, pos, malla, val)
            self.URRxpos = self.URRxpos + 1
        

        yxPPosVals =  [self.DLUypos,  self.DLUxpos], [self.URRypos, self.URRxpos], [self.URDypos, self.URDxpos], [self.DRLypos, self.DRLxpos]                
        self.record("Per #1   Per #2   Per #3   Per #4", yxPPosVals)
        #Start Left turn down
        x1 = str(self.DLUypos)
        y1 = str(self.DLUxpos)
        ans1 = x1 + ', ' + y1
        self.dic1.append(ans1)
        #Start left turn up
        x2 = str(self.URRypos)
        y2 = str(self.URRxpos)
        ans2 = x2 + ', ' + y2
        self.dic2.append(ans2)
        #Start Down turn right
        x3 = str(self.URDypos)
        y3 = str(self.URDxpos)
        ans3 = x3 + ', ' + y3
        self.dic3.append(ans3)
        #Start Down turn left
        x4 = str(self.DRLypos)
        y4 = str(self.DRLxpos)
        ans4 = x4 + ', ' + y4
        self.dic4.append(ans4)
        
    def printt(self, pos):
        with open('peatoness.json', 'a') as f:
            json.dump([self.dic1, self.dic2, self.dic3, self.dic4], f)


#Modelo
class mainModel(ap.Model):
    def setup(self):
        self.ans1 = []

        c = self.p.carros
        p = self.p.peatones
        s = self.p.size
        self.grid = ap.Grid(self, (s, s), track_empty=True)

        self.pos = matriz()   
        self.agenteCarro = ap.AgentList(self, c, Carro)
        self.agentePeaton = ap.AgentList(self, p, Peaton)
        self.grid.add_agents(self.agenteCarro, random=True, empty=True)
        self.grid.add_agents(self.agentePeaton, random=True, empty=True)

    def step(self):
        self.agenteCarro.accelera(self.pos)
        self.agentePeaton.camina(self.pos)
    
    def end(self):
        self.agenteCarro.printt(self.pos)
        self.agentePeaton.printt(self.pos)
     

def main():
    model = mainModel(parameters)
    result = model.run()
    print()
    print("Posiciones de Carros")
    print(result.variables.Carro)
    print()
    print("Posiciones de Peatones")
    print(result.variables.Peaton)
main()