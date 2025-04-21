#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h> // For max function if needed, or use a ternary operator

#define BOARD_SIZE 8

// Board to keep track of how many princesses attack each square
// A square is safe if attacked_count[r][c] == 0
int attacked_count[BOARD_SIZE][BOARD_SIZE];

// Store the maximum number of princesses found so far
int max_princesses = 0;

// Possible movements for the princess (dr, dc)
// Range 1: Horizontal, Vertical, Diagonal
// Range 2: Horizontal, Vertical, Diagonal
int moves_dr[] = {-1, -1, -1, 0, 0, 1, 1, 1, // Range 1
                  -2, -2, -2, 0, 0, 2, 2, 2}; // Range 2
int moves_dc[] = {-1, 0, 1, -1, 1, -1, 0, 1, // Range 1
                  -2, 0, 2, -2, 2, -2, 0, 2}; // Range 2

// Function to check if a position is within the board boundaries
bool is_valid(int r, int c) {
    return (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE);
}

// Function to update the attacked_count grid when placing or removing a princess
// delta will be +1 for placing, -1 for removing
void update_attacked_count(int r, int c, int delta) {
    // Mark/unmark the current square as attacked by *other* pieces (though not strictly needed for safety check of *this* piece)
    // More importantly, mark all squares attacked by a piece at (r, c)
    for (int i = 0; i < 16; ++i) { // 16 possible move types (8 range 1, 8 range 2)
        int next_r = r + moves_dr[i];
        int next_c = c + moves_dc[i];

        if (is_valid(next_r, next_c)) {
            attacked_count[next_r][next_c] += delta;
        }
    }
}

// Backtracking function to find the maximum number of princesses
// square_index: the linear index of the current square being considered (0 to 63)
// current_count: the number of princesses placed so far in this configuration
void solve(int square_index, int current_count) {
    // Base case: All squares considered
    if (square_index == BOARD_SIZE * BOARD_SIZE) {
        if (current_count > max_princesses) {
            max_princesses = current_count;
        }
        return;
    }

    int r = square_index / BOARD_SIZE; // Current row
    int c = square_index % BOARD_SIZE; // Current column

    // Option 1: Do not place a princess at the current square
    solve(square_index + 1, current_count);

    // Option 2: Place a princess at the current square, if it's safe
    if (attacked_count[r][c] == 0) {
        // Place the princess
        update_attacked_count(r, c, 1); // Mark squares attacked by this princess

        // Recurse to the next square
        solve(square_index + 1, current_count + 1);

        // Backtrack: Remove the princess and unmark attacked squares
        update_attacked_count(r, c, -1);
    }
}

int main() {
    // Initialize attacked_count board to all zeros
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            attacked_count[i][j] = 0;
        }
    }

    // Start the backtracking search from the first square (index 0)
    solve(0, 0);

    printf("Maximum number of non-attacking princesses: %d\n", max_princesses);

    return 0;
}