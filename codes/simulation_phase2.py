
import simpy
import random
import copy
import statistics as stat
import math

WARM_UP = 150
NUMBER_OF_CUSTOMERS = 20
CAPACITY = 4
UNIFORM_LOW =  5.43
UNIFORM_HIGH = 6.43
SERVER_UTILIZATION = 0.8 
INTERARRIVAL_TIME = (UNIFORM_HIGH + UNIFORM_LOW) / 2
INTERARRIVAL_RATE = 1 / INTERARRIVAL_TIME
SERVICE_RATE = INTERARRIVAL_RATE / (SERVER_UTILIZATION * CAPACITY)

sojourn_list = []

random.seed(RANDOM_SEED)
customers = []#List of customers
service_times = [] #Duration of the conversation between the customer and the operator (Service time)
queue_w_times = [] #Time spent by a customer while it waits for the operator (Queue waiting time Wq)
sojourn_times = [] #Time spent by a customer in the system.
customer_count_over_time = dict()

if START_CONDITION == 3:
    NUMBER_OF_CUSTOMERS += WARM_UP


class Customer(object):
    def __init__(self, name, env, operator):
        self.env = env
        self.name = name
        self.operator = operator
        self.arrival_t = self.env.now
        self.action = env.process(self.call())
    
    def call(self):
        #print('%s initiated a call at %g' % (self.name, self.env.now))

        with self.operator.request() as req:
            yield req
            #print('%s is assigned to an operator at %g' % (self.name, self.env.now))
            queue_w_times.append(self.env.now - self.arrival_t)
            yield self.env.process(self.ask_question())
            #print('%s is done at %g' % (self.name, self.env.now))
            sojourn_times.append(self.env.now - self.arrival_t)
            
    def ask_question(self):
        duration = random.expovariate(SERVICE_RATE)
        yield self.env.timeout(duration)
        service_times.append(duration)
           
def customer_generator(env, operator):
    """Generate new customers that call the line."""
    for i in range(NUMBER_OF_CUSTOMERS):
        if START_CONDITION == 2:
            if i < 4 :
                yield env.timeout(0)
            else:
                yield env.timeout(random.uniform(UNIFORM_LOW, UNIFORM_HIGH))
        else:
            yield env.timeout(random.uniform(UNIFORM_LOW, UNIFORM_HIGH))
        customer = Customer('Cust %s' %(i+1), env, operator)
        customers.append(customer)  

def runner():
    env = simpy.Environment()
    operator = simpy.Resource(env, capacity = CAPACITY)
    env.process(customer_generator(env, operator))
    env.run() 
    #print("Simulation started.")
    global queue_w_times
    global service_times
    global sojourn_times
    global sojourn_list
    #print("Simulation finished.")

    sojourn_list.append(copy.deepcopy(sojourn_times))  
    queue_w_times.clear()
    service_times.clear()
    sojourn_times.clear()

for i in range(REP_COUNT):
    runner()

ensemble_averages = [0 for i in range(len(sojourn_list[0]))]
for elm in sojourn_list:
    for i in range(len(elm)):
        ensemble_averages[i] += elm[i]

for i in range(len(ensemble_averages)):
    ensemble_averages[i] = ensemble_averages[i] / REP_COUNT


estimator = 0
if START_CONDITION == 3:
    ensemble_averages1 = ensemble_averages[WARM_UP:]
else:
    ensemble_averages1 = ensemble_averages

estimator = stat.mean(ensemble_averages1)
deviation = stat.stdev(ensemble_averages1)

# t-value for alpha=0.025 (at NUMBER_OF_CUSTOMERS-1 d.o.f.): 2.093
t_value = 2.093
half_width = t_value * (deviation / math.sqrt(NUMBER_OF_CUSTOMERS))
upper_limit = estimator + half_width
lower_limit = estimator - half_width 
