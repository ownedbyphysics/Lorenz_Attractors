import pygame
import random

initials_dictionary = { 'sizeX' : 20,
                     'sizeY' : 20,
                     'sizeZ' : 50,
                     'X' : 0.1,
                     'Y' : 0,
                     'Z' : 0
                    }

class Lorentz_equations:
    def __init__(self):
        self.xmin, self.xmax = -initials_dictionary['sizeX'], initials_dictionary['sizeX']
        self.ymin, self.ymax = -initials_dictionary['sizeY'], initials_dictionary['sizeY']
        self.zmin, self.zmax = -initials_dictionary['sizeZ']+30, initials_dictionary['sizeZ']
        self.X, self.Y, self.Z = initials_dictionary['X'], initials_dictionary['Y'], initials_dictionary['Z']
        self.ghostX, self.ghostY, self.ghostZ = self.X, self.Y, self.Z
        self.dt = 0.0005
        self.sigma = 10 
        self.ro = 28 
        self.beta = 3
        self.pixelwidth = 1
        
    def loop(self):
        self.ghostX, self.ghostY, self.ghostZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.sigma * (self.Y - self.X))
        self.Y = self.Y + (self.dt * (self.X * (self.ro - self.Z) - self.Y))
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.beta * self.Z))
        
    def draw(self, displaySurface):
        width, height = displaySurface.get_size()
        
        before = self.show(self.ghostX, self.ghostZ,
                                      self.xmin, self.xmax,
                                      self.zmin, self.zmax,
                                      width, height)
        
        after = self.show(self.X, self.Z,
                                      self.xmin, self.xmax,
                                      self.zmin, self.zmax,
                                      width, height)
        
        updateGraph = pygame.draw.line(displaySurface, 
                                   self.pixelColour, 
                                   before, 
                                   after,
                                   self.pixelwidth
                                   )
        
        return updateGraph
             
    def show(self, x, y, xmin, xmax, ymin, ymax, width, height):
        updateX = width * ((x-xmin) / (xmax-xmin))
        updateY = height * ((y-ymin) / (ymax-ymin))
        return round(updateX), round(updateY)
    

class Attractors_app:
    def __init__(self):
        self.RUNNING = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        self.canvasDimension = self.width, self.height = 1200, 800
        self.count = 0
        self.outputCount = 1
        self.file = 'Michael Nyman - The heart asks for pleasure first.mp3'
        
    def on_init(self):
        pygame.init()
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.play(-1)
        self.displaySurface = pygame.display.set_mode(self.canvasDimension)
        self.RUNNING = True
        self.fpsClock = pygame.time.Clock()
        
        colour = []
        colour.append((255,215,0))
        colour.append((255,64,64))
        colour.append((0,178,238))
    
        for trajectory in range(0,3):
            self.attractors.append(Lorentz_equations())
            self.attractors[trajectory].X = random.uniform(0.0, 0.01)
            self.attractors[trajectory].pixelColour = colour[trajectory]
             
        pygame.display.set_caption("My {} Lorenz Attractors in 2D display".
                                   format(len(self.attractors)))
            
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.RUNNING = False
            
    def on_loop(self):
        for attractor in self.attractors:
            attractor.loop()
        
    def on_render(self):
        for attractor in self.attractors:
            updateGraph = attractor.draw(self.displaySurface)
            pygame.display.update(updateGraph)
        
    def startMe(self):
        if self.on_init() == False:
            self.RUNNING = False
            
        while self.RUNNING:
            for event in pygame.event.get():
                self.on_event(event)
                
            self.on_loop()
            self.on_render()
            
            self.fpsClock.tick()
            self.count += 1
            
        pygame.quit()
        
        
if __name__ == "__main__":
    app = Attractors_app()
    app.startMe()
        
