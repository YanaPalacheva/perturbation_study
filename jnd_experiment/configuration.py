from resources import pitch_FL_text, pause_text

general_experiment_configs = {"task_types": ["pitch", "FL", "pause"],
                              "num_runs": 3,
                              "num_trials_each_run": 60,
                              "base_stimuli_path": 'audio/',  # input path is generated as base_stimuli_path+task name
                              "output_path": 'results/'}


def get_task_specific_config(task, subfolder):
    config = {"task": "", "stim_prefix": "", "instructions": "",
              "stimuli_path": "",
              "baseline": 0, "initial_difference": 0}
    if subfolder == 'ch':
        if task == "pitch":
            config['task'] = "pitch"
            config['stim_prefix'] = f'nelli_{subfolder}_rise'
            config['baseline'] = 0.01
            config['initial_difference'] = 13.1
        elif task == "pause":
            config['task'] = "pause"
            config['stim_prefix'] = f'lilli_lisa_{subfolder}_{task}'
            config['baseline'] = 0.005
            config['initial_difference'] = 0.540  # todo check if still relevant changed here
        elif task == "FL":
            config['task'] = "FL"
            config['stim_prefix'] = f'mimmi_{subfolder}_{task}'
            config['baseline'] = 0.002
            config['initial_difference'] = 0.162
        else:
            raise Exception(f"No configs for task {task} specified")
    elif subfolder == '03':
        if task == "pitch":
            config['stim_prefix'] = f'manni_{subfolder}_rise'
            config['baseline'] = 0.1
            config['initial_difference'] = 16.6
        elif task == "pause":
            config['stim_prefix'] = f'lilli_manu_{subfolder}_{task}'
            config['baseline'] = 0.005
            config['initial_difference'] = 0.530
        elif task == "FL":
            config['stim_prefix'] = f'mimmi_{subfolder}_{task}'
            config['baseline'] = 0.002
            config['initial_difference'] = 0.199
        else:
            raise Exception(f"No configs for task {task} specified")
    else:
        raise Exception(f"No data in {subfolder} subfolder")
    if task == 'pitch' or task == 'FL':
        config['instructions'] = pitch_FL_text
    elif task == 'pause':
        config['instructions'] = pause_text
    config["stimuli_path"] = f"{general_experiment_configs['base_stimuli_path']}audio-{task}/{subfolder}/"
    return config


def get_step_size(task, first_incorrect=False, test_difference=1000):
    if task == "pitch":
        if test_difference <= 2:
            return 0.1
        elif first_incorrect:
            return 0.3
        else:
            return 0.5
    if task == "FL":
        if test_difference <= 0.02:
            return 0.001
        elif first_incorrect:
            return 0.003
        else:
            return 0.005

    if task == "pause":
        if test_difference <= 0.095:
            return 0.005
        elif first_incorrect:
            return 0.01
        else:
            return 0.015


# def get_step_size_old(task, subfolder, correct_answers):
#     if task == "pitch":
#         if correct_answers <= 10:
#             return 0.5
#         elif correct_answers <= 20:
#             return 0.4
#         elif correct_answers <= 30:
#             return 0.3
#         elif correct_answers <= 40:
#             return 0.2
#         else:
#             return 0.1
#         pass
#     if subfolder == 'ch':
#         if task == "pause":
#             if correct_answers <= 15:
#                 return 0.015
#             elif correct_answers <= 40:
#                 return 0.01
#             else:
#                 return 0.005
#         else:  # task = "FL"
#             if correct_answers <= 12:
#                 return 0.005
#             elif correct_answers <= 22:
#                 return 0.004
#             elif correct_answers <= 32:
#                 return 0.003
#             elif correct_answers <= 41:
#                 return 0.002
#             else:
#                 return 0.001
#     elif subfolder == '03':
#         if task == "pause":
#             if correct_answers <= 6:
#                 return 0.015
#             elif correct_answers <= 35:
#                 return 0.01
#             else:
#                 return 0.005
#         else:  # task = "FL"
#             if correct_answers <= 14:
#                 return 0.005
#             elif correct_answers <= 28:
#                 return 0.004
#             elif correct_answers <= 40:
#                 return 0.003
#             elif correct_answers <= 50:
#                 return 0.002
#             else:
#                 return 0.001
