"""
Pitch JND task procedure, based on Contributions of Auditory and Somatosensory Feedback to Vocal Motor Control
by Smith et al.
"""
from psychopy import core, sound, visual, gui, data, event, prefs
import random
import glob
import os
import time

prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

# the pre-recorded stimuli should follow the following naming convention: word_pitch.wav (e.g. moni_400.wav)
stimuli_path = 'audio_stimuli/'
output_path = 'results/'
if not os.path.exists(output_path):
    os.mkdir(output_path)
stimuli = glob.glob(stimuli_path + '*.wav')

experiment_name = "JND_Pitch"
stim_name = 'moni'
# here and later: the f0 measurement unit is cent
baseline_pitch = 400
initial_difference = 50
# change_boundaries = range(0, 800)

exp_config = {'subject': 'SUBJECT_ID', 'cur_date': data.getDateStr()}

dlg = gui.DlgFromDict(exp_config, title=f'{experiment_name} Experiment', fixed=['cur_date'])

# make a text file to save data
output_filename = experiment_name + '_' + exp_config['subject'] + '_' + exp_config['cur_date'] + '.csv'
experiment_output = open(output_path + output_filename, 'w')
experiment_output.write('trial,recording_A,recording_B,recording_X,response,correct,difference,direction\n')

# initial window
win = visual.Window([800, 600], allowGUI=True, monitor='testMonitor', units='deg')
# win = visual.Window(fullscr=True)

# display instructions and wait
message1 = visual.TextStim(win, pos=[0, 0],
                           text="You will be presented with three recordings. Please listen to each recording carefully."
                                "The third recoding will be similar to either the first (A) or the second (B).\n"
                                "Press '<- A' (left) if the third and the first (A) recordings are similar."
                                "'B ->' (right) if the third and the second (B) recordings are similar.\n")
message2 = visual.TextStim(win, pos=[0, -7], text='Hit any key when ready.')

message1.draw()
message2.draw()
win.flip()  # to display the messages
event.waitKeys()  # wait until there's a keypress

# create visuals
a_label = visual.TextStim(win, pos=[-7, -5], text="<- A")
b_label = visual.TextStim(win, pos=[+7, -5], text='B ->')


# logic (implementation of an algorithm described in Smith et al.)
baseline_stimulus = f'{stimuli_path}{stim_name}_{baseline_pitch}.wav'
test_stimulus = f'{stimuli_path}{stim_name}_{baseline_pitch+initial_difference}.wav'
current_difference = initial_difference
step_size = 10
two_down_one_up = False
correct_in_a_row = 1
trial_index = 0  # the number of trials aka choices (from 0 to 60)
reversals = -1  # number of times the direction of the staircase is changed (up/down)
previous_direction = 'none'

recording_len = 2  # seconds

# trial session
while trial_index < 60 or reversals < 10:  # stop conditions
    # window set-up
    a_label.draw()
    b_label.draw()
    win.flip()  # flip window

    # listening phase
    recording_A, recording_B = random.sample([baseline_stimulus, test_stimulus], k=2)
    stimulus_A = sound.Sound(recording_A)
    stimulus_B = sound.Sound(recording_B)
    AB_dict = {'A': recording_A, 'B': recording_B}
    x_key = random.choice(['A', 'B'])
    recording_X = AB_dict[x_key]
    stimulus_X = sound.Sound(recording_X)
    stimulus_A.play()
    time.sleep(recording_len+0.5)  # interstimulus interval 500 ms
    stimulus_B.play()
    time.sleep(recording_len+0.5)  # interstimulus interval 500 ms
    stimulus_X.play()
    keys = event.waitKeys()

    # evaluation phase
    key_choice_map = {'left': 'A', 'right': 'B'}
    participant_choice = key_choice_map.get(keys[0], None)
    if participant_choice == x_key:
        correct = True
        correct_in_a_row += 1
        if correct_in_a_row >= 2:
            direction = 'down'
            new_difference = current_difference - step_size
        else:
            direction = 'none'
            new_difference = current_difference
    else:
        correct = False
        correct_in_a_row = 0
        direction = 'up'
        if not two_down_one_up:
            two_down_one_up = True
            new_difference = current_difference + step_size
            step_size = 4
        else:
            new_difference = current_difference + step_size

    experiment_output.write(','.join([str(trial_index+1), recording_A, recording_B, recording_X,
                                     participant_choice, str(correct), str(current_difference), direction]) + '\n')
    # prepare for the next iteration
    trial_index += 1
    current_difference = new_difference
    if current_difference <= 10 and step_size != 1:
        step_size = 1
    if previous_direction != direction:
        reversals += 1
    previous_direction = direction
    test_stimulus = f'{stimuli_path}{stim_name}_{baseline_pitch + current_difference}.wav'

experiment_output.close()

# give some on-screen feedback
feedback1 = visual.TextStim(
        win, pos=[0,+3],
        text='Good job, thank you! Press any key to finish :)')

win.flip()
event.waitKeys()  # wait for participant to respond

win.close()
core.quit()
