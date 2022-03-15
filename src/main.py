"""!
@file main.py
    This file is the overarching program that controls the plotter. In this file are
    different tasks set up to perform the different duties in the motor, run and shared
    through the cotasks file. The tasks created are encoders, controllers, and 
    motor drivers. This file was created from a previous file made by professor JR Ridgely
    and modified for the purpose of this lab.
    
   @author Aleya Dolorfino
   @author Chloe Chou
   @author Christian Roberts
   @author JR Ridgely

@date   2022-03-15 Updated template from basictasks.py, created by JR Ridgely.
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import encoder
import motor_driver
import ClosedLoopVC
import task_encoder
import math

from pyb import USB_VCP
vcp = USB_VCP()

coords = []
coords2 = []
pen_move = []

def task1_encoder1 ():

    """!
    Generator task which controls Encoder 1 on the plotter.
    """
    counter = 0
    enc_1.zero()
    while True:
        enc_1.update()
        pos = enc_1.get_position()
        vel = enc_1.get_velocity()
        S_position1.put(int(pos))
        S_velocity1.put(int(vel))
        counter += 1
        yield (0)


def task2_motor1 ():
    """!
    Generator task which controls Motor 1 on the plotter.
    """

    
    while True:
        duty = S_duty1.get()
        motor1.set_pwm(duty)


        yield (0)

def task3_controller1 ():
    """!
    Generator task which runs a closed loop calculation to return values for Encoder
    1 and determine necessary position or velocity on the plotter.
    """


    while True:
        velocity = S_velocity1.get()
        location = S_position1.get()
        duty = controller1.run(location, velocity)
        S_duty1.put(duty)
        if abs(duty) <= 20:
            S_Flag_1.put(1)
            controller1.switch_state()
        yield (0)
        

def task4_read ():
    """!
    An assigned task that ultimately did not get used
    """
    while True:
        
        yield (0)


def task5_setcoords ():
    """!
    A generator task to update the r and theta destination coordinates for both motors to follow
    """
    counter = 0
    while True:
        
        if S_Flag_1.get() == 1 and S_Flag_2.get() == 1:
            counter += 1
            if Q_r.any() and Q_th.any():
                r_val = Q_r.get()
                controller1.set_setpoint(r_val)
                S_Flag_1.put(0)
                
                th_val = Q_th.get()
                controller2.set_setpoint(th_val)
                S_Flag_2.put(0)
                print('Coordinate Number is ', counter)
        yield (0)

def task6_encoder2 ():

    """!
    Generator task which controls Encoder 2 on the plotter.
    """
    counter = 0
    enc_2.zero()
    while True:
        enc_2.update()
        pos = enc_2.get_position()
        vel = enc_2.get_velocity()
        S_position2.put(int(pos))
        S_velocity2.put(int(vel))
        counter += 1
        yield (0)


def task7_motor2 ():
    """!
    Generator task which controls Encoder 2 on the plotter.
    """
    while True:
        duty = S_duty2.get()
        motor2.set_pwm(duty)


        yield (0)

def task8_controller2 ():
    """!
    Generator task which runs a closed loop calculation to return values for Encoder
    2 and determine necessary position or velocity on the plotter.
    """
    while True:
        velocity = S_velocity2.get()
        location = S_position2.get()
        duty = controller2.run(location, velocity)
        S_duty2.put(duty)
        if abs(duty) <= 15:
            S_Flag_2.put(1)
            controller2.switch_state()

        yield (0)
        
# This code creates a 8 shares and 8 tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JStarting ME405 Term Project Pen Plotter\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share to pass the velocity value from the encoder.
    S_velocity1 = task_share.Share ('l', thread_protect = False, name = "S_velocity1")
    # Create a share to hold the position value at any given time.
    S_position1 = task_share.Share ('l', thread_protect = False, name = "S_position1")
    
    #Create a queue to pass the required duty cycle to the motor.
    S_duty1 = task_share.Share('f', thread_protect = False, name = "S_duty1")
        
    S_velocity2 = task_share.Share ('l', thread_protect = False, name = "S_velocity2")
    # Create a share to hold the position value at any given time.
    S_position2 = task_share.Share ('l', thread_protect = False, name = "S_position2")
    
    #Create a queue to pass the required duty cycle to the motor.
    S_duty2 = task_share.Share('f', thread_protect = False, name = "S_duty2")
    
    #Create a flag that will tell if we have reached our final destination.
    S_Flag_1 = task_share.Share('h', thread_protect = False, name = 'S_Flag_1')
    S_Flag_2 = task_share.Share('h', thread_protect = False, name = 'S_Flag_2')
    S_Flag_1.put(0)
    S_Flag_2.put(0)
    
    #Create a queue to hold all of the coordinates to plot for the Radial value.
    Q_r = task_share.Queue('f', 1000, thread_protect = False, name = "Q_r")
    
    #Create a queue to hold all of the coordinates to plot for the Theta value.
    Q_th = task_share.Queue('f', 1000, thread_protect = False, name = "Q_th")
    
    #Create a queue to hold all of the coordinates to plot for the X value.
    Q_x = task_share.Queue('l', 1000, thread_protect = False, name = "Q_x")
    
    #Create a queue to hold all of the coordinates to plot for the Y value.
    Q_y = task_share.Queue('l', 1000, thread_protect = False, name = "Q_y")
    
    #Opening the designated file of text containing the HGPL text to run.
    with open('figure8_OG.txt') as my_file:

        print(my_file)
        hpgl = my_file.read()
        commands = hpgl.split(';')
        commands2 = []
        for n in range(0,len(commands)-1):
            #Clean the data. Remove all pen-up, pen-down, and pen selection commands.
            #With time, this would become the point where we stored this data in another place to use.
            commands[n] = commands[n].replace("PU","")
            commands[n] = commands[n].replace("PD","")
            commands[n] = commands[n].replace("SP1","")
            commands[n] = commands[n].replace("SP0","")
            if commands[n] != 'IN' and commands[n] != '':
                commands2.append(commands[n])
                
        counter = 0
        for n in range(0,len(commands2)-1):
            data = commands2[n].split(',')
          
            for n in range(0,len(data)-1,2):
                #Store the values from the HGPL file in an X/Y set of Queues.
                Q_x.put(int(data[n]))
                Q_y.put(int(data[n+1]))
                counter += 1
        for n in range(0,counter):
            #Convert each point to a float in inches rather than ticks.
            x = float(Q_x.get())/1016
            y = float(Q_y.get())/1016
            #Convert to polar coordinates, then scale based on tuning.
            r = ((x**2 + y**2)**0.5)*165864/8
            try:
                th = round(math.atan(y/x)*180/math.pi)*(12250/90)
            except ZeroDivisionError:
                th = 0
            #Store radial and theta values in a queue.
            Q_r.put(r)
            Q_th.put(th)

    #Creating Motors and Encoder Objects
    #Motor 1
    m1_pin_1 = pyb.Pin.board.PB4
    m1_pin_2 = pyb.Pin.board.PB5
    m1_enable = pyb.Pin.board.PA10
    m1_timer = pyb.Timer(3, freq = 20000)
    motor1 = motor_driver.MotorDriver(m1_enable, m1_pin_1, m1_pin_2, m1_timer)
    
    #Motor 2
    m2_pin_1 = pyb.Pin.board.PA0
    m2_pin_2 = pyb.Pin.board.PA1
    m2_enable = pyb.Pin.board.PC1
    m2_timer = pyb.Timer(5, freq = 20000)
    motor2 = motor_driver.MotorDriver(m2_enable, m2_pin_1, m2_pin_2, m2_timer)
    
    #Encoder 1
    e1_pin_1 = pyb.Pin.cpu.B6
    e1_pin_2 = pyb.Pin.cpu.B7
    e1_channel = 4
    enc_1 = encoder.Encoder(e1_channel, e1_pin_1, e1_pin_2)
    
    #Encoder 2
    e2_pin_1 = pyb.Pin.cpu.C6
    e2_pin_2 = pyb.Pin.cpu.C7
    e2_channel = 8
    enc_2 = encoder.Encoder(e2_channel, e2_pin_1, e2_pin_2)    
    
    #Create two controller objects: one for each motor.
    controller1 = ClosedLoopVC.ClosedLoop(0,0,200,0,0.05, 0.4)
    controller2 = ClosedLoopVC.ClosedLoop(0,0,150,0,0.05, 0.3)
    
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed.
    task1 = cotask.Task (task1_encoder1, name = 'Task_1', priority = 1, 
                         period = 30, profile = True, trace = False)
    task2 = cotask.Task (task2_motor1, name = 'Task_2', priority = 3, 
                         period = 50, profile = True, trace = False)
    task3 = cotask.Task (task3_controller1, name = 'Task_3', priority = 2, 
                         period = 30, profile = True, trace = False)
    task5 = cotask.Task (task5_setcoords, name = 'Task_5', priority = 1,
                         period = 120, profile = True, trace = False)
    task6 = cotask.Task (task6_encoder2, name = 'Task_6', priority = 1, 
                         period = 30, profile = True, trace = False)
    task7 = cotask.Task (task7_motor2, name = 'Task_7', priority = 3, 
                         period = 50, profile = True, trace = False)
    task8 = cotask.Task (task8_controller2, name = 'Task_8', priority = 2, 
                         period = 30, profile = True, trace = False)

    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task5)
    cotask.task_list.append (task6)
    cotask.task_list.append (task7)
    cotask.task_list.append (task8)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
