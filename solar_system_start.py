import turtle           # Imports library that allows user to alter a turtle. A turtle is something that has a position and a direction, and can draw lines
from turtle import *    # Imports functions from the turtle library that allow user to alter the turtle
from tkinter import *   # Imports functions from the Tkinter library that allow user to create a Graphical User Interface (GUI)
from math import *      # Imports functions from the math library that allows user to use math functions (ex. sine, cosine, square root)

# Global constant definitions 
G = 6.67428e-11         # The gravitational constant G

AU = 149.6e9            # AU = Astronomical Unit = distance from earth to the sun = 149.6 million km, in meters.
SCALE = 75.0 / AU       # Scale 1 AU to 30 pixels

# Class definitions: planet
class planet(Turtle):   # This function defines the parameters for each planets

    # Initialize planet name, location, velocity        
    vx = vy = 0.0       
    xloc = yloc = 0.0  
    
    # Compute the attraction between planet and other body
    def attraction(self, other, date):        

        # Compute x, y, and total distances between planet and other body
        rx = (other.xloc-self.xloc)                     
        ry = (other.yloc-self.yloc)                    
        r = sqrt(rx**2 + ry**2)                        

        # Test if there is a collision between planets, handle the error!
        if r < self.diameter and other.name != 'MarsRover':   
            raise ValueError("Collision between objects %r and %r"      
                             % (self.name, other.name))

        ##############
        # Add in function that handles the spacecraft landing case and returns fx, fy = 0,0          
             
        # Otherwise, update the gravitational force!
        f = G * self.mass * other.mass / (r**2)          

        theta = atan2(ry, rx)           # Find the angle between the hypotenuse and the adjacent side
        fx = cos(theta) * f             # Compute the x component of the force on the planet
        fy = sin(theta) * f             # Compute the y component of the force on the planet

        return fx, fy                   # Return the x and y components of the force to the main loop

    #########
    # Add a testlanding function for the spacecraft! Return 1 if within diameter, 0 if not

    # Include a test for spacecraft to mars distance
    
        
def loop(system):                       # This function calculates the orbit of each planet and displays it in a window
    
    timestep = 1*24*3600                # One earth day
    date = 0                            # Starting date for the simulation - date increases for every iteration of the loop

    #########
    # Add date for thrust and velocity to add
    
    for body in system:                                 # Runs a loop for each planet
        body.goto(body.xloc*SCALE, body.yloc*SCALE)     # Puts the planet in its proper location on the display
        body.pendown()                                  # Puts down the pen - this means that a line will be draw to show the path of the orbit  

    while True:                         # Loop will run until user interrupts program (ctrl+c)
        force = {}                      # Create a dictionary that holds the total forces on each planet  
                 
        for body in system:

            total_fx = total_fy = 0.0   # Initialize the x and y components on the planet as 0

            # Update all forces exerted on the planets through gravity
            for other in system:                        
                if body is other:                       # Don't calculate the planet's attraction to itself
                    continue                            # Skip to the next planet
                fx, fy = body.attraction(other, date)   # Goes to the function called attraction (line 19)
                total_fx += fx                          # Sums up the x components of the gravitational forces on the planet
                total_fy += fy                          # Sums up the y components of the gravitational forces on the planet
                
            force[body] = (total_fx, total_fy)        # Assign the total force exerted on the planet to the dictionary, force

        # Update velocities, test for landing
        for body in system:                                       
            fx, fy = force[body]                                 # Assign the components of the total force to the variables fx and fy

            # Compute velocities from gravity
            body.vx += fx / body.mass * timestep                # Calculate the new x component of the velocity
            body.vy += fy / body.mass * timestep                # Calculate the new y component of the velocity

            #######
            # Add print statement to see the sizes of the velocities from each planet!

            ######
            # If the body is earth, compute the angle theta to use to compute the new velocity angle for a Hohmann transfer

            ######
            # Test if spacecraft has landed! use a test over all other bodies in system and call testLanding function if it's the spacecraft
            # Set the onPlanet to be initialized to zero inside of the loop 

            ######
            # If landed, use planet velocity (other.vx, other.vy) instead

            ######
            # Apply thrust on specified date: only to the spacecraft at the desired angle!

                
        # Update locations of all bodies
        for body in system:
            body.xloc += body.vx * timestep                     # Calculate the new x component of the position
            body.yloc += body.vy * timestep                     # Calculate the new y component of the position 
            body.goto(body.xloc*SCALE, body.yloc*SCALE)         # Move everything!

                
        date += 1                                                   # After updating the positions and velocities of the planet, go to the next day   
        
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
    planet.xloc = number            Gives the planet an x component position
    planet.yloc = number            Gives the planet a y component position
    planet.vx = number              Gives the planet an x component velocity
    planet.vy = number              Gives the planet a y component velocity
    """

    sun = planet()
    sun.name = 'Sun'
    sun.mass = 1.98892 * 10**30
    sun.penup() 
    sun.color('yellow')
    sun.shape('circle')
    sun.diameter = 1.3914 * 10**6
    sun.shapesize(2.0,2.0,1)
    """sun.vx = 1000
    sun.vy = 0"""
       
    earth = planet()
    earth.name = 'Earth'
    earth.mass = 5.97 * 10**24
    earth.penup() 
    earth.color('green')
    earth.shape('circle')
    earth.shapesize(0.6,0.6,1)
    earth.diameter = 12742
    earth.yloc = (1 * AU) * 0.80696031214
    earth.xloc = (1 * AU) * -0.59060566762
    earth.vy = 29.8 * 1000 * -0.59060566762          
    earth.vx = 29.8 * 1000 * -0.80696031214   

    """moon = planet()
    moon.name = 'Moon'
    moon.mass = 734.9 * 10**20
    moon.penup()
    moon.color('black')
    moon.shape('circle')
    moon.shapesize(0.1,0.1,1)
    moon.xloc = (1.453403112345339e-03 * AU) + (1 * AU) * -0.59060566762
    moon.yloc = (1.982115197585754e-03 * AU) + (1 * AU) * 0.80696031214
    moon.vx = (-4.929852973437543e-04 * AU)/(24*3600) + 29.8 * 1000 * -0.80696031214 
    moon.vy = (3.641097640628609E-04 * AU)/(24*3600) + 29.8 * 1000 * -0.59060566762"""

    venus = planet()
    venus.name = 'Venus'
    venus.mass = 4.87 * 10**24
    venus.penup() 
    venus.color('purple')
    venus.shape('circle')
    venus.diameter = 12104
    venus.shapesize(0.6,0.6,1)
    venus.yloc = (0.723 * AU)
    venus.vx = -35.02 * 1000
    
    mars = planet()
    mars.name = 'Mars'
    mars.mass = 6.3 * 10**24
    mars.penup() 
    mars.color('red')
    mars.shape('circle')
    mars.shapesize(0.5,0.5,1)
    #### If it's hard to land, increase diameter here!
    mars.diameter = 6779
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
    mercury.diameter = 4879
    mercury.shapesize(0.3,0.3,1)
    mercury.xloc = (0.39 * AU) * -0.74547599968
    mercury.yloc = (0.39 * AU) * -0.66653247024
    mercury.vy = 47.36 * 1000 * -0.74547599968 
    mercury.vx = 47.36 * 1000 * 0.66653247024

    jupiter = planet()
    jupiter.name = 'Jupiter'
    jupiter.mass = 1.9 * 10**27
    jupiter.penup() 
    jupiter.color('orange')
    jupiter.shape('circle')
    jupiter.diameter = 139822
    jupiter.shapesize(1.2,1.2,1)
    jupiter.xloc = (5.2 * AU) * -0.97480014384
    jupiter.yloc = (5.2 * AU) * -0.22307998468
    jupiter.vy = 13.06 * 1000 * -0.97480014384
    jupiter.vx = 13.06 * 1000 * 0.22307998468

    ######
    # Add space craft! Give it a name! Give it a mass (400-50,000kg)!
    # Initialize it to earth's velocity and location

    
    """
    alien = planet()
    alien.name = 'Bob'
    alien.mass = 3.4 * 10**27
    alien.penup()
    alien.color('pink')
    alien.shape('turtle')
    alien.shapesize(3.0,3.0,1)
    alien.xloc = (5.8 * AU) * 0.97480014384
    alien.yloc = (2.0 * AU)
    alien.vx = -15000
    """

    loop([sun, mercury, venus, earth, mars, jupiter, marsrover])       # Goes to the function called loop (line 37). Takes these planets and creates a solar system.

    
if __name__ == '__main__':          # The code starts here
    main()                          # Goes to the function called main (line 80)
