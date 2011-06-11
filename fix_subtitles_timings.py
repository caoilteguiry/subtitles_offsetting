#!/usr/bin/env python

"""Offsets the timings in mis-aligned subrip subtitles files.

Author: Caoilte Guiry
Name: fix_subtitles_offset.py 
License: BSD License

"""

import os
import sys
from datetime import timedelta
import re

__author__ = "Caoilte Guiry"
__copyright__ = "Copyright (c) 2011 Caoilte Guiry."
__version__ = "1.0.1"
__license__ = "BSD License"

def main():
    """Read user-input for subtitles file and offset, and offset timings.""" 
    # Check the correct number of args have been passed
    # TODO: implement proper options parsing here (allow explicit specification
    # of hours, mins, secs)
    if len(sys.argv)!=3:
        show_usage()
        sys.exit(1)

    # Input validation
    try:
        seconds_offset = int(sys.argv[1])
    except ValueError:
        print "seconds_offset must be an integer"
        sys.exit(1)    

    # Create an offset which we will add to the current timings (this value can 
    # be either positive or negative)
    offset = timedelta(seconds=seconds_offset)
        
    subtitles_file = sys.argv[2]    

    # We'll just append a ".offset" to the file we'll write. We want to make  
    # sure it doesn't already exist, to prevent accidental clobbering
    new_filename = subtitles_file+".offset"
    if os.path.isfile(new_filename):
        answer = raw_input("File '%s' already exists. Do you wish to overwrite "
                           "it?" % new_filename)
        if answer.lower()[0]!="y":
            print "Exiting..."
            sys.exit(1)

    
    offset_timings(subtitles_file, new_filename, offset)
    
    
def offset_timings(subtitles_file, new_filename, offset):
    """a subtitles file and offset the timings by a specified amount."""    
    new_file = open(new_filename, "w")
    # Compile a re which we'll use to match the timing commands 
    prog = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})[ ]+[-]+>"
                       "[ ]+(\d{2}):(\d{2}):(\d{2}),(\d{3})")
    # Read the subtiltes file, updating the lines if necessary
    try:        
        for line in open(subtitles_file,'r'):
            re_search = prog.findall(line)
            
            # Check if a timing command was found
            if(re_search):
                # Extract the values...
                [h1, m1, s1, ms1, h2, m2, s2, ms2] = re_search[0]
                t1 = timedelta(hours=int(h1), minutes=int(m1), seconds=int(s1),
                               milliseconds=int(ms1))
                t2 = timedelta(hours=int(h2), minutes=int(m2), seconds=int(s2), 
                               milliseconds=int(ms2))
                # ... add add the offset
                new_t1, new_t2 = t1+offset, t2+offset  
                # Extract the values again (would be great if timedelta had 
                # hours and minutes attributes)
                new_h1, remainder = divmod(new_t1.seconds, 3600)
                new_m1, new_s1 = divmod(remainder, 60)
                new_ms1 = new_t1.microseconds/1000
                new_h2, remainder = divmod(new_t2.seconds, 3600)
                new_m2, new_s2 = divmod(remainder, 60)
                new_ms2 = new_t2.microseconds/1000                
                # Write the updated timing command
                new_file.write("%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d\n"%
                                (new_h1, new_m1, new_s1, new_ms1, new_h2,
                                 new_m2, new_s2, new_ms2))
            else:
                # Not a timing command, no update required
                # Fix line endings.. :-/
                new_file.write(line.rstrip("\r\n")+"\n")
        new_file.close()
        print "Updated subtitles have been written to '%s'." % (new_filename)
    except IOError:
        print "Invalid filename '%s'" % (subtitles_file)
        show_usage()
        sys.exit(1)
            
    

def show_usage():
    """ print script usage """
    print "Usage: %s <seconds_offset> <subtitles-file>" % (sys.argv[0])


if __name__ == "__main__":
    sys.exit(main())
