#!/usr/bin/env python
# -*- coding:utf-8 -*- 


##############################################################################
## license :
##============================================================================
##
## File :        HorizontalMotor.py
## 
## Project :     
##
## This file is part of Tango device class.
## 
## Tango is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Tango is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Tango.  If not, see <http://www.gnu.org/licenses/>.
## 
##
## $Author :      diana.ichalova$
##
## $Revision :    $
##
## $Date :        $
##
## $HeadUrl :     $
##============================================================================
##            This file is generated by POGO
##    (Program Obviously used to Generate tango Object)
##
##        (c) - Software Engineering Group - ESRF
##############################################################################

""""""

__all__ = ["HorizontalMotor", "HorizontalMotorClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(HorizontalMotor.additionnal_import) ENABLED START -----#
import sys
sys.path.insert(0, 'lib')
import ximc
import time
import ConfigParser
from contextlib import closing
#----- PROTECTED REGION END -----#	//	HorizontalMotor.additionnal_import

## Device States Description
## STANDBY : 
## MOVING : 

class HorizontalMotor (PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(HorizontalMotor.global_variables) ENABLED START -----#
    CONFIG_PATH = 'tango_ds.cfg'

    def get_port_from_config(self):
        config = ConfigParser.RawConfigParser()
        config.read(HorizontalMotor.CONFIG_PATH)
        motor_port = config.get("horizontal motor", "port")
        return motor_port

    def _read_position(self, motor):
        self.debug_stream("In _read_position()")

        self.debug_stream("Reading position...")
        try:
            steps = motor.get_position()
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            self.init_device()
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise
        self.info_stream("Position = {}".format(steps))
        return steps

    def _write_position(self, motor, steps):
        self.debug_stream("In _write_position()")

        self.info_stream("Setting position = {}".format(steps))
        try:
            motor.move_to_position(steps)
            motor.wait_for_stop()
            self.debug_stream("Position has been set")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            self.init_device()
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise
    #----- PROTECTED REGION END -----#	//	HorizontalMotor.global_variables

    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        HorizontalMotor.init_device(self)
        #----- PROTECTED REGION ID(HorizontalMotor.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(HorizontalMotor.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_position_read = 0
        self.attr_speed_read = 0
        self.attr_accel_read = 0
        #----- PROTECTED REGION ID(HorizontalMotor.init_device) ENABLED START -----#

        motor_port = self.get_port_from_config()

        try:
            self.debug_stream("Creating link to motor drivers...")
            self.horizontal_motor = ximc.Motor(motor_port, 1)
            self.debug_stream("Links were created")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

        with closing(self.horizontal_motor.open()):
            self.horizontal_motor.set_move_settings(200, 200)
            steps = self._read_position(self.horizontal_motor)
        self.attr_position_read = steps

        self.set_state(PyTango.DevState.STANDBY)
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(HorizontalMotor.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.always_executed_hook

    #-----------------------------------------------------------------------------
    #    HorizontalMotor read/write attribute methods
    #-----------------------------------------------------------------------------
    
    def read_position(self, attr):
        self.debug_stream("In read_position()")
        #----- PROTECTED REGION ID(HorizontalMotor.position_read) ENABLED START -----#
        with closing(self.horizontal_motor.open()):
            self.attr_position_read = self._read_position(self.horizontal_motor)
        attr.set_value(self.attr_position_read)
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.position_read
        
    def write_position(self, attr):
        self.debug_stream("In write_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(HorizontalMotor.position_write) ENABLED START -----#
        prev_state = self.get_state()
        self.set_state(PyTango.DevState.MOVING)
        steps = data
        with closing(self.horizontal_motor.open()):
            self._write_position(self.horizontal_motor, steps)
        self.set_state(prev_state)
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.position_write
        
    def read_speed(self, attr):
        self.debug_stream("In read_speed()")
        #----- PROTECTED REGION ID(HorizontalMotor.speed_read) ENABLED START -----#
        with closing(self.horizontal_motor.open()):
            self.attr_speed_read = self.horizontal_motor.get_move_settings()["Speed"]
        attr.set_value(self.attr_speed_read)
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.speed_read
        
    def write_speed(self, attr):
        self.debug_stream("In write_speed()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(HorizontalMotor.speed_write) ENABLED START -----#
        speed = data
        with closing(self.horizontal_motor.open()):
            self.horizontal_motor.set_move_settings(speed=speed)
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.speed_write
        
    def read_accel(self, attr):
        self.debug_stream("In read_accel()")
        #----- PROTECTED REGION ID(HorizontalMotor.accel_read) ENABLED START -----#
        with closing(self.horizontal_motor.open()):
            self.attr_accel_read = self.horizontal_motor.get_move_settings()["Accel"]
        attr.set_value(self.attr_accel_read)
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.accel_read
        
    def write_accel(self, attr):
        self.debug_stream("In write_accel()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(HorizontalMotor.accel_write) ENABLED START -----#
        accel = data
        with closing(self.horizontal_motor.open()):
            self.horizontal_motor.set_move_settings(accel=accel)
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.accel_write
        
    
    
        #----- PROTECTED REGION ID(HorizontalMotor.initialize_dynamic_attributes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.initialize_dynamic_attributes
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(HorizontalMotor.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.read_attr_hardware


    #-----------------------------------------------------------------------------
    #    HorizontalMotor command methods
    #-----------------------------------------------------------------------------
    

class HorizontalMotorClass(PyTango.DeviceClass):
    #--------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(HorizontalMotor.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	HorizontalMotor.global_class_variables

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`HorizontalMotor.initialize_dynamic_attributes` for each device
    
        :param dev_list: list of devices
        :type dev_list: :class:`PyTango.DeviceImpl`"""
    
        for dev in dev_list:
            try:
                dev.initialize_dynamic_attributes()
            except:
                import traceback
                dev.warn_stream("Failed to initialize dynamic attributes")
                dev.debug_stream("Details: " + traceback.format_exc())
        #----- PROTECTED REGION ID(HorizontalMotor.dyn_attr) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	HorizontalMotor.dyn_attr

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        }


    #    Attribute definitions
    attr_list = {
        'position':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "position",
                'unit': "steps",
                'max value': "3000",
                'min value': "-5000",
            } ],
        'speed':
            [[PyTango.DevULong,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "speed",
                'unit': "steps/s",
                'max value': "2000",
                'min value': "0",
            } ],
        'accel':
            [[PyTango.DevULong,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "acceleration",
                'unit': "steps/s^2",
                'max value': "2000",
                'min value': "1",
            } ],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(HorizontalMotorClass,HorizontalMotor,'HorizontalMotor')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()
