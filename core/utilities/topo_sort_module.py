from collections import defaultdict, deque

def topo_sort_modules(modules):
    """
    modules = {
        "attendance": {"depends": ["employees"]},
        "employees": {"depends": []},
    }
    returns ordered list: ['employees', 'attendance']
    """


    graph = defaultdict(list)
    indegree = defaultdict(int)

    # initialize indegree
    for module, data in modules.items():
        indegree[module] = 0

    for module, data in modules.items():
        for dep in data["depends"]:
            if dep not in modules:
                print(f"Missing dependency '{dep}' for module '{module}'")
                continue

            graph[dep].append(module)
            indegree[module] += 1

    # Kahn’s topo sort
    queue = deque([m for m in modules if indegree[m] == 0])
    order = []

    while queue:
        m = queue.popleft()
        order.append(m)

        for child in graph[m]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                print(child)
    print(order)
    return order
