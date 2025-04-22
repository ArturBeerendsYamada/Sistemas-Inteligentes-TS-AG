import random
import sys
import os

def create_matrix(n):
    matrix = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            value = random.randint(-100, 1000)
            if value <= 0:
                value = sys.maxsize # Use maxsize to represent infinity
            matrix[i][j] = value
            matrix[j][i] = value
    return matrix

def save_matrix_to_file(matrix, filename):
    with open(filename, "w") as f:
        for row in matrix:
            f.write(";".join(map(str, row)) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_input.py <n>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n <= 0:
            raise ValueError("n must be a positive integer.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

    matrix = create_matrix(n)

    # Ensure the ../input directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "../input")
    os.makedirs(output_dir, exist_ok=True)

    # Save the matrix to a file named <n>.txt in the ../input directory
    output_file = os.path.join(output_dir, f"matriz_size_{n}.csv")
    save_matrix_to_file(matrix, output_file)

    print(f"Matrix saved to {output_file}")
