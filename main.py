import pygame
import random

# Initialize Game Window
pygame.init()
size = width, height = 550, 650 # Screen dimensions
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Feed The Squirrel")
clock = pygame.time.Clock()


# Game States
game_is_running = True
nut_is_cut = False
squirrel_is_asking = True
measure_cut_nut = False
display_results = False
user_cut_correctly = False


# Game Constants
CUTTER_SPEED = [0, 2]
ACORN_FALL_SPEED = 2
ERROR_MARGIN = 3
WIN_PURPLE = (95, 21, 214)
FAIL_RED = (150, 0, 0)
ACORN_XPOS_ADJUST = 1.21


# Game Text Data
random_percent = random.randint(1, 100)
font = pygame.font.SysFont(None, 48)
wanted_percent = font.render(f'{random_percent:02}%', True, 0) # How much the squirrel wants


# Load Acorn Image
acorn = pygame.image.load("Images/acorn_img.png").convert_alpha()
acorn = pygame.transform.scale(acorn, (16*9, 25*9)) # Scale acorn image down
acornRec = acorn.get_rect() # Rectangular transformation border

# Load Background Image
bg = pygame.image.load("Images/bg_image.png")
bg_rec = bg.get_rect()

# Load Squirrel waiting sprite
squirrel_waiting = pygame.image.load("Images/squirrel_sprites/Squirrel_waiting.png")
squirrel_waiting_rect = squirrel_waiting.get_rect()

# Load Squirrel sad sprite
squirrel_sad = pygame.image.load("Images/squirrel_sprites/Squirrel_sad.png")
squirrel_sad = pygame.transform.scale(squirrel_sad, (squirrel_sad.get_width()*1.5, squirrel_sad.get_height()*1.5))
squirrel_sad_rect = squirrel_sad.get_rect()
squirrel_sad_rect.center = (width // 2, height * 0.68)

# Load Squirrel happy sprite
squirrel_happy = pygame.image.load("Images/squirrel_sprites/Squirrel_happy.png")
squirrel_happy_rect = squirrel_happy.get_rect()
squirrel_happy_rect.center = (width * 0.55, height * 0.6)

# Load Nut cutter sprite
nut_cutter = pygame.image.load("Images/nut_cutter.png")
nut_cutter_rect = nut_cutter.get_rect()
nut_cutter_rect.x = width - acorn.get_width() * 1.5
nut_cutter_rect.y = acornRec.height // 2
nut_cutter = pygame.transform.scale(nut_cutter, (nut_cutter_rect.width, nut_cutter_rect.height * 0.3)) # Scale acorn image down

# Load Nut measuring scale sprite
measuring_scale = pygame.image.load("Images/measuring_scale.png")
measuring_scale_rect = measuring_scale.get_rect()
measuring_scale_rect.x = width - (measuring_scale.get_width() + 10)
measuring_scale_rect.y = height - (measuring_scale.get_height() + 15)


# Variables to handle the split acorn
split_acorn_parts = []
acorn_cut_bottom_yPos = 0
cut_acorn_rect = None


# Game Functions (Methods)
def split_image(image, split_height):
    """
    Takes an image and splits it into two parts (a top part and bottom part) and assigns it to the specified global
    variable

    :param image: The image that is going to be split
    :param split_height: where the image should be split
    :return: void
    """

    global acorn_cut_bottom_yPos, split_acorn_parts

    image_width = image.get_width()
    image_height = image.get_height()

    print(split_height, image_height)
    if split_height < 0:
        return None, image
    elif split_height > image_height:
        return image, None
    else:
        top_part = image.subsurface(pygame.Rect(0, 0, image_width, split_height))
        bottom_part = image.subsurface(pygame.Rect(0, split_height, image_width, image_height - split_height))

        acorn_cut_bottom_yPos = top_part.get_height()
        split_acorn_parts = [top_part, bottom_part]

def calculate_percentage_cut(cut_portion):
    """
    Calculates what percent of the entire acorn image is the cut_portion. In other words cut_portion is x% of
    entire acorn

    :param cut_portion: the size of the acorn the user cut off
    :return: percentage of acorn that was cut off
    """

    acorn_total_height = acorn.get_height()
    cut_piece_height = cut_portion.get_height()

    return cut_piece_height * 100 // acorn_total_height

def check_if_cut_right_amount(percentage_wanted, cut_percentage):
    """
    Compares the percentage of the acorn the user cut to the percentage requested by the squirrel (with a specified
    margin of error)

    :param percentage_wanted: percentage of acorn requested by squirrel
    :param cut_percentage: percentage of acorn cut by the user
    :return: True if user cuts the wanted percentage (or a value within the error margin) and False otherwise
    """
    if  percentage_wanted - ERROR_MARGIN <= cut_percentage <= percentage_wanted + ERROR_MARGIN:
        return True

    return False

def reset_all_game_states():
    """
    Resets all the states of the game to their pre-while loop values, and generates a new random value to act as the
    percentage of nut the squirrel wants. This method updates global variables.

    :return: Void
    """
    game_states = globals()
    game_states["game_is_running"] = True
    game_states["nut_is_cut"] = False
    game_states["squirrel_is_asking"] = True
    game_states["measure_cut_nut"] = False
    game_states["display_results"] = False

    new_percentage_wanted = random.randint(1, 100)
    game_states["random_percent"] =  new_percentage_wanted # Generate new random number
    game_states["wanted_percent"] = font.render(f'{new_percentage_wanted:02}%', True, 0) # How much the squirrel wants


# Start of game loop
while game_is_running:
    # check for events occurring
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False

    key_states = pygame.key.get_pressed() # Returns list of states of all keyboard keys
    if key_states[pygame.K_SPACE]: # If the space bar is pressed
        print("Key pressed")
        split_image(acorn, nut_cutter_rect.top) # Split the acorn image at the point space bar  was pressed
        nut_is_cut = True

    if key_states[pygame.K_RETURN]: # Reset Game
        reset_all_game_states()

    # Clean the screen for each frame
    screen.fill("grey")
    screen.blit(bg, bg_rec)

    if display_results:
        if user_cut_correctly:
            font = pygame.font.SysFont(None, 48)
            win_message = font.render(f'Nice Cutting Skills ;)', True, WIN_PURPLE)
            screen.blit(win_message, (115, 110))
            screen.blit(squirrel_happy, squirrel_happy_rect)
        else:
            font = pygame.font.SysFont(None, 48)
            loss_message = font.render(f"That's not what I wanted :(", True, FAIL_RED)
            screen.blit(loss_message, (80, 110))
            screen.blit(squirrel_sad, squirrel_sad_rect)

    else:
        # Display the nut measuring scale on screen
        screen.blit(measuring_scale, measuring_scale_rect)

        if nut_is_cut:
            # Place the top part of the nut where it should be
            screen.blit(split_acorn_parts[0], (width - split_acorn_parts[0].get_width() * ACORN_XPOS_ADJUST, 0))

            # Rect for the bottom part of the nut that was cut
            cut_acorn_rect = split_acorn_parts[1].get_rect()
            cut_acorn_rect.x = width - split_acorn_parts[0].get_width() * ACORN_XPOS_ADJUST
            cut_acorn_rect.y = acorn_cut_bottom_yPos

            # Check if the cut portion of the nut has reached the measuring scale
            if cut_acorn_rect.bottom > measuring_scale_rect.y + 5:
                nut_is_cut = False
                measure_cut_nut = True
                squirrel_is_asking = False
                screen.blit(split_acorn_parts[1], cut_acorn_rect)
            else:
                # Move the nut down if it hasn't reached the scale
                acorn_cut_bottom_yPos += ACORN_FALL_SPEED
                screen.blit(split_acorn_parts[1], cut_acorn_rect)

        elif measure_cut_nut:
            screen.blit(split_acorn_parts[0], (width - split_acorn_parts[0].get_width() * ACORN_XPOS_ADJUST, 0))
            screen.blit(split_acorn_parts[1], cut_acorn_rect)

            percentage_cut = calculate_percentage_cut(split_acorn_parts[1])
            font = pygame.font.SysFont(None, 40)
            cut_acorn_size = font.render(f'{percentage_cut:02}%', True, 0)
            screen.blit(cut_acorn_size, (measuring_scale_rect.x * 1.17, measuring_scale_rect.y * 1.15)) # Display scale reading

            user_cut_correctly = check_if_cut_right_amount(random_percent, percentage_cut)
            display_results = True

            pygame.display.flip()
            pygame.time.wait(1000)

        else:
            # if nut has not be cut then keep moving the nut cutter that shows where to cut nut
            screen.blit(acorn, (width - acorn.get_width() * ACORN_XPOS_ADJUST, 0))  # Display acorn image

            # Moves the nut cutter vertically across the nut
            nut_cutter_rect = nut_cutter_rect.move(CUTTER_SPEED)
            if nut_cutter_rect.top >= acornRec.height or nut_cutter_rect.top <= 0:  # Move only across the nut
                CUTTER_SPEED[1] = -CUTTER_SPEED[1]

            screen.blit(nut_cutter, nut_cutter_rect)


        if squirrel_is_asking:
            screen.blit(squirrel_waiting, (0, height - squirrel_waiting.get_height()))  # Display squirrel asking image
            screen.blit(wanted_percent,(squirrel_waiting.get_width() * 0.46, height - squirrel_waiting.get_height() * 0.38))

    # Update the screen
    pygame.display.flip()

    clock.tick(60)


