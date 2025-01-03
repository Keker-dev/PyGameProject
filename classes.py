import pygame
from pygame import Vector2, Rect
import sys


class Scene:
    def __init__(self, screen, camera):
        self.screen = screen
        self.Camera = camera
        self.objects = []

    def Render(self):
        self.screen.fill((0, 0, 0))
        UI_objects = sorted(list(filter(lambda x: x.layer == "UI", self.objects)), key=lambda a: a.render_order)
        Base_objects = sorted(list(filter(lambda x: x.layer != "UI", self.objects)), key=lambda a: a.render_order)
        for i in Base_objects:
            i.render(self.Camera)
        for i in UI_objects:
            i.render(self.Camera)

    def Update(self):
        for i in self.objects:
            i.OrderUpdate()


class BaseObject:
    def __init__(self, screen, pos=(0, 0), rotation=0, sprite_type=None, visible=True, rend_order=0, **kwargs):
        self.screen = screen
        if isinstance(pos, Vector2):
            self.position = pos
        else:
            self.position = Vector2(*pos)
        self.rotation = rotation
        self.sprite_type = sprite_type
        self.visible = visible

        self.size = 1
        self.color = (255, 255, 255)
        self.render_order = rend_order
        self.layer = "Base"
        self.childrens = []
        self.additions = []
        self.render_settings = {}

    def move_to(self, pos, time=0):
        if time == 0:
            self.position = pos
        else:
            pass

    def move(self, rel, time=0):
        if time == 0:
            self.position += rel
        else:
            pass

    def render(self, cam):
        if self.layer == "UI":
            cam_pos = Vector2(0, 0)
        else:
            cam_pos = Vector2(cam.position.x, cam.position.y)
        if self.sprite_type is None:
            return
        if not self.visible:
            return
        if self.sprite_type == "Circle":
            rend_sett = {"surface": self.screen, "color": self.color, "center": self.position - cam_pos,
                         "radius": self.size}
            for i in self.render_settings.keys():
                if "radius" == i:
                    rend_sett[i] = int(self.render_settings[i] * self.size)
                else:
                    rend_sett[i] = self.render_settings[i]
            pygame.draw.circle(**rend_sett)
        if self.sprite_type == "Rect":
            size = Vector2(1, 1) * self.size
            size.x, size.y = int(size.x), int(size.y)
            rend_sett = {"surface": self.screen, "color": self.color,
                         "rect": Rect(self.position - size // 2 - cam_pos, size)}
            for i in self.render_settings.keys():
                if i == "size":
                    size = self.render_settings[i] * self.size
                    size.x, size.y = int(size.x), int(size.y)
                    rend_sett["rect"] = Rect(self.position - self.render_settings[i] // 2 - cam_pos, size)
                else:
                    rend_sett[i] = self.render_settings[i]
            pygame.draw.rect(**rend_sett)
        if self.sprite_type == "Image":
            image_surf = pygame.image.load(self.render_settings["image"]).convert_alpha()
            scale = pygame.transform.scale(image_surf, (
                int(image_surf.get_width() * self.size), int(image_surf.get_height() * self.size)))
            rot = pygame.transform.rotate(scale, self.rotation)
            rot_rect = rot.get_rect(center=self.position - cam_pos)
            self.screen.blit(rot, rot_rect)

    def set_view(self, sprite_type, layer, **kwargs):
        if sprite_type in [None, "Circle", "Rect", "Image"] and layer in "Base|UI":
            self.sprite_type = sprite_type
            self.layer = layer
            self.render_settings = kwargs

    def OrderUpdate(self):
        self.Update(pygame.event.get())
        self.UpdateAdditions()
        self.FixedUpdate(pygame.event.get())

    def Update(self, events):
        pass

    def UpdateAdditions(self):
        pass

    def FixedUpdate(self, events):
        pass


class Player(BaseObject):
    def __init__(self, *args, **kwargs):
        self.speed = kwargs.pop("speed")
        super().__init__(*args, **kwargs)

    def FixedUpdate(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.position += Vector2(10, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.position += Vector2(-10, 0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.position += Vector2(0, -10)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.position += Vector2(0, 10)


class Camera(BaseObject):
    def __init__(self, *args, **kwargs):
        self.FolowAt = kwargs.pop("FolowAt")
        super().__init__(*args, **kwargs)

    def FixedUpdate(self, events):
        pos = Vector2(self.FolowAt.position.x, self.FolowAt.position.y)
        pos.x -= self.screen.get_width() // 2
        pos.y -= self.screen.get_height() // 2
        self.position = pos
