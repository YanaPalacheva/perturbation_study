"""
Pitch JND task procedure, based on Contributions of Auditory and Somatosensory Feedback to Vocal Motor Control
by Smith et al.
* AXB pattern (AAB or ABB sequences, randomly chosen)
"""
from psychopy import sound, visual, event
import random
import time
from librosa import get_duration
from configuration import get_step_size, get_task_specific_config, general_experiment_configs
from pathchecks import stimulus_exists


def generate_stimulus_path(path_prefix, value):
    value_suffix = str(value).replace('.', '_')
    stim_path = f'{path_prefix}_{value_suffix}.wav'
    if stimulus_exists(stim_path):
        return stim_path
    else:  # some file names are like "bla_bla_0_530.wav, number is Python are stripped from last 0
        stim_path = f'{path_prefix}_{value_suffix}0.wav'
        if stimulus_exists(stim_path):
            return stim_path
    raise Exception(f'No stimulus found: {stim_path}')


def run_jnd_task(exp_data, task, win, session_type='trial'):
    exp_config = get_task_specific_config(task, exp_data['subfolder'])
    # display instructions and wait
    instructions = visual.TextStim(win, alignText='center', height=0.05, anchorHoriz='center',
                                   text=exp_config["instructions"])

    instructions.draw()
    a_label = visual.TextStim(win, pos=[-0.5, -0.5], text="<- 1", autoDraw=True)
    b_label = visual.TextStim(win, pos=[0.5, -0.5],  text='3 ->', autoDraw=True)
    a_label.draw()
    b_label.draw()
    win.flip()  # to display the message
    event.waitKeys()  # wait until there's a keypress

    path_prefix = f'{exp_config["stimuli_path"]}{exp_config["stim_prefix"]}'

    if session_type == 'trial':
        run_trial_session(path_prefix, exp_data, exp_config)
    elif session_type == 'practice':
        run_practice_session(path_prefix, exp_config, win)
    else:
        raise Exception(f"Run type can be either 'trial' or 'practice', received {type}")


def run_trial_session(path_prefix, exp_data, exp_config):
    for run in range(general_experiment_configs['num_runs']):
        baseline_stimulus = generate_stimulus_path(path_prefix, exp_config["baseline"])
        test_value = exp_config["baseline"] + exp_config["initial_difference"]
        if exp_config["task"] == "pitch":
            test_value -= 0.01  # because the lowest value is 0.01, but we pretend it's 0
        test_stimulus = generate_stimulus_path(path_prefix, test_value)

        current_difference = exp_config["initial_difference"]
        first_incorrect = False
        step_size = get_step_size(exp_config["task"], first_incorrect)
        two_down_one_up = False
        correct_in_a_row = 1
        trial_index = 0  # the number of trials aka choices
        reversals = -1  # number of times the direction of the staircase is changed (up/down)
        previous_direction = 'none'  # that's why we initialize reversals as -1
        last_two_combinations = []  # to make sure there's no more than 3 in a row (AAB or ABB)

        output_filename = f"JND_{exp_config['task']}_{exp_data['subject']}_{exp_data['cur_date']}_run_{run+1}.csv"
        experiment_output = open(general_experiment_configs['output_path'] + output_filename, 'w')
        # todo: add triplet pattern (aab or abb)
        experiment_output.write('trial,recording_A,recording_B,recording_X,response,correct,difference,direction\n')

        while trial_index < general_experiment_configs["num_trials_each-run"] or reversals < 10:  # stop conditions
            # randomization phase
            recording_A, recording_B = random.sample([baseline_stimulus, test_stimulus], k=2)
            AB_dict = {'1': recording_A, '3': recording_B}
            x_key = random.choice(['1', '3'])
            current_combination = f"1{x_key}3"

            if len(last_two_combinations) < 2:
                last_two_combinations.append(current_combination)
            elif last_two_combinations[0] == last_two_combinations[1]:
                while current_combination == last_two_combinations[0]:
                    x_key = random.choice(['1', '3'])
                    current_combination = f"1{x_key}3"
                last_two_combinations[0] = last_two_combinations[1]
                last_two_combinations[1] = current_combination

            recording_X = AB_dict[x_key]

            # listening phase
            stimulus_A = sound.Sound(recording_A)
            stimulus_B = sound.Sound(recording_B)
            stimulus_X = sound.Sound(recording_X)
            stimulus_A.play()
            time.sleep(get_duration(path=recording_A) + 0.5)  # interstimulus interval 500 ms
            stimulus_X.play()
            time.sleep(get_duration(path=recording_X) + 0.5)  # interstimulus interval 500 ms
            stimulus_B.play()
            keys = event.waitKeys()

            # evaluation phase
            key_choice_map = {'left': '1', 'right': '3'}
            participant_choice = key_choice_map.get(keys[0], None)
            if participant_choice == x_key: # correct
                correct = True
                correct_in_a_row += 1
                if not two_down_one_up:
                    direction = 'down'
                    new_difference = current_difference - step_size
                else:
                    if correct_in_a_row >= 2:
                        direction = 'down'
                        new_difference = current_difference - step_size
                    else:
                        direction = 'none'
                        new_difference = current_difference
            else:
                correct = False
                first_incorrect = True
                two_down_one_up = True
                correct_in_a_row = 0
                direction = 'up'
                new_difference = current_difference + step_size

            experiment_output.write(','.join([str(trial_index+1), recording_A, recording_X, recording_B,
                                             participant_choice, str(correct), str(current_difference), direction]) + '\n')

            # prepare for the next iteration
            trial_index += 1
            current_difference = new_difference
            step_size = get_step_size(exp_config["task"], first_incorrect, test_difference=current_difference)
            if previous_direction != direction:
                reversals += 1
            previous_direction = direction
            test_stimulus = generate_stimulus_path(path_prefix, exp_config['baseline'] + current_difference)

        experiment_output.close()


def run_practice_session(path_prefix, exp_config, win):
    baseline_stimulus = generate_stimulus_path(path_prefix, exp_config["baseline"])
    test_value = exp_config["baseline"] + exp_config["initial_difference"]
    if exp_config["task"] == "pitch":
        test_value -= 0.01
    test_stimulus = generate_stimulus_path(path_prefix, test_value)
    stimulus_A = sound.Sound(baseline_stimulus)
    stimulus_B = sound.Sound(test_stimulus)
    A_rec_len = get_duration(path=baseline_stimulus)
    B_rec_len = get_duration(path=test_stimulus)

    # 2 runs (AAB and ABB)
    for stimulus_X, correct_choice, X_rec_length in [(stimulus_A, '3', A_rec_len), (stimulus_B, '1', B_rec_len)]:
        participant_choice = not correct_choice
        # todo: change to at least 3 practice trials

        while participant_choice != correct_choice:
            win.flip()
            stimulus_A.play()
            time.sleep(A_rec_len + 1)  # interstimulus interval 500 ms # todo 500 ms is too little I think
            stimulus_X.play()
            time.sleep(X_rec_length + 1)  # interstimulus interval 500 ms
            stimulus_B.play()
            keys = event.waitKeys()
            key_choice_map = {'left': '1', 'right': '3'}
            participant_choice = key_choice_map.get(keys[0], None)
            if participant_choice != correct_choice:
                feedback = visual.TextStim(win, text="Falsch, versuchen Sie bitte nochmal.")
                feedback.draw()
                win.flip()
                time.sleep(1)

        # assuming whe loop is finished because of the correct answer, not the endless looping
        feedback = visual.TextStim(win, text="Richtig!")
        feedback.draw()
        win.flip()
        time.sleep(1)
    return

