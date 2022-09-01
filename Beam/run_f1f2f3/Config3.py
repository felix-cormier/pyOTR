logfile = name + '.log'  # log output will be directed to this file and to screen

nrays = 1_000_000
chunck = 1_000  # 0 if no division is to be made
source = 'filament_v2' #backlight (filament/filament_v2), proton beam (protons), or laser (laser)

pm = {
    'psi': np.array([0.,0.,0.])        
}

beam = {
    #'x': -1000., #for filament backlight
    'x': 0.,
    'y': 0.,
    #'z': 0.,
    'z': -100.,
    #'gamma':21., #E = 20 GeV
    'gamma':32., #E = 30 GeV
#    'gamma':53.5, #E = 50 GeV
    'cov': np.diag([9., 9., 0.]),
    'Vtype': 'parallel',  # need to implement divergent beam also
    'vcov': np.diag([0.05, 0.05, 1.]),  # not yet used, vz needs to be constrained by vx/vy

}

laser = {
    'X': np.array([-1051.9 + pm['psi'][0], 868.6 + pm['psi'][1], pm['psi'][2]]),
    #'X': np.array([-1128.875, 735.489, 0.]),
    'angles': np.array([0.,0.,Conv(52.15)])
}

filament = {
        'X': np.array([-1051.9 + pm['psi'][0], 868.6 + pm['psi'][1], pm['psi'][2]]),
        #'X': np.array([-1128.875 + pm['psi'][0], 735.489 + pm['psi'][1], pm['psi'][2]]),
        'angles': np.array([0.,0.,Conv(52.15)]),
        'Vtype': 'divergent',
        'wire': True,
        'reflector': False,
        'spread': 0.01,
