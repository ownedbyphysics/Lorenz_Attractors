import pygame
import random

class Lorentz_equations:
    def __init__(self):
        self.xmin, self.xmax = -30, 30
        self.ymin, self.ymax = -30, 30
        self.zmin, self.zmax =  0, 20
        self.X, self.Y, self.Z = 0.1, 0.0, 0.0
        self.ghostX, self.ghostY, self.ghostZ = self.X, self.Y, self.Z
        self.dt = 0.00001
        self.sigma, self.ro, self.beta = 10, 28, 8/3
        self.pixelwidth = 1
        
    def loop(self):
        self.ghostX, self.ghostY, self.ghostZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.sigma * (self.Y - self.X))
        self.Y = self.Y + (self.dt * (self.X * (self.ro - self.Z) - self.Y))
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.beta * self.Z))
        
    def draw(self, displaySurface):
        width, height = displaySurface.get_size()
        
        before = self.show(self.ghostX, self.ghostY,
                                      self.xmin, self.xmax,
                                      self.ymin, self.ymax,
                                      width, height)
        
        after = self.show(self.X, self.Y,
                                      self.xmin, self.xmax,
                                      self.ymin, self.ymax,
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
        self.canvasDimension = self.width, self.height = 1400, 800
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
        colour.append((50, 130, 200))
        colour.append((255, 130, 0))
        colour.append((255, 200, 0))
        
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
        
        
        
        
        
        
        
        
        
        
        