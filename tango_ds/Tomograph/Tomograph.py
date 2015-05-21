#!/usr/bin/env python
# -*- coding:utf-8 -*- 


##############################################################################
## license :
##============================================================================
##
## File :        Tomograph.py
## 
## Project :     Tomograph
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

"""Wrapper class for Source, Shutter, Motor, Detector classes"""

__all__ = ["Tomograph", "TomographClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
# ----- PROTECTED REGION ID(Tomograph.additionnal_import) ENABLED START -----#

import datetime
import json

# ----- PROTECTED REGION END -----# //  Tomograph.additionnal_import

## Device States Description
## ON : 
## OFF : 

class Tomograph (PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(Tomograph.global_variables) ENABLED START -----#

    #----- PROTECTED REGION END -----#  //  Tomograph.global_variables

    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        Tomograph.init_device(self)
        #----- PROTECTED REGION ID(Tomograph.__init__) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Tomograph.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(Tomograph.delete_device) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Tomograph.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_xraysource_voltage_read = 0.0
        self.attr_xraysource_current_read = 0.0
        self.attr_angle_position_read = 0.0
        self.attr_horizontal_position_read = 0
        self.attr_vertical_position_read = 0
        #----- PROTECTED REGION ID(Tomograph.init_device) ENABLED START -----#

        self.set_state(PyTango.DevState.OFF)

        self.motor = PyTango.DeviceProxy('tomo/motor/1')
        self.source = PyTango.DeviceProxy('tomo/source/1')
        self.shutter = PyTango.DeviceProxy('tomo/shutter/1')
        self.detector = PyTango.DeviceProxy('tomo/detector/1')
        self.detector.set_timeout_millis(40000)

        self.SelfTest()

        self.attr_xraysource_voltage_read = self.source.voltage
        self.attr_xraysource_current_read = self.source.current

        self.attr_angle_position_read = self.motor.angle_position
        self.attr_horizontal_position_read = self.motor.horizontal_position
        self.attr_vertical_position_read = self.motor.vertical_position

        self.set_state(PyTango.DevState.ON)

        #----- PROTECTED REGION END -----#  //  Tomograph.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(Tomograph.always_executed_hook) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Tomograph.always_executed_hook

    #-----------------------------------------------------------------------------
    #    Tomograph read/write attribute methods
    #-----------------------------------------------------------------------------
    
    def read_xraysource_voltage(self, attr):
        self.debug_stream("In read_xraysource_voltage()")
        #----- PROTECTED REGION ID(Tomograph.xraysource_voltage_read) ENABLED START -----#

        self.attr_xraysource_voltage_read = self.source.voltage
        attr.set_value(self.attr_xraysource_voltage_read)
        
        #----- PROTECTED REGION END -----#  //  Tomograph.xraysource_voltage_read
        
    def write_xraysource_voltage(self, attr):
        self.debug_stream("In write_xraysource_voltage()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Tomograph.xraysource_voltage_write) ENABLED START -----#
        self.source.voltage = data
        #----- PROTECTED REGION END -----#  //  Tomograph.xraysource_voltage_write
        
    def read_xraysource_current(self, attr):
        self.debug_stream("In read_xraysource_current()")
        #----- PROTECTED REGION ID(Tomograph.xraysource_current_read) ENABLED START -----#

        self.attr_xraysource_current_read = self.source.current
        attr.set_value(self.attr_xraysource_current_read)
        
        #----- PROTECTED REGION END -----#  //  Tomograph.xraysource_current_read
        
    def write_xraysource_current(self, attr):
        self.debug_stream("In write_xraysource_current()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Tomograph.xraysource_current_write) ENABLED START -----#
        self.source.current = data
        #----- PROTECTED REGION END -----#  //  Tomograph.xraysource_current_write
        
    def read_angle_position(self, attr):
        self.debug_stream("In read_angle_position()")
        #----- PROTECTED REGION ID(Tomograph.angle_position_read) ENABLED START -----#

        self.attr_angle_position_read = self.motor.angle_position
        attr.set_value(self.attr_angle_position_read)
        
        #----- PROTECTED REGION END -----#  //  Tomograph.angle_position_read
        
    def write_angle_position(self, attr):
        self.debug_stream("In write_angle_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Tomograph.angle_position_write) ENABLED START -----#

        self.motor.angle_position = data
        
        #----- PROTECTED REGION END -----#  //  Tomograph.angle_position_write
        
    def read_horizontal_position(self, attr):
        self.debug_stream("In read_horizontal_position()")
        #----- PROTECTED REGION ID(Tomograph.horizontal_position_read) ENABLED START -----#

        self.attr_horizontal_position_read = self.motor.horizontal_position
        attr.set_value(self.attr_horizontal_position_read)
        
        #----- PROTECTED REGION END -----#  //  Tomograph.horizontal_position_read
        
    def write_horizontal_position(self, attr):
        self.debug_stream("In write_horizontal_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Tomograph.horizontal_position_write) ENABLED START -----#

        self.motor.horizontal_position = data
        
        #----- PROTECTED REGION END -----#  //  Tomograph.horizontal_position_write
        
    def read_vertical_position(self, attr):
        self.debug_stream("In read_vertical_position()")
        #----- PROTECTED REGION ID(Tomograph.vertical_position_read) ENABLED START -----#

        self.attr_vertical_position_read = self.motor.vertical_position
        attr.set_value(self.attr_vertical_position_read)
        
        #----- PROTECTED REGION END -----#  //  Tomograph.vertical_position_read
        
    def write_vertical_position(self, attr):
        self.debug_stream("In write_vertical_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(Tomograph.vertical_position_write) ENABLED START -----#

        self.motor.vertical_position = data

        #----- PROTECTED REGION END -----#  //  Tomograph.vertical_position_write
        
    
    
        #----- PROTECTED REGION ID(Tomograph.initialize_dynamic_attributes) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Tomograph.initialize_dynamic_attributes
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Tomograph.read_attr_hardware) ENABLED START -----#

        #----- PROTECTED REGION END -----#  //  Tomograph.read_attr_hardware


    #-----------------------------------------------------------------------------
    #    Tomograph command methods
    #-----------------------------------------------------------------------------
    
    def DevicesInfo(self):
        """ Returns information about available devices
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevString """
        self.debug_stream("In DevicesInfo()")
        argout = ''
        # ----- PROTECTED REGION ID(Tomograph.DevicesInfo) ENABLED START -----#

        # ----- PROTECTED REGION END -----# //  Tomograph.DevicesInfo
        return argout
        
    def SelfTest(self):
        """ Tests equipment
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In SelfTest()")
        #----- PROTECTED REGION ID(Tomograph.SelfTest) ENABLED START -----#

        self.motor.ping()
        self.source.ping()
        self.shutter.ping()
        self.detector.ping()

        #----- PROTECTED REGION END -----#  //  Tomograph.SelfTest
        
    def MotorStatus(self):
        """ Returns motor information
        
        :param : 
        :type: PyTango.DevVoid
        :return: Information about motor
        :rtype: PyTango.DevString """
        self.debug_stream("In MotorStatus()")
        argout = ''
        #----- PROTECTED REGION ID(Tomograph.MotorStatus) ENABLED START -----#

        motor_data = {'state': str(self.motor.State()),
                      'horizontal_position': self.motor.horizontal_position,
                      'vertical_position': self.motor.vertical_position,
                      'angle_position': self.motor.angle_position}

        json_data = json.dumps(motor_data)
        argout = json_data

        #----- PROTECTED REGION END -----#  //  Tomograph.MotorStatus
        return argout
        
    def ResetAnglePosition(self):
        """ Sets current motor position to 0
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In ResetAnglePosition()")
        #----- PROTECTED REGION ID(Tomograph.ResetAnglePosition) ENABLED START -----#
        self.motor.ResetAnglePosition()
        #----- PROTECTED REGION END -----#  //  Tomograph.ResetAnglePosition
        
    def XRaySourceStatus(self):
        """ 
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevString """
        self.debug_stream("In XRaySourceStatus()")
        argout = ''
        #----- PROTECTED REGION ID(Tomograph.XRaySourceStatus) ENABLED START -----#

        source_data = {'model': 'Isovolt 3003',
                       'state': str(self.source.State()),
                       'voltage': self.source.voltage, 'current': self.source.current}

        json_data = json.dumps(source_data)
        argout = json_data

        #----- PROTECTED REGION END -----#  //  Tomograph.XRaySourceStatus
        return argout
        
    def PowerOn(self):
        """ Turns on the X-ray source
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In PowerOn()")
        #----- PROTECTED REGION ID(Tomograph.PowerOn) ENABLED START -----#

        self.source.On()

        #----- PROTECTED REGION END -----#  //  Tomograph.PowerOn
        
    def PowerOff(self):
        """ Turns off the X-ray source
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In PowerOff()")
        # ----- PROTECTED REGION ID(Tomograph.PowerOff) ENABLED START -----#

        self.source.Off()

        #----- PROTECTED REGION END -----#  //  Tomograph.PowerOff
        
    def ShutterStatus(self):
        """ 
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevString """
        self.debug_stream("In ShutterStatus()")
        argout = ''
        #----- PROTECTED REGION ID(Tomograph.ShutterStatus) ENABLED START -----#

        shutter_data = {'state': str(self.shutter.State())}

        json_data = json.dumps(shutter_data)
        argout = json_data

        #----- PROTECTED REGION END -----#  //  Tomograph.ShutterStatus
        return argout
        
    def OpenShutter(self, argin):
        """ 
        
        :param argin: 
        :type: PyTango.DevLong
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In OpenShutter()")
        #----- PROTECTED REGION ID(Tomograph.OpenShutter) ENABLED START -----#

        self.shutter.Open(argin)

        # ----- PROTECTED REGION END -----# //  Tomograph.OpenShutter
        
    def CloseShutter(self, argin):
        """ 
        
        :param argin: 
        :type: PyTango.DevLong
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In CloseShutter()")
        # ----- PROTECTED REGION ID(Tomograph.CloseShutter) ENABLED START -----#

        self.shutter.Close(argin)

        #----- PROTECTED REGION END -----#  //  Tomograph.CloseShutter
        
    def DetectorStatus(self):
        """ 
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevString """
        self.debug_stream("In DetectorStatus()")
        argout = ''
        #----- PROTECTED REGION ID(Tomograph.DetectorStatus) ENABLED START -----#

        detector_data = {'model': 'Ximea xiRAY',
                         'state': str(self.detector.State())}

        json_data = json.dumps(detector_data)
        argout = json_data

        #----- PROTECTED REGION END -----#  //  Tomograph.DetectorStatus
        return argout
        
    def GetFrame(self, argin):
        """ Return image from detector with metadata in JSON
        
        :param argin: exposure
        :type: PyTango.DevLong
        :return: 
        :rtype: PyTango.DevString """
        self.debug_stream("In GetFrame()")
        argout = ''
        #----- PROTECTED REGION ID(Tomograph.GetFrame) ENABLED START -----#

        exposure = argin

        self.detector.exposure = exposure
        image = self.detector.GetFrame()
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        detector_data = {'model': 'Ximea xiRAY'}
        image_data = {'exposure': exposure, 'datetime': current_datetime, 'detector': detector_data}
        object_data = {'angle position': self.motor.angle_position}
        shutter_data = {'open': self.shutter.State() == PyTango.DevState.OPEN}
        source_data = {'voltage': self.source.voltage, 'current': self.source.current}

        json_data = json.dumps({'image_data': image_data, 'object': object_data,
                                'shutter': shutter_data, 'X-ray source': source_data})

        argout = json_data

        #----- PROTECTED REGION END -----#  //  Tomograph.GetFrame
        return argout
        
    def MoveAway(self):
        """ 
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In MoveAway()")
        #----- PROTECTED REGION ID(Tomograph.MoveAway) ENABLED START -----#
        self.motor.horizontal_position = -4200
        #----- PROTECTED REGION END -----#  //  Tomograph.MoveAway
        
    def MoveBack(self):
        """ 
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In MoveBack()")
        #----- PROTECTED REGION ID(Tomograph.MoveBack) ENABLED START -----#
        self.motor.horizontal_position = 0
        #----- PROTECTED REGION END -----#  //  Tomograph.MoveBack
        

class TomographClass(PyTango.DeviceClass):
    #--------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(Tomograph.global_class_variables) ENABLED START -----#

    #----- PROTECTED REGION END -----#  //  Tomograph.global_class_variables

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`Tomograph.initialize_dynamic_attributes` for each device
    
        :param dev_list: list of devices
        :type dev_list: :class:`PyTango.DeviceImpl`"""
    
        for dev in dev_list:
            try:
                dev.initialize_dynamic_attributes()
            except:
                import traceback
                dev.warn_stream("Failed to initialize dynamic attributes")
                dev.debug_stream("Details: " + traceback.format_exc())
        #----- PROTECTED REGION ID(Tomograph.dyn_attr) ENABLED START -----#

                #----- PROTECTED REGION END -----#  //  Tomograph.dyn_attr

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        'DevicesInfo':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevString, "none"]],
        'SelfTest':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'MotorStatus':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevString, "Information about motor"]],
        'ResetAnglePosition':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'XRaySourceStatus':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevString, "none"]],
        'PowerOn':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'PowerOff':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'ShutterStatus':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevString, "none"]],
        'OpenShutter':
            [[PyTango.DevLong, "none"],
            [PyTango.DevVoid, "none"]],
        'CloseShutter':
            [[PyTango.DevLong, "none"],
            [PyTango.DevVoid, "none"]],
        'DetectorStatus':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevString, "none"]],
        'GetFrame':
            [[PyTango.DevLong, "exposure"],
            [PyTango.DevString, "none"]],
        'MoveAway':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        'MoveBack':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        'xraysource_voltage':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'unit': "kV",
            } ],
        'xraysource_current':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'unit': "mA",
            } ],
        'angle_position':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'horizontal_position':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'vertical_position':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(TomographClass,Tomograph,'Tomograph')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()
