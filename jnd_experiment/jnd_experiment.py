from psychopy import core, visual, gui, data, event, prefs
from configuration import general_experiment_configs
from audio_jnd import run_jnd_task
from pathchecks import check_config_paths
import random

prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo', 'pygame']
# todo: add quit option, make fullscreen

check_config_paths(general_experiment_configs["base_stimuli_path"],
                   general_experiment_configs["task_types"],
                   general_experiment_configs["output_path"])  # make sure that in and out paths exist

# show initial dialog (timestamp and date)
exp_data = {'subject': 'SUBJECT_ID', 'cur_date': data.getDateStr(), 'subfolder': 'ch'}
dlg = gui.DlgFromDict(exp_data, title=f'JND Experiment', fixed=['cur_date'])
if not dlg.OK:
    core.quit()

# open the experiment window
win = visual.Window(size=[1000, 800], monitor='laptop', units='norm')
win.flip()

randomized_tasks = random.sample(general_experiment_configs["task_types"],
                                 k=len(general_experiment_configs["task_types"]))
for ind, task in enumerate(randomized_tasks):
    # run practice session
    run_jnd_task(exp_data, task, win, session_type='practice')

    # run the experiment
    run_jnd_task(exp_data, task, win, session_type='trial')
    # give some on-screen feedback?
    visual.TextStim(win, text=f"Sehr gut! Schon {ind+1}/{len(randomized_tasks)} geschafft. "
                              f"Drücken Sie auf den weiter-Button,"
                              f" sobald Sie bereit für die nächste Runde sind.").draw()

    win.flip()
    event.waitKeys()  # wait for participant to react by pressing any key

visual.TextStim(win, text='Gut gemacht, vielen dank! Drücken Sie eine beliebige Taste zum Beenden :)').draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
