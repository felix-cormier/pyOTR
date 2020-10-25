import numpy as np

def Undistort(Image, control_points_foil, control_points_camera, poly_size = 6):

    x_calc = []
    y_calc = []
    for coord in Image:

        phi_check = np.zeros([poly_size, len(control_points_camera)])
        phi_xy = np.zeros([poly_size])

        # Weight function calculation, one weight for every calibration hole
        w = Weight(control_points_camera, coord[0], coord[1])

        for i in range(poly_size):
            phi_xy[i] = Poly_Basis(i, coord[0], coord[1])
            phi_check[i] = Poly_Basis(i, control_points_camera[:,0], control_points_camera[:,1])

            for j in range(i):
                num = np.sum(w*phi_check[j]*Poly_Basis(i, control_points_camera[:,0], control_points_camera[:,1]))
                denum = np.sum(w * phi_check[j] * phi_check[j])

                phi_check[i] = phi_check[i] - (num / denum) * phi_check[j]
                phi_xy[i] = phi_xy[i] - (num/denum) * phi_xy[j]

        a = np.zeros([poly_size])
        b = np.zeros([poly_size])

        for i in range(poly_size):
            num1= np.sum(w*control_points_foil[:,0]*phi_check[i])
            num2= np.sum(w*control_points_foil[:,1]*phi_check[i])
            denum= np.sum(w*phi_check[i]*phi_check[i])

            a[i] = num1/denum
            b[i] = num2/denum

        x_calc.append(np.sum(a*phi_xy))
        y_calc.append(np.sum(b*phi_xy))

    return x_calc, y_calc

def Poly_Basis(n, x, y):
    switcher = {
        0: 1,
        1: x,
        2: y,
        3: x * x,
        4: x * y,
        5: y * y,
        6: x * x * x,
        7: y * y * y
    }
    return switcher.get(n, "out of range")

def Weight(c_points, x, y):

    xc = x - c_points[:, 0]
    yc = y - c_points[:, 1]
    xc[np.abs(xc)>96] = 500
    yc[np.abs(yc)>105] = 500
    w_t = np.exp(-1 * (np.sqrt((xc * xc) + (yc * yc))/50))

    return w_t

