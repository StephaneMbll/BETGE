import mne
import numpy as np
import pandas as pd

import re
import glob
import os

def betge_symmetry(filepath):
    return betge_general("symmetry", filepath)

def betge_lucifer(filepath):
    return betge_general("lucifer", filepath)

def betge_general(task, filepath):
    raw = mne.io.read_raw_cnt(filepath, preload=True)
    raw_ref = raw.copy().set_eeg_reference('average')
    raw_ref_downsampled = raw_ref.resample(256, npad='auto')

    reg = "[0-9]{3}_"
    tmp = []
    csv = ""
    patient_number = re.findall(reg, filepath)[0][:-1]
    for filename in glob.glob("betge/data/*"):
        if patient_number in filename:
            tmp.append(filename)
    for found in tmp:
        if task in found:
            csv = found
    df = pd.read_csv(csv)

    tmp = 0
    df['new_col'] = 4
    if task == "lucifer":
        df.loc[df['left_ans'] == df['ans_candidate'], 'new_col'] = 1
    else:
        df.loc[df["ans_candidate"] == 0, 'new_col'] = 1
    tmp = df['new_col'].to_numpy()

    answer_array = tmp[3:]
    events, events_id = mne.events_from_annotations(raw_ref_downsampled)
    print(events_id)
    events_id = {'1' : 1, '64' : 4}

    found = 0
    if task == "lucifer":
        start = 6
    else:
        start = 3
    for i in range(len(events)):
        if (events[i][2] == start) and not found:
            found = i
        if (events[i][2] == 2 or (task == "lucifer" and events[i][2] == 3)):
            events[i][2] = 4
    events = events[found+1:]

    tmp_answer = answer_array[-1]
    answer_array[-1] = -1

    j = 0
    del_list = []
    end = False

    for answer in answer_array:
        if (answer == -1):
            end = True
            answer = tmp_answer
        while(j < len(events) and (events[j][2] != answer or answer == -1)):
            del_list.append(j)
            j += 1
        j += 1
        if (end):
            while(j < len(events)):
                del_list.append(j)
                j += 1

    events = np.delete(events, del_list, 0)
    return build_epoch(raw_ref_downsampled, events, events_id)

def build_epoch(raw_ref_downsampled, eeg_events, events_id):
    picks = mne.pick_types(raw_ref_downsampled.info, eeg=True, stim=False, exclude='bads')
    tmin = -0.250
    tmax = 0.250
    baseline = None
    reject = dict(eeg=150e-6)
    epochs = mne.Epochs(raw_ref_downsampled, eeg_events, events_id, tmin, tmax,
            picks = picks,
            baseline = baseline)
    epochs.drop_bad()
    return epochs
