import csv
import heapq
from collections import defaultdict


def generate_terrain_grid():
    """Generate the 150x300 terrain grid"""
    grid = []

    for row in range(150):
        line = []
        for col in range(300):
            # Water (oceans and major water bodies)
            # Top rows - only water in far northeast corner (Atlantic)
            if row < 15 and col > 280:
                value = 999  # Atlantic NE water
            # Bottom rows (Gulf of Mexico)
            elif row > 130 and col > 60 and col < 180:
                value = 999
            # Left edge (Pacific Ocean) - but allow coastal cities
            elif col < 3:
                value = 999
            # Right edge (Atlantic Ocean)
            elif col > 292:
                value = 999
            # Great Lakes region
            elif row < 40 and col > 180 and col < 240 and row < 30:
                value = 999

            # Mountain ranges
            # Rocky Mountains (western region)
            elif col > 30 and col < 90 and row > 20 and row < 120:
                value = 30
            # Sierra Nevada / Cascade Range
            elif col > 5 and col < 35 and row > 25 and row < 100:
                value = 30
            # Appalachian Mountains (eastern region)
            elif col > 210 and col < 250 and row > 50 and row < 110:
                value = 30

            # Flat/hilly terrain (everything else)
            else:
                value = 20

            line.append(value)

        grid.append(line)

    return grid


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
    print("Generating terrain grid...")
    grid = generate_terrain_grid()

    print("Loading cities...")
    cities = get_cities()

    print(f"Loaded {len(cities)} cities and {len(grid)}x{len(grid[0])} terrain grid")

    # Debug: Check terrain at city locations
    print("\nCity terrain values:")
    for name, row, col in cities[:5]:  # Show first 5
        print(f"  {name}: terrain={grid[row][col]} at ({row},{col})")

    print("\nCalculating shortest paths between all city pairs...")
    print("This may take a while...\n")

    path_costs = calculate_all_paths(cities, grid)

    print("\nWriting results to city_paths.csv...")
    write_results(cities, path_costs, 'city_paths.csv')

    print("Done! Results saved to city_paths.csv")
    print(f"Total city pairs calculated: {len(cities) * len(cities)}")