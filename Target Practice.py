import os
import sys
import pygame
from pygame.locals import *
import time
from random import randint

# How to set timers: https://stackoverflow.com/a/59944869
# pygame.time.set_timer(pygame.USEREVENT, number_of_miliseconds)

# VAR
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOW_SIZE = (640, 640)
TARGET_SIZE = (64, 64)

# SYSTEM
os.environ["SDL_VIDEO_CENTERED"] = "1" # to fix bug where countdown goes into negative

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption("Target Practice")
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

NUMBER_OF_TARGETS = 60
target_coors = {}
score = 0
max_score = 0
total_hits = 0

# FUNCTIONS
count = 3
start_count = False
pygame.time.set_timer(USEREVENT, 1000)
while count >= 0:
    if count == 3 and not start_count:
        text = pygame.font.SysFont("Helvetica", 64).render(str(count), False, WHITE)
        text_rect = text.get_rect(center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        start_count = True
    for event in pygame.event.get():
        if event.type == USEREVENT:
            screen.fill(BLACK)
            if count == 0:
                pygame.time.set_timer(USEREVENT, 0)
                text = pygame.font.SysFont("Helvetica", 64).render("GO", False, WHITE)
            else:
                pygame.time.set_timer(USEREVENT, 0)
                text = pygame.font.SysFont("Helvetica", 64).render(str(count), False, WHITE)
                pygame.time.set_timer(USEREVENT, 1000)
            text_rect = text.get_rect(center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            screen.blit(text, text_rect)
            count -= 1
            pygame.display.update()

target_timers = {}
ENDGAME = USEREVENT
TARGET_SPAWN_INTERVAL = 500
TARGET_DESPAWN_INTERVAL = 2000
STARTGAME = pygame.time.get_ticks() - TARGET_SPAWN_INTERVAL
pygame.time.set_timer(ENDGAME, NUMBER_OF_TARGETS * TARGET_SPAWN_INTERVAL + TARGET_DESPAWN_INTERVAL)

# GAME LOOP
done = False
game = True
while not done:
    if game:
        screen.fill(BLACK)

        # Game time
        game_time = pygame.time.get_ticks()

        # Target spawn
        if (game_time - STARTGAME) // TARGET_SPAWN_INTERVAL > max_score and (game_time - STARTGAME) // TARGET_SPAWN_INTERVAL <= NUMBER_OF_TARGETS:
            max_score += 1
            target_coors[max_score] = (randint(0, WINDOW_SIZE[0] - TARGET_SIZE[0]), randint(0, WINDOW_SIZE[0] - TARGET_SIZE[0]))
            target_timers[max_score] = game_time

        # Target despawn
        targets_to_despawn = [user_event for user_event in target_timers if (game_time - target_timers[user_event]) > TARGET_DESPAWN_INTERVAL]
        for user_event in targets_to_despawn:
            target_coors.pop(user_event)
            target_timers.pop(user_event)

        # Target rendering
        target_rects = []
        for user_event in target_coors:
            target_rects.append(pygame.draw.rect(screen, GREEN, pygame.Rect(target_coors[user_event], TARGET_SIZE)))

    # Event manager
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
            
        if event.type == ENDGAME:
            pygame.time.set_timer(ENDGAME, 0)
            screen.fill(BLACK)
            text = pygame.font.SysFont("Helvetica", 64).render("GAME END!", False, WHITE)
            text_rect = text.get_rect(center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            time.sleep(1)

            screen.fill(BLACK)
            text = pygame.font.SysFont("Helvetica", 64).render(f"Score: {score}/{max_score}", False, WHITE)
            text_rect = text.get_rect(center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 60))
            screen.blit(text, text_rect)
            try:
                text = pygame.font.SysFont("Helvetica", 64).render(f"Accuracy: {int(round(score/total_hits, 2) * 100)}%", False, WHITE)
            except: # div by zero
                text = pygame.font.SysFont("Helvetica", 64).render(f"Accuracy: 0%", False, WHITE)
            text_rect = text.get_rect(center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 60))
            screen.blit(text, text_rect)
            pygame.display.update()
            game = False
            
        if game:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for target_rect in target_rects:
                        if target_rect.collidepoint(pygame.mouse.get_pos()):
                            deleted_user_events = [user_event for user_event in target_coors if target_coors[user_event] == (target_rect.x, target_rect.y)]
                            if deleted_user_events:
                                target_coors.pop(deleted_user_events[0])
                                target_timers.pop(deleted_user_events[0])
                                score += 1
                            break
                    total_hits += 1

    pygame.display.update()
    clock.tick(60)

# EXIT
pygame.quit()
sys.exit()
