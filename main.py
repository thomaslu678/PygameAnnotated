import pygame



class Game:
    screen = None
    aliens = []
    rockets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        self.width = width #width
        self.height = height #height
        self.screen = pygame.display.set_mode((width, height)) #create the screen using pygame.display
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock() #a clock
        done = False #the default done value is False

        hero = Hero(self, width / 2, height - 20) #Create a hero from the hero function, with centered x, lower y
        generator = Generator(self) #Run the generator function to generate aliens
        rocket = None #No rockets yet

        while not done: #while the game is not done
            if len(self.aliens) == 0: #if the created aliens 'array' has no one left, display the text victory achieved
                self.displayText("VICTORY ACHIEVED")

            pressed = pygame.key.get_pressed() #Defining the press function using pygame pressed method
            if pressed[pygame.K_LEFT]:
                hero.x -= 5 if hero.x > 20 else 0  #move the x value left if not at the left border
            if pressed[pygame.K_RIGHT]:
                hero.x += 5 if hero.x < width - 20 else 0 #move the x value right if not the right border


            for event in pygame.event.get():
                if event.type == pygame.QUIT: #if the event is the pygame QUIT
                    done = True #then set done = True, ending this whole while loop
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                #if the event is a key pressed down and the key is the space bar and condition lost is not true:
                    self.rockets.append(Rocket(self, hero.x, hero.y)) #add a rocket using the defined function

            pygame.display.flip() #constantly updating the screen
            self.clock.tick(60) #sets framerate / game speed
            self.screen.fill((0, 0, 0)) #after creating everything, now fill the background

            for alien in self.aliens: #check every alien
                alien.draw() #draw the alien
                alien.checkRocketCollision(self) #check for collisions (defined function in alien class)

                if (alien.y > height): #if the alien's y is greater than the window's height
                    self.lost = True #set lost to true
                    self.displayText("YOU DIED") #you have died

            for rocket in self.rockets: #for each rocket (that was appended earlier)
                rocket.draw() #draw using the rocket function

            if not self.lost: hero.draw() #if you haven't lost, draw the hero
            #disappears if lost

    def displayText(self, text):
        pygame.font.init() #initialize pygame fonts
        font = pygame.font.SysFont('Arial', 50) #using arial with font size 50
        textsurface = font.render(text, False, (44, 0, 62)) #rendering the text
        self.screen.blit(textsurface, (110, 160)) #using blit to add the text onto screen


class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 30

    def draw(self):
        pygame.draw.rect(self.game.screen, #rendering screen
                         (53, 48, 88), #color of the aliens
                         pygame.Rect(self.x, self.y, self.size, self.size)) #location and size of rect
        self.y += 0.5

    def checkRocketCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + self.size and      #if rocket x is between alien's dimensions
                    rocket.x > self.x - self.size and
                    rocket.y < self.y + self.size and #if rocket y is between alien's dimensions
                    rocket.y > self.y - self.size):
                game.rockets.remove(rocket) #remove the rocket
                game.aliens.remove(self) #remove the alien


class Hero: #code to create a hero
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (210, 250, 251),
                         pygame.Rect(self.x, self.y, 8, 5))


class Generator:
    def __init__(self, game):
        margin = 30  #space from the edge of the screen
        width = 50  #gap between aliens, for each for loop, with 50 between each x value
        for x in range(margin, game.width - margin, width): #across the width of the screen, with 50 margin
            for y in range(-400, int(game.height / 2), width): #across top to halfway screen
                game.aliens.append(Alien(game, x, y)) #add aliens with those x and y values

        #game.aliens.append(Alien(game, 280, 50))


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,  #rendering area
                         (254, 52, 110),  #color of object
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 5  # rocket goes up 2 y value every frame

game = Game(600, 400)