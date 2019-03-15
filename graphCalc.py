#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 23:24:10 2019

@author: patrickkuang
"""

# -*- coding: utf-8 -*-
#imports required packages
import numpy as np  
import matplotlib.pyplot as plt  
import math
#import numpy.ma as M# -*- coding: utf-8 -*-


#this function is the driver function that calls the other functions to create the result graph
def graph(formula,min_x,max_x,min_y,max_y,x,fc,y,interval):  

    # formula after translation (e.g. x^2 is converted to x**2).  fc = formula_converted
    d1 = derivative(fc,x) #calls derivative function to store f'(x) values for x
    d2 = derivative2(fc,x) # calls 2nd derivative function to store f'(x) values for x
    maximums = [] #empty array for x-values of relative maxima
    maximumsy = [] #empty array for y-values of relative maxima
    maximums, maximumsy = maxs(d1,fc,x_range_min,interval) #calls maximum function to fill maxima arrays
    minimums = [] #empty array for x-values of relative minima
    minimumsy = [] #empty array for x-values of relative maxima
    minimums, minimumsy = mins(d1,fc,x_range_min,interval) #calls minimum function to fill minima arrays
    pointsofinflection = [] #empty array for x-values of points of inflection
    pointsofinflectiony = [] #empty array for y-values of points of inflection
    pointsofinflection, pointsofinflectiony = inflection(d2,fc,x_range_min,interval) #calls POI function to fill POI arrays
    x_zeroes = x - x #x-axis
    y_values = np.arange(min_y,max_y,interval) #array used for creating y-axis
    y_zeroes = y_values - y_values #y-axis
    # plot the various
    plt.plot(x,y) #plots f(x)
    plt.ylim([min_y,max_y]) #limits for y-axis
    plt.xlim([min_x,max_x])  #limits for x-axis
    plt.plot(x, d1) #plots f'(x)
    plt.plot(x, d2) #f''(x)
    #plot aysmptote
    plt.plot(maximums, maximumsy, "o") #plots points that are relative maxima
    plt.plot(minimums, minimumsy, "o") #plots points that are relative minima
    plt.plot(pointsofinflection, pointsofinflectiony, "o") #plots points of inflection
    holesx = [] #empty array for x-values of holes
    holesy = []  #empty array for y-values of holes
    holesx, holesy = (holes(x_range_min,interval,y,fc)) #calls holes function to fill minima arrays
    holesx = np.asarray(holesx) #makes holes array readable for matlab
    np.around(holesx,6) #rounds holes array so the points could be plotted
    plt.plot(holesx,holesy,"ow") #plots white points for holes
    plt.plot(x,x_zeroes,"k") #draws x-axis
    plt.plot(y_zeroes,y_values,"k") #draws y-axis
    asympx = (asymptote(x_range_min,interval,y,fc))  #calls asymptote function to find vertical asymptotes
    asympx = np.asarray(asympx) #makes asymptotes array readable for matlab
    np.around(asympx,6) #rounds asymptotes array so the points could be plotted
    if(asympx.size > 0):  #loop to draw each asymptote
        for nums in asympx:
            plt.axvline(nums,linewidth=2,color='k',ls='--')
    plt.title('f(x)='+func) #titles the graph
    plt.xlabel('X Values') #labels x-axis
    plt.ylabel('Y Values')  #labels y-axis
    lines = ["f(x)","f'(x)","f''(x)","Maxs","Mins","Points of Inflection","holes"] #sets guidelines for legend
    plt.legend(lines,'upper right') #draws the legend on the upper right of the graph
    plt.show()  #shows the GUI of the graph

#derivative function called in the main graph function used to return an array of f'(x) for x
def derivative(formulas,x):
    # x should be passed, and define outside the this function
    y1 = eval(formulas) #sets y1 to an array of the evaluated version of all the given equation for all the x-values
    dc = formulas.replace("x","(x-.001)")#sets dc to an equation with x set back by .001
    return ((y1-eval(dc))/.001) #returns an array of values for f'(x) on x by calculating the slope between points an interval of .001 apart

#maximum function called in the main graph function to return arrays for x and y values of relative maxima                     
def maxs(d1, fc, min_x,interval):
    maxs = [] #empty array for x-values of relative maxima
    maxsy = [] #empty array for y-values of relative maxima
    counter = 0
    for val in d1: #loop to set the initial values of previousnum and previousnum2
        counter += 1
        if counter == 1: 
            previousnum2 = val
        if counter == 2:
            previousnum = val
    index = min_x
    for num in d1: #loops through every value in the array of f'(x) to find changes from positive to negative
        index += interval
        if previousnum < 0.01 and previousnum > -0.01:
            if previousnum2 > 0:
                if num < 0:
                    maxs.append(index-interval)
                    maxsy.append(eval(fc.replace("x","("+str(index-interval)+")")))
        previousnum2 = previousnum
        previousnum = num
    return maxs, maxsy #returns the x and y arrays for relative maxima

#minimum function called in the main graph function to return arrays for x and y values of relative minima
#works the exact same way as maximum function but it looks to see if f'(x) changes from negative to positive on x
def mins(d1, fc, min_x,interval):
    mins = []
    minsy = []
    counter = 0
    for val in d1:
        counter += 1
        if counter == 1:
            previousnum2 = val
        if counter == 2:
            previousnum = val
    index = min_x
    for num in d1:
        index += interval
        if previousnum < 0.01 and previousnum > -0.01:
            if previousnum2 < 0:
                if num > 0:
                    mins.append(index-.001)
                    minsy.append(eval(fc.replace("x","("+str(index-interval)+")")))
        previousnum2 = previousnum
        previousnum = num
    return mins, minsy

#Point of Inflection function called in the main graph function to return arrays for x and y values of Points of Inflection
#works the exact same way as maximum function but it looks to see if f''(x) changes from either negative to positive or positive to negative
def inflection(d2, fc, min_x,interval):
    pois = [] # points of inflections - x (pois_x)
    poisy = []
    counter = 0
    for val in d2:
        counter += 1
        if counter == 1:
            previousnum2 = val
        if counter == 2:
            previousnum = val
    index = min_x
    for num in d2:
        index += interval
        if previousnum < 0.01 and previousnum > -0.01:
            if previousnum2 < -.00001:
                if num > 0.00001:
                    pois.append(index-interval)
                    poisy.append(eval(fc.replace("x","("+str(index-interval)+")")))
            if previousnum2 > 0.00001:
                if num < -.00001:
                    pois.append(index-interval)
                    poisy.append(eval(fc.replace("x","("+str(index-interval)+")")))
        previousnum2 = previousnum
        previousnum = num
    return pois, poisy
            
        
#second derivative function called in the main graph function used to return an array of f''(x) for x   
def derivative2(formulas,x):
    y1 = eval(formulas)
    cc = formulas.replace("x","(x-.002)")
    dc = formulas.replace("x","(x-.001)")
    dpoint1 = derivative(formulas,x)
    dpoint2 = (eval(dc)-eval(cc))/.001
    return (dpoint1-dpoint2)/.001

#integration function called later on
#takes the expression and upper and lower limits to integrate from
#uses trapezoidal method
def integrate(solution,formula,int_low,int_upper):
    interval = (int_upper - int_low)/100000
    x = np.arange(int_low,int_upper,interval)
    fc = formula(x)
    y = eval(fc)
    integrationfunction = []
    yprim = derivative(fc,x)
    if solution == 1:
        integrationfunction = y
    if solution == 2:
        integrationfunction = yprim
    total = 0
    for v in integrationfunction:
        v_prev = v
        if (v+v_prev)/2 > 0:
            total += (((v+v_prev)/2) * interval)
        if (v+v_prev)/2 < 0:
            total += (((v+v_prev)/2) * interval)
    return str(round(total, 2))

    
#Holes function called in the main graph function to return arrays for x-values and y-limits of holes
#finds holes by finding where y values are marked as NaN by python but not where the x domain is limited
def holes(x_range_min,interval,y,fc):
    nan = []
    nany = []
    nans = []
    streak = False
    counter = x_range_min
    counter1 = x_range_min
    for val in y:
        if math.isnan(val):
            if streak == False:
                nans.append(True)
                streak = True
        else:
            nans.append(False)
            streak = False
        counter += interval
    index = x_range_min
    for val in nans:
        index += interval
        if val == True:
            nan.append(index)
            for valss in y:
                counter1 += interval
                if (counter1 == (index+interval)):
                    nany.append(valss)
    return nan,nany




#Asymptote function called in the main graph function to return arrays for x-values of asymptotes
#works similarly to holes function
def asymptote(x_range_min,interval,y,fc):
    asympx = []
    nans = np.isinf(y)
    index = x_range_min
    for val in nans:
        index += interval
        if val == True:
            asympx.append(index)
    return asympx

# takes integral of derivative of given function and prints it out 
def secondftc(formula,int_low,int_upper):
     yprim = derivative(fc,x)
     answer = integrate(2,formula,int_low,int_upper)
     print("the definite integral of the derivative of your input from "+str(int_low)+" to "+str(int_upper)+" is " + str(answer))
     print("f("+str(int_upper)+") - f("+str(int_low)+") = "+answer)
    
#function to make input function readable for python
def my_formula(x):
    m = func.replace("^","**")
    m = m.replace(")(",")*(")
    m = m.replace("1x","1*x")
    m = m.replace("2x","2*x")
    m = m.replace("3x","3*x")
    m = m.replace("4x","4*x")
    m = m.replace("5x","5*x")
    m = m.replace("6x","6*x")
    m = m.replace("7x","7*x")
    m = m.replace("8x","8*x")
    m = m.replace("9x","9*x")
    m = m.replace("0x","0*x")
    m = m.replace("sin(","np.sin(")
    m = m.replace("cos(","np.cos(")
    m = m.replace("tan(","np.tan(")
    m = m.replace("cot(","1/np.tan(")
    m = m.replace("csc(","1/np.sin(")
    m = m.replace("sec(","1/np.cos(")
    m = m.replace("e","2.718281828459045235")
    m = m.replace("log(","np.log10(")
    m = m.replace("ln(","np.log(")
    if "x" not in m: #if user enters a constant it still makes the expression in terms of x 
        m += "+(x-x)"
    return m



    
    


# get inputs from command line
print("Enter Expression (in terms of x):")
#func = raw_input()
func = input()
#to pick presets for graph
window_selection = input('select zoom preference \n 1. Standard \n 2. Decimal \n 3. manual \n')
#global x_range_min, x_range_max, y_range_min, y_range_max
x_range_min = -10
x_range_max = 10
y_range_min = -10
y_range_max = 10
interval = .0001

if window_selection == 1:
    x_range_min = -10
    x_range_max = 10
    y_range_min = -10
    y_range_max = 10
    interval = .0001

    
if window_selection == 2:
    x_range_min = -6.6
    x_range_max = 6.6
    y_range_min = -4.1 
    y_range_max = 4.1
    interval = .0001


if window_selection == 3:
    x_range_min = float(input("x-minimum:"))
    x_range_max = float(input("x-maximum:"))
    y_range_min = float(input("y-minimum:"))
    y_range_max = float(input("y-maximum:"))
    interval = .0001

#these variables will be global for all functions to access
x = np.arange(x_range_min, x_range_max, interval)
x = np.around(x,6)
fc = my_formula(x)
y = eval(fc)

                            
user_choice = str(input("Type 'int' for definite integral algorithim and second ftc \n press enter to skip \n"))

#does integration and second ftc if user types ‘int’
if user_choice == 'int':
    lowerlimit = float(input("input lower limit:"))
    upperlimit = float(input("input upper limit:"))
    y = eval(fc)
    integral = integrate(1,my_formula,lowerlimit,upperlimit)
    print("The definite integral for your input is "+str(integral))
    yprim = derivative(fc,x)
    secondftc(my_formula,lowerlimit,upperlimit)
else:
    graph(my_formula,x_range_min,x_range_max,y_range_min,y_range_max,x,fc,y,interval)





