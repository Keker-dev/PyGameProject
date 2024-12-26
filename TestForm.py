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
    player = Player(screen, speed=2, rend_order=1)
    cam = Camera(screen, FolowAt=player)
    other = BaseObject(screen)
    other.set_view("Rect", "Base", size=Vector2(50, 50), color=(255, 0, 0))
    player.set_view("Circle", "Base", radius=20, color=(255, 255, 255))

    BaseScene = Scene(screen, cam)
    BaseScene.objects += [player, other, cam]

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        BaseScene.Update()
        BaseScene.Render()

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
    return 0


if __name__ == '__main__':
    sys.exit(main("TEST"))
