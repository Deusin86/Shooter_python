import pygame, random

from Main import Game

monitor_largura=1000
monitor_altura=600

def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [monitor_largura, monitor_altura]
    screen = pygame.display.set_mode(size)

 #   imagem = pygame.image.load("bola.png").convert_alpha()
    pygame.display.set_caption("Shooter by Hugo e Vicente")
  #  pygame.display.set_icon(imagem)
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events

    #    game.shoot()
        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
