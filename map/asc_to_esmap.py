import os
import re
import sys
import math
import struct


def asc_to_esmap(folder):

    ncols = 1
    nrows = 1
    cellsize = 1
    lon = 0.0
    lat = 0.0
    nodata = 0
    top = 0
    EQUATOR_DEG = 40075000 / 360

    data = []

    with open(os.path.join(folder, 'map.asc')) as f:

        n = 1

        for line in f:

            if n > 6:

                for d in line.strip(' ').replace('\n', '').split(' '):
                    int_d = int(d)

                    if int_d == nodata:
                        int_d = 0

                    data.append(int_d)

                    if int_d > top:
                        top = int_d

                continue

            if line.startswith('ncols'):
                ncols = int(line[13:])\

            if line.startswith('nrows'):
                nrows = int(line[13:])

            if line.startswith('xllcorner'):
                lon = float(line[13:])

            if line.startswith('yllcorner'):
                lat = float(line[13:])

            if line.startswith('NODATA_value'):
                nodata = int(line[13:])

            if line.startswith('cellsize'):
                cellsize = math.cos(lat*math.pi/180) * EQUATOR_DEG * float(line[13:]) # Get the cellsize in meters
                print(math.cos(lat))
                print(EQUATOR_DEG)
                print(float(line[13:]))
                print(line)


            n += 1

    with open(os.path.join(folder, 'map.esmap'), 'wb') as f:
        print(cellsize)
        f.write(struct.pack('=HHhf', ncols, nrows, top, cellsize))

        for d in data:
            f.write(struct.pack('=h', d))
        

if __name__ == '__main__':

    if len(sys.argv) != 2:
        exit()

    asc_to_esmap(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            sys.argv[1]
        )
    )
    