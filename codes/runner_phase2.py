import matplotlib.pyplot as plt
import math

# Specify the file path of the simulation code
simulation_file_path = "simulation_phase2.py"

# Specify the parameter value
RANDOM_SEED = 10
REP_COUNT = 10
START_CONDITION = 1

# Read the contents of the simulation file
with open(simulation_file_path, "r") as file:
    simulation_code = file.read()

globals_dict = {'RANDOM_SEED': RANDOM_SEED, 'REP_COUNT' : REP_COUNT, 'START_CONDITION' : START_CONDITION}
exec(simulation_code, globals_dict)
upper_limit1 = globals_dict['upper_limit']
lower_limit1 = globals_dict['lower_limit']
ensemble_averages1 = globals_dict['ensemble_averages1']

START_CONDITION = 2
globals_dict = {'RANDOM_SEED': RANDOM_SEED, 'REP_COUNT' : REP_COUNT, 'START_CONDITION' : START_CONDITION}
exec(simulation_code, globals_dict)
upper_limit2 = globals_dict['upper_limit']
lower_limit2 = globals_dict['lower_limit']
ensemble_averages2 = globals_dict['ensemble_averages1']

START_CONDITION = 3
globals_dict = {'RANDOM_SEED': RANDOM_SEED, 'REP_COUNT' : REP_COUNT, 'START_CONDITION' : START_CONDITION}
exec(simulation_code, globals_dict)
upper_limit3 = globals_dict['upper_limit']
lower_limit3 = globals_dict['lower_limit']
ensemble_averages3 = globals_dict['ensemble_averages1']

# Plotting the figure
plt.plot(ensemble_averages1, label='Average Values 1')
plt.axhline(upper_limit1, linestyle='--', color='red', label='Upper Limit 1')  # Add upper limit line
plt.axhline(lower_limit1, linestyle='--', color='purple', label='Lower Limit 1')  # Add lower limit line
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot of Confidence Intervals with Average Values of Start Condition 1')
plt.legend()  # Add a legend to differentiate between the two lines
plt.show()

# Plotting the figure
plt.plot(ensemble_averages2, label='Average Values 2')
plt.axhline(upper_limit2, linestyle='--', color='red', label='Upper Limit 2')  # Add upper limit line
plt.axhline(lower_limit2, linestyle='--', color='purple', label='Lower Limit 2')  # Add lower limit line
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot of Confidence Intervals with Average Values of Start Condition 2')
plt.legend()  # Add a legend to differentiate between the two lines
plt.show()

# Plotting the figure
plt.plot(ensemble_averages3, label='Average Values 3')
plt.axhline(upper_limit3, linestyle='--', color='red', label='Upper Limit 3')  # Add upper limit line
plt.axhline(lower_limit3, linestyle='--', color='purple', label='Lower Limit 3')  # Add lower limit line
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot of Confidence Intervals with Average Values of Start Condition 3')
plt.legend()  # Add a legend to differentiate between the two lines
plt.show()
