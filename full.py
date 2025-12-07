import csv
import heapq

from mapGenerator import generate_terrain_grid, save_terrain_map


def get_cities():
    """Return list of cities with coordinates"""
    return [
        ("New York NY", 50, 264),
        ("Los Angeles CA", 91, 34),
        ("Chicago IL", 44, 193),
        ("Houston TX", 118, 153),
        ("Phoenix AZ", 95, 66),
        ("Philadelphia PA", 55, 260),
        ("San Antonio TX", 120, 137),
        ("San Diego CA", 99, 40),
        ("Dallas TX", 99, 146),
        ("San Jose CA", 71, 15),
        ("Austin TX", 114, 141),
        ("Jacksonville FL", 114, 227),
        ("Fort Worth TX", 99, 143),
        ("Columbus OH", 55, 217),
        ("Charlotte NC", 84, 229),
        ("San Francisco CA", 69, 11),
        ("Indianapolis IN", 56, 201),
        ("Seattle WA", 8, 12),
        ("Denver CO", 56, 103),
        ("Washington DC", 61, 248),
        ("Boston MA", 41, 279),
        ("El Paso TX", 105, 95),
        ("Nashville TN", 79, 197),
        ("Detroit MI", 41, 222),
        ("Oklahoma City OK", 83, 143),
    ]


def save_cities(cities, filename='cities.csv'):
    """Save cities to CSV"""
    print(f"Saving cities to {filename}...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['City', 'Lat', 'Lon', 'Row', 'Col'])
        for name, row, col in cities:
            # Dummy lat/lon for compatibility
            writer.writerow([name, 0, 0, row, col])
    print(f"Cities saved: {len(cities)} cities")


def dijkstra(grid, start_row, start_col, end_row, end_col):
    """Find shortest path using Dijkstra's algorithm"""
    rows = len(grid)
    cols = len(grid[0])

    # Priority queue: (cost, row, col)
    pq = [(0, start_row, start_col)]
    visited = set()
    distances = {}
    distances[(start_row, start_col)] = 0

    # 8 directions: N, S, E, W, NE, NW, SE, SW
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while pq:
        current_cost, row, col = heapq.heappop(pq)

        if (row, col) in visited:
            continue

        visited.add((row, col))

        # Check if we reached the destination
        if row == end_row and col == end_col:
            return current_cost

        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Check boundaries
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if (new_row, new_col) not in visited:
                    terrain_cost = grid[new_row][new_col]

                    # Skip water (999) - treat as impassable
                    if terrain_cost >= 999:
                        continue

                    # Diagonal moves cost sqrt(2) times the terrain cost
                    if dr != 0 and dc != 0:
                        move_cost = terrain_cost * 1.414
                    else:
                        move_cost = terrain_cost

                    new_cost = current_cost + move_cost

                    if (new_row, new_col) not in distances or new_cost < distances[(new_row, new_col)]:
                        distances[(new_row, new_col)] = new_cost
                        heapq.heappush(pq, (new_cost, new_row, new_col))

    return float('inf')  # No path found


def calculate_all_paths(cities, grid):
    """Calculate shortest paths between all city pairs"""
    n = len(cities)
    path_costs = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        print(f"Calculating paths from {cities[i][0]}... ({i + 1}/{n})")
        for j in range(n):
            if i == j:
                path_costs[i][j] = 0
            else:
                cost = dijkstra(grid, cities[i][1], cities[i][2],
                                cities[j][1], cities[j][2])
                if cost == float('inf'):
                    path_costs[i][j] = 'inf'
                    print(f"  Warning: No path found from {cities[i][0]} to {cities[j][0]}")
                else:
                    path_costs[i][j] = round(cost, 2)

    return path_costs


def write_results(cities, path_costs, output_filename):
    """Write results to CSV with city names as headers"""
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header row
        header = [''] + [city[0] for city in cities]
        writer.writerow(header)

        # Data rows
        for i, city in enumerate(cities):
            row = [city[0]] + path_costs[i]
            writer.writerow(row)


# Main execution
if __name__ == "__main__":
    print("=" * 70)
    print("Step 1: Generating terrain grid...")
    print("=" * 70)
    grid = generate_terrain_grid()
    save_terrain_map(grid, 'map.csv')

    print("\n" + "=" * 70)
    print("Step 2: Generating city data...")
    print("=" * 70)
    cities = get_cities()
    save_cities(cities, 'cities.csv')

    print("\n" + "=" * 70)
    print("Step 3: Calculating shortest paths...")
    print("=" * 70)

    # Debug: Check terrain at city locations
    print("\nCity terrain values (first 5):")
    for name, row, col in cities[:5]:
        print(f"  {name}: terrain={grid[row][col]} at ({row},{col})")

    print("\nCalculating shortest paths between all city pairs...")
    print("This may take a while...\n")

    path_costs = calculate_all_paths(cities, grid)

    print("\n" + "=" * 70)
    print("Step 4: Saving results...")
    print("=" * 70)
    write_results(cities, path_costs, 'city_paths.csv')

    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print("Generated files:")
    print("  - map.csv (terrain grid)")
    print("  - cities.csv (city coordinates)")
    print("  - city_paths.csv (all shortest paths)")
    print(f"\nTotal city pairs calculated: {len(cities) * len(cities)}")