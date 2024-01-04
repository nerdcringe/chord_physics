# Chord Physics with Pygame
A little Pygame application that makes it easy to play chords and experiment with music theory.
It generates Pygame Sndarray objects with Numpy and plays the sounds through the Pygame Mixer.
I made a UI to control the key, octave, chord, and more settings. Each chord is played by pressing the number keys on the keyboard.

![image](https://github.com/nerdcringe/chord_physics/assets/54510965/e5eddb9b-c98c-4c81-a37e-45d97b5cb99e)

## Waveforms
For fun, I made it so you could select a different waveform to play. It includes the basic shapes: sine, square, sawtooth, and triangle. The waves are graphed with matplotlib.
On the left is the amplitude vs. time graph, and on the right is the amplitude vs. frequency graph (found with fourier transform)

Here's sine, square, sawtooth, and triangle respectively:
![image](https://github.com/nerdcringe/chord_physics/assets/54510965/c677a942-143b-441e-aa85-2cba37372d10)
![image](https://github.com/nerdcringe/chord_physics/assets/54510965/22b0d757-89f0-4ff7-891e-c79ec49144da)
![image](https://github.com/nerdcringe/chord_physics/assets/54510965/55997dac-4a49-4c88-b22b-525c089d0d7b)
![image](https://github.com/nerdcringe/chord_physics/assets/54510965/46e31d2a-8382-4d12-9bbb-cd3e2ba923c5)


After making this, I started making a physical project to play chords with an Arduino. See it here! https://github.com/nerdcringe/arduino-chord-player.
