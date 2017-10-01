"""
 Sample Breakout Game

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""

# --- Import libraries used for this program

import math
import pygame

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# Size of break-out blocks
block_width = 35
block_height = 20

class Block(pygame.sprite.Sprite):
	"""This class represents each block that will get knocked out by the ball
	It derives from the "Sprite" class in Pygame """

	def __init__(self, color, x, y):
		""" Constructor. Pass in the color of the block,
			and its x and y position. """

		# Call the parent class (Sprite) constructor
		super().__init__()

		# Create the image of the block of appropriate size
		# The width and height are sent as a list for the first parameter.
		self.image = pygame.Surface([block_width, block_height])

		# Fill the image with the appropriate color
		self.image.fill(color)

		# Fetch the rectangle object that has the dimensions of the image
		self.rect = self.image.get_rect()

		# Move the top left of the rectangle to x,y.
		# This is where our block will appear..
		self.rect.x = x
		self.rect.y = y


class Ball(pygame.sprite.Sprite):
	""" This class represents the ball
		It derives from the "Sprite" class in Pygame """

	# Speed in pixels per cycle
	speed = 10.0

	# Floating point representation of where the ball is
	x = 0.0
	# y = 180.0
	y = 500.0

	# Direction of ball (in degrees)
	# direction = 200
	direction = 10
	# width = 10
	# height = 10
	width = 100
	height = 100
	# Constructor. Pass in the color of the block, and its x and y position
	def __init__(self):
		# Call the parent class (Sprite) constructor
		super().__init__()

		# Create the image of the ball
		self.image = pygame.image.load("saudi2.png")
		self.image = pygame.transform.scale(self.image, (40, 40))
		#pygame.Surface([self.width, self.height])

		# Color the ball
		#self.image.fill(white)

		# Get a rectangle object that shows where our image is
		self.rect = self.image.get_rect()

		# Get attributes for the height/width of the screen
		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

	def bounce(self, diff):
		""" This function will bounce the ball
			off a horizontal surface (not a vertical one) """

		self.direction = (180 - self.direction) % 360
		self.direction -= diff

	def update(self):
		""" Update the position of the ball. """
		# Sine and Cosine work in degrees, so we have to convert them
		direction_radians = math.radians(self.direction)

		# Change the position (x and y) according to the speed and direction
		self.x += self.speed * math.sin(direction_radians)
		self.y -= self.speed * math.cos(direction_radians)

		# Move the image to where our x and y are
		self.rect.x = self.x
		self.rect.y = self.y

		# Do we bounce off the top of the screen?
		if self.y <= 0:
			self.bounce(0)
			self.y = 1

		# Do we bounce off the left of the screen?
		if self.x <= 0:
			self.direction = (360 - self.direction) % 360
			self.x = 1

		# Do we bounce of the right side of the screen?
		if self.x > self.screenwidth - self.width:
			self.direction = (360 - self.direction) % 360
			self.x = self.screenwidth - self.width - 1

		# Did we fall off the bottom edge of the screen?
		if self.y > 600:
			return True
		else:
			return False

class Player(pygame.sprite.Sprite):
	""" This class represents the bar at the bottom that the
	player controls. """

	def __init__(self):
		""" Constructor for Player. """
		# Call the parent's constructor
		super().__init__()

		self.width = 100
		self.height = 10


		self.image = pygame.Surface([self.width, self.height])
		self.image.fill((white))

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.screenheight = pygame.display.get_surface().get_height()
		self.screenwidth = pygame.display.get_surface().get_width()

		self.rect.x = 0
		self.rect.y = self.screenheight - self.height - 10

	def update(self):
		""" Update the player position. """
		# Get where the mouse is
		pos = pygame.mouse.get_pos()
		# Set the left side of the player bar to the mouse position
		self.rect.x = pos[0]
		# Make sure we don't push the player paddle
		# off the right side of the screen
		if self.rect.x > self.screenwidth - self.width:
			self.rect.x = self.screenwidth - self.width



def level(num):
	top = 80
	blockcount = 32
	ready = False

	if(num < 5):
		curr_time = pygame.time.get_ticks()

		while not ready:
			screen.fill(black)
			text = font.render("Level " + str(num), True, white)
			screen.blit(text, [350, 290])
			pygame.display.flip()

			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					ready = True

		if(pygame.time.get_ticks() == curr_time + 10):
			print('test')
			ready = True

		#Game isnt over
		for row in range(num + 2):
			# 32 columns of blocks
			for column in range(0, blockcount):
				# Create a block (color,x,y)
				block = Block(blue, column * (block_width + 2) + 1, top)
				blocks.add(block)
				allsprites.add(block)
			# Move the top of the next row down
			top += block_height + 2
		return False
	else:
		#They won the game
		return True

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Boarder Breaker')

# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# Create the player paddle object
player = Player()
allsprites.add(player)

# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)

# The top of the block (y position)
# top = 80

# Number of blocks to create
#blockcount = 32

# --- Create blocks

# Game Level
game_level = 1


# Clock to limit speed
clock = pygame.time.Clock()

# Is the game over?
game_over = False

#Is game finished?
finished_game = False

# Exit the program?
exit_program = False

# Define some colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Starting position of the rectangle
rect_x = 50
rect_y = 50

# Speed and direction of rectangle
rect_change_x = 5
rect_change_y = 5

display_instructions = True
instruction_page = 1

# -------- Instruction Page Loop -----------
while display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            display_instructions = False
            exit_program = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            instruction_page += 1
            if instruction_page > 2:
                display_instructions = False

    # Set the screen background
    screen.fill(RED)

    if instruction_page == 1:
        # Draw instructions, page 1
        # This could also load an image created in another program.
        # That could be both easier and more flexible.
        font = pygame.font.SysFont("Times New Roman", 72)
        text = font.render("Welcome to Boarder Breaker!", True, white)
        text_rect = text.get_rect(center=(800 / 2, 600 / 2))
        screen.blit(text, text_rect)
        # screen.blit(text, [10, 10])

    if instruction_page == 2:
        # Draw instructions, page 2
        font = pygame.font.SysFont("Times New Roman", 72)
        text = font.render("Pick your flag!", True, white)
        screen.blit(text, [240, 10])
        image = pygame.image.load('syria2.png')
        image = pygame.transform.scale(image, (200, 200))
        screen.blit(image, (70, 70))
        image2 = pygame.image.load('nigeria2.png')
        image2 = pygame.transform.scale(image2, (200, 200))
        screen.blit(image2, (310, 70))
        image3 = pygame.image.load('turkey2.png')
        image3 = pygame.transform.scale(image3, (200, 200))
        screen.blit(image3, (550, 70))
        image4 = pygame.image.load('usa2.png')
        image4 = pygame.transform.scale(image4, (200, 200))
        screen.blit(image4, (430, 300))
        image5 = pygame.image.load('saudi2.png')
        image5 = pygame.transform.scale(image5, (200, 200))
        screen.blit(image5, (190, 300))

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

level(game_level)
# Main program loop
while not exit_program:

	# Limit to 30 fps
	clock.tick(30)
	# Clear the screen
	screen.fill(black)

	# Process the events in the game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit_program = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				print('Pressed ' + str(pygame.K_r))
				for block in blocks.sprites():
					block.kill()

	# Update the ball and player position as long
	# as the game is not over.
	if not game_over:
		# Update the player and ball positions
		player.update()
		game_over = ball.update()

	# If we are done, print game over
	if game_over:
		text = font.render("Game Over", True, white)
		textpos = text.get_rect(centerx=background.get_width() / 2)
		textpos.top = 300
		screen.blit(text, textpos)

	# See if the ball hits the player paddle
	if pygame.sprite.spritecollide(player, balls, False):
		# The 'diff' lets you try to bounce the ball left or right
		# depending where on the paddle you hit it
		diff = (player.rect.x + player.width / 2) - (ball.rect.x + ball.width / 2)

		# Set the ball's y position in case
		# we hit the ball on the edge of the paddle
		ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
		ball.bounce(diff)

	# Check for collisions between the ball and the blocks
	deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

	# If we actually hit a block, bounce the ball
	if len(deadblocks) > 0:
		ball.bounce(0)

		# Game ends if all the blocks are gone
	if len(blocks) == 0:
		game_level += 1
		finished_game = level(game_level)
		#game_over =
	#  True

	if finished_game:
		game_over = True
		print('Finished Game')

	# Draw Everything
	allsprites.draw(screen)

	# Flip the screen and show what we've drawn
	pygame.display.flip()

pygame.quit()