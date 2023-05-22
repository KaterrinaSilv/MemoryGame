import pygame


class Button():
    def __init__(self, image, pos):
        pygame.font.init()
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = pygame.font.Font(None, 36)
        self.text_input = ''
        self.text = self.font.render(self.text_input, True, 'black')
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

