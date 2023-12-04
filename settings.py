# Screen
resolution = screen_width, screen_height = 1200, 650
screen_half_width = screen_width // 2
screen_half_height = screen_height // 2
fps = 30

# Text
font_size = screen_height // 10

# Menu
menu_background_color = "cadetblue4"
menu_button_color = "khaki2"
menu_text_color = "gray"

# Game rendering
sky_proportion = 0.6

# Fighter
animation_speed = 90
fighter_size_on_screen = int(0.3 * screen_height)
movement_distance = int(0.1 * screen_width)
max_health = 3
telegraphing_limit = 1
health_bar_offset = 0.05

# NPC
fight_distance = screen_width // 2
ai_update_wait = animation_speed