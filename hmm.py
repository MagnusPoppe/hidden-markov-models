#%%
import numpy as np

### PART 1: Describe the “Umbrella domain” as an HMM: 

#%%
# Transition model for state_t 
X_t = np.array([[0.7, 0.3], [0.3, 0.7]])

# Sensor model for state_t
E_1 = np.array([[0.9, 0], [0, 0.2]])
E_3 = np.array([[0.1, 0], [0, 0.8]])

print("Transition model:\n", X_t)
print("Sensor model \n", E_1, "\n", E_3)