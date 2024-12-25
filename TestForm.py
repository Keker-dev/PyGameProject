from classes import *


def main(name_window):
    pygame.init()
    running = True

    screen = pygame.display.set_mode((600, 600))
    screen.fill((0, 0, 255))
    pygame.display.set_caption(name_window)
    clock = pygame.time.Clock()

    pos = Vector2(0, 0)
    fps = 60
    player = Player(screen, speed=2, pos=Vector2(0, 0))
    cam = Camera(screen, FolowAt=player, pos=Vector2(0, 0))
    other = BaseObject(screen, Vector2(0, 0))
    other.set_view("Rect", size=Vector2(50, 50), color=(255, 0, 0))
    player.set_view("Circle", radius=20, color=(255, 255, 255))

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        player.Movement(events)
        cam.FixedUpdate(events)
        other.render(cam)
        player.render(cam)

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
    return 0


if __name__ == '__main__':
    sys.exit(main("TEST"))
