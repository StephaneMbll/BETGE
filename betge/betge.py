import mne
import numpy as np
import pandas as pd

import re
import glob
import os

from pathlib import Path

def betge_symmetry(filepath):
    return betge_general("symmetry", filepath)

def betge_lucifer(filepath):
    return betge_general("lucifer", filepath)

def check_events(events, answer_array):
    for i in range(1, len(events)):
        if events[i, 2] != answer_array[i - 1]:
            return False
    return True

def time_between_events(task, events, j, df):
    stim_dur = 0
    if task == "lucifer":
        if df["group"][70] == "common":
            stim_dur = 2
        else:
            if df["no_trial"][j] < 50:
                stim_dur = 2
            else:
                stim_dur = 1

    elif task == "symmetry":
        stim_dur = 2
    bad_event = False
    if (events[j, 3]) < stim_dur:
        #print(stim_dur)
        bad_event = True
    return bad_event

def betge_general(task, filepath):
    package_dir = Path(__file__).parent.absolute()
    data_dir = os.path.join(package_dir, 'data', '*')
    raw = mne.io.read_raw_cnt(filepath, preload=True)
    raw_ref = raw.copy().set_eeg_reference('average')
    raw_ref_downsampled = raw_ref.resample(256, npad='auto')

    reg = "[0-9]{3}_"
    tmp = []
    csv = ""
    patient_number = re.findall(reg, filepath)[0][:-1]
    for filename in glob.glob(data_dir):
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

    answer_array = tmp[3:-1]
    events, events_id = mne.events_from_annotations(raw_ref_downsampled)
    #print(len(events))
    #print(len(answer_array))
    annotations = mne.annotations_from_events(events, 256)
    annotations_df = annotations.to_data_frame()
    L = [annotations_df["onset"][0]]
    for i in range(1, len(annotations_df)):
        L.append(round((annotations_df["onset"][i] - annotations_df["onset"][i - 1]).total_seconds(), 2))
    events = np.c_[events, np.array(L)]
    found = 0
    start = events_id['8']
    for i in range(len(events)):
        if (events[i, 2] == start) and not found:
            found = i
            events[i, 2] = 9
        if events[i, 2] == events_id['64']:
            events[i, 2] = 4
        if events[i, 2] == events_id['1']:
            events[i, 2] = 1
        if '16' in events_id.keys():
            if events[i, 2] == events_id['16']:
                events[i, 2] = 4
        if '32' in events_id.keys():
            if events[i, 2] == events_id['32']:
                events[i, 2] = 4
        if '2' in events_id.keys():
            if events[i, 2] == events_id['2']:
                events[i, 2] = 4
        if '4' in events_id.keys():
            if events[i, 2] == events_id['4']:
                events[i, 2] = 4

    events = events[found:-1, ]  # on a les nouveaux events, qu'il faut nettoyer
    #print('len(events) after cleaning : ', len(events))
    events_id = {'1': 1, '2': 1, '4': 1, '16': 4, '32': 4, '64': 4, '8': 9}
    for i in ['2', '4', '16', '32']:
        if i not in events_id.keys():
            del events_id[i]

    for i in range(1, 100):
        print(i, events[i, 2], answer_array[i - 1], events[i, 2] == answer_array[i - 1], events[i, 3])
    # for i in range(1, len(events[:, 2])):
    #    print(i, events[i, 2], answer_array[i+1], events[i, 2] == answer_array[i+1])

    # on sélectionne le premier flag car apparition première image,
    # et on enlève le dernier event car ne nous sert à rien

    j = 1  # on regarde pas le premier c'est le flag de départ
    del_list = []

    while j < len(events):
        if events[j, 2] != answer_array[j - 1] or time_between_events(task, events, j, df):
            events = np.delete(events, j, 0)
            del_list.append(j)
        j += 1
    print("check_events = ",
          check_events(events, answer_array))  # check si les nouveaux events fittent bien avec answer_array
    print("patient_id : ", patient_number, "| task : ", task)
    if len(del_list) == 0:
        print("Aucun bad event a été supprimé !\n")
    elif len(del_list) == 1:
        print(len(del_list), "bad event a été supprimé ! bad_event =", del_list, "\n")
    else:
        print(len(del_list), "bad events ont été supprimés ! bad_events =", del_list, "\n")
    events = np.delete(events, 3, 1)
    events = events.astype(int)
    return build_epoch(raw_ref_downsampled, events, events_id)


def build_epoch(raw_ref_downsampled, eeg_events, events_id):
    picks = mne.pick_types(raw_ref_downsampled.info, eeg=True, stim=False, exclude='bads')
    tmin = -0.2
    tmax = 0.4
    baseline = None
    reject = dict(eeg=150e-6)
    epochs = mne.Epochs(raw_ref_downsampled, eeg_events, events_id, tmin, tmax,
                        picks=picks,
                        baseline=baseline)
    epochs.drop_bad()
    return epochs
