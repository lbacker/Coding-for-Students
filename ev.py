import pygame
import random
import math

size = 70 # boxes per side of grid (change number of boxes in the simulation)
pixels = 9 # pixels per side of box (change how big the boxes are)

genes = ['p']
dict = {'blue': 0.85, 'green': 0.5, 'red': 0.15, 'water': 0.99, 'leaf': 0.5, 'fire': 0.01}
randomness, cooperation, start, winner, health, mem = 0.01, 0.3, 0.5, 0.5, 10, 0.5

# User input questions
simulation = raw_input('Which simulation would you like to run? (options = normal/tumour/memorizer/pokemon): ')

if simulation == 'normal' or simulation == 'tumour':
    randomness = input('What fraction of evolution would you like to be random? (ex. 0.02 = 2 percent are random): ')
    cooperation = input('What fraction of cooperation would you like between cells? (ex. 0.0 = only fighting, 1.0 = only cooperation): ')
    start = raw_input('What would you like to be the dominant gene at the beginning? (options = blue/green/red): ')
    winner = raw_input('What would you like to be the dominant gene at the end? (options = blue/green/red): ')
elif simulation == 'pokemon':
    while(True):
        health = input('What is each Pokemons health? (10-100): ')

        if health < 10 or health > 100:
            print('Error! Health must be between 10 and 100')
            continue

        r_attack = input('What is fires attack power? (1-4): ')
        g_attack = input('What is leafs attack power? (1-4): ')
        b_attack = input('What is waters attack power? (1-4): ')

        if r_attack < 1 or r_attack > 4 or g_attack < 1 or g_attack > 4 or b_attack < 1 or b_attack > 4:
            print('Error! Attack power must be between 1 and 4')
            continue
        else:
            break
else:
    randomness = input('What fraction of evolution would you like to be random? (ex. 0.02 = 2 percent are random): ')
    cooperation = input('What fraction of cooperation would you like between cells? (ex. 0.0 = only fighting, 1.0 = only cooperation): ')
    start = raw_input('What would you like to be the dominant gene at the beginning? (options = blue/green/red): ')
    mem = raw_input("What colour would you like to memorize its last move? (blue/green/red/all): ")


# Normal simulation of evolution of cells
def normal(x, y):
    # returns your score
    # x = your move, y = the opponent
    # inputs are 'f' for Fight, 'c' for Cooperate

    if x == 'f': # you Fight
        if y == 'f': # they Fight
            return -1
        else: # they Cooperate
            return 2

    else: # you Cooperate
        if y == 'f':
            return -2
        else:
            return 1


# Simulation of cancerous cells invading healthy cells
def tumour(x, y):
    # returns your score
    # x = your move, y = the opponent
    # inputs are 'f' for Fight, 'c' for Cooperate, 'canc' for Cancer, 'anti' for Antibodies

    if x == 'f': # you Fight
        if y == 'f': # they Fight
            return -1
        elif y == 'c': # they Cooperate
            return 2
        elif y == 'canc':
            return -1
        else:
            return 1

    elif x == 'c': # you Cooperate
        if y == 'f':
            return -2
        elif y == 'c':
            return 1
        elif y == 'canc':
            return -3
        else:
            return 1
    elif x == 'canc':
        if y == 'f':
            return -1
        elif y == 'c':
            return 1
        elif y == 'canc':
            return 0
        else:
            return -3
    else:
        if y == 'f':
            return -1
        elif y == 'c':
            return 0
        elif y == 'canc':
            return -2           # Antibody strength
        elif y == 'anti_c':
            return 1
        else:
            return -1

# SImulation of Pokemon-like battle between cells
def pokemon(x, y, your_type, opp_type):
    if your_type == dict['fire']:
        if opp_type == dict['fire']:
            if x == 'f':
                if y == 'f':
                    return -r_attack
                else:
                    return r_attack
            else:
                if y == 'c':
                    return 1
                else:
                    return -r_attack
        elif opp_type == dict['leaf']:
            if x == 'f':
                if y == 'f':
                    return -0.5*g_attack
                else:
                    return 1.5*r_attack
            else:
                if y == 'c':
                    return 0
                else:
                    return -0.5*g_attack
        else:
            if x == 'f':
                if y == 'f':
                    return -1.5*b_attack
                else:
                    return 0.5*r_attack
            else:
                if y == 'c':
                    return 0
                else:
                    return -1.5*b_attack
    elif your_type == dict['leaf']:
        if opp_type == dict['fire']:
            if x == 'f':
                if y == 'f':
                    return -1.5*r_attack
                else:
                    return 0.5*g_attack
            else:
                if y == 'c':
                    return 0
                else:
                    return -1.5*r_attack
        elif opp_type == dict['leaf']:
            if x == 'f':
                if y == 'f':
                    return -g_attack
                else:
                    return g_attack
            else:
                if y == 'c':
                    return 1
                else:
                    return -g_attack
        else:
            if x == 'f':
                if y == 'f':
                    return -0.5*b_attack
                else:
                    return 1.5*g_attack
            else:
                if y == 'c':
                    return 0
                else:
                    return -0.5*b_attack
    else:       # Remove this line 
        return 0    # Remove this line
    """else: # Water type Pokemon
        if opp_type == dict['fire']:
            if x == 'f':
                if y == 'f':
                    return 
                else:
                    return 
            else:
                if y == 'c':
                    return 
                else:
                    return 
        elif opp_type == dict['leaf']:
            if x == 'f':
                if y == 'f':
                    return 
                else:
                    return 
            else:
                if y == 'c':
                    return 
                else:
                    return 
        else:
            if x == 'f':
                if y == 'f':
                    return 
                else:
                    return 
            else:
                if y == 'c':
                    return 
                else:
                    return """


# If a cell dies, breed a new one based on the simulation chosen
def breed(self, a, b):
    r = random.random()

    if self.sim == 'tumour':
        if (a == 0 and b == 1) or (a == 1 and b == 0):
            if (r < 0.5):
                return 0
            else:
                return 1

        elif a == 0:
            if (r < 0.49):
                return max(a, b)
            elif (r < (1.0 - self.rand)):
                return min(a, b)
            else:
                return 1

        else:
            if (r < (0.9999 - 0.02 - self.rand) * (1.0/3.0)):   # Strength - there is a 2% chance (0.02) that the cells will breed the dominant gene
                return (a + b) / 2
            elif (r < (0.9999 - 0.02 - self.rand) * (2.0/3.0)):
                return max(a, b)
            elif (r < (0.9999 - 0.02 - self.rand)):
                return min(a, b)
            elif (r < (0.9999 - self.rand)):
                return dict[winner]
            elif (r < 0.9999):
                return random.random()
            else:
                return 0

    elif self.sim == 'normal':
        if (r < (1.0 - 0.02 - self.rand) * (1.0/3.0)): 
            return (a + b) / 2
        elif (r < (1.0 - 0.02 - self.rand) * (2.0/3.0)):
            return max(a, b)
        elif (r < (1.0 - 0.02 - self.rand)):
            return min(a, b)
        elif (r < (1.0 - self.rand)):
            return dict[winner]
        else:
            return random.random()

    elif self.sim == 'memorizer':
        if (r < (1.0 - self.rand) * (1.0/3.0)): 
            return (a + b) / 2
        elif (r < (1.0 - self.rand) * (2.0/3.0)):
            return max(a, b)
        elif (r < (1.0 - self.rand)):
            return min(a, b)
        else:
            return random.random()

    else:
        return a

class Agent:

    # The cell chooses what it wants to do - 'f' or 'c', or 'canc' or 'anti_c' or 'anti_f' for tumour simulation
    def choice(self, opp):
        if self.sim == 'tumour':
            if self.g['p'] == 0:
                ch = 'canc'

            elif self.g['p'] == 1:
                r = random.random()
                if(r < 0.5):            # Ratio of cooperative antibodies to fighting antibodies
                    ch = 'anti_c'
                else:
                    ch = 'anti_f'

            elif random.random() < self.coop:
                ch = 'c'
            else:
                ch = 'f'

        elif self.sim == 'normal':
            if random.random() < self.coop:
                ch = 'c'
            else:
                ch = 'f'

        elif self.sim == 'pokemon':
            if random.random() < 0.5:
                ch = 'c'
            else:
                ch = 'f'

        # Memorizer Simulator
        else:
            if mem == 'red':
                if 0 < self.g['p'] <= 0.33:
                    A = opp.uniqueId

                    # If first time for this opponent:
                    if(A not in self.prevOutcome):
                        self.prevOutcome[A] = random.choice([-2,-1,1,2])
                        self.prevChoice[A] = random.choice(['f','c'])

                    # Won last time
                    if self.prevOutcome[A] > 0:
                        if random.random() < self.g['p']:
                            ch = self.prevChoice[A]
                        else:
                            ch = flip(self.prevChoice[A])

                    # Lost last time
                    else:
                        if random.random() < self.g['p']:
                            ch = self.prevChoice[A]
                        else:
                            ch = flip(self.prevChoice[A])

                    self.prevChoice[A] = ch
                else:
                    if random.random() < self.coop:
                        ch = 'c'
                    else:
                        ch = 'f'
            elif mem == 'green':
                if 0.33 < self.g['p'] <= 0.66:
                    A = opp.uniqueId

                    if(A not in self.prevOutcome):
                        self.prevOutcome[A] = random.choice([-2,-1,1,2])
                        self.prevChoice[A] = random.choice(['f','c'])

                    if self.prevOutcome[A] > 0:
                        if random.random() < self.g['p']:
                            ch = self.prevChoice[A]
                        else:
                            ch = flip(self.prevChoice[A])

                    else:
                        if random.random() < self.g['p']:
                            ch = self.prevChoice[A]
                        else:
                            ch = flip(self.prevChoice[A])

                    self.prevChoice[A] = ch
                else:
                    if random.random() < self.coop:
                        ch = 'c'
                    else:
                        ch = 'f'
            elif mem == 'blue':
                if 0.66 < self.g['p'] < 1:
                    A = opp.uniqueId

                    if(A not in self.prevOutcome):
                        self.prevOutcome[A] = random.choice([-2,-1,1,2])
                        self.prevChoice[A] = random.choice(['f','c'])

                    if self.prevOutcome[A] > 0:
                        if random.random() < self.g['p']:
                            ch = self.prevChoice[A]
                        else:
                            ch = flip(self.prevChoice[A])

                    else:
                        if random.random() < self.g['p']:
                            ch = self.prevChoice[A]
                        else:
                            ch = flip(self.prevChoice[A])

                    self.prevChoice[A] = ch
                else:
                    if random.random() < self.coop:
                        ch = 'c'
                    else:
                        ch = 'f'
            else:
                A = opp.uniqueId

                if(A not in self.prevOutcome):
                    self.prevOutcome[A] = random.choice([-2,-1,1,2])
                    self.prevChoice[A] = random.choice(['f','c'])

                if self.prevOutcome[A] > 0:
                    if random.random() < self.g['p']:
                        ch = self.prevChoice[A]
                    else:
                        ch = flip(self.prevChoice[A])

                else:
                    if random.random() < self.g['p']:
                        ch = self.prevChoice[A]
                    else:
                        ch = flip(self.prevChoice[A])

                self.prevChoice[A] = ch

        return ch

    # Select opponent
    def opponent(self):
        i = bound(self.i + random.choice([-1,0,1]))
        j = bound(self.j + random.choice([-1,0,1]))
        if i==self.i and j==self.j: # cannot fight self
            return self.opponent() # try again
        else:
            return sim[i][j]

    def battle(self, a):
        ch = self.choice(a)
        ach = a.choice(self)

        if self.sim == 'tumour':
            s = tumour(ch, ach)
            self.score += s
            sa = tumour(ach, ch)
            a.score += sa
        
        elif self.sim == 'normal' or self.sim == 'memorizer':
            s = normal(ch, ach)
            self.score += s
            self.prevOutcome[a.uniqueId] = s
            sa = normal(ach, ch)
            a.score += sa
            a.prevOutcome[self.uniqueId] = sa

        else:
            s = pokemon(ch, ach, self.g['p'], a.g['p'])
            self.score += s
            sa = pokemon(ach, ch, a.g['p'], self.g['p'])
            a.score += sa

    def update(self):
        a = self.opponent()
        self.battle(a)

        if self.score <= 0:
            if self.sim == 'pokemon':
                self.score = health
            else:
                self.score = 10
            self.prevChoice = {}
            self.prevOutcome = {}
            self.g['p'] = breed(self, a.g['p'], self.g['p'])
            if self.g['p'] == 1:
                self.score += 1
            elif self.g['p'] == 0:
                self.score -= 2
            self.draw()


    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.uniqueId = len(seq)
        self.prevChoice = {}
        self.prevOutcome = {}
        self.g = {}
        self.sim = simulation
        self.rand = randomness
        self.coop = cooperation
        if self.sim != 'pokemon':
            self.g['p'] = random.triangular(0, 1, dict[start])
            self.score = 10
        else:
            self.g['p'] = random.choice([dict['fire'], dict['leaf'], dict['water']])
            self.score = health
        self.draw()

    def draw(self):
        x = base + self.i * pixels
        y = base + self.j * pixels
        boxes.append([shift(x,y,'p'), color(self.g['p'])])

def flip(ch):
    if ch=='f':
        return 'c'
    else:
        return 'f'

def bound(x):
    return max(0, min(size-1, x))

def color(x):
    z = pygame.Color(0,0,0,0)
    if x == 0:
        z.hsva = [0, 0, 0, 0]
    elif x == 1:
        z.hsva = [0, 0, 100, 0]
    else:
        z.hsva = [x*250, 95, 95, 0]
    return z

def draw():
    global boxes
    rlist = []
    for b in boxes:
        R = pygame.Rect(b[0], (pixels, pixels))
        pygame.draw.rect(screen, b[1], R, 0)
        rlist.append(R)
    boxes = []
    pygame.display.update(rlist)

def shift(x, y, g):
    if g=='p':
        return (x,y)


# initialize graphics window:
pygame.init()
base = 20
nPix = int(base*2+math.ceil(pixels*size))
screen = pygame.display.set_mode([nPix, nPix])
pygame.display.set_caption("Agent-Based Evolution")
white = [255, 255, 255]
black = [0, 0, 0]
screen.fill(white)
pygame.display.flip()
font = pygame.font.Font(None, 25)

# initialize agents:
boxes = [] # only used in 'draw': tracks changed genes
seq = [] # one-dimensional list, permuted each turn
sim = [] # fixed two-dimensional grid for 'opponent' lookup
for i in range(0,size):
    row = []
    sim.append(row)
    for j in range(0,size):
        A = Agent(i, j)
        row.append(A) # sim[i][j]
        seq.append(A)
draw()

# main animation loop:
done = False
clock = pygame.time.Clock()
while done==False:
    clock.tick(120) # max frames per second (speed up or slow down simulation)
    time = pygame.time.get_ticks() / 1000.0
    print(time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    random.shuffle(seq)
    for a in seq:
        a.update()
    draw()
pygame.quit()

# print summary statistics:
avg = {}
avg['p'] = 0
for a in seq:
    avg['p'] += a.g['p']
N = len(seq)
print('p'+"="+str(round(100*avg['p']/N)/100))