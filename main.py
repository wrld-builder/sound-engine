from volume_gen import MelodyNotesGenerator, BeepGenerator
import pyaudio
import time

if __name__ == '__main__':
    mg = MelodyNotesGenerator(44100)
    tones = mg.generate_tones(0.64)

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(width=2), channels=2, rate=mg.samplerate, output=True)

    for i in range(len(tones)):
        stream.write(tones[i])

    bg = BeepGenerator(2500, 3, 50000, 10000, max_duration_ms=1000)
    bg.generate_random_beep_np()
    time.sleep(1)
    for _ in range(10):
        bg.generate_random_win_beep()
