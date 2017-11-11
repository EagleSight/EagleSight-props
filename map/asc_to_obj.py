import os
import re
import sys
import math


def asc_to_obj(folder):

    ncols = 1
    nrows = 1
    cellsize = 1
    nodata = 0
    distance = 0.1

    data = []

    with open(os.path.join(folder, 'map.asc')) as f:

        n = 1

        for line in f:

            if n > 6:

                for d in line.strip(' ').replace('\n', '').split(' '):
                    data.append(int(d))

                continue

            if line.startswith('ncols'):
                ncols = int(line[13:])
            
            if line.startswith('nrows'):
                nrows = int(line[13:])

            if line.startswith('cellsize'):
                cellsize = float(line[13:]) * 1 / distance

            n += 1

    with open(os.path.join(folder, 'map.obj'), 'w') as f:

        for i, d in enumerate(data):
            f.write('v ' + ' '.join([
                str(math.floor(i / nrows) * distance),
                str(round(d * cellsize, 5)),
                str((i % nrows) * distance)
            ]) + '\n')                                                                                              
        

        for i, d in enumerate(data):

            f.write('v ' + ' '.join([
                str(math.floor(i / nrows) * distance),
                str(round(d * cellsize, 5)),
                str((i % nrows) * distance)
            ]) + '\n')                                                                                              
        

if __name__ == '__main__':

    if len(sys.argv) != 2:
        exit()

    asc_to_obj(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            sys.argv[1]
        )
    )
    