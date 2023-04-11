from Line import *
from find_peaks import *

def upAndOver(start, end, max_alt):
    line = Line(start, end).getLine()
    peaks = findPeaks(line, max_alt)
    ascent = 0

    for peak in peaks:
        peak_alt = Altitude(peak).getAltitude
        ascent += (peak_alt - max_alt)

    return ascent


if __name__ == "__main__":
    upAndOver((51.838353847600885, -10.156763362936477),(51.679318843246996, -9.451819063072634), 400)
