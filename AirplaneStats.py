"""
Carwash (3) example with Statistics computation.

Modified by Mario Meireles

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they can use one.

"""
from __future__ import division
import random

import simpy


RANDOM_SEED = 42
NUM_MACHINES = 3  # Numero de pistas no aeroporto
WASHTIME = 5      # tempo que leva para pousar / decolar
T_INTER = 7       # Chegada de um novo aviao a cada T_INTER minutos
SIM_TIME = 50     # Tempo da simulacao
LANDTIME = 5
DEPART_TIME = 20

class Stats:
	""" Mantem as principais estatisticas da simulacao em curso
	
	"""
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
		
	def report(self):
		print ('\n*** SimPy Simulation Report ***\n')
		print ('Total Simulation Time: %.4f' % SIM_TIME)
		print ('Total Arrivals: %d' % self.num_arrivals)
		print ('Total Departures: %d' % self.num_complet)
		print ('Arrival Rate: %2f' % self.arrival_rate)
		print ('Throughput: %2f' % self.throughput)
		
class Carwash(object):
    """A carwash has a limited number of machines (``NUM_MACHINES``) to
    clean cars in parallel.

    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(LANDTIME)
#         yield self.env.timeout(random.expovariate(1.0 / WASHTIME))

    def partida(self,car):
		yield self.env.timeout(DEPART_TIME)
	
	


	
			  
def car(env, name, cw):
    """The car process (each car has a ``name``) arrives at the carwash
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
        yield env.process(cw.wash(name))

	
        yield env.process(cw.partida(name))

        print('%s parte do aeroporto em  %.2f. Tempo do servico: %.2f' % (name, env.now, env.now - start))

	
		

        stat.new_completion()


def setup(env, num_machines, washtime, t_inter): 
    """Create a carwash, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the carwash
    carwash = Carwash(env, num_machines, washtime)

    # Create 4 initial cars
    for i in range(4):
        env.process(car(env, 'Car %d' % i, carwash))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter-2, t_inter+2))
#         yield env.timeout(random.expovariate(1.0 / t_inter))
        i += 1
        env.process(car(env, 'Car %d' % i, carwash))


# Setup and start the simulation
print('===== Carwash =====')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create statistics object
stat = Stats()

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER))

# Execute!
env.run(until=SIM_TIME)

# Report stats
stat.calcstats()
stat.report()
