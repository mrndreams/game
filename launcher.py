import pygame as pg
import json
import subprocess

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = inactive_colour
        self.text = text
        self.txt_surface = fonts[32].render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = active_colour if self.active else inactive_colour
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.text.__len__() < 32:
                        self.text += event.unicode
                self.txt_surface = fonts[32].render(self.text, True, self.color)

    def update(self):
        width = max(ui_width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

class Button():
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = button_colour
        self.txt_surface = fonts[32].render(text, True, self.color)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.clicked = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mousePos = pg.mouse.get_pos()
            if self.rect.collidepoint(mousePos):
                self.clicked = True

    def update(self):
        return self.clicked
    
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

if __name__ == "__main__":
    try:
        config = json.load(open("config.json", "rt"))
    except FileNotFoundError:
        with open("config.json", "wt") as f:
            f.write('{\n    "HOST": "0.0.0.0",\n    "PORT": "38491",\n    "NAME": "Player"\n}')
        print("config.json created. Open it and enter a host, port and username.")
        pg.quit()
        quit()

    pg.init()
    pg.display.set_caption("Game Launcher")

    inactive_colour = pg.Color("darkorchid4")
    active_colour = pg.Color("darkorchid1")
    button_colour = pg.Color("white")

    w, h = 1920 / 4, 1080 / 3
    display = pg.display.set_mode((w, h))
    clock = pg.time.Clock()
    fonts = {size: pg.font.Font(None, size) for size in [32,48,64]}

    ui_width = 250
    ui_height = 30
    configured = False

    window_center = tuple(i / 2 for i in pg.display.get_window_size())

    hostname_field = InputBox(window_center[0] - ui_width / 2, window_center[1] + ui_height*-3, ui_width, ui_height, config["HOST"])
    port_field = InputBox(window_center[0] - ui_width / 2, window_center[1] + ui_height*-2, ui_width, ui_height, config["PORT"])
    name_field = InputBox(window_center[0] - ui_width / 2, window_center[1] + ui_height*-1, ui_width, ui_height, config["NAME"])

    join_button = Button(window_center[0] - ui_width / 2, window_center[1] + ui_height*4, ui_width, ui_height, "Join")

    while configured == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            hostname_field.handle_event(event)
            port_field.handle_event(event)
            name_field.handle_event(event)
            join_button.handle_event(event)

        hostname_field.update()
        port_field.update()
        name_field.update()
        if join_button.update() == True:
            configured = True


        display.fill(pg.Color("black"))

        hostname_field.draw(display)
        port_field.draw(display)
        name_field.draw(display)
        join_button.draw(display)

        pg.display.flip()
        clock.tick(30)

    config["HOST"] = hostname_field.text
    config["PORT"] = port_field.text
    config["NAME"] = name_field.text 

    with open("config.json", "wt") as f:
        f.write('{\n    "HOST": "' + config["HOST"] + '",\n    "PORT": "' + config["PORT"] + '",\n    "NAME": "' + config["NAME"] + '"\n}')
        f.close()
    subprocess.run(["python", "client.py"])
