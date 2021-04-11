# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 2015
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[Exps.SoundCard] Importing dependencies...')
import numpy as np
from queue import Queue, Empty

from sciscripts.Analysis.Plot import Plot
from sciscripts.IO import SoundCard
print('[Exps.SoundCard] Done.')


def Oscilloscope(Rate, XLim, YLim, System, FramesPerBuffer=512, Rec=False):
    """
        Read data from sound board input and plot it until the windows is
        closed (with a delay).
        Pieces of code were taken from Sounddevice's readthedocs page:
        https://python-sounddevice.readthedocs.io/en/0.3.12/examples.html#plot-microphone-signal-s-in-real-time
    """

    Animation = Plot.Return('animation')
    plt = Plot.Return('plt')

    Channels = [0]
    DownSample = 10
    Window = 200
    Interval = 30
    SoundQueue = Queue()

    SoundCard.AudioSet(Rate)

    def audio_callback(indata, outdata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status: print(status, flush=True)
        SoundQueue.put(indata[::DownSample, Channels])


    def PltUp(n):
        global DataPlot
        Block = True

        while True:
            try:
                Data = SoundQueue.get(block=Block)
                Data = SoundCard.DAqs.Normalize(Data, System, 'In')
            except Empty:
                break
            Shift = len(Data)
            DataPlot = np.roll(DataPlot, -Shift, axis=0)
            DataPlot[-Shift:, :] = Data
            Block = False

        for Col, Line in enumerate(Lines):
            Line.set_ydata(DataPlot[:, Col])

        return(Lines)

    DataLength = int(Window * Rate / (1000 * DownSample))
    DataPlot = np.zeros((DataLength, len(Channels)))

    Fig, Ax = plt.subplots()
    Lines = Ax.plot(DataPlot)

    if len(Channels) > 1:
        Ax.legend(['Channel {}'.format(Channel) for Channel in Channels],
                  loc='lower left', ncol=len(Channels))

    Ax.axis((0, len(DataPlot), -1, 1))
    Ax.set_yticks([0])
    Ax.yaxis.grid(True)
    Ax.tick_params(bottom='off', top='off', labelbottom='off',
                   right='off', left='off', labelleft='off')
    Ax.set_xlim(XLim)
    Ax.set_ylim(YLim)
    Fig.tight_layout(pad=0)

    Stream = SoundCard.SD.Stream(channels=max(Channels)+1, blocksize=0, callback=audio_callback, never_drop_input=True)
    Anim = Animation(Fig, PltUp, interval=Interval, blit=False)

    with Stream:
        plt.show()

   # if Rec:
       # Writers = Animation.writers['ffmpeg']
       # Writer = Writers(fps=15, metadata=dict(artist='Me'))
       # Anim.save('MicrOscilloscope.mp4', writer=Writer)

   # plt.show()

    return(None)


