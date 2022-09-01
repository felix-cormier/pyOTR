import numpy as np


def MakeHoles(fHdist=7., fHdmtr=1.2, save='Beam/data/calib_holes'):
    holes = []
    # central holes:
    holes.append((2.8, 0.0, 2.8, 0.8))
    holes.append((0.0, 0.0, 0.0, 0.8))
    for i in range(1, 4):
        dist = i * fHdist
        step = 0.5 / i
        t = 0.
        if i == 3:  # the edge holes
            step = 1.0
            t = 0.5
        while t < 4:
            x, z = ParaSquare(t)
            if x != -999 and z != -999:
                # Save the scaled points
                holes.append((dist * x, 0.0, dist * z, fHdmtr))
                t += step
            else:
                print('"ParaSquare" function returned an error')
                break
    holes = np.array(holes)
    np.save(save, holes)
    return holes

def MakeCross(dx=5.657, dy=4., diam=1.2, cross=1):
    holes = []
    for i in range(1,4):
        x = i*dx
        y = i*dy
        holes.append((x, 0., 0., diam))
        holes.append((-x, 0., 0., diam))
        holes.append((0., 0., y, diam))
        holes.append((0., 0., -y, diam))
        if cross == 2:
            holes = holes[-4:]
    return np.array(holes)


def ParaSquare(t):
    if t >= 0. and t < 1:
        return -2 * t + 1.0, 1.0
    elif t >= 1 and t < 2:
        return -1.0, -2 * t + 3.0
    elif t >= 2 and t < 3:
        return 2 * t - 5.0, -1.0
    elif t >= 3 and t < 4:
        return 1.0, 2 * t - 7.0
    else:
        return -999, -999  # Bad parameter value


def PrintHolePos(holes, screen=False):
    with open('calib_holes.txt', 'w') as holefile:
        for i, ihole in enumerate(holes):
            holefile.write('{0} {1} {2}\n'.format(i, ihole[0], ihole[2]))
            if screen:
                print('{0} {1} {2}'.format(i, ihole[0], ihole[2]))


if __name__ == "__main__":
    holes = MakeHoles(save='../data/calib_holes')
    print('Generated holes')
    PrintHolePos(holes, screen=True)
