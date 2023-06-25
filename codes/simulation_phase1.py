
import simpy
import random
import copy
import statistics as stat
import math

NUMBER_OF_CUSTOMERS = 1000
CAPACITY = 4
UNIFORM_LOW =  5.43
UNIFORM_HIGH = 6.43
SERVER_UTILIZATION = 0.9 # (0.6,0.7,0.8,0.9)
INTERARRIVAL_TIME = (UNIFORM_HIGH + UNIFORM_LOW) / 2
INTERARRIVAL_RATE = 1 / INTERARRIVAL_TIME
SERVICE_RATE = INTERARRIVAL_RATE / (SERVER_UTILIZATION * CAPACITY)
ACTIVE_CUSTOMER_COUNT = 0
WARM_UP = 600
WARM_UP_TIME = [] 
TIME_STEP = 3

sojourn_list = []
system_customer_list = []

random.seed(RANDOM_SEED)
customers = []#List of customers
service_times = [] #Duration of the conversation between the customer and the operator (Service time)
queue_w_times = [] #Time spent by a customer while it waits for the operator (Queue waiting time Wq)
sojourn_times = [] #Time spent by a customer in the system.
customer_count_over_time = dict()

class Customer(object):
    def __init__(self, name, env, operator):
        self.env = env
        self.name = name
        self.operator = operator
        self.arrival_t = self.env.now
        self.action = env.process(self.call())
    
    def call(self):
        #print('%s initiated a call at %g' % (self.name, self.env.now))
        global ACTIVE_CUSTOMER_COUNT
        ACTIVE_CUSTOMER_COUNT += 1
        customer_count_over_time[self.env.now] = ACTIVE_CUSTOMER_COUNT
        with self.operator.request() as req:
            yield req
            #print('%s is assigned to an operator at %g' % (self.name, self.env.now))
            queue_w_times.append(self.env.now - self.arrival_t)
            yield self.env.process(self.ask_question())
            #print('%s is done at %g' % (self.name, self.env.now))
            sojourn_times.append(self.env.now - self.arrival_t)
            ACTIVE_CUSTOMER_COUNT -= 1
            customer_count_over_time[self.env.now] = ACTIVE_CUSTOMER_COUNT
            customer_id = int((self.name).split(" ")[1])
            global WARM_UP
            global WARM_UP_TIME
            if customer_id == WARM_UP:
                WARM_UP_TIME.append(self.env.now)
            
    def ask_question(self):
        duration = random.expovariate(SERVICE_RATE)
        yield self.env.timeout(duration)
        service_times.append(duration)
           
def customer_generator(env, operator):
    """Generate new customers that call the line."""
    for i in range(NUMBER_OF_CUSTOMERS):
        yield env.timeout(random.uniform(UNIFORM_LOW, UNIFORM_HIGH))
        customer = Customer('Cust %s' %(i+1), env, operator)
        customers.append(customer)

def normalize_dict(init_dict, step):
    normal_dict = dict()
    init_keys = list(init_dict.keys())
    init_keys.sort()
    max_time = init_keys[-1]
    min_time = init_keys[0]
    counter = 0
    index = 1
    while counter < min_time:
        normal_dict[counter] = 0
        counter += step

    while counter < max_time:
        if counter < init_keys[index]:
            normal_dict[counter] = init_dict[init_keys[index-1]]
            counter += step 
        else:
            index += 1
    return normal_dict 

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
    global system_customer_list
    global customer_count_over_time
    global ACTIVE_CUSTOMER_COUNT
    #print(queue_w_times, "\n")
    #print(service_times, "\n")
    #print(sojourn_times, "\n")
    #print("Simulation finished.")

    sojourn_list.append(copy.deepcopy(sojourn_times))
    system_customer_list.append(copy.deepcopy(customer_count_over_time))    
    queue_w_times.clear()
    service_times.clear()
    sojourn_times.clear()
    customer_count_over_time.clear()
    ACTIVE_CUSTOMER_COUNT = 0

def riemann_sum(time, time_dict):
    area_under = 0
    for i in range(len(time_list)-1):
        if time == time_list[i]:
            break
        current_time = time_list[i]
        next_time = time_list[i+1]
        duration = next_time - current_time
        customer_count = time_dict[current_time]
        value =  customer_count*duration
        area_under += value
    return area_under

for i in range(REP_COUNT):
    runner()

# Part 1.1.1
sojourn_avg_list = [0 for i in range(len(sojourn_list[0]))]

for elm in sojourn_list:
    for i in range(len(elm)):
        sojourn_avg_list[i] += elm[i]

for i in range(len(sojourn_avg_list)):
    sojourn_avg_list[i] = sojourn_avg_list[i] / len(sojourn_list)

# Part 1.1.2.1 - Calculating Significance Levels
unbiased_sojourn_avg_list = sojourn_avg_list[WARM_UP:]
estimator = stat.mean(unbiased_sojourn_avg_list)
deviation = stat.stdev(unbiased_sojourn_avg_list)

#t-value for alpha=0.025 (at infinity): 1.96 
t_value = 1.96
half_width = t_value * (deviation / math.sqrt(len(unbiased_sojourn_avg_list)))
upper_limit = estimator + half_width
lower_limit = estimator - half_width 


# Part 1.1.2.2
sojourn_cumulative_avg_list = [0 for i in range(len(sojourn_avg_list))]
for i in range(len(sojourn_avg_list)):
    if i == 0:
        sojourn_cumulative_avg_list[i] = sojourn_avg_list[i]
        continue
    sojourn_cumulative_avg_list[i] = sojourn_cumulative_avg_list[i-1] + sojourn_avg_list[i]  

sojourn_avg_smooth_list = [0 for i in range(len(sojourn_avg_list))]
for i in range(len(sojourn_avg_list)):
    sojourn_avg_smooth_list[i] = sojourn_cumulative_avg_list[i] / (i+1)

# Part 1.2
cumulative_customer_dict_list = []
for elm in system_customer_list:
    cummulative_customer_dict = dict() 
    time_list = list(elm.keys())
    time_list.sort()
    for i in range(len(time_list)):
        time = time_list[i]
        cummulative_customer_dict[time] = riemann_sum(time, elm) / time
    cumulative_customer_dict_list.append(copy.deepcopy(cummulative_customer_dict))

cumulative_customer_dict_list_normalized = []
for elm in cumulative_customer_dict_list:
    cumulative_customer_dict_list_normalized.append(copy.deepcopy(normalize_dict(elm, TIME_STEP)))

min_lenght = math.inf
for elm in cumulative_customer_dict_list_normalized:
    lenght = len(list(elm.keys()))
    if lenght < min_lenght:
        min_lenght = lenght

ensemble_average_cumulative_customer = []
for i in range(min_lenght):
    var = 0 
    for j in range(REP_COUNT):
        elm = cumulative_customer_dict_list_normalized[j]
        key_list = list(elm.keys())
        var += elm[key_list[i]] 
    var = var / REP_COUNT 
    ensemble_average_cumulative_customer.append(var)

warm_up_index = stat.mean(WARM_UP_TIME) // TIME_STEP
warm_up_index = int(warm_up_index)
unbiased_ensemble_average_cumulative_customer = ensemble_average_cumulative_customer[warm_up_index:]
estimator = stat.mean(unbiased_ensemble_average_cumulative_customer)
deviation = stat.stdev(unbiased_ensemble_average_cumulative_customer)

#t-value for alpha=0.025 (at infinity): 1.96 
t_value = 1.96
half_width = t_value * (deviation / math.sqrt(len(unbiased_ensemble_average_cumulative_customer)))
upper_limit_customers = estimator + half_width
lower_limit_customers = estimator - half_width 


        

