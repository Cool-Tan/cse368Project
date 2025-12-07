import csv

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


def save_terrain_map(grid, filename='map.csv'):
    """Save terrain grid to CSV"""
    print(f"Saving terrain map to {filename}...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(grid)
    print(f"Terrain map saved: {len(grid)} rows x {len(grid[0])} columns")