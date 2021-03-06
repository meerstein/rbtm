#!/usr/bin/env python
# -*- coding:utf-8 -*- 


##############################################################################
## license :
##============================================================================
##
## File :        XRayShutter.py
## 
## Project :     XRayshutter
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
## $Author :      mariya.riabova$
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

"""Shutter of the X-ray sourse. It is used for opening and closing a shutter."""

__all__ = ["XRayShutter", "XRayShutterClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(XRayShutter.additionnal_import) ENABLED START -----#
import ConfigParser
import threading
from shutter import Shutter
#----- PROTECTED REGION END -----#  //  XRayShutter.additionnal_import

## Device States Description
## CLOSE : Shutter is closed.
## OPEN : Shutter is open.

class XRayShutter (PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(XRayShutter.global_variables) ENABLED START -----#
    EPS = 1e-5

    CONFIG_PATH = 'tango_ds.cfg'

    def get_port_from_config(self):
        config = ConfigParser.RawConfigParser()
        config.read(XRayShutter.CONFIG_PATH)
        shutter_port = config.get("shutter", "port")
        relay_number = int(config.get("shutter", "relay"))
        return shutter_port, relay_number

    #----- PROTECTED REGION END -----#  //  XRayShutter.global_variables

    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        XRayShutter.init_device(self)
        #----- PROTECTED REGION ID(XRayShutter.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRayShutter.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(XRayShutter.delete_device) ENABLED START -----#
        #----- PROTECTED REGION END -----#  //  XRayShutter.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        #----- PROTECTED REGION ID(XRayShutter.init_device) ENABLED START -----#
        shutter_port, relay_number = self.get_port_from_config()

        self.shutter = Shutter(shutter_port, relay_number)
        if self.shutter.is_open():
            self.set_state(PyTango.DevState.OPEN)
        else:
            self.set_state(PyTango.DevState.CLOSE)

        #----- PROTECTED REGION END -----#  //  XRayShutter.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(XRayShutter.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRayShutter.always_executed_hook

    #-----------------------------------------------------------------------------
    #    XRayShutter read/write attribute methods
    #-----------------------------------------------------------------------------
    
    
    
        #----- PROTECTED REGION ID(XRayShutter.initialize_dynamic_attributes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRayShutter.initialize_dynamic_attributes
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(XRayShutter.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRayShutter.read_attr_hardware


    #-----------------------------------------------------------------------------
    #    XRayShutter command methods
    #-----------------------------------------------------------------------------
    
    def Open(self, argin):
        """ Opens the shutter
        
        :param argin: Automatically closes the shutter after the given time. Stays opened if 0.
        :type: PyTango.DevDouble
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In Open()")
        #----- PROTECTED REGION ID(XRayShutter.Open) ENABLED START -----#
        # check time for reasonable values.
        # time in seconds currently, maybe we need ms. threading.Timer accepts floating point seconds.
        # looks like tango doesn't have function overloading. impossible to have zero or one argument for function
        
        time = argin

        self.shutter.open()
        self.set_state(PyTango.DevState.OPEN)

        if abs(time) < XRayShutter.EPS:
            pass
        elif time < 0:
            PyTango.Except.throw_exception("XRayShutter_IllegalArgument",
                                           "Time can't be negative",
                                           "XRayShutter.Open()")
        else:
            threading.Timer(time, self.Close, args=[0]).start()

        #----- PROTECTED REGION END -----#  //  XRayShutter.Open
        
    def Close(self, argin):
        """ Closes the shutter
        
        :param argin: Automatically opens the shutter after the given time. Stays closed if 0.
        :type: PyTango.DevDouble
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In Close()")
        #----- PROTECTED REGION ID(XRayShutter.Close) ENABLED START -----#

        time = argin

        self.shutter.close()
        self.set_state(PyTango.DevState.CLOSE)

        if abs(time) < XRayShutter.EPS:
            pass
        elif time < 0:
            PyTango.Except.throw_exception("XRayShutter_IllegalArgument",
                                           "Time can't be negative",
                                           "XRayShutter.Close()")
        else:
            threading.Timer(time, self.Open, args=[0]).start()

        #----- PROTECTED REGION END -----#  //  XRayShutter.Close
        

class XRayShutterClass(PyTango.DeviceClass):
    #--------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(XRayShutter.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#  //  XRayShutter.global_class_variables

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`XRayShutter.initialize_dynamic_attributes` for each device
    
        :param dev_list: list of devices
        :type dev_list: :class:`PyTango.DeviceImpl`"""
    
        for dev in dev_list:
            try:
                dev.initialize_dynamic_attributes()
            except:
                import traceback
                dev.warn_stream("Failed to initialize dynamic attributes")
                dev.debug_stream("Details: " + traceback.format_exc())
        #----- PROTECTED REGION ID(XRayShutter.dyn_attr) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#  //  XRayShutter.dyn_attr

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        'Open':
            [[PyTango.DevDouble, "Automatically closes the shutter after the given time. Stays opened if 0."],
            [PyTango.DevVoid, "none"]],
        'Close':
            [[PyTango.DevDouble, "Automatically opens the shutter after the given time. Stays closed if 0."],
            [PyTango.DevVoid, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(XRayShutterClass,XRayShutter,'XRayShutter')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()
