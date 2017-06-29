import mne
from mne import io, Epochs
from mne.preprocessing import ICA

def plot_data(fname):
    raw = io.read_raw_eeglab('109_raw.set')
    raw.plot(block=True)