# Lunar Lander Simulation
from math import radians, sqrt, log
from ggmath import Label, Slider
from ggame import Color
from ggrocket import Rocket, Planet

G = 6.673E-11   # universal gravitation constant
moonmass = 7.3477E22
moonradius = 1738000
alt = 15000     # approximately 15 km orbital altitude
vel = sqrt(G*moonmass/(moonradius + alt))

# Lunar Lander specifications
mascent = 4700          # Ascent stage gross (fueled) mass
mdescent = 10344        # Descent stage gross (fueled) mass
mdescfuel = 8200        # Descent stage fuel mass
Fdmax = 45040           # Descent stage maximum thrust
SpecIdesc = 3050        # Descent specific impulse (Ns/kg)
mdotmax = Fdmax/SpecIdesc # Maximum propellent flow rate
MinThrottle = 0.1       # 10% minimum throttle
MaxThrottle = 0.6       # 60% full throttle
MinThrust = MinThrottle * Fdmax
MaxThrust = MaxThrottle * Fdmax


class Lem(Rocket):
    def __init__(self, planet, **kwargs):
        kwargs['thrust'] = self.GetThrust
        kwargs['mass'] = self.GetMass
        self.LastTime = 0
        self.ElapsedTime = 1
        self.FuelLeft = mdescfuel
        self.ThrustPct = 0
        self.LastAltitude = 0
        self.DeltaAltitude = 0
        # Clue for the thrust slider
        self.lab1 = Label((10,340), "Thrust: up/down key", positioning="physical", size=15)
        # Define a thrust slider
        self.ThrustSlider = Slider((10,360), 0, MaxThrottle, 0, positioning="physical", steps=20, leftkey="down arrow", rightkey="up arrow")
        # Fuel Gauge
        self.FuelGage = Label((10,390), self.FuelPct, positioning="physical", size=15)
        # Vertical Speedometer
        self.VSpeed = Label((10,420), self.VertVel, positioning="physical", size=15)
        super().__init__(planet, **kwargs)
        self.LastTime = self.shiptime
        
    def dynamics(self, timer):
        super().dynamics(timer)
        self.ElapsedTime = self.shiptime - self.LastTime
        self.LastTime = self.shiptime
        self.DeltaAltitude = self.altitude - self.LastAltitude
        self.LastAltitude = self.altitude
        self.ThrustPct = self.ThrustSlider()
        if self.ThrustPct >= 0.1 and self.FuelLeft > 0:
            self.FuelLeft = self.FuelLeft - mdotmax*self.ThrustPct*self.ElapsedTime

    # Create a function for determining the rocket thrust
    def GetThrust(self):
        thrustpct = self.ThrustSlider()
        if thrustpct < 0.1:
            return 0
        elif self.FuelLeft > 0:
            return Fdmax*self.ThrustPct
        return 0
    
    # Function for calculating the total rocket mass, based on burn time and total
    # propellent mass.
    def GetMass(self):
        return self.FuelLeft + mdescent - mdescfuel + mascent
    
    # Function for calculating the percent of fuel remaining, as text
    def FuelPct(self):
        return "Fuel Supply: {0:.1f}%".format(100*self.FuelLeft/mdescfuel)

    # Function for showing the vertical velocity
    def VertVel(self):
        if not self.ElapsedTime:
            return "Vertical Velocity N/A"
        else:
            return "Vertical Velocity: {0:.1f} m/s".format(self.DeltaAltitude/self.ElapsedTime)

moon = Planet(planetmass=moonmass, radius=moonradius, viewscale=0.02, color=0x202020) 

#Create and "run" the rocket
lander = Lem(moon, altitude=alt, velocity=vel)

moon.run(lander)
