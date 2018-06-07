import random
import sys
actions = ["LEFT", "RIGHT", "UP", "DOWN"]

def perform_action(x, y, action):
    if action == "LEFT"  and x != 0: return x-1, y
    if action == "RIGHT" and x != 3: return x+1, y
    if action == "UP"    and y != 0: return x, y-1
    if action == "DOWN"  and y != 2: return x, y+1
    return x, y

def transition_model(x, y, action):
    preferred = [
        ["RIGHT", "RIGHT", "RIGHT", "LEFT"],
        ["UP",    "DOWN",  "UP",    "UP"   ],
        ["UP",    "LEFT",  "UP",    "LEFT"],
    ][y][x] 
    return 1 if action == preferred else 0.0
 
def policy_evaluation(policy, utilities, states, discount):
    for x, y in states:
        transitions = [transition_model(x, y, policy[y][x]) * utilities[yy][xx] for xx, yy in all_possibles(x, y)]
        utilities[y][x] = reward[y][x] + discount * sum(transitions)
    return utilities


def best_action(state, u):
    best_action = (None, -sys.maxsize)
    for a in actions:
        score = aciton_score(state, a, u)
        if score > best_action[1]:
            best_action = (a, score)
    return best_action

all_possibles = lambda x, y: [perform_action(x, y, action) for action in actions]
aciton_score = lambda s, a, u: sum([transition_model(x, y, a) * u[y][x] for x, y in all_possibles(*s)])


reward = [
    [-0.04, -0.04, -0.04, +1],
    [-0.04, -100,  -0.04, -1],
    [-0.04, -0.04, -0.04, -0.04],
]
states = [(x, y) for x in range(4) for y in range(3)]
random_initial_policy = [random.sample(actions, 4)]*3

def policy_iteration(mdp, policy, discount):
    
    unchanged = False 
    u = [[0]*4]*3
    i = 0
    while not unchanged: 
        # Evaluate policy using bellman equation
        u = policy_evaluation(policy, u, states, discount)
        unchanged = True
        
        for state in mdp:
            x, y = state
            # Compare with action in policy with all others to see if best:
            if best_action(state, u)[1] > aciton_score(state, policy[y][x], u):
                policy[y][x] = best_action(state, u)[0]

                # Mark as changed to loop one more time.
                unchanged = False
        if i == 100: break
        i += 1
    return policy
    
print(policy_iteration(states, random_initial_policy, 0.9))