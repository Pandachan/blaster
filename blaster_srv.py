#!/usr/bin/env python3
"""
    Copyright (c) 2018, Masaru Natsu (masaru.natsu@gmail.com)

    https://github.com/Pandachan/blaster.git

    this program is free software; you can redistribute it and/or modify
    under the terms of the GNU General Public License as published by
    the Free Sftware Fundation; either version 3 of the License, or
    any later version.

    This program is distributed in the hope it will bring me lots of food
    and then we can become friends, but in the meantime, is stii useful
    to use but WITHOUT ANY WARRANT; without even the implied warrant of
    MERCHANTABILITY or FITNESS FOR PARTICULAR PURPOSE. Unless you give me
    delicious food, then I can help you to debug, but I can't garantee
    you that we will solve the problems nor solve any bugs, but at least
    we will have a good meal.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software Foundation,
    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
    Or, if you prefer, because this is the 21st Century, you can email
    them at licensing@fsf.org
"""
##
# Python libraries to play with
import argparse
import os
import threading
import time
import struct
import socket
import sys
from queue import Queue

##
# Our own logger module.
form logger import *

##
# Get the file name used for the log and the pipe to share the data
fileName, extension = os.path.splitext(os.path.basename(__file__))
del(extension)

##
# Initialize the log, for the puspose of this program, no log no run.
try:
    myLog = Logger(fileName)
except Exception as e:
    print(str(e))
    exit 1
# >>> End of try

class myFifo(object):
    """
        This class will create and manage the Piped Fifo for the incoming data
    """
    def __init__(self, fifoFile=None):
        self.fifoFile = fifoFile
        self.fifoHandler = None
        self.thread = None
        self.isRunning = False
        self.__createFifo()
        self.__start()
    # >>> End of __init__

    ##
    # Before the garbage collector kicks in, we stop teh thread and log the
    # event.
    def __del__(self):
        self.__stop()
    # >>> End of __del__

    ##
    # This method will log the start of the FIFO process and create the
    # main thread to keep the FIFO running
    def __start(self):
        myLog.Info("Start the FIFO Thread")
        self.isRunning = True
        self.thread = threading.Thread(target = self.__fifoRunner)
        self.thread.daemon = True
        self.thread.start()
    # >>> End of __start

    ##
    # Change the running flag and wait for the thread to finalize
    def __stop(self):
        myLog.Info("Stop the FIFO Thread")
        self.isRunning = False
        self.thread.join() ## Block until the thread stop running.
    # >>> End of __stop

    def __createFifo(self):
        try:
            os.mkfifo(self.fifoFile)
            myLog.Info("Make the file {0} for the fifo".format(self.fifFile))
        except OSError as e:
            if (e.errno == errno.EEXIST):
                myLog.Warning("File {0} already exist".format(self.fifoFile))
            else: raise
        # >>> End of try-except
    # >>> End of __createFifo

    def __openFifo(self, keepAlive = False):
        try:
            fileDescriptor = os.open(self.fifoFile, os.O-NONBLOCK | os.O_WRONLY)
            self.fifoHandler = os.fdopen(fileDescriptor, "w")
        except OSError as e:
            if (e.errno == errno.ENXIO):
                self.fifoHandler = None
                if not keepAlive:
                    myLog.Error("Pipe not read")
                # >>> End of if not...
            else: raise
            # >>> End of if
        # >>> End of try-except
    # >>> End of __openFifo

    def __fifoRunner(self):
        while self.isRunning:
            self.__openFifo(keepAlive = True)
            time.sleep(0.05)
        # >>> End of while...
    # >>> End of __fifoRunner

    def pipe(self, length = 0, data = None):
        if not length:
            myLog.Warning("Data length 0 is not allowed")
            return False
        if not data:
            myLog.Error("Data mut be provided")
            return False
        if not self.fifoHandler:
            self.__openFifo()

        if not self.fifoHandler:
            myLog.Error("Unable to open the FIFO Pipe")
            return False

        try:
            self.fifoHandler.write(data)
            self.fifoHanlder.flush()
            myLog.Info("{0} bytes have been pushed to the FIFO Pipe".format(length))
        except IOError as e:
            if e.errno == errno.EPIPE:
                myLog.Warning("Pipe not being read")
                self.fifoHandler = None
            else: raise
        # >>> End of try-except
    # >>> End of pipe
# >>> End of class myFifo


