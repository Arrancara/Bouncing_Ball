# -*- coding: utf-8 -*-
"""
Title: Bouncing Ball

The program calculates the number of bounces required for a ball's bounce
height to fall below a minimum and outputs the number of bounces and the time
taken to do so. It relies on user input to obtain the intial height of the
ball, the efficiency of energy transfer and the minimum bounce height.
It also produces a displacment-time graph of the ball. Numerical process is
used with a variable time step that the user can change within the code for
better accuracy at the cost of performance.

Aavash Subedi, UID:10638164 19/10/2021
"""
import math
import numpy as np
import matplotlib.pyplot as plt

GRAVITATIONAL_ACCELERATION = 9.81
TIME_STEP = 0.005

def input_checker(user_input):
    """
    Checks the user input to ensure that it is a float.

    Args:
        user_input : float

    Returns:
        user_input : float

    """
    while True:
        try:
            user_input = float(user_input)
            if user_input <= 0:
                user_input = input("Please enter a positive value: ")
                continue
        except ValueError:
            user_input = input("Please enter a numerical value: ")
        else:
            break
    return user_input

def number_of_bounces_calculator(
        height_initial, height_minimum, energy_efficiency):
    """
    Calculates the minimum number of bounces required for the bounce height to
    be below the minimum height.

    Parameters
    ----------
    height_initial : float
        Initial height.
    energy_efficiency : float
        Efficiency of bounces.
    height_minimum : float
        Minimum height.

    Returns
    -------
    required_bounces: float
    required_bounces_rounded: float

    """
    required_bounces = (np.log(height_minimum/height_initial)/
                        np.log(energy_efficiency))
    required_bounces_rounded = math.floor(required_bounces)
    return required_bounces, required_bounces_rounded


def calculator(init_height, min_height, efficiency_coeff, theoretical_bounces):
    """
    Main part of the code, it takes in all the users' input and calculates the
    number of bounces to achieve the minimum height and also outputs the time,
    and produces a plot.

    Parameters
    ----------
    init_height : float
        Inital height.
    min_height : float
        Minimum height.
    efficiency_coeff : float
        Efficiency as inputted by the user.
    theoretical_bounces: float
    Takes in the calculated value for the number of bounces.

    Returns
    -------
    None.

    """
    number_of_bounces = 0
    height = float(init_height)
    velocity = 0
    current_time = 0
    time_at_bounces = []
    displacement_time_store = [[], []]
    while number_of_bounces <= theoretical_bounces +3:
        velocity -= GRAVITATIONAL_ACCELERATION*TIME_STEP
        if height < 0:
            expected_bounce_height = ((init_height*efficiency_coeff**
                                       (number_of_bounces+1)))
            #Logical error check incase the heights are equal.
            if expected_bounce_height == min_height:
                theoretical_bounces -= 1
            bounce_velocty = (2*GRAVITATIONAL_ACCELERATION*
                              expected_bounce_height)**0.5
            velocity = bounce_velocty
            height = 0
            number_of_bounces += 1
            time_at_bounces.append(current_time)
        height += velocity*TIME_STEP
        current_time += TIME_STEP
        displacement_time_store[0].append(height)
        displacement_time_store[1].append(current_time)

    #Error check, to prevent future errors.
    if theoretical_bounces < 0:
        bounces_required_time = time_at_bounces[0]

    else:
        bounces_required_time = time_at_bounces[theoretical_bounces]

    plt.plot(displacement_time_store[1], displacement_time_store[0])
    plt.hlines(float(min_height), 0, current_time, color='r',
               linestyle="--")
    plt.axvline(bounces_required_time, color="r", linestyle="--")
    plt.title("Height vs Time", fontsize=20)
    plt.xlabel("Time(s)")
    plt.ylabel("Height(m)")
    plt.show()

    print("The number of bounces required is {0:d}, and this takes {1:.2f} "
          "seconds to achieve.".format(int(theoretical_bounces),
                                       bounces_required_time))


#Obtains and checks the initial height of the ball.
INITIAL_HEIGHT_CHECKED = False
while not INITIAL_HEIGHT_CHECKED:
    initial_height = input("Please enter the intial height: ")
    initial_height = input_checker(initial_height)
    if initial_height > 0:
        INITIAL_HEIGHT_CHECKED = True
    else:
        print("The initial height cannot be 0.")
        continue

MINIMUM_HEIGHT_CHECKED = False
while not MINIMUM_HEIGHT_CHECKED:
    minimum_height = input("Please enter the minimum height: ")
    minimum_height = input_checker(minimum_height)
    if minimum_height <= initial_height:
        MINIMUM_HEIGHT_CHECKED = True
    else:
        print("The minimum height cannot be greater than the initial.")
        continue


EFFICIENCY_CHECKED = False
while not EFFICIENCY_CHECKED:
    efficiency = input("Please enter the value of efficiency: ")
    efficiency = input_checker(efficiency)
    if efficiency < 1.0:
        EFFICIENCY_CHECKED = True
    else:
        print("Please enter a value between 0 and 1 inclusive.")
        continue
theoretical_number_of_bounces = (number_of_bounces_calculator(initial_height,
                                                              minimum_height,
                                                              efficiency))[1]

calculator(initial_height, minimum_height, efficiency,
           theoretical_number_of_bounces)
