# Librerias
import agentpy as ap
import random

#  Agente Carro
class Carro(ap.Agent):

    def setup(self):
        self.grid = self.model.grid
        self.random = self.model.random
        self.speed = 0
        self.estado = 0
        self.currentPosition = ()

    #  Falta Evitar que colisionen
    def carrosVecinos(self):
        vecinos = self.grid.neighbors(self, distance=5)
        vecinos = vecinos.to_list()
        return vecinos

    #  Falta: Recto = direccion a donde apunta 
    #  al frente del Vehiculo
    def recto(self):     
        self.grid.move_to(self,(self.currentPosition[0], self.currentPosition[1]))
        self.currentPosition = self.grid.positions[self]
    
    #  Falta: Gira = A la derecha Siempre
    def gira(self):     
        self.grid.move_to(self,(self.currentPosition[0]+1, self.currentPosition[1]))
        self.currentPosition = self.grid.positions[self]

    #  Falta: 
    #  Posible funcion velocidad
    #  Para frenar/disminuir la velocidad
    
    #  Por el momento le dice al auto que se mueva
    #  de manera aleatoria
    def accelera(self):
        if not self.currentPosition:
            self.currentPosition = self.grid.positions[self]
        
        direccion = self.random.randint(0,1)
        if direccion == 0:
            self.recto()
        
        if direccion == 1:
            self.gira()
        
        self.currentPosition = self.grid.positions[self]
        print(self.currentPosition)

#Agente Semaforo
class Semaforo(ap.Agent):
    def setup(self):
        self.currentPosition = (4,2)
        self.grid = self.model.grid
        self.random = self.model.random

    #  Falta: Cambiar estado con base a peaton
    #  Falta: Timer de 10 seg
    #  Falta: Timer de 1 min
    def estado(self):
        estado = random.randint(0,5)
        if estado == 0:
            print("Verde") 
        if estado == 1:
            print("Verde") 
        if estado == 2:
            print("Verde") 
        if estado == 3:
            print("Amarillo") 
        if estado == 4:
            print("Rojo") 
        if estado == 5:
            print("Rojo")  

        
#Agente Peaton
class Peaton(ap.Agent):

    def setup(self):
        self.grid = self.model.grid
        self.random = self.model.random
        self.speed = 0
        self.estado = 0
        self.currentPosition = ()

    #  Falta Evitar que colisionen
    def peatonesVecinos(self):
        pVecinos = self.grid.neighbors(self, distance=1)
        pVecinos = pVecinos.to_list()
        return pVecinos

    #  Para mover sumar posicion
    #  Falta: 
    #  Posible funcion velocidad
    #  Para frenar/disminuir la velocidad
    #  Funcion Boton para activar Semaforo
    def pRecto(self):     
        self.grid.move_to(self,(self.currentPosition[0]+1, self.currentPosition[1]+1))
        self.currentPosition = self.grid.positions[self]

    #  Falta: 
    #  Darle una meta destino aleatoria (investigar pathfinder)
    #  Buscar por donde ir en X & Y
    #  Reaccionar con el semaforo
    #  Activar boton
    def camina(self):
        if not self.currentPosition:
            self.currentPosition = self.grid.positions[self]
        
        direccion = self.random.randint(0,0)
        if direccion == 0:
            self.pRecto()
        
        self.currentPosition = self.grid.positions[self]
        print(self.currentPosition)



class mainModel(ap.Model):
    def setup(self):
        s = self.p.size
        c = self.p.carros
        pp = self.p.peatones
        sp = self.p.semaforos

        self.grid = ap.Grid(self, (s, s), track_empty=True)
        self.agenteCarro = ap.AgentList(self, c, Carro)
        self.agenteSemaforo = ap.AgentList(self, sp, Semaforo) 
        self.agentePeaton = ap.AgentList(self, pp, Peaton) 
        self.grid.add_agents(self.agenteCarro, random=True, empty=True)
        self.grid.add_agents(self.agentePeaton, random=True, empty=True)
        self.grid.add_agents(self.agenteSemaforo, random=True, empty=True)

    def update(self):
        print("\nPosiciones de Autos:")
        self.agenteCarro.accelera()
        print("\nEstados del semaforo:")
        self.agenteSemaforo.estado()
        print("\nPosiciones de Peatones:")
        self.agentePeaton.camina()

    def step(self):
        print("\n")
        print("\nPosiciones de Autos:")
        self.agenteCarro.accelera()
        print("\nEstados del semaforo:")
        self.agenteSemaforo.estado()
        print("\nPosiciones de Peatones:")
        self.agentePeaton.camina()
        

parameters = {
    'carros': 10,
    'peatones': 10,
    'size': 100,
    'steps': 50,
    'semaforos': 4
}

#  Imprimir Resultados
#  Falta imprimir en archivo
model = mainModel(parameters)
resultados = model.run()
print(resultados)


#def animation_plot(model, ax):
#    group_grid = model.grid.attr_grid('moving')
#    color_dict = {0:'#7FC97F', 1:'#d62c2c', 2:'#e5e5e5', None:'#d5e5d5'}
#    ap.gridplot(group_grid, ax=ax, color_dict=color_dict, convert=True)
#    ax.set_title(f"Simulation of a forest fire\n")

#fig, ax = plt.subplots()
#model = SuperBlockModel(parameters)
#animation = ap.animate(model, fig, ax, animation_plot)
#IPython.display.HTML(animation.to_jshtml(fps=60))




