#!/usr/bin/env python3
# get_bt_itp
import sys
import os
import pandas as pd
import datetime
from scipy import interpolate

def usage():
    name = sys.argv[0]
    print ("----------------------------------------------")
    print ("USAGE: ", name, " TCID YYYY MM DD HH [sep]")
    print ("")
    print ("       argv1:  Target typhoon")
    print ("                  TCID: tropical cyclon number ID (TCID)")
    print (" ")
    print ("       argv2-5: Target date and time")
    print ("                   YYYY: year")
    print ("                     MM: month")
    print ("                     DD: day")
    print ("                     HH: hour")
    print ("")
    print ("       argv6  : Separator for output (option)")
    print ("                   ' ': space (default)")
    print ("                   ',': comma")
    print ("")
    print ("OUTPUT: hourly interpolated data")
    print ("    YYYYMMDDHH  lon  lat  p")
    print ("")
    print ("----------------------------------------------")
    sys.exit()

def variables():
    print ("----------------------------------------------")
    print (" VARIABLES:")
    print ("   time: Time of analysis (yymmddhh)")
    print ("  grade: 2-9 (see doc for detail)")
    print ("    lat: Latitude of the center (0.1deg.)")
    print ("    lon: Longitude of the center (0.1deg.)")
    print ("      p: Central pressure (hPa)")
    print ("     ws: Maximum sustained wind speed (kt)")
    print ("----------------------------------------------")
    sys.exit()

def header(all_lines, ityid):
    n=0
    for line in all_lines:
     if line.find('66666') >= 0:
       hline = line.strip()
       col = hline.split()
       tyid = col[1]
       num_data_line = col[2]
       yy = tyid[0:2]
       nstart = n + 1
       if (ityid == tyid):
         print(hline)
       elif (ityid == "ALL"):
         print(hline)
       elif (ityid == "NONE") and (iyy == yy):
        print(hline)
     n += 1

def data_vars(all_lines, ityid, var_list, sep):
    of = open(tmp_csv,'wt')
    sw = 0
    nd = 0
    for line in all_lines:
     if sw == 0:
      if line.find('6666') >= 0:
       hline = line.strip()
       col = hline.split()
       tyid = col[1]
       num_data_line = int(col[2])
       yy = tyid[0:2]
       if (ityid == tyid):
#         print(hline)
         sw = 1
     elif sw == 1:
       if (ityid == tyid):
        if nd <= num_data_line-1:
         dline = line.strip()
         dline_var = dline.split()
         out_list=[]
         out_list =  make_out_list(dline_var,var_list, out_list)
         out = sep.join(out_list)
         of.write(out)
         of.write("\n")
         nd += 1
        else:
         sw=0
         nd=0
         of.close()

def interpolation(var_list, yy, mo, dy, hr, sep):
    # out_sep
    if (sep == ' '):
     out_sep=' '
    else:
     out_sep=sep
    
    # read csv
    df = pd.read_csv(tmp_csv, names=(var_list))

    # define date_time
    df['date_time']=pd.to_datetime(df['time'], format='%y%m%d%H')

    # set index
    df = df.set_index('date_time')

    # time index
    x = df.index

    # variables: lon, lat, p, ws
    lon = df.lon.values
    lat = df.lat.values
    p = df.p.values
    ws = df.ws.values

    # make time index for interpolation
    date = df.index
    s = date[0]
    e = date[-1]
    x_in = pd.date_range(s, e, freq='H')

    # Interpolation: p
    flon = interpolate.interp1d(x.to_julian_date(), lon*0.1)
    flat = interpolate.interp1d(x.to_julian_date(), lat*0.1)
    fp = interpolate.interp1d(x.to_julian_date(), p) 
    fws = interpolate.interp1d(x.to_julian_date(), ws)
    y_flon = flon(x_in.to_julian_date())
    y_flat = flat(x_in.to_julian_date())
    y_fp = fp(x_in.to_julian_date())
    y_fws = fws(x_in.to_julian_date())
   
    # make dataframe
    df1 = pd.DataFrame(x_in, columns=['time'])
    df2 = pd.DataFrame(y_flon, columns=['lon'])
    df3 = pd.DataFrame(y_flat, columns=['lat'])
    df4 = pd.DataFrame(y_fp, columns=['p'])
    df5 = pd.DataFrame(y_fws, columns=['ws'])

    # combine dataframes
    df6=pd.concat([df1,df2,df3,df4,df5],axis=1)
    df6['date_time']=pd.to_datetime(df6['time'], format='%y%m%d%H')
    df6=df6.set_index('date_time')

    # save (if you want all csv output, please comment out
    #df6.to_csv( path_or_buf = "output.csv")

    # final output print
    tstr = yy+mo+dy+hr
    target_date_time = datetime.datetime.strptime(tstr,'%Y%m%d%H') 
    df = df6[ df6['time'] == target_date_time ]
    otime = df['time'].dt.strftime("%Y%m%d%H")
    otime.name='out_time'
    out_df=pd.concat([df,otime],axis=1) 
    print(out_df.to_csv(columns=['out_time', 'lon', 'lat','p'], sep=out_sep, index=False, header=False))

def make_out_list(dline_var,var_list, out_list):
    for var in var_list:
       if var == 'time':
         out_list.append(dline_var[0])
       elif var == 'grade':
         out_list.append(dline_var[2])
       elif var == 'lat':
         out_list.append(dline_var[3])
       elif var == 'lon':
         out_list.append(dline_var[4])
       elif var == 'p':
         out_list.append(dline_var[5])
       elif var == 'ws':
         out_list.append(dline_var[6])
    return(out_list)

def clean():
    command='rm ' + tmp_csv
    os.system(command)
 
    
# main
pid = os.getpid()
tmp_csv='./tmp_'+str(pid)+'.csv'
nargv = len(sys.argv)
#print(nargv)

# Get arg
if nargv == 7:
  ityid = sys.argv[1]
  itarget_yy = sys.argv[2]
  itarget_mo = sys.argv[3]
  itarget_dy = sys.argv[4]
  itarget_hr = sys.argv[5]
  sep=sys.argv[6]
elif nargv == 6:
  ityid = sys.argv[1]
  itarget_yy = sys.argv[2]
  itarget_mo = sys.argv[3]
  itarget_dy = sys.argv[4]
  itarget_hr = sys.argv[5]
  sep=' '
else:
  usage()

#Debug
#print(ityid)
#print(itarget_yy,itarget_mo,itarget_dy)

#---------------------------------------
#---------------------------------------
# Input file
f = open('./ORG/bst_all.txt', 'rt')
bst_all_lines = f.readlines()
f.close()
#---------------------------------------
#---------------------------------------

# Command
var_list = ['time','lon','lat','p','ws']
data_vars(bst_all_lines, ityid, var_list, ',')
interpolation(var_list,itarget_yy, itarget_mo, itarget_dy, itarget_hr, sep) 
clean()

