#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Outputs max peak height for spectral lines above the discriminator height in and xgremlin .asc output file

Command line: peakfind [input .asc file] [discriminator] [output file]
"""

author = "Christian Clear"
version = "1.0"
date = "22-10-15"

import sys

if len(sys.argv) == 1:
    print """
    ---------------------------------------------------------------------------
    FTS Peak Finder v%s (built %s)
    
    Syntax usage:
        ftspeakfind <input file> <discriminator> <output file>
    
    <input file>    :  An Xgremlin .asc file creates using writeasc
    <discriminator> :  The minumum peak height
    <output file>   :  Either a .aln or .syn filetype must be used

    ---------------------------------------------------------------------------
    """ % (version, date)
    
    sys.exit()


input_filetype = str(sys.argv[3]).split(".")[-1]  # returns the input filetype

if input_filetype != "asc":
    print "ERROR: the input file must be an Xgremlin .asc file"
    sys.exit()
    

f = open(str(sys.argv[1]))
fout = open(str(sys.argv[3]), 'w+')


line = []
height = []
wavenumbers = []

for point in f:
    if point[0] == "!":  # skips header lines at the top of the input file
        continue
    
    if float(point[14:]) >= float(sys.argv[2]):  # check to see of point has SNR >= discriminator
        line.append(point)
        height.append(float(point[14:]))
    
    else:
        if not height:  # Check if height is empty - eliminates problem with having an empty height array on the first iteration
            continue
        else:
            wavenumbers.append(line[height.index(max(height))])
            line = []   
            height = []
            

output_filetype = str(sys.argv[3]).split(".")[-1]  # returns the output filetype

if output_filetype == "syn":
    for line in wavenumbers:
        fout.write('s6D)4d e5P       ' + line[:12]+ '   30.0000   100.00  0.0000' + '\n')

elif output_filetype == "aln":
    fout.write("""  NO wavenumber correction applied. (wavcorr =    0.0000000000000000       not used.)
  NO air correction applied to wavelengths.
  NO intensity calibration.
  line    wavenumber      peak    width      dmp   eq width   itn   H tags     epstot     epsevn     epsodd     epsran  identification\n""")
    for line in wavenumbers:
        fout.write("     1  " + line[1:12] + " " + line[14:26] + "    00.00  -0.0000 0.0000E+00     0   0    F .00000E+00 .00000E+00 .00000E+00 .00000E+00 no id                          000.000000\n")

else:
    print "Filetype is not supported. Please specify .aln or .syn"


f.close()
fout.close()    