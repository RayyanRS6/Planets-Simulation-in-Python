import pygame
import math
import random

pygame.init()

# pygame window adjustment
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

YELLOW = (255, 255, 0)  # Sun
GREEN = (144, 238, 144)  # Mercury
MUD = (112, 84, 62)  # Venus
BLUE = (100, 100, 255)  # Earth
RED = (255, 0, 0)  # Mars
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont("Poppins", 16)


class Planet:
    # au = astronomical unit jo roughly equal hota distance of earth to sun
    AU = 149.6e6 * 1000
    # gravitational constant jo phy mein prha tha (its not gravity)
    G = 6.67428e-11
    SCALE = 200 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        # yeh straight line force aur distance ko x aur y components mein break krdia
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)  # G * MM / (r Square)

        if other.sun:
            self.distance_to_sun = distance

        # calculating G * MM / (r Square)
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


#just for a starry night sky (nothing special)
class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.brightness = random.randint(0, 255)
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(3, 3)

    def update(self):
        self.brightness += self.direction * self.speed
        if self.brightness <= 0:
            self.brightness = 0
            self.direction = 1
        elif self.brightness >= 255:
            self.brightness = 255
            self.direction = -1

    def draw(self, win):
        color = (self.brightness, self.brightness, self.brightness)
        win.fill(color, (self.x, self.y, 2, 2))


def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        stars.append(Star(x, y))
    return stars


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, GREEN, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, MUD, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]
    stars = create_stars(100)

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for star in stars:
            star.update()
            star.draw(WIN)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
