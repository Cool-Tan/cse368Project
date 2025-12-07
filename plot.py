import matplotlib.pyplot as plt

from full import get_cities

def visualize_mst_map(cities, mst_edges):
    # Extract coordinates
    name_to_coord = {name: (row, col) for name, row, col in get_cities()}

    plt.figure(figsize=(10, 6))

    # Plot cities
    for name, (row, col) in name_to_coord.items():
        plt.scatter(col, row, color='red')
        plt.text(col+1, row+1, name, fontsize=6)

    # Plot MST edges
    for city1, city2, cost in mst_edges:
        r1, c1 = name_to_coord[city1]
        r2, c2 = name_to_coord[city2]
        plt.plot([c1, c2], [r1, r2], color='blue', linewidth=1)

    plt.gca().invert_yaxis()
    plt.title("MST High-Speed Rail Network")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.tight_layout()
    plt.show()
