"""!
    @file    encoder.py
        This file interacts directly with the hardware of the Nucleo to
        read motor encoders and return information as called.
            
    @author              Aleya Dolorfino
    @author              Chloe Chou
    @author              Christian Roberts
    @date                March 8, 2022
"""
import pyb
import utime


class Encoder:
    """! 
    @brief  Interface with quadrature encoders
    @details Creates a class for the encoder to call encoder position, 
        change in encoder position, and datums the motor. 
        
    """

    def __init__(self, timNum, pin1, pin2):
        """!
            @brief Constructs an encoder object
            @param timNum   Corresponds to the timer channel that the
                            encoder is connected to. 
        """
        self.datumPosition = 0
        self.old_counter = 0
        self.delta = 0
        self.count = 0
        self.position = 0
        self.cap = 65535
        self.oldDelta = -1
        self.time_last = utime.ticks_ms()
        
        self.tim = pyb.Timer(timNum,prescaler = 0, period = 65535)
        TIM4_CH1 = self.tim.channel(1, mode = pyb.Timer.ENC_A, pin = pin1)
        TIM4_CH2 = self.tim.channel(2, mode = pyb.Timer.ENC_B, pin = pin2)
    
    def read(self):
        '''!
            @brief   Gets encoder timer  
            @return  The value of the timer encoder
        '''
        return self.tim.counter()
    
    def zero(self):
        '''!
            @brief   Gets encoder timer  
            @return  The value of the timer encoder
        '''
        self.datumPosition = 0
    
    def update(self):
        """!
            @brief      Updates encoder position and delta
            @details    Updates the encoder postion,delta, and 
                        handles the enconter over and underflow. 
        """
        self.time_now = utime.ticks_ms()
        self.time_diff = utime.ticks_diff(self.time_now, self.time_last)
        self.count = self.read()
        self.delta = self.count - self.old_counter
        self.old_counter = self.count
        if (abs(self.delta) >= self.cap/2):
                if(self.delta >= self.cap/2):
                    self.delta-=self.cap
                else:
                    self.delta+=self.cap
        if(self.delta!=self.oldDelta):
            self.datumPosition += self.delta
            self.oldDelta = self.delta
            
        self.time_last = self.time_now
        if self.time_diff != 0:
            self.velocity = self.delta / self.time_diff
        else:
            self.velocity = 0

    def get_position(self): 
        """!
            @brief Returns encoder position
            @details
            @return The position of the encoder shaft
        """
        
        return self.datumPosition
        
    def set_position(self, position):
        """!
            @brief Sets encoder position
            @details
            @param position The new position of the encoder shaft
        """
        
        self.datumPosition = self.position
    
    def get_delta(self):
        """!
            @brief Returns encoder delta
            @details
            @return The change in position of the encoder shaft
            between the two most recent updates
        """
        return self.delta
    
    def get_velocity(self):
        """!
        @brief Returns velocity calculated in the "Update" function.
        @details
        @return The angular velocity in """
        return self.velocity
if __name__ =='__main__':    
    e_pin_1 = pyb.Pin.cpu.C6
    e_pin_2 = pyb.Pin.cpu.C7
    e_channel = 8
    enc_1 = Encoder(e_channel, e_pin_1, e_pin_2)
    e_2 = pyb.Pin.cpu.B6
    e_21 = pyb.Pin.cpu.B7
    enc_c_2 = 4
    enc_2 = Encoder(enc_c_2, e_2, e_21)
    while True:
        enc_1.update()
        enc_2.update()
        print('1', enc_1.get_position())
        print('2', enc_2.get_position())
        utime.sleep_ms(10)