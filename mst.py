import csv
from plot import visualize_mst_map


class UnionFind:
    """Union-Find data structure for Kruskal's algorithm"""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


def read_city_paths(filename):
    """Read the city path cost matrix"""
    cities = []
    cost_matrix = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        cities = header[1:]  # Skip first empty cell

        for row in reader:
            city_name = row[0]
            costs = []
            for val in row[1:]:
                if val == 'inf' or val == '':
                    costs.append(float('inf'))
                else:
                    costs.append(float(val))
            cost_matrix.append(costs)

    return cities, cost_matrix


def kruskal_mst(cities, cost_matrix):
    """Construct MST using Kruskal's algorithm"""
    n = len(cities)
    edges = []

    # Create list of all edges
    for i in range(n):
        for j in range(i + 1, n):
            if cost_matrix[i][j] != float('inf') and cost_matrix[i][j] > 0:
                edges.append((cost_matrix[i][j], i, j))

    print(f"Total valid edges found: {len(edges)}")

    # Sort edges by cost
    edges.sort()

    # Build MST using Union-Find
    uf = UnionFind(n)
    mst_edges = []
    total_cost = 0

    for cost, u, v in edges:
        if uf.union(u, v):
            mst_edges.append((cities[u], cities[v], cost))
            total_cost += cost
            if len(mst_edges) == n - 1:
                break

    # Check if MST is complete
    if len(mst_edges) < n - 1:
        print(f"\nWARNING: MST is incomplete! Only {len(mst_edges)} edges found, need {n - 1}")
        print("Some cities may not be reachable. Checking connectivity...")

        # Find which cities are disconnected
        components = {}
        for i in range(n):
            root = uf.find(i)
            if root not in components:
                components[root] = []
            components[root].append(cities[i])

        print(f"\nNumber of disconnected components: {len(components)}")
        for idx, (root, city_list) in enumerate(components.items(), 1):
            print(f"Component {idx}: {', '.join(city_list)}")

    return mst_edges, total_cost


def write_mst_results(mst_edges, total_cost, output_filename):
    """Write MST results to CSV"""
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['City 1', 'City 2', 'Cost'])
        for city1, city2, cost in mst_edges:
            writer.writerow([city1, city2, f'{cost:.2f}'])
        writer.writerow([])
        writer.writerow(['Total MST Cost', f'{total_cost:.2f}'])
        writer.writerow(['Number of Edges', len(mst_edges)])


def print_mst_results(mst_edges, total_cost):
    """Print MST results to console"""
    print("\nMinimum Spanning Tree (MST) Edges:")
    print("=" * 70)
    print(f"{'City 1':<25} {'City 2':<25} {'Cost':>15}")
    print("-" * 70)

    for city1, city2, cost in mst_edges:
        print(f"{city1:<25} {city2:<25} {cost:>15.2f}")

    print("-" * 70)
    print(f"{'Total MST Cost:':<50} {total_cost:>15.2f}")
    print(f"{'Number of edges:':<50} {len(mst_edges):>15}")
    print("=" * 70)


def visualize_mst_ascii(cities, mst_edges):
    """Create a simple text representation of MST connections"""
    # Build adjacency list
    connections = {city: [] for city in cities}
    for city1, city2, cost in mst_edges:
        connections[city1].append((city2, cost))
        connections[city2].append((city1, cost))

    print("\nMST Connection Summary:")
    print("=" * 70)
    for city in sorted(cities):
        if connections[city]:
            print(f"\n{city}:")
            for connected_city, cost in sorted(connections[city]):
                print(f"  └─ {connected_city} (cost: {cost:.2f})")
    print("=" * 70)


# Main execution
if __name__ == "__main__":
    print("Reading city path costs from city_paths.csv...")
    cities, cost_matrix = read_city_paths('city_paths.csv')

    print(f"Loaded {len(cities)} cities")

    print("\nConstructing Minimum Spanning Tree using Kruskal's algorithm...")
    mst_edges, total_cost = kruskal_mst(cities, cost_matrix)

    # Display results
    print_mst_results(mst_edges, total_cost)

    # Write to file
    print("\nWriting MST to mst_results.csv...")
    write_mst_results(mst_edges, total_cost, 'mst_results.csv')

    # Show connections
    visualize_mst_ascii(cities, mst_edges)

    print("\nVisualizing MST on map...")
    visualize_mst_map(cities, mst_edges)

    print("\nDone! MST results saved to mst_results.csv")
