
# coding: utf-8

# In[8]:

from __future__ import division
import random
import copy
import simpy
import plotly
import math

RANDOM_SEED = 42
NUM_TRACKS = 1  # Numero de pistas no aeroporto
LANDTIME = 10      
T_INTER = 5       # Chegada de um novo aviao a cada T_INTER minutos
SIM_TIME = 180     # Tempo da simulacao
LANDTIME = 5     #tempo de pouso
DEPART_TIME = 10 # tempo de partida
WAIT_TIME = []    #tempo de espera 
SERVICE_TIME = []   # tempo de servico
SYSTEM_TIME = []    #tempo no sistema

MSS = 1460#bytes
FRAMEOVHD = 18#bytes
httpRequest = 290#bytes
lanBandWidth = 10#mbps
docSize = 22.23#KB
# Gera o gráfico 		
def plot ():
		plotly.offline.plot({
		"data" : [
			plotly.graph_objs.Bar(
				x=['Tempo de Espera 2 pistas','Tempo de Espera 3 pistas', 'Tempo no Sistema 2 pistas', 'Tempo no Sistema 3 pistas'],
				y=[stat1.mean_wait,stat2.mean_wait, stat1.mean_residence, stat2.mean_residence]
			)
			],
		"layout" : plotly.graph_objs.Layout(
			title = "Simulacao de numero de pistas",
			barmode = "group"
		)
			
		})
def nDatagrams(msgSize):
    return math.ceil(msgSize / MSS)
def overhead(msgSize):
    return nDatagrams(MsgSize) * (20 + 20 + FrameOvhd)
def netTime(msgSize,bandWidth):
    return((msgSize + Overhead(msgSize)) * 8) / (bandWidth * 1000000)
   


# In[2]:

class Stats:
    def __init__(self):
        self.num_arrivals = 0
        self.num_complet = 0

    def new_arrival(self):
        self.num_arrivals+=1

    def new_completion(self):
        self.num_complet+=1

    def calcstats(self):
        self.arrival_rate = self.num_arrivals/SIM_TIME
        self.throughput = self.num_complet/SIM_TIME
        if (sum(SERVICE_TIME)) > SIM_TIME:
            self.busy_time =  SIM_TIME 
        else:
            self.busy_time = (sum(SERVICE_TIME))

        self.average_time = (self.busy_time/self.num_arrivals)
        self.mean_wait = float(sum(WAIT_TIME))/len(WAIT_TIME)
        self.mean_residence = (sum(SYSTEM_TIME)/len(SYSTEM_TIME))

    def report(self):
        total_wait = (sum(WAIT_TIME))/len(WAIT_TIME)
        total_service = (sum(SYSTEM_TIME)/len(SYSTEM_TIME))
        print ('\n*** SimPy Simulation Report ***\n')
        print ('Total Simulation Time: %.4f' % SIM_TIME)
        print ('Total Arrivals: %d' % self.num_arrivals)
        print ('Total Departures: %d' % self.num_complet)
        print ('Arrival Rate: %2f' % self.arrival_rate)
        print ('Throughput: %2f' % self.throughput)
        print ('Busy Time: %2f' % self.busy_time)
        print ('Average Service Time %2f' % self.average_time)
        print ('Average wait time %2f' % self.mean_wait)
        print ('Average Residence time %2f' % self.mean_residence)


# In[3]:

class Lan(object):
    """ fila independente de carga"""
    def __init__(self, env):
        self.env = env
        self.demanda = 0
    def findDemand():
        self.demanda = netTime(httpRequest,lanBandWidth)+ netTime(docSize*1024,lanBandWidth)
    def delay(self):
        yield self.env.timeout(5)
class linkSaida(object):
    """ fila independente de carga"""
    def __init__(self, env):
        self.env = env
    def findDemand():
        self.demanda = netTime(httpRequest,lanBandWidth)+ netTime(0.0001,lanBandWidth)
    def delay(self):
        yield self.env.timeout(5)
class linkEntrada(object):
    """ fila independente de carga"""
    def __init__(self, env):
        self.env = env
    def findDemand():
        self.demanda = netTime(docSize*1024,lanBandWidth)+ 2*netTime(0.0001,lanBandWidth)
    def delay(self):
        yield self.env.timeout(5)


# In[ ]:

class Client(object):
    """Fila de espera, com recurso limitados"""
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(WASHTIME)
        print("Carwash removed %d%% of %s's dirt." %
              (random.randint(50, 99), car))
class Roteador(object):
    """Fila de espera, com recurso limitados"""
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(WASHTIME)
        print("Carwash removed %d%% of %s's dirt." %
              (random.randint(50, 99), car))
class Internet(object):
    """Fila de espera, com recurso limitados"""
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(WASHTIME)
        print("Carwash removed %d%% of %s's dirt." %
              (random.randint(50, 99), car))


# In[6]:

def plane(env, name, cw):
    """The plane process (each plane has a ``name``) arrives at the airport
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s Chega ao aeroporto em %.2f.' % (name, env.now))
    stat.new_arrival()
    arrive = env.now
    with cw.machine.request() as request:
        yield request

        print('%s entra na pista de pouso em %.2f. Tempo de espera: %.2f' % (name, env.now, env.now - arrive))
        start = env.now
        WAIT_TIME.append(env.now - arrive)
        yield env.process(cw.delay())

        yield env.process(cw.partida(name))

        print('%s parte do aeroporto em  %.2f. Tempo do servico: %.2f' % (name, env.now, env.now - start))
        SERVICE_TIME.append(env.now - start)
        SYSTEM_TIME.append(env.now - arrive)

        stat.new_completion()


def setup(env, NUM_TRACKS, landtime, t_inter): 
    """Create a airport, a number of initial planes and keep creating planes
    approx. every ``t_inter`` minutes."""
    # Create the airport
    airport = Airport(env, NUM_TRACKS, landtime)

    # Create 4 initial planes
    for i in range(1):
        env.process(plane(env, 'Aviao %d' % i, airport))

    # Create more planes while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter-2, t_inter+2))
#       yield env.timeout(random.expovariate(1.0 / t_inter))
        i += 1
        env.process(plane(env, 'Aviao %d' % i, airport))


# Setup and start the simulation
print('===== Airport =====')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create statistics object
stat = Stats()

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_TRACKS, LANDTIME, T_INTER))

# Execute!
env.run(until=SIM_TIME)

# Report stats
stat.calcstats()

# Salva os dados da primeira simulação
stat1 = copy.deepcopy(stat)
stat1.report()
plot()


