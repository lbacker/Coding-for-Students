#!/usr/bin/env python3

import math
from turtle import *
import turtle
from Tkinter import *

# The gravitational constant G
G = 6.67428e-11

# Assumed scale: 25 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 62.5 / AU

class Body(Turtle):
    
    name = 'Body'
    mass = None
    vx = vy = 0.0
    xloc = yloc = 0.0
    
    def attraction(self, other):

        # Compute the distance of the other body.
        rx = (other.xloc-self.xloc)
        ry = (other.yloc-self.yloc)
        r = math.sqrt(rx**2 + ry**2)

        # Collision!!!
        if r == 0:
            raise ValueError("Collision between objects %r and %r"
                             % (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (r**2)

        # Compute the force in components
        fx = math.cos(math.atan2(ry, rx)) * f
        fy = math.sin(math.atan2(ry, rx)) * f
        return fx, fy

def loop(bodies):
    timestep = 1*24*3600  # One ( earth) day
    
    step = 1
    for body in bodies:
        body.goto(body.xloc*SCALE, body.yloc*SCALE)
        body.pendown()
    date = 0
    
    while True:
        step += 1

        force = {}
        for body in bodies:

            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.xloc += body.vx * timestep
            body.yloc += body.vy * timestep
            body.goto(body.xloc*SCALE, body.yloc*SCALE)
        date = date + 1
        turtle.clear()
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(300, 300)
        turtle.pendown()
        turtle.color("black")
        turtle.write(str(date) + " Days",False, align="right", font=("Arial", 18, "normal"))
        ts = turtle.getscreen()
        ts.getcanvas().postscript(file=str(date)+".eps", colormode='color')

def main():
    # Planets start at average distance from sun, with mean speed
    # Start in locations for January 26th
    
    turtle.setup(800, 800)      # set the window size to 800 by 600 pixels
    turtle.bgcolor("white")

    sun = Body()
    sun.name = 'Sun'
    sun.mass = 1.98892 * 10**30
    sun.penup() 
    sun.color('yellow')
    sun.shape("circle")
       
    earth = Body()
    earth.name = 'Earth'
    earth.mass = 5.97 * 10**24
    earth.penup() 
    earth.color('green')
    earth.shape("circle")
    earth.yloc = 1*AU*0.80696031214
    earth.xloc = 1*AU*-0.59060566762
    earth.vy = 29.8 * 1000*-0.59060566762          
    earth.vx = 29.8 * 1000*-0.80696031214        

    venus = Body()
    venus.name = 'Venus'
    venus.mass = 4.87 * 10**24
    venus.penup() 
    venus.color('purple')
    venus.shape("circle")
    venus.yloc = 0.723 * AU
    venus.vx = -35.02 * 1000
    
    mars = Body()
    mars.name = 'Mars'
    mars.mass = 6.3 * 10**23
    mars.penup() 
    mars.color('red')
    mars.shape("circle")
    mars.xloc = 1.524 * AU * 0.85391432258
    mars.yloc = 1.524 * AU * 0.52041361405
    mars.vy = 24.1 * 1000 * 0.85391432258 
    mars.vx = 24.1 * 1000 * - 0.52041361405

    mercury = Body()
    mercury.name = 'Mercury'
    mercury.mass = 3.285 * 10**23
    mercury.penup() 
    mercury.color('black')
    mercury.shape("circle")
    mercury.xloc = 0.39 * AU * - 0.74547599968
    mercury.yloc = 0.39 * AU * - 0.66653247024
    mercury.vy = 47.36 * 1000 * - 0.74547599968 
    mercury.vx = 47.36 * 1000 * 0.66653247024

    jupiter = Body()
    jupiter.name = 'Jupiter'
    jupiter.mass = 1.9 * 10**27
    jupiter.penup() 
    jupiter.color('orange')
    jupiter.shape("circle")
    jupiter.xloc = 5.2 * AU*-0.97480014384
    jupiter.yloc = 5.2 * AU*-0.22307998468
    jupiter.vy = 13.06 * 1000*-0.97480014384
    jupiter.vx = 13.06 * 1000*0.22307998468

    saturn = Body()
    saturn.name = 'Saturn'
    saturn.mass = 5.683 * 10**26
    saturn.penup() 
    saturn.color('blue')
    saturn.shape("circle")
    saturn.yloc = 9 * AU*-0.98768834059
    saturn.xloc = 9 * AU*-0.15643446504
    saturn.vx = 9.68 * 1000*0.98768834059
    saturn.vy = 9.68 * 1000*-0.15643446504

    loop([sun, mercury, venus, earth, mars, jupiter])

    
if __name__ == '__main__':
    main()
