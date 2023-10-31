
keys = ('A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#')

note_nums = {}
for i in range(88):
    note_nums[i] = keys[i % 12]


chords = {
    1: {
        'steps': 0,
        'label': 'I',
        'type': 'major',
    }, 2: {
        'steps': 2,
        'label': 'ii',
        'type': 'minor',
    }, 3: {
        'steps': 4,
        'label': 'iii',
        'type': 'minor',
    }, 4: {
        'steps': 5,
        'label': 'IV',
        'type': 'major',
    }, 5: {
        'steps': 7,
        'label': 'V',
        'type': 'major',
    }, 6: {
        'steps': 9,
        'label': 'vi',
        'type': 'minor',
    }, 7: {
        'steps': 11,
        'label': 'viiø',
        'type': 'half dim.',
    }, 8: {
        'steps': 12,
        'label': 'I',
        'type': 'major',
    },
}


# return the correct type after checking if major and minor are swapped
def check_chord_swap(diatonic_type, swapped):
    chord_type = diatonic_type
    if swapped:
        if diatonic_type == 'major':
            chord_type = 'minor'
        elif diatonic_type == 'minor':
            chord_type = 'major'
    return chord_type



def get_chord_steps(chord_num, inversion_num=0, seventh=False, maj_minor_swap=False):
    type = check_chord_swap(chords[chord_num]['type'], maj_minor_swap)
    steps_root = 0
    if type == 'major':
        steps_3rd = 4
        steps_5th = 7
        if chord_num == 5 or maj_minor_swap:
            steps_7th = 10  # dominant 7th for V chord
        else:
            steps_7th = 11
    elif type == 'minor':
        steps_3rd = 3
        steps_5th = 7
        steps_7th = 10
    else:  # half diminished
        steps_3rd = 3
        steps_5th = 6
        steps_7th = 10

    if inversion_num >= 1:
        steps_root += 12
    if inversion_num >= 2:
        steps_3rd += 12
    if inversion_num >= 3:
        steps_5th += 12

    steps = [steps_root, steps_3rd, steps_5th]
    if seventh:
        steps.append(steps_7th)
    return steps
