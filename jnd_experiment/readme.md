### Step by step guide on executing the JND experiment

The staircase algorithm is based on the paper [Contributions of Auditory and Somatosensory Feedback to Vocal Motor Control](https://pubs.asha.org/doi/full/10.1044/2020_JSLHR-19-00296) by Smith et al. 
We used [PsychoPy](https://www.psychopy.org/) to set up the experiment. This code is tested on Python 3.8.

**Preparation:**
* clone this repository with `git clone https://github.com/YanaPalacheva/perturbation_study.git`
* prepare a virtual environment for the experiment 
    * e.g. if you use Anaconda, run in Anaconda Prompt the following commands:
        * `conda conda create -n jnd_env python=3.8`
        * `conda activate jnd_env`
        * `pip install psychopy librosa`
        * `cd YOUR_PATH/perturbation_study/jnd_experiment`
* create a folder "**audio**" and put there the stimuli recordings (for this experiment: **audio-FL, audio-pause, audio-pitch**)

**Run experiment:** `python jnd_experiment.py`

First, a small dialogue window will appear. Enter the subject id, name of the subfolder (here: **ch** or **03**) and press "OK". The follow the visual cues in the newly opened window.
The results will be recorded in the file "JND_*TaskName*\_*SUBJECTID*_*timestamp*.csv" in the "**results**" folder.
