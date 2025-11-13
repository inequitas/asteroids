#import all the things
import pygame
import sys
import os
import json
from constants import *
from logger import log_state,log_event
from player import Player
from asteroid import Asteroid
from AsteroidField import AsteroidField
from shot import Shot

#initialize pygame
pygame.init()

#set the screen and clock parameters
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

#making the groups
updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()


#assigning groups to classes
Player.containers = (updatable, drawable)
Asteroid.containers = (asteroids, updatable, drawable)
AsteroidField.containers = (updatable)
Shot.containers = (updatable, drawable)

#create player instance
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots)
field = AsteroidField()

def load_high_scores():
    if not os.path.exists(HIGH_SCORE_FILE):
        return []
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                cleaned = []
                for entry in data:
                    if (
                        isinstance(entry, dict)
                        and "name" in entry
                        and "score" in entry
                        and isinstance(entry["score"], int)
                    ):
                        cleaned.append(entry)
                cleaned.sort(key=lambda e: e["score"], reverse=True)
                return cleaned[:3]
    except Exception:
        return []
    return []


def save_high_scores(scores):
    scores = sorted(scores, key=lambda e: e["score"], reverse=True)[:3]
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump(scores, f)


def get_points_for_asteroid(asteroid):
    # Bigger asteroids are worth more
    kind = max(1, int(asteroid.radius / ASTEROID_MIN_RADIUS))
    return kind * 10

def ask_player_name(screen, font):
    name = ""
    entering = True
    input_clock = pygame.time.Clock()

    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                entering = False
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if event.unicode and event.unicode.isprintable() and len(name) < 12:
                        name += event.unicode

        screen.fill("black")

        prompt = font.render("New High Score! Enter your name:", True, "white")
        name_display = name if name else "_"
        name_surf = font.render(name_display, True, "white")

        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        name_rect = name_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))

        screen.blit(prompt, prompt_rect)
        screen.blit(name_surf, name_rect)

        info_surf = font.render("Press Enter to confirm", True, "white")
        info_rect = info_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(info_surf, info_rect)

        pygame.display.flip()
        input_clock.tick(30)

    return name or "Anonymous"

def show_high_scores_screen(screen, font, scores, final_score):
    waiting = True
    hs_clock = pygame.time.Clock()

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill("black")

        title = font.render("Top 3 High Scores", True, "white")
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Draw the scores
        for i, entry in enumerate(scores[:3]):
            line = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, "white")
            line_rect = line.get_rect(center=(SCREEN_WIDTH // 2, 160 + i * 40))
            screen.blit(line, line_rect)

        # Player's score
        your_score_text = font.render(f"Your score: {final_score}", True, "white")
        your_score_rect = your_score_text.get_rect(center=(SCREEN_WIDTH // 2, 160 + 3 * 40 + 20))
        screen.blit(your_score_text, your_score_rect)

        info = font.render("Press any key to quit", True, "white")
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        screen.blit(info, info_rect)

        pygame.display.flip()
        hs_clock.tick(30)

    pygame.quit()
    sys.exit()

def handle_game_over(screen, font, score):
    high_scores = load_high_scores()

    qualifies = score > 0 and (len(high_scores) < 3 or score > min(e["score"] for e in high_scores))

    if qualifies:
        name = ask_player_name(screen, font)
        if not name:
            name = "Anonymous"
        high_scores.append({"name": name, "score": score})
        save_high_scores(high_scores)
        high_scores = load_high_scores()  # re-load to ensure sorted & clipped

    show_high_scores_screen(screen, font, high_scores, score)

def run():
    # initialize pygame
    pygame.init()

    # set the screen and clock parameters
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # font for score and UI
    font = pygame.font.SysFont(None, 32)

    # making the groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # assigning groups to classes
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable      # NOTE: no tuple here, matches your original
    Shot.containers = (updatable, drawable)

    # create player instance
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots)
    field = AsteroidField()

    # load existing high scores to get current high score value
    high_scores = load_high_scores()
    high_score_value = high_scores[0]["score"] if high_scores else 0

    # start loop
    score = 0
    done = False
    while not done:
        # let me quit out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # logging
        log_state()

        # clear screen
        screen.fill("black")

        # update everything
        updatable.update(dt)

        # collision: player vs asteroid
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                handle_game_over(screen, font, score)

        # collision: shot vs asteroid
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += get_points_for_asteroid(asteroid)
                    if score > high_score_value:
                        high_score_value = score
                    asteroid.split()

        # draw everything
        for item in drawable:
            item.draw(screen)

        # draw current score (top left)
        score_surf = font.render(f"Score: {score}", True, "white")
        screen.blit(score_surf, (10, 10))

        # draw high score (top right)
        hs_surf = font.render(f"High: {high_score_value}", True, "white")
        hs_rect = hs_surf.get_rect()
        hs_rect.topright = (SCREEN_WIDTH - 10, 10)
        screen.blit(hs_surf, hs_rect)

        # flip buffers
        pygame.display.flip()

        # FPS & dt
        clock.tick(60)
        dt = clock.tick(60) / 1000
    
#start main
def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    run()


if __name__ == "__main__":
    main()