class OpticalSystem():
    def __init__(self):
        self.components = []

    def AddComponent(self, component):
        self.components.append(component)

    def TraceRays(self, X, V, generator_options, isGenerator):
        if len(self.components) == 0:
           # print('ERROR! No optical components were declared.\nExiting...')
           # return 0, 0 #original
            return X, V
        
        if not generator_options.not_parallel:
            hh_container = []
            xedges_container = []
            yedges_container = []
            hh_f_container = []
            xedges_f_container = []
            yedges_f_container = []
            hh_r_container = []
            xedges_r_container = []
            yedges_r_container = []
            name_container = []
            dim_container = []

        initial_name = 'initial'
        if isGenerator:
            initial_name = initial_name+'_generation'
        if not isGenerator:
            initial_name = initial_name+'_propagation'
        dim = [-10,10,-10,10]

        if generator_options.not_parallel:
            generator_options.diagnosticImage(X,V, initial_name, dim, isGenerator)
        else:
            hh, xedges, yedges, hh_f, xedges_f, yedges_f, hh_r, xedges_r, yedges_r = generator_options.diagnosticImage(X,V, initial_name, dim, isGenerator, parallel=True)
            hh_container.append(hh)
            xedges_container.append(xedges)
            yedges_container.append(yedges)
            hh_f_container.append(hh_f)
            xedges_f_container.append(xedges_f)
            yedges_f_container.append(yedges_f)
            hh_r_container.append(hh_r)
            xedges_r_container.append(xedges_r)
            yedges_r_container.append(yedges_r)
            name_container.append(initial_name)
            dim_container.append(dim)
        for comp in self.components:
            radius = 60
            x = 0
            y = 0
            dir_comp=0
            ref_dir = 3
            trans_dir = 3
            if not isGenerator and 'ParaMirror1' in comp.name:
                x = generator_options.M1['X'][0][1]
                y = generator_options.M1['X'][0][2]
                dir_comp = generator_options.M1['dir_comp']
                ref_dir = generator_options.M1['refl']
                trans_dir = generator_options.M1['trans']
            if not isGenerator and 'ParaMirror2' in comp.name:
                x = generator_options.M2['X'][0][1]
                y = generator_options.M2['X'][0][2]
                dir_comp = generator_options.M2['dir_comp']
                ref_dir = generator_options.M2['refl']
                trans_dir = generator_options.M2['trans']
            if not isGenerator and 'ParaMirror3' in comp.name:
                x = generator_options.M3['X'][0][2]
                y = generator_options.M3['X'][0][0]
                dir_comp = generator_options.M3['dir_comp']
                ref_dir = generator_options.M3['refl']
                trans_dir = generator_options.M3['trans']
            if not isGenerator and 'ParaMirror4' in comp.name:
                x = generator_options.M4['X'][0][1]
                y = generator_options.M4['X'][0][2]
                dir_comp = generator_options.M4['dir_comp']
                ref_dir = generator_options.M4['refl']
                trans_dir = generator_options.M4['trans']
            if not isGenerator and 'Image' in comp.name:
                x = 0
                y = 0
                ref_dir = generator_options.camera['refl']
                trans_dir = generator_options.camera['trans']
            if 'Foil' in comp.name:
                print("FOUND FOIL")
                ref_dir = generator_options.foil['refl']
                trans_dir = generator_options.foil['trans']
                #ref_dir = 3
                #trans_dir = -3
            if 'Reflector' in comp.name:
                ref_dir = generator_options.reflector['refl']
                trans_dir = generator_options.reflector['trans']
            if 'Filament' in comp.name:
                ref_dir = generator_options.filament['refl']
                trans_dir = generator_options.filament['trans']

            try:
                radius = comp.R
            except AttributeError:
                pass
            try:
                radius = comp.diam/2
            except AttributeError:
                pass
            dim = [x-radius, x+radius, y-radius, y+radius]
            if 'ImagePlane' in comp.name:
                dim = [-generator_options.camera['L']*(0.5), generator_options.camera['L']*(0.5),
                        -generator_options.camera['H']*(0.5), generator_options.camera['H']*(0.5)]
            print("Passing through " + str(comp.name))
            X, V = comp.RaysTransport(X, V)
            if X.shape[0] == 0:
                if generator_options.not_parallel:
                    print("NO X")
                    return 0, 0
                else:
                    return 0,0,0,0,0,0,0,0,0,0,0,0,0
            if generator_options.not_parallel:
                generator_options.diagnosticImage(X,V, comp.name, dim, isGenerator, ref_dir = ref_dir, trans_dir=trans_dir)
            else:
                hh, xedges, yedges, hh_f, xedges_f, yedges_f, hh_r, xedges_r, yedges_r = generator_options.diagnosticImage(X,V, comp.name, dim, isGenerator, parallel=True, dir_comp=dir_comp, ref_dir=ref_dir, trans_dir=trans_dir, generator_options=generator_options)
                hh_container.append(hh)
                xedges_container.append(xedges)
                yedges_container.append(yedges)
                hh_f_container.append(hh_f)
                xedges_f_container.append(xedges_f)
                yedges_f_container.append(yedges_f)
                hh_r_container.append(hh_r)
                xedges_r_container.append(xedges_r)
                yedges_r_container.append(yedges_r)
                name_container.append(comp.name)
                dim_container.append(dim)
        #generator_options.diagnosticImage_parallel(hh_container, xedges_container, yedges_container, hh_f_container, xedges_f_container, yedges_f_container, hh_r_container, xedges_r_container, yedges_r_container, name_container, dim_container)
        if generator_options.not_parallel:
            return X, V
        else:
            return X, V, hh_container, xedges_container, yedges_container, hh_f_container, xedges_f_container, yedges_f_container, hh_r_container, xedges_r_container, yedges_r_container, name_container, dim_container
