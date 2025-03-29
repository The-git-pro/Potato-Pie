import pygame #type: ignore
import random
import sys

pygame.init()

window = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

pygame.display.set_caption("Mwahahahahahahahahahahahahahahahahahahahahahahahahah")

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (500, 500))

darkness_surface = pygame.Surface(background.get_rect().size)
darkness_surface.fill((0, 0, 0))
darkness_surface.set_alpha(15)  # 128 is 50% transparency, adjust as needed

def game():
  speed = 0.0
  score = -1

  high_score = open("high_score.txt", "r")
  high_score = high_score.read()
  high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))

  left = False
  right = False

  potato_image = pygame.image.load("potato.png")
  potato_image = pygame.transform.scale(potato_image, (50, 50))
  potato_rect = potato_image.get_rect()
  potato_rect.x = 200
  potato_rect.y = 0
  potato_x = 200
  potato_y = 0

  pie_image = pygame.image.load("pie.png")
  pie_image = pygame.transform.scale(pie_image, (100, 100))
  pie_rect = pie_image.get_rect()
  pie_rect.x = 200
  pie_rect.y = 0
  pie_x = 225
  pie_y = 425

  while True:
    clock.tick(60)
    potato_y += speed

    if pygame.Rect.colliderect(potato_rect, pie_rect):
      score += 1
      increment = 1.25 / (speed + 1)
      speed += increment
      potato_y = 0
      pie_x = random.randint(50, 450)

    if potato_y > 500:
      restart(score, high_score)

    if potato_x >= 500:
      potato_x = 10

    if potato_x <= 0:
      potato_x = 450

    for event in pygame.event.get():
      if event.type == 256:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          left = True
        if event.key == pygame.K_RIGHT:
          right = True
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
          left = False
        if event.key == pygame.K_RIGHT:
          right = False

    if left:
      potato_x -= 2.5
    if right:
      potato_x += 2.5

    window.blit(background, (0, 0))
    window.blit(darkness_surface, (0, 0))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))

    window.blit(potato_image, (potato_x, potato_y))
    window.blit(pie_image, (pie_x, pie_y))
    window.blit(score_text, (25, 25))
    window.blit(high_score_text, ((500 - high_score_text.get_width()) - 25, 25))

    potato_rect.x = potato_x
    potato_rect.y = potato_y

    pie_rect.x = pie_x
    pie_rect.y = pie_y

    pygame.display.update()

def restart(score, high_score):
  window = pygame.display.set_mode((1100, 25), pygame.RESIZABLE)
  window.fill((0, 0, 0))

  if score > int(high_score):
    high_score = open("high_score.txt", "w")
    high_score.write(str(score))
    high_score = None

  text = font.render(f"No more pies for you! (Unless you press R). But even if you don't, you will still have fallen into {score}.", True, (255, 255, 255))
  text = pygame.transform.scale(text, (1100, 25))
  text_rect = text.get_rect()
  text_x = 550 - (text_rect.width / 2)
  text_y = 12.5 - (text_rect.height / 2)

  window.blit(text, (text_x, text_y))

  pygame.display.update()

  while True:
    for event in pygame.event.get():
      if event.type == 256:
        sys.exit()
    
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          window = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
          game()

game()