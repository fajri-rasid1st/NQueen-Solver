Simple Hill Climbing:

```
def hill_climbing(problem):
    current = problem.INITIAL_STATE
    while True:
        neighbor = highest_value_successor_of current
        if (neighbor.VALUE <= current.VALUE):
            return current.STATE
        current = neighbor
```

Random Restart Hill Climbing:

```
def hill_climbing_random_restart(problem):
    current = problem.INITIAL_STATE
    heuristic = h(current)
    while heuristic != 0:
        current = problem.STATE_WITH_MIN_HEURISTIC
        heuristic = h(current)
    return current.STATE
```

Genetic Algorithm:

```
function genetic_algorithm():
    p = population()
    evaluate(p)
    while not done, do
        p' = select_parent(p)
        reproduce(p')
        mutate(p')
        evaluate(p')
            p = survive(p, p')
    return best_solution
```

CSP forward checking:

```
function forward_checking(variable, csp) // list of variables with new domains, or failure
    for each constraint in connected_constraints(variable) do
        if connected_variable is assigned then
            if constraint is not satisfied then
                return failure
        else
            for each value in connected_variable.domain do
                connected_variable.assign(value)
                if constraint is not satisfied do
                    remove value from connected_variable.domain
                if connected_variable.domain.count == 0 then
                    return failure
                add connected_variable to solution
    return solution
```
