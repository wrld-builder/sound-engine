import random
import numpy as np
import sounddevice as sd
import winsound

class BeepGenerator:
    def __init__(self, max_freq, max_duration_s, samplerate, amplitude, max_duration_ms=None):
        self.__MAX_FREQUENCY = max_freq
        self.__MAX_DURATION = max_duration_s
        self.__MAX_DURATION_MS = max_duration_ms     # for using win_beep
        self.__samplerate = samplerate       # set a bit rate
        self.__amplitude = amplitude

    def __repr__(self):
        return \
            'Max frequency: {}\n' \
            'Max duration: {}\n' \
            'Max duration(ms, for winsound): {}\n' \
            'Samplerate: {}\n' \
            'Amplitude: {}'\
            .format(self.__MAX_FREQUENCY, self.__MAX_DURATION, self.__MAX_DURATION_MS, self.__samplerate, self.__amplitude)

    def generate_random_beep_np(self):
        random_frequency = random.randint(1, self.__MAX_FREQUENCY)
        random_duration = random.randint(1, self.__MAX_DURATION)
        new_time = np.arange(random_duration * self.__samplerate) / self.__samplerate
        signal = self.__amplitude * np.sin(2 * np.pi * random_frequency * new_time)
        sd.play(signal)
        sd.wait()

    def generate_random_win_beep(self):
        if self.__MAX_DURATION_MS is None: raise ValueError('Exception: MS_DURATION not allowed')
        random_frequency = random.randint(1, self.__MAX_FREQUENCY)
        random_duration = random.randint(1, self.__MAX_DURATION_MS)
        winsound.Beep(random_frequency, random_duration)

    @property
    def samplerate(self):
        return self.__samplerate

    @samplerate.setter
    def samplerate(self, new_samplerate):
        self.samplerate = new_samplerate

class MelodyNotesGenerator:
    def __init__(self, samplerate):
        self.__BIT_COUNT = 2 ** 16  # 16-bit sound
        self.__samplerate = samplerate  # set a bit rate
        self.__notes_freq_array = np.array([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88])  # notes [1 oct.]

    def generate_sample(self, frequency, duration, volume):
        new_amplitude = np.round(volume * self.__BIT_COUNT)
        total_samples_count = np.round(self.__samplerate * duration)
        new_frequency = float(2) * np.pi * frequency / self.__samplerate
        return np.round(new_amplitude * np.sin(np.arange(0, total_samples_count) * new_frequency))

    def generate_tones(self, duration):
        tones = []

        for freq in self.__notes_freq_array:
            tone = np.array(self.generate_sample(freq, duration, 1.0), dtype=np.int16)
            tones.append(tone)
        return tones

    @property
    def samplerate(self):
        return self.__samplerate

    @samplerate.setter
    def samplerate(self, new_rate):
        self.__samplerate = new_rate
