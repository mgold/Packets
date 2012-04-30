import pygame, sys
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
        self.color = (0, 192, 0) #Change if you like
        self.num_chars_per_line = 35
        self.offset = 15 #Increment the y value to print a new line of text

        #Store contents of text file in 'message'
        self.message = ""
        for name in filename, "virus/"+filename:
            try:
                with open(name, 'r') as f:
                    self.message = f.read()
                break
            except Exception:
                pass

        self.current = 0 #Keeps track of which char we're on for slicing
        
        self.max_time_to_next_char = 3
        self.time_to_next_char = self.max_time_to_next_char #Spaces out printing of chars one by one
        
        #print self.message
        
    def update(self):
        if self.time_to_next_char == 0:
            self.current += 1
            self.time_to_next_char = self.max_time_to_next_char
            #print "Current = " + str(self.current)
        else:
            self.time_to_next_char -= 1

    def draw(self):
		if self.current > self.num_chars_per_line:
			num_lines = self.current / self.num_chars_per_line # Calculate number of lines that will be needed to print the message
			if self.current % self.num_chars_per_line > 0:
				num_lines += 1
			for line in range(num_lines): # Iterate through that number of lines
				for char in range(self.num_chars_per_line):
					to_print = self.font.render(str(self.message[(line*self.num_chars_per_line):(line*self.num_chars_per_line + char)]), True, self.color) # For each line, print the right segment of the message
					self.screen.blit(to_print, (self.x,self.y+(self.offset*line))) # At y+(line # * 5) or whatever increment
		else:
			to_print = self.font.render(str(self.message[:self.current]), True, self.color) #Take what we have of the message so far...
			self.screen.blit(to_print, (self.x,self.y)) #...and blit it to the screen

#Testing module
if __name__ == "__main__":
    main()

def main():

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
    some_text = Text(screen, 10, 10, "message.txt")

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
