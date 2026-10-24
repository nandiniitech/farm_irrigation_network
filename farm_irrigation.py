
import heapq
import time

# ==========================================
# FARM IRRIGATION NETWORK OPTIMIZATION
# DAA MINI PROJECT
# ==========================================

# Weighted, undirected graph
# Edge weights represent pipeline installation costs.

graph = {
    "Water Source": {
        "Storage Tank": 4,
        "Field A": 6
    },
    "Storage Tank": {
        "Water Source": 4,
        "Field A": 2,
        "Field B": 5
    },
    "Field A": {
        "Water Source": 6,
        "Storage Tank": 2,
        "Field B": 3,
        "Field C": 7
    },
    "Field B": {
        "Storage Tank": 5,
        "Field A": 3,
        "Field C": 4,
        "Field D": 6
    },
    "Field C": {
        "Field A": 7,
        "Field B": 4,
        "Field D": 2
    },
    "Field D": {
        "Field B": 6,
        "Field C": 2
    }
}


# ==========================================
# 1. DISPLAY NETWORK
# ==========================================

def display_network():
    print("\n========== FARM IRRIGATION NETWORK ==========")

    if not graph:
        print("The network is empty.")
        return

    for location, neighbours in graph.items():
        print(f"\nLocation: {location}")

        if neighbours:
            for neighbour, cost in neighbours.items():
                print(f"  -> {neighbour}: Pipeline cost = {cost:g}")
        else:
            print("  No connected pipelines")

    print("\nTotal locations:", len(graph))
    print("=============================================")


# ==========================================
# 2. ADD PIPELINE
# ==========================================

def add_pipeline():
    source = input("Enter starting location: ").strip()
    destination = input("Enter destination location: ").strip()

    if not source or not destination:
        print("Location names cannot be empty.")
        return

    if source == destination:
        print("A pipeline cannot connect a location to itself.")
        return

    try:
        cost = float(input("Enter pipeline installation cost: "))

        if cost <= 0:
            print("Cost must be greater than zero.")
            return

    except ValueError:
        print("Invalid cost. Enter a number.")
        return

    # Create locations if they do not exist.
    graph.setdefault(source, {})
    graph.setdefault(destination, {})

    # Add a bidirectional pipeline.
    graph[source][destination] = cost
    graph[destination][source] = cost

    print("\nPipeline added successfully!")
    print(f"{source} <-> {destination}, Cost = {cost:g}")


# ==========================================
# 3. PRIM'S ALGORITHM
# Minimum Spanning Tree
# ==========================================

def prim_mst():
    if not graph:
        print("The network is empty.")
        return

    start = next(iter(graph))

    visited = set()
    min_heap = [(0, start, None)]

    total_cost = 0
    selected_pipelines = []

    while min_heap and len(visited) < len(graph):
        cost, current, parent = heapq.heappop(min_heap)

        if current in visited:
            continue

        visited.add(current)

        if parent is not None:
            selected_pipelines.append(
                (parent, current, cost)
            )
            total_cost += cost

        for neighbour, weight in graph[current].items():
            if neighbour not in visited:
                heapq.heappush(
                    min_heap,
                    (weight, neighbour, current)
                )

    print("\n========== PRIM'S ALGORITHM ==========")

    # Check connectivity.
    if len(visited) != len(graph):
        unreachable = set(graph.keys()) - visited

        print("The network is disconnected!")
        print("An MST cannot connect all locations.")
        print("Unreachable locations:", ", ".join(sorted(unreachable)))
        print("Please add pipelines connecting these locations.")
        return

    print("Minimum-cost pipeline network:\n")

    for source, destination, cost in selected_pipelines:
        print(f"{source} -> {destination}: Cost = {cost:g}")

    print("\nTotal minimum installation cost:", f"{total_cost:g}")
    print("Total pipelines selected:", len(selected_pipelines))
    print("Total locations connected:", len(visited))
    print("\nTime Complexity: O(E log V)")
    print("Space Complexity: O(V + E)")
    print("======================================")


# ==========================================
# 4. DIJKSTRA'S ALGORITHM
# Shortest / Minimum-Cost Route
# ==========================================

def dijkstra():
    if not graph:
        print("The network is empty.")
        return

    source = input("Enter source location: ").strip()
    destination = input("Enter destination location: ").strip()

    if source not in graph:
        print("Source location does not exist.")
        return

    if destination not in graph:
        print("Destination location does not exist.")
        return

    distances = {
        location: float("inf")
        for location in graph
    }

    previous = {
        location: None
        for location in graph
    }

    distances[source] = 0
    min_heap = [(0, source)]

    while min_heap:
        current_distance, current = heapq.heappop(min_heap)

        if current_distance > distances[current]:
            continue

        if current == destination:
            break

        for neighbour, weight in graph[current].items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current

                heapq.heappush(
                    min_heap,
                    (new_distance, neighbour)
                )

    print("\n========== DIJKSTRA'S ALGORITHM ==========")

    if distances[destination] == float("inf"):
        print("No route exists between these locations.")
        return

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    print("Shortest route:")
    print(" -> ".join(path))

    print("Minimum route cost:", f"{distances[destination]:g}")
    print("\nTime Complexity: O((V + E) log V)")
    print("Space Complexity: O(V + E)")
    print("==========================================")


# ==========================================
# 5. PERFORMANCE ANALYSIS
# ==========================================

def performance_analysis():
    if not graph:
        print("The network is empty.")
        return

    vertex_count = len(graph)

    edge_count = sum(
        len(neighbours)
        for neighbours in graph.values()
    ) // 2

    print("\n========== PERFORMANCE ANALYSIS ==========")
    print("Number of locations (V):", vertex_count)
    print("Number of pipelines (E):", edge_count)

    start_time = time.perf_counter()

    visited = set()
    start = next(iter(graph))

    min_heap = [(0, start)]
    total_cost = 0

    while min_heap and len(visited) < vertex_count:
        cost, current = heapq.heappop(min_heap)

        if current in visited:
            continue

        visited.add(current)
        total_cost += cost

        for neighbour, weight in graph[current].items():
            if neighbour not in visited:
                heapq.heappush(
                    min_heap,
                    (weight, neighbour)
                )

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    if len(visited) == vertex_count:
        print("Network status: Connected")
        print("Minimum spanning tree cost:", f"{total_cost:g}")
    else:
        print("Network status: Disconnected")
        print("A spanning tree cannot connect all locations.")

    print(f"Execution time: {elapsed_time:.9f} seconds")

    print("\nTheoretical Complexity:")
    print("Prim's Algorithm: O(E log V)")
    print("Dijkstra's Algorithm: O((V + E) log V)")
    print("Graph Storage: O(V + E)")
    print("===========================================")


# ==========================================
# 6. MAIN MENU
# ==========================================

def main():
    while True:
        print("\n")
        print("==========================================")
        print(" FARM IRRIGATION NETWORK OPTIMIZATION")
        print("==========================================")
        print("1. Display Farm Network")
        print("2. Add Pipeline")
        print("3. Find Minimum-Cost Network (Prim)")
        print("4. Find Shortest Route (Dijkstra)")
        print("5. Performance Analysis")
        print("6. Exit")
        print("==========================================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            display_network()

        elif choice == "2":
            add_pipeline()

        elif choice == "3":
            prim_mst()

        elif choice == "4":
            dijkstra()

        elif choice == "5":
            performance_analysis()

        elif choice == "6":
            print("\nThank you for using the Farm Irrigation System!")
            break

        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
