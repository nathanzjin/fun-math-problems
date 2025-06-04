import sys

pentominoes_base = {
    'F': [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
    'I': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    'L': [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
    'N': [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)],
    'P': [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
    'T': [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    'U': [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    'V': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    'W': [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    'X': [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    'Y': [(0, 0), (1, 0), (2, 0), (3, 0), (2, 1)],
    'Z': [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
}

def rotate_90(coord):
    x, y = coord
    return (y, -x)

def reflect(coord):
    x, y = coord
    return (-x, y)

def normalize(coords):
    min_x = min(x for x, y in coords)
    min_y = min(y for x, y in coords)
    normalized = sorted((x - min_x, y - min_y) for x, y in coords)
    return tuple(normalized)

def generate_all_orientations(base_shape):
    seen = set()
    current = [tuple(coord) for coord in base_shape]
    for _ in range(4):
        norm = normalize(current)
        seen.add(norm)
        current = [rotate_90(c) for c in current]
    reflected = [reflect(c) for c in base_shape]
    current = [tuple(c) for c in reflected]
    for _ in range(4):
        norm = normalize(current)
        seen.add(norm)
        current = [rotate_90(c) for c in current]
    return [list(shape) for shape in seen]

pentomino_templates = []
for name, base in pentominoes_base.items():
    orientations = generate_all_orientations(base)
    for orient in orientations:
        pentomino_templates.append((name, orient))

grid = [[i * 10 + j + 1 for j in range(10)] for i in range(10)]
valid_pentominoes = []
seen_cells = set()

for name, template in pentomino_templates:
    for i in range(10):
        for j in range(10):
            cells = []
            valid = True
            for dx, dy in template:
                x = i + dx
                y = j + dy
                if not (0 <= x < 10 and 0 <= y < 10):
                    valid = False
                    break
                cells.append((x, y))
            if not valid:
                continue
            
            # Deduplication check
            cell_key = frozenset(cells)  # Use frozenset to handle different orderings
            if cell_key in seen_cells:
                continue
            seen_cells.add(cell_key)
            
            total = sum(grid[x][y] for x, y in cells)
            if total % 5 == 0:
                valid_pentominoes.append((cells, total, name))

def format_pentomino(cells):
    min_row = min(x for x, y in cells)
    max_row = max(x for x, y in cells)
    min_col = min(y for x, y in cells)
    max_col = max(y for x, y in cells)
    
    output = []
    for x in range(min_row, max_row + 1):
        row = []
        for y in range(min_col, max_col + 1):
            if (x, y) in cells:
                row.append(f"{grid[x][y]:3}")  # 3-digit width for alignment
            else:
                row.append("   ")
        output.append(" ".join(row).rstrip())
    return "\n".join(output)

with open('pentomino_results.txt', 'w') as f:
    f.write(f"Total valid pentominoes: {len(valid_pentominoes)}\n\n")
    for idx, (cells, total, name) in enumerate(valid_pentominoes, 1):
        f.write(f"Pentomino {idx}: Type {name}, Sum = {total}\n")
        f.write(format_pentomino(cells) + "\n\n")

print("Results saved to pentomino_results.txt")
