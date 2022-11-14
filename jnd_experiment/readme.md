### Step by step guide on executing the JND experiment

The staircase algorithm is based on the paper [Contributions of Auditory and Somatosensory Feedback to Vocal Motor Control](https://pubs.asha.org/doi/full/10.1044/2020_JSLHR-19-00296) by Smith et al. 
We used [PsychoPy](https://www.psychopy.org/) to set up the experiment.

**Preparation:**
* clone this repository with `git clone https://github.com/YanaPalacheva/perturbation_study.git`
* prepare a virtual environment for the experiment 
    * e.g. if you use Anaconda, run in Anaconda Prompt the following commands:
        * `conda conda create -n jnd_env python=3.8`
        * `pip install psychopy`
        * `cd YOUR_PATH/perturbation_study/jnd_experiment`
* create a folder "**audio_stimuli**" and put there the stimuli recordings 
(the filenames should follow the convention id_pitch.wav, e.g. moni_400.wav)

**Run experiment:** `python audio_jnd.py`

First, a small dialogue window will appear. Enter the subject id and press "OK". The follow the visual cues in the newly opened window.
The results will be recorded in the file "JND_Pitch_*SUBJECTID*_*timestamp*.csv" in the "**results**" folder.
