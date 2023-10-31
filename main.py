import time
import pygame
from pygame import mixer
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from pygame_widgets.dropdown import Dropdown

from wave import *
from theory import *


# Initialize Pygame
pygame.init()
mixer.init(channels=1)

# Screen settings
WIDTH, HEIGHT = 750, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chord Physics')
clock = pygame.time.Clock()


h = 25
key_slider = Slider(screen, 200, h, 500, 40, min=0, max=11, step=1, initial=3)
key_output = TextBox(screen, 25, h, 125, 50, fontSize=25)
key_output.disable()
h += 75
octave_slider = Slider(screen, 200, h, 500, 40, min=0, max=5, step=1, initial=3)
octave_output = TextBox(screen, 25, h, 125, 50, fontSize=25)
octave_output.disable()
h += 75
chord_slider = Slider(screen, 200, h, 500, 40, min=1, max=8, step=1, initial=1)
chord_output = TextBox(screen, 25, h, 125, 50, fontSize=30)
chord_output.disable()
h += 75
inversion_slider = Slider(screen, 200, h, 500, 40, min=0, max=3, step=1, initial=0)
inversion_output = TextBox(screen, 25, h, 125, 50, fontSize=25)
inversion_output.disable()
h += 75
swap_toggle = Toggle(screen, 200, h, 50, 40, startOn=False)
swap_output = TextBox(screen, 25, h, 125, 50, fontSize=25)
swap_output.disable()
h += 75
diminish_toggle = Toggle(screen, 200, h, 50, 40, startOn=False)
diminish_output = TextBox(screen, 25, h, 125, 50, fontSize=25)
diminish_output.disable()
h += 75
seventh_toggle = Toggle(screen, 200, h, 50, 40, startOn=True)
seventh_output = TextBox(screen, 25, h, 125, 50, fontSize=25)
seventh_output.disable()
h += 75

wave_dropdown = Dropdown(screen, 25, h, 700, 30, name='Select Waveform', fontSize=30,
                         choices=['sine', 'square', 'sawtooth', 'triangle'], values=['sine', 'square', 'sawtooth', 'triangle'])

chord_wave = None
key_num = key_slider.getValue()
chord_num = chord_slider.getValue()
last_played_type = ''


# Main game loop
running = True
start = time.time()
while running:
    time_delta = clock.tick(60)/1000.0

    play_now = False
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.unicode.isdigit():
                if int(event.unicode) == 9:
                    if swap_toggle.getValue():
                        swap_toggle.toggle()
                if int(event.unicode) == 0:
                    if diminish_toggle.getValue():
                        diminish_toggle.toggle()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_now = True
                plt.show()

            if event.unicode.isdigit():
                root_num = int(event.unicode)
                if root_num >= 1 and root_num <= 8:
                    chord_slider.setValue(root_num)
                    play_now = True
                if int(event.unicode) == 9:
                    if not swap_toggle.getValue():
                        swap_toggle.toggle()
                if int(event.unicode) == 0:
                    if not diminish_toggle.getValue():
                        diminish_toggle.toggle()

            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                inversion_slider.setValue((inversion_slider.getValue()+1) % (inversion_slider.max+1))
            if event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                inversion_slider.setValue((inversion_slider.getValue()-1) % (inversion_slider.max+1))

            if event.key == pygame.K_RIGHT:
                key_slider.setValue((key_slider.getValue()+1) % (key_slider.max+1))
            if event.key == pygame.K_LEFT:
                key_slider.setValue((key_slider.getValue()-1) % (key_slider.max+1))

            if event.key == pygame.K_UP:
                octave_slider.setValue((octave_slider.getValue()+1) % (octave_slider.max+1))
            if event.key == pygame.K_DOWN:
                octave_slider.setValue((octave_slider.getValue()-1) % (octave_slider.max+1))

    key_num = key_slider.getValue()
    chord_num = chord_slider.getValue()

    if play_now:
        root_num = key_num + chords[chord_num]['steps']
        root_num += octave_slider.getValue() * 12
        inversion_num = inversion_slider.getValue()
        do_sevenths = seventh_toggle.getValue()
        do_maj_min_swap = swap_toggle.getValue()
        do_diminish = diminish_toggle.getValue()
        wave_type = wave_dropdown.getSelected()

        steps = get_chord_steps(chord_num,
                                inversion_num=inversion_num,
                                seventh=True,
                                maj_minor_swap= do_maj_min_swap,
                                diminish=do_diminish)
        freqs = get_chord_freqs(root_num, steps)
        chord_wave = play_chord(freqs, wave_type)

        # record chord type so graph title is correct
        last_played_type = check_chord_swap(chords[chord_num]['type'], do_maj_min_swap)

        title = note_nums[root_num] + " " + last_played_type
        plot(get_sample_times(), chord_wave, title, 600)
        play_now = False

    # Clear the screen
    screen.fill((35, 35, 35))
    key_output.setText("Key: " + keys[key_num])
    chord_output.setText("Chord: " + str(chords[chord_num]['label']))

    inversion_output.setText("Inversion: " + str(inversion_slider.getValue()))
    octave_output.setText("Octave: " + str(octave_slider.getValue()))
    seventh_output.setText("7ths")
    diminish_output.setText("Diminish")
    swap_output.setText("Swap Maj/Min")

    pygame_widgets.update(events)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()