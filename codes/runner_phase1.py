import matplotlib.pyplot as plt
import math

# Specify the file path of the simulation code
simulation_file_path = "simulation_phase1.py"

# Specify the parameter value
RANDOM_SEED = 30
REP_COUNT = 30

# Read the contents of the simulation file
with open(simulation_file_path, "r") as file:
    simulation_code = file.read()

# Execute the simulation code with the specific random number
globals_dict = {'RANDOM_SEED': RANDOM_SEED, 'REP_COUNT' : REP_COUNT}
exec(simulation_code, globals_dict)

# Access the modified random_number from the simulation code
result = globals_dict['sojourn_avg_list']
result2 = globals_dict['sojourn_avg_smooth_list']
upper_limit = globals_dict['upper_limit']
lower_limit = globals_dict['lower_limit']
upper_limit_customers = globals_dict['upper_limit_customers']
lower_limit_customers = globals_dict['lower_limit_customers']

# Plotting the figure
plt.plot(result, label='Ensemble Average of Wi')
plt.plot(result2, label='Cumulative Average of Blue Data')  # Add the second line
plt.axhline(upper_limit, linestyle='--', color='r', label='Upper Limit')  # Add upper limit line
plt.axhline(lower_limit, linestyle='--', color='g', label='Lower Limit')  # Add lower limit line
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot of Sojourn Times')
plt.legend()  # Add a legend to differentiate between the two lines
plt.show()

# Access the modified random_number from the simulation code
result3 = globals_dict['ensemble_average_cumulative_customer']

# Plotting the figure
plt.plot(result3, label='Ensemble Average of Customer')
plt.axhline(upper_limit_customers, linestyle='--', color='r', label='Upper Limit')  # Add upper limit line
plt.axhline(lower_limit_customers, linestyle='--', color='g', label='Lower Limit')  # Add lower limit line
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot of Customer')
plt.legend()  # Add a legend to differentiate between the two lines
plt.show()



