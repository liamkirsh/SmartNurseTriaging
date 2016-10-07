import pyaudio
import wave
from aubio import tempo, source
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "output.wav"

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

sys.exit(0)

filename = WAVE_OUTPUT_FILENAME

samplerate = 0
#if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    if is_beat:
        this_beat = o.get_last_s()
        beats.append(this_beat)
    total_frames += read
    if read < hop_s: break

if len(beats) > 1:
    # do plotting
    from numpy import mean, median, diff
    import matplotlib.pyplot as plt
    bpms = 60./ diff(beats)
    print('mean period: %.2fbpm, median: %.2fbpm' % (mean(bpms), median(bpms)))
    print('plotting %s' % filename)
    plt1 = plt.axes([0.1, 0.75, 0.8, 0.19])
    plt2 = plt.axes([0.1, 0.1, 0.8, 0.65], sharex = plt1)
    plt.rc('lines',linewidth='.8')
    for stamp in beats: plt1.plot([stamp, stamp], [-1., 1.], '-r')
    plt1.axis(xmin = 0., xmax = total_frames / float(samplerate) )
    plt1.xaxis.set_visible(False)
    plt1.yaxis.set_visible(False)

    # plot actual periods
    plt2.plot(beats[1:], bpms, '-', label = 'raw')

    # plot moving median of 5 last periods
    median_win_s = 5
    bpms_median = [ median(bpms[i:i + median_win_s:1]) for i in range(len(bpms) - median_win_s ) ]
    plt2.plot(beats[median_win_s+1:], bpms_median, '-', label = 'median of %d' % median_win_s)
    # plot moving median of 10 last periods
    median_win_s = 20
    bpms_median = [ median(bpms[i:i + median_win_s:1]) for i in range(len(bpms) - median_win_s ) ]
    plt2.plot(beats[median_win_s+1:], bpms_median, '-', label = 'median of %d' % median_win_s)

    plt2.axis(ymin = min(bpms), ymax = max(bpms))
    #plt2.axis(ymin = 40, ymax = 240)
    plt.xlabel('time (mm:ss)')
    plt.ylabel('beats per minute (bpm)')
    plt2.set_xticklabels([ "%02d:%02d" % (t/60, t%60) for t in plt2.get_xticks()[:-1]], rotation = 50)

    #plt.savefig('/tmp/t.png', dpi=200)
    plt2.legend()
    plt.show()

else:
    print('mean period: %.2fbpm, median: %.2fbpm' % (0, 0))
    print('plotting %s' % filename)