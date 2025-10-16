


import pygame
import os
pygame.init()
pygame.mixer.init()

set_minutes = 2
set_seconds = 60

def timer_text(font, font_color, mins, secs, main_surface_width, main_surface_height):
    text = font.render(f"{mins:02}:{secs:02}", True, font_color)
    text_pos = ((main_surface_width // 2) - (text.get_width() // 2) - 5,
                (main_surface_height // 2) - (text.get_height() // 2) + 25)
    
    return (text, text_pos)

def load_explosion_frames(path):
    frames = []
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".png"):
            explosion_frame = pygame.image.load(os.path.join(path, filename)).convert_alpha()
            frames.append(explosion_frame)

    return frames

# screen settings
screen_width, screen_height = 300, 130
screen_color = (0, 0, 0)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Timer")

# bomb image settings
bomb_image = pygame.image.load("assets/images/bomb.png").convert_alpha()
scale_factor = min(screen_width / bomb_image.get_width(), screen_height / bomb_image.get_height())
scaled_img_width = bomb_image.get_width() * scale_factor
scaled_img_height = bomb_image.get_height() * scale_factor
scaled_bomb_image = pygame.transform.smoothscale(bomb_image, (scaled_img_width, scaled_img_height))
bomb_image_pos = ((screen_width // 2) - (scaled_img_width // 2),
                  (screen_height // 2) - (scaled_img_height // 2))

explosion_frames = load_explosion_frames("assets/images/explosion frames")

# timer font settings
timer_text_font = pygame.font.Font("assets/font/digital-7-mono.ttf", 25)
timer_text_color = (150, 20, 30)
initialMinutes = 0
initialSeconds = 0
show_text = True

# blink variables
starting_blink_start = None
fMaxBlinks = 2
fBlinkCount = 0
blinkInterval = 60

counter_start_time = None
counterInterval = 1000

ending_blink_start = None
eBlinkCount = 0
eMaxBlinks = 5

timer_end = False

# sounds
oklessgo = pygame.mixer.Sound("assets/sounds/oklessgo.wav")
beep = pygame.mixer.Sound("assets/sounds/beep.wav")
doublebeep = pygame.mixer.Sound("assets/sounds/doublebeep.wav")
explode = pygame.mixer.Sound("assets/sounds/explode.wav")

# ending gif settings
explosion_active = False
explosion_start_time = None
explosion_frame_index = 0
explosionInterval = 60

clock = pygame.time.Clock()

# main loop
is_running = True
while is_running:
    screen.fill(screen_color)
    screen.blit(scaled_bomb_image, bomb_image_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                initialMinutes = set_minutes - 1
                initialSeconds = set_seconds - 1
                starting_blink_start = pygame.time.get_ticks()
                show_text = True
                fBlinkCount = 0
                counter_start_time = pygame.time.get_ticks()
                oklessgo.play()
                explosion_active = False
                explosion_frame_index = 0
                ending_blink_start = None
                eBlinkCount = 0

    if starting_blink_start is not None:
        starting_blink_change = pygame.time.get_ticks()
        if starting_blink_change - starting_blink_start >= blinkInterval and fBlinkCount < fMaxBlinks:
            show_text = not show_text
            fBlinkCount += 1
            starting_blink_start = starting_blink_change
    
    if ending_blink_start is not None:
        ending_blink_change = pygame.time.get_ticks()
        if ending_blink_change - ending_blink_start >= blinkInterval and eBlinkCount < eMaxBlinks:
            show_text = not show_text
            eBlinkCount += 1
            ending_blink_start = ending_blink_change

        if eBlinkCount >= eMaxBlinks and not explosion_active:
            timer_end = True
            explosion_active = True
            explosion_frame_index = 0
            explosion_start_time = pygame.time.get_ticks()
            explode.play()
            ending_blink_start = None

    if explosion_active:
        explosion_time_change = pygame.time.get_ticks()
        if explosion_start_time is not None:
            if explosion_time_change - explosion_start_time >= explosionInterval:
                explosion_start_time = explosion_time_change
                explosion_frame_index += 1

            if explosion_frame_index < len(explosion_frames):
                eFrame = explosion_frames[explosion_frame_index]
                screen.blit(eFrame, ((screen_width // 2) - (eFrame.get_width() // 2),
                                     (screen_height // 2) - (eFrame.get_height() // 2)))
                
            else:
                explosion_active = False
                timer_end = False
            
    if show_text:
        if counter_start_time is not None:
            counter_time_change = pygame.time.get_ticks()
            if counter_time_change - counter_start_time >= counterInterval:
                counter_start_time = counter_time_change
                if initialSeconds > -1:
                    initialSeconds -= 1

                if initialMinutes > 0:
                    if initialSeconds == 0:
                        initialSeconds = 60
                        initialMinutes -= 1

                if initialMinutes == 0 and initialSeconds < 11 and initialSeconds > -1:
                    beep.play()

                if initialMinutes == 0 and initialSeconds == -1:
                    ending_blink_start = pygame.time.get_ticks()
                    eBlinkCount = 0
                    initialSeconds = 0
                    doublebeep.play()
            
        time_text, time_text_pos = timer_text(timer_text_font, timer_text_color, initialMinutes,
                                            initialSeconds, screen_width, screen_height)
        screen.blit(time_text, time_text_pos)

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()


