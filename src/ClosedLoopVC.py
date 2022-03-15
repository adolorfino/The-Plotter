"""!
    @file                ClosedLoopVC.py
        A closed loop controller with both position and velocity controls. The motor
        takes the location and specified setpoint of the motor and uses that information
        to calculate a duty cycle appropriately using a proportional gain. The velocity
        controller is used until the velocity controller reaches a set threshold, then
        switches to position for an accurate location.
        
   @author              Aleya Dolorfino
   @author              Chloe Chou
   @author              Christian Roberts
   @date                2022-Mar-15
"""
import utime
import cotask
import task_share

class ClosedLoop:
    '''!
    @brief Closed-loop controller class
    @details Closed loop controller class to control the speed of the motor 
    '''

    
    def __init__(self,location,setpoint,vpoint, velocity, kp, kv):
        '''!
        @brief Object contructor for Closed Loop class
        @param location This parameter defines the current location of the encoder.
        @param setpoint This parameter defines the set location to acheive.
        @param vpoint This parameter defines the target velocity of the motor.
        @param velocity This parameter defines the current velocity of the motor.
        @param kp This is the proportional gain constant for the positional control.
        @param kv This is the proportional gain constant for the velocity control.
               

        '''
        self.setpoint = setpoint
        self.location = location
        self.kp = kp
        self.error = self.setpoint - self.location
        self.vpoint = vpoint
        self.velocity = velocity
        self.v_error = self.vpoint - self.velocity
        #Defining a state that will determine whether the velocity controlled
        #regime or the position-controlled regime will dominate.
        self.state = 'V_ERROR'
        self.kv = kv
        
        self.printout = []
        self.times = []
        self.duty = 0
        
    def run(self, position, velocity):
        '''!
        @brief Runs controller function 
        @details The function runs the closedloop feedback system. The system
            determines whether it is in the velocity regime or the positional 
            regime, and applies a closed loop control equation to determine a 
            new duty cycle. The velocity regime dominates until the motor is 
            within 1000ticks of the target location, at which point the 
            positional regime takes over and calculates a new duty cycle. If the
            new calculated duty is below -100 or above 100 then the duty is set
            to the maximum duty of either -100 or 100. 
        @return duty This function returns the new calculated duty cycle for 
            the DC motor.
        @param position A floating point value containing the position of the 
            motor. This is calculated from the Encoder class.
        @param velocity A floating point value containing the velocity of the 
            motor. This is calculated using the Encoder class.
        '''

        self.position = position
        self.velocity = velocity
        
        self.set_location(self.position)
        self.error = self.setpoint - self.location
        
        self.v_error = abs(abs(self.vpoint) - abs(self.velocity))
        
        if self.state == 'V_ERROR':
            if abs(self.error) <= 1000:
                self.state = 'P_ERROR'
                self.duty = 0
            elif abs(self.v_error) >=5:
                if self.error > 0:
                    self.duty = self.kv*(self.v_error)
                else:
                    self.duty = self.kv  * (self.v_error) * (-1)

            else:
                pass
        elif self.state == 'P_ERROR':
            if abs(self.error) >= 50:
                self.duty = self.kp*(self.error)
            else:
                self.state = 'V_ERROR'
        
        if self.duty >100:
            self.duty = 100
        if self.duty <-100:
            self.duty = -100
        return self.duty
        
    def get_Kp(self):
        """!
        @brief Returns the Kp value assigned to the closed loop
        @return Kp value.
        """
        return self.kp
     
    def set_Kp(self, kp):
        """!
        @brief Changes the input Kp value
        @param kp The new proportional gain to set.
        """
        self.kp = kp
        
    def get_setpoint(self):
        """!
        @brief Returns the setpoint value assigned to the closed loop
        @return The current setpoint of the controller.
        """
        return self.setpoint
        
    def set_setpoint(self, setpoint):
        """!
        @brief Changes the input setpoint value
        @param setpoint The new setpoint to set
        """
        self.setpoint = setpoint
        
    def set_location(self, location):
        """!
        @brief Changes the location for the closed loop to calculate
        """
        self.location = location
        
    def set_vpoint(self, vpoint):
        """!
        @brief Changes the velocity limit for the controller
        """
        self.vpoint = vpoint
        
        
    def switch_state(self):
        """!
        @brief Sets the control scheme to dominate.
        @details A debugging tool to manually change the regime of the controller.
        """
        if self.state == 'V_ERROR':
            self.state = 'P_ERROR'
        elif self.state == 'P_ERROR':
            self.state = 'V_ERROR' 