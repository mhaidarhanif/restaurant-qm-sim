import random
import simpy

temp=0
calculate=[0]*20

timeServ1 = 2	
timeServ2 = 2
timeServ3 = 5

rangeCustomers = 15  	
simulationTime = 60     # Simulation time in minutes


class firstCounter(object):

    def __init__(self, env ):
        self.env = env
	self.machine = simpy.Resource(env, 1)

    def lay(self, car):
        yield self.env.timeout(random.randint(timeServ1-1, timeServ1+1))
	print("%s has ordered the menu %.2f."%(car,env.now))

class secondCounter(object):

    def __init__(self, env):
        self.env = env
        self.machine = simpy.Resource(env, 1)

    def lay(self, car):
        yield self.env.timeout(random.randint(timeServ2-1, timeServ2+1))
	print("%s has paid their order %.2f."%(car,env.now))

class thirdCounter(object):

    def __init__(self, env):
        self.env = env
        self.machine = simpy.Resource(env, 1)

    def lay(self, car):
        yield self.env.timeout(random.randint(timeServ3-2, timeServ3+2))
	print("%s has got their order %.2f."%(car,env.now))

def car(env, name, cw1,cw2,cw3):
    print("%s arrives at McDonald's at %.2f." % (name, env.now))
    with cw1.machine.request() as request:
        yield request
        print('>>> %s choosing their order at %.2f.' % (name, env.now))
	calculate[int(name[4:])]=env.now
        yield env.process(cw1.lay(name))
        print('%s go to the 2nd counter at %.2f.' % (name, env.now))
	env.process(car2(env, name, cw1,cw2,cw3))

def car2(env, name, cw1,cw2,cw3):
    with cw2.machine.request() as request:
	yield request
	print('>>> %s paying their bill at %.2f.' % (name, env.now))
	yield env.process(cw2.lay(name))
	print('%s go to the 3rd counter at %.2f.' % (name, env.now))
	env.process(car3(env, name, cw1,cw2,cw3))

def car3(env, name, cw1,cw2,cw3):
    with cw3.machine.request() as request:
	yield request
	print('>>> %s wait and take their order at %.2f.' % (name, env.now))
	yield env.process(cw3.lay(name))
	print("	%s leaves the McDonald's at %.2f." % (name, env.now))
	global temp
	temp=int(name[4:])
	calculate[int(name[4:])]=env.now-calculate[int(name[4:])]


def setup(env, RC):
    counter1 = firstCounter(env)
    counter2 = secondCounter(env)
    counter3 = thirdCounter(env)

    for i in range(3):
        env.process(car(env, 'Car %d' % i, counter1,counter2,counter3))
    while True:
        yield env.timeout(random.randint(RC-2, RC+2))
        i += 1
        env.process(car(env, 'Car %d' % i, counter1,counter2,counter3))


print('~DriveThru~/n')

env = simpy.Environment()
env.process(setup(env, rangeCustomers))
env.run(until=simulationTime)

sumAll=0.00

for j in range (temp+1):
    sumAll=sumAll+calculate[j]

averageTimeService = sumAll/(temp+1)
servicePerSecond = 1.00/(averageTimeService*60)

print ('Average time	: %.2f' % averageTimeService)
print ('service per second	: %f' %servicePerSecond)
