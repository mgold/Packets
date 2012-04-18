import pygame
from pygame.locals import *
from core.Device import Device

class Text(Device):
    """
    Text - Virus

    Displays text. Not really a device, just a subclass of it to make things
    easier. 
    """
    def __init__ (self, screen, x, y, filename):
		self.screen = screen
		self.x = x
		self.y = y

		self.font = pygame.font.SysFont(u'couriernew,courier', 18, bold=True)
		self.color = (0, 128, 255) #Change if you like

		#Store contents of text file in 'message'
		with open(filename, 'r') as f:
			self.message = f.read()

		self.current = 0 #Keeps track of which char we're on for slicing
		
		self.time_to_next_char = 0 #Spaces out printing of chars one by one
		self.max_time_to_next_char = 5
		
    def update(self):
		if self.time_to_next_char == 0:
			self.current += 1
			self.time_to_next_char = self.max_time_to_next_char
		else:
			self.time_to_next_char -= 1

    def draw(self):
    	to_print = self.message[:self.current] #Take what we have of the message so far...
        self.screen.blit(to_print, (self.x,self.y)) #...and blit it to the screen


#Testing module
if __name__ == "__main__":
		
	#Define Variables
	FPS = 50
	SCREEN_WIDTH, SCREEN_HEIGHT = 800,600
	BG_COLOR = (0,0,0)

	#Initialize Pygame, screen, and clock
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0,32)
	pygame.display.set_caption('Text Test')
	clock = pygame.time.Clock()

	#Initialize Text instance
	some_text = Text(screen, 10, 10, "nessage.txt")

	#Main Loop
	while True:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

		#Refill the screen
		screen.fill(BG_COLOR)

		#Update and draw
		some_text.update()
		some_text.draw()

        #Advance the frame
        pygame.display.flip()