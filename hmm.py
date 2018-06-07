# %%
import numpy as np

# Transition model for state_t (Answer to to PART A, 1)
Xt = np.array([[0.7, 0.3], [0.3, 0.7]])

# Sensor model for state_t (Answer to PART A, 2)
O1 = np.array([[0.9, .0], [.0, 0.2]])
O3 = np.array([[0.1, .0], [.0, 0.8]])


init = np.array([0.5, 0.5])


def forward(f, Xt, OT, OF, E, k):
    t = Xt.transpose().dot(f)        # Transition
    u = (OT if E[k] else OF).dot(t)  # Update
    delta = u / np.sum(u)            # Normalize

    # Day 0 (base case)?
    if not k:
        return delta
    return forward(delta, Xt, OT, OF, E, k-1)

def backward(Xt, OT, OF, E, k):
    e = (OT if E[k] else OF)
    if k < len(E)-1:
        res = Xt.dot(e).dot(backward(Xt, OT, OF, E, k+1))
    else: 
        res = Xt.dot(e).dot(np.array([1, 1]))
    
    return res / np.sum(res)

E = [True, True]
rain_day_2 = forward(init, Xt, O1, O3, E, len(E)-1)
print("Probability of rain on day 2 using forward:  ", rain_day_2)

E = np.array([True, True, False, True, True]) 
print("Probability of rain on day 5 using forward:  ", forward(init, Xt, O1, O3, E, len(E)-1))
print("Probability of rain on day 2 using backward: ", backward(Xt, O1, O3, E, 0)) 

