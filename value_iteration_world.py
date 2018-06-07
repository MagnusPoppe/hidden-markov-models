import copy

# Setup:
s = "s"
states = ["s", "!s"]
actions = ["N", "M"]
Xt = {"A1": 1.0, "A2": 1.0}
R = {"s": 2.0, "!s": 3.0}
y = 0.5

def E(c, R):
    E = c * max(R.values())
    return E

def max_key(dictionary):
    return list(Xt.keys())[list(Xt.values()).index(max(Xt.values()))]

def value_iteration(states, Xt, y):
    iterations = 0
    best = 0
    U = [0] * len(states)
    U_ = [0] * len(states)
    A = [""] * len(states)

    while (best < E((1 - y), R) / y and iterations < 1000):
        U = copy.deepcopy(U_)
        best = 0
        for i, state in enumerate(states):

            # VELGER UANSETT DEN MEST SANNSYNLIGE TRANSITION... DET ER JO IKKE NOE BRA POLICY...

            best_action = max_key(Xt)
            U_[i] = R[state] + y * max([a * U[i] for a in Xt.values()])
             
            if abs(U_[i] - U[i]) > best:
                best = abs(U_[i] - U[i])

        iterations += 1
        # y = y * 0.99

    print("Found optimal policy after %d iteration(s)" % iterations)
    print("Best policy: ", str(A))


value_iteration(states, Xt, y)
