import os
import re
import math
import sys


def convert(folder):
    cellsize = 1.0
    nodata_value = -9999
    cols_count = 1
    rows_count = 1

    point_distance = 0.1

    water = 0

    data = []

    asc_file = os.path.join(folder, 'map.asc')

    if not os.path.exists(asc_file) and not os.path.isfile(asc_file):
        print('')
        return

    # Open the Arc ASCII file
    with open(asc_file) as f:

        line_number = 0
        vertex_index = 1

        for line in f:
            if line_number > 5:
                for i in line.replace('\n', '').split(' ')[1:]:
                    h = int(i)
                    if h == water or h == nodata_value:
                        data.append((0, vertex_index))
                    else:
                        data.append((h, vertex_index))
                        vertex_index += 1

                continue

            if line.startswith('cellsize'):
                cellsize = float(re.sub(' +', ' ', line).replace('\n','').split(' ')[1]) * (1 / point_distance)

            if line.startswith('NODATA_value'):
                nodata_value = int(re.sub(' +', ' ', line).replace('\n','').split(' ')[1])

            if line.startswith('ncols'):
                cols_count = int(re.sub(' +', ' ', line).replace('\n','').split(' ')[1])
            if line.startswith('nrows'):
                rows_count = int(re.sub(' +', ' ', line).replace('\n','').split(' ')[1])

            line_number += 1

    # Write the .obj file
    with open(os.path.join(folder, './map.obj'), mode='w') as f:

        print('Doing points...')

        # Write all the points
        for i, d in enumerate(data):

            if d[1] != -1:
                f.write('v ' + ' '.join([
                    str(round((i % cols_count) * point_distance, 5)),
                    str(round(d[0] * cellsize, 8)),
                    str(round(math.floor(i / cols_count) * point_distance, 5))
                    ]) + '\n')


        last_of_line = cols_count - 1
        stop_at = len(data) - cols_count - 1 #We want to stop one "line" before the end

        print('Doing faces...')
        # Write all the faces
        for i, d in enumerate(data):
            if i > stop_at:
                break

            if i % cols_count == last_of_line:
                continue

            # Face 1
            f.write('f ' + ' '.join([
                str(data[i][1]),
                str(data[i+1][1]),
                str(data[i+cols_count+1][1]),
                str(data[i+cols_count][1])
                ]) + '\n')


if __name__ == '__main__':

    if len(sys.argv) != 2:
        exit()

    if sys.argv[1] == '--help':
        print('Transform an .asc file to .obj')
        print('\nEnter the name of the folder containing a \n')
        exit()

    FOLDER = os.path.join(os.getcwd(), sys.argv[1])

    if not os.path.exists(FOLDER) and not os.path.isdir(FOLDER):
        print('The provided folder does not exists or is not a folder')
        exit()

    print('\nConverting ' + sys.argv[1].replace('/', '').upper() + '\'s map.asc to map.obj...')

    convert(FOLDER)
