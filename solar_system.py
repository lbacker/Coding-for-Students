import turtle           # Imports library that allows user to alter a turtle. A turtle is something that has a position and a direction, and can draw lines
from turtle import *    # Imports functions from the turtle library that allow user to alter the turtle
from Tkinter import *   # Imports functions from the Tkinter library that allow user to create a Graphical User Interface (GUI)
from math import *      # Imports functions from the math library that allows user to use math functions (ex. sine, cosine, square root)

G = 6.67428e-11         # The gravitational constant G

AU = 149.6e9            # AU = Astronomical Unit = distance from earth to the sun = 149.6 million km, in meters.
SCALE = 75.0 / AU       # Scale 1 AU to 30 pixels

class planet(Turtle):   # This function defines the parameters for each planets
    
    name = 'planet'     # Initialize name of the planet as planet
    mass = None         # Initialize mass of the planet as nothing
    vx = vy = 0.0       # Initialize velocity of the planet as 0 metres per second
    xloc = yloc = 0.0   # Initialize location of the planet as 0 metres
    

    def attraction(self, other):        # This function calculates the gravitational forces between the planets

        rx = (other.xloc-self.xloc)                     # Compute the x distance of the other planet in metres
        ry = (other.yloc-self.yloc)                     # Compute the y distance of the other planet in metres
        r = sqrt(rx**2 + ry**2)                         # Compute the hypotenuse 

        if r == 0:                                                      # Conditional statement for if there is a collision between planets
            raise ValueError("Collision between objects %r and %r"      # Raise the error statement, "Collision between planet 1 and and planet 2"
                             % (self.name, other.name))

        f = G * self.mass * other.mass / (r**2)          # Compute the force of attraction between two planets

        theta = atan2(ry, rx)           # Find the angle between the hypotenuse and the adjacent side
        fx = cos(theta) * f             # Compute the x component of the force on the planet in Newtons
        fy = sin(theta) * f             # Compute the y component of the force on the planet in Newtons
        
        return fx, fy                   # Return the x and y components of the force to the main loop

def loop(bodies):                       # This function calculates the orbit of each planet and displays it in a window
    
    timestep = 1*24*3600                # One earth day (in seconds)
    date = 0                            # Starting date for the simulation - date increases for every iteration of the loop
    
    for planet in bodies:                                 # Runs a loop for each planet
        planet.goto(planet.xloc*SCALE, planet.yloc*SCALE)     # Puts the planet in its proper location on the display
        planet.pendown()                                  # Puts down the pen - this means that a line will be draw to show the path of the orbit  
    
    while True:                         # Loop will run until user interrupts program (ctrl+c)
        force = {}                      # Create a dictionary that holds the total forces on each planet                   
        for planet in bodies:

            total_fx = total_fy = 0.0   # Initialize the x and y components on the planet as 0

            for other in bodies:                        # This loop adds up all of the forces exerted on each planet
                if planet is other:                     # Don't calculate the planet's attraction to itself
                    continue                            # Skip to the next planet
                fx, fy = planet.attraction(other)       # Goes to the function called attraction (line 19)
                total_fx += fx                          # Sums up the x components of the gravitational forces on the planet
                total_fy += fy                          # Sums up the y components of the gravitational forces on the planet

            force[planet] = (total_fx, total_fy)        # Assign the total force exerted on the planet to the dictionary, force

        for planet in bodies:                                       # Update positions and velocities based on the force
            fx, fy = force[planet]                                  # Assign the components of the total force to the variables fx and fy

            planet.vx += fx / planet.mass * timestep                # Calculate the new x component of the velocity
            planet.vy += fy / planet.mass * timestep                # Calculate the new y component of the velocity

            planet.xloc += planet.vx * timestep                     # Calculate the new x component of the position
            planet.yloc += planet.vy * timestep                     # Calculate the new y component of the position
            planet.goto(planet.xloc*SCALE, planet.yloc*SCALE)       # Tell the turtle to go to the new position on the display
        
        date += 1                       # After updating the positions and velocities of the planet, go to the next day   
        
        turtle.clear()                                              # Restart the position of the turtle
        turtle.penup()                                              # Pick up the turtle to make sure it does not draw a line when you move it
        turtle.hideturtle()                                         # Hide the turtle when you move it
        turtle.goto(300, 300)                                       # Move turtle to the top right corner
        turtle.write(str(date) + " Days",False, align="right",      # Writes the number of days that have passed since the start of the simulation
                        font=("Arial", 18, "normal"))

def main():                             # Sets up the positions, velocities, colours, and shapes of the planets on the display

    # Planets start at average distance from sun, with mean speed
    # Start in locations for January 26th
    
    turtle.setup(800, 800)          # Set the window size to 800 by 800 pixels
    turtle.bgcolor("white")         # Set up the window with a white background

    """
    For each planet, the setup follows the same procedure:
    planet = planet()               Sets up the variables for the planet, goes to the function called planet (line 11)
    planet.name = 'planet name'     Names the planet
    planet.mass = number            Gives the planet a mass
    planet.penup()                  Picks up the turtle so it does not draw a line when you move it
    planet.color('colour')          Gives the planet a colour (ex. yellow)
    planet.shape('shape')           Gives the planet a shape (ex. circle)
    planet.xloc = number            Gives the planet an x component position in metres
    planet.yloc = number            Gives the planet a y component position in metres
    planet.vx = number              Gives the planet an x component velocity in metres per second
    planet.vy = number              Gives the planet a y component velocity in metres per second
    """

    sun = planet()
    sun.name = 'Sun'
    sun.mass = 1.98892 * 10**30
    sun.penup() 
    sun.color('yellow')
    sun.shape('circle')
    sun.shapesize(2.0,2.0,1)
       
    earth = planet()
    earth.name = 'Earth'
    earth.mass = 5.97 * 10**24
    earth.penup() 
    earth.color('green')
    earth.shape('circle')
    earth.shapesize(0.6,0.6,1)
    earth.yloc = (1 * AU) * 0.80696031214
    earth.xloc = (1 * AU) * -0.59060566762
    earth.vy = 29.8 * 1000 * -0.59060566762          
    earth.vx = 29.8 * 1000 * -0.80696031214   
    
    mars = planet()
    mars.name = 'Mars'
    mars.mass = 6.3 * 10**24
    mars.penup() 
    mars.color('red')
    mars.shape('circle')
    mars.shapesize(0.5,0.5,1)
    mars.xloc = (1.524 * AU) * 0.85391432258
    mars.yloc = (1.524 * AU) * 0.52041361405
    mars.vy = 24.1 * 1000 * 0.85391432258 
    mars.vx = 24.1 * 1000 * -0.52041361405

    mercury = planet()
    mercury.name = 'Mercury'
    mercury.mass = 3.285 * 10**23
    mercury.penup() 
    mercury.color('black')
    mercury.shape('circle')
    mercury.shapesize(0.3,0.3,1)
    mercury.xloc = (0.39 * AU) * -0.74547599968
    mercury.yloc = (0.39 * AU) * -0.66653247024
    mercury.vy = 47.36 * 1000 * -0.74547599968 
    mercury.vx = 47.36 * 1000 * 0.66653247024

    """
    alien = planet()
    alien.name = 'Bob'
    alien.penup()
    alien.color('pink')
    alien.shape('turtle')
    alien.shapesize(3.0,3.0,1)
    alien.xloc = (5.8 * AU) * 0.97480014384
    alien.yloc = (2.0 * AU)
    """

    loop([sun, mercury, earth, mars])       # Goes to the function called loop (line 37). Takes these planets and creates a solar system.

    
if __name__ == '__main__':          # The code starts here
    main()                          # Goes to the function called main (line 80)
