import pygame
import random
import time

pygame.init()

#(pygame has 0, 0 at top left)

#colours
BLACK = (0, 0, 0)
DEADCOL = (23, 26, 33)
ALIVECOL = (150, 197, 176)


#environment variables
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60


#init screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#clock
clock = pygame.time.Clock()


#generate random positions
def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


#draw grid
def draw_grid(positions):
    #draw position format: (col, row)
    for position in positions:
        col, row = position
        #top left corner
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, ALIVECOL, (*top_left, TILE_SIZE, TILE_SIZE)) #unpacks top_left and plots TILE_SIZE (X) x TILE_SIZE (Y)


    #draw horizontal lines
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK , (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
    #draw vertical lines
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK , (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


#updating the grid
def adjust_grid(positions):
    #init sets for new cells before replacing old ones
    all_neighbours = set()
    new_positions = set()

    for position in positions:
        neighbours = get_neighbours(position) #get neighbours of each position
        all_neighbours.update(neighbours) #update all_neighbours with neighbours

        neighbours = list(filter(lambda x: x in positions, neighbours)) #filter out neighbours that are in positions

        if len(neighbours) in [2, 3]:
            new_positions.add(position) #add position to new_positions (keep them) if it has 2 or 3 neighbours

    for position in all_neighbours:
        neighbours = get_neighbours(position)
        neighbours = list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) == 3:
            new_positions.add(position)

    return new_positions

def get_neighbours(pos):
    x, y = pos
    neighbours = []
    for dx in [-1, 0, 1]: #dx = displacement in x
        if x + dx < 0 or x + dx > GRID_WIDTH: #if x + dx is out of bounds, skip
            continue

        for dy in [-1, 0, 1]: #dy = displacement in y
            if y + dy < 0 or y + dy > GRID_WIDTH: #if y + dy is out of bounds, skip
                continue
            if dx == 0 and dy == 0: #if dx and dy are 0, skip
                continue

            neighbours.append((x + dx, y + dy)) #add neighbour to neighbours

    return neighbours


#main loop
def main():
    running = True
    playing = False
    count = 0
    update_frequency = 4

    start_time = time.time()  # Initial start time for the timer
    elapsed_time = 0  # Tracks total elapsed time

    positions = set()  # Init positions as a set

    while running:
        clock.tick(FPS)

        # Only update elapsed time if the game is playing
        if playing:
            elapsed_time = time.time() - start_time

            # Increment count and update the grid if needed
            count += 1
            if count >= update_frequency:
                count = 0
                positions = adjust_grid(positions)

        # Update the window title with the current game status and timer
        pygame.display.set_caption(f"{'Playing' if playing else 'Paused'} - Timer: {int(elapsed_time)} seconds")

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                # Toggle the game state between playing and paused
                if event.key == pygame.K_SPACE:
                    playing = not playing
                    if playing:
                        # Resuming: Reset the start time to adjust for the paused period
                        start_time = time.time() - elapsed_time
                    else:
                        # Pausing: Store the current elapsed time
                        elapsed_time = time.time() - start_time

                # Clear positions and reset timer
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    start_time = time.time()
                    elapsed_time = 0

                # Generate random positions
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH)

        # Drawing and refreshing the screen
        screen.fill(DEADCOL)  # Fill screen with the background color
        draw_grid(positions)  # Draws grid after filling screen
        pygame.display.update()  # Refresh the display

    pygame.quit()

#only run main if this file is run
if __name__ == "__main__":
    main()
