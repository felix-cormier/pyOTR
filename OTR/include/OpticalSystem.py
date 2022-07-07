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
            generator_options.diagnosticImage(X,V, initial_name, dim)
        else:
            hh, xedges, yedges, hh_f, xedges_f, yedges_f, hh_r, xedges_r, yedges_r = generator_options.diagnosticImage(X,V, initial_name, dim, parallel=True)
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
            radius = 0
            try:
                radius = comp.R
            except AttributeError:
                pass
            try:
                radius = comp.diam/2
            except AttributeError:
                pass
            dim = [-radius, radius, -radius, radius]
            print("Passing through " + str(comp.name))
            X, V = comp.RaysTransport(X, V)
            if generator_options.not_parallel:
                generator_options.diagnosticImage(X,V, comp.name, dim)
            else:
                hh, xedges, yedges, hh_f, xedges_f, yedges_f, hh_r, xedges_r, yedges_r = generator_options.diagnosticImage(X,V, comp.name, dim, parallel=True)
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
