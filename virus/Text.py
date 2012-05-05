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
        self.offset = 15 #Increment the y value to print a new line of text

        #Store contents of text file in 'message'
        self.message = [] #List of strings (lines of the message)
        for name in filename, "virus/"+filename:
            try:
                self.message = [line.strip() for line in open('filename')]
                break
            except Exception:
                pass

        self.current_char = 0 #Keeps track of which char we're on for slicing
        self.current_line = 0 #Keeps track of which line in the message we're on (index for the list)
        
        self.max_time_to_next_char = 3
        self.time_to_next_char = self.max_time_to_next_char #Spaces out printing of chars one by one
        
        print self.message
        
    def update(self):
        if self.time_to_next_char == 0:
            if self.current_char > len(self.message[self.current_line]): #If we've gotten to the end of this line
                self.current_line += 1 #Move onto the next line and start working on that one
                self.current_char = 0 #Reset to the first char of the next line
            else:
                self.current_char += 1
            self.time_to_next_char = self.max_time_to_next_char

        else:
            self.time_to_next_char -= 1

    def draw(self):
        line = 0
        #Print all previously printed lines
        while line < self.current_line:
            to_print = self.font.render(str(self.message[line]), True, self.color)
            y = self.offset + self.offset*line
            self.print_message(to_print, y)
            line += 1
        #Then print the next char on the current line
        to_print = str(self.message[self.current_line])
        to_print = self.font.render(str(to_print[:self.current_char]), True, self.color)
        y = self.offset + self.offset*self.current_line
        self.print_message(to_print, y)
    
    def print_message(self, to_print, y):
        self.screen.blit(to_print, (self.x,y))

        
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
