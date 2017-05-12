#!/usr/bin/python

import re
import sys
import numpy


#Set-up regular expression for parameters matching
e = '-?(?:\\d+\\.?\\d*|\\.\\d+)[eEdD](?:\\+|-)?\\d+' # exponential notation
f = '-?\\d+\\.\\d*|-?\\.\\d+'                        # floating point
i = '-?\\d+'                                         # integer
value = e+'|'+f+'|'+i                                # numeric field
tag = '\\w+(?::\\w+)*'                               # text tag field

aprepo_regex = re.compile('^\s*\{\s*(' + tag + ')\s*=\s*(' + value +')\s*\}$') #aprepro file format
std_param_regex = re.compile('^\s*(' + value + ')\s+(' + tag + ')$') #std file format


def PreProcessing(filename):
    #Gets the parameters values and the requested responses
    file = open(filename, 'r')
    
    param_dict = {}
    for line in file:
        m = aprepo_regex.match(line)
        if m:
            param_dict[m.group(1)] = m.group(2)
        else:
            m = std_param_regex.match(line)
            if m:
                param_dict[m.group(2)] = m.group(1)
                
    file.close()
    
    # crude error checking; handle both standard and aprepro cases

    num_vars = 0
    if ('variables' in param_dict):
        num_vars = int(param_dict['variables'])
    elif ('DAKOTA_VARS' in param_dict):
        num_vars = int(param_dict['DAKOTA_VARS'])
    
    num_fns = 0
    if ('functions' in param_dict):
        num_fns = int(param_dict['functions'])
    elif ('DAKOTA_FNS' in param_dict):
        num_fns = int(param_dict['DAKOTA_FNS'])
    
    if (num_vars != 2 or num_fns != 1):
        print "Rosenbrock requires 2 variables and 1 function;\nfound " + \
       str( num_vars) + " variables and " + str(num_fns) + " functions." 
        sys.exit(1)
        
    #Formating data to send to the Objective Function
    cv = numpy.array([float(param_dict['x1']), float(param_dict['x2'])])
    asv = [int(param_dict['ASV_1:obj_fn'])]
    
    rosen_param = {}
    rosen_param['cv'] = cv
    rosen_param['asv'] = asv
    rosen_param['functions'] = 1
    
    return rosen_param


def Rosembrock(**kwargs):
    num_func = kwargs['functions']
    x = kwargs['cv']
    asv = kwargs['asv']
    
    f0 = x[1] - x[0]**2
    f1 = 1.0 - x[0]
    
    retval = {}
    if (asv[0] & 1):  #***** f:
        f = numpy.array([100.0*f0*f0+f1*f1])
        retval['fns'] = f
        
    if (asv[0] & 2): #***** df/dx:
        g = numpy.array([[-400.0*f0*x[0] - 2*f1, 200.0*f0]])
        retval['fnGrads'] = g
        
    if (asv[0] & 4): #***** d^2f/dx^2:
        fx = x[1]-3.0*x[0]*x[0]
        
        h = numpy.array([ [ [-400*fx + 2, -400*x[0]],
              [-400*x[0],    200     ] ] ]    )
        retval['fnHessians'] = h
    
    return retval


def PosProcessing(params, rosen_result, filename):
    file = open(filename, 'w')
    
    num_func = params['functions']
    x = params['cv']
    asv = params['asv']
    
    #Write functions
    for func_ind in xrange(0, num_func):
        if (asv[func_ind] & 1):
            functions = rosen_result['fns']
            file.write(str(functions[func_ind]) + ' f' + str(func_ind) + '\n')
            
    #Write gradients
    for func_ind in xrange(0, num_func):
        if (asv[func_ind] & 2):
            grad = rosen_result['fnGrads'][func_ind]
            file.write('[ ')
            for deriv in grad:
                file.write(str(deriv) + ' ')
            file.write(']\n')
            
    #Write Hessian
    for func_ind in xrange(0, num_func):
        if (asv[func_ind] & 4):
            hessian = rosen_result['fnHessians'][func_ind]
            file.write('[[ ')
            for hessrow in hessian:
                for hesscol in hessrow:
                    file.write(str(hesscol) + ' ')
                file.write('\n')
            file.write(']]\n')
            
    file.close()
    
    
    
    
if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    params = PreProcessing(input_file)
    results = Rosembrock(**params) #Dont forget the ** before params we are passing the dict
    PosProcessing(params, results, output_file)
    
        

        



