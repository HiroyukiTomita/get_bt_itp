# get_bt_itp  

A command line tool to get hourly interpolated value from RSMC Best track data  
 
## DATA  
RSMC Tokyo Typhoon center :  
http://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/besttrack.html  
To get data file  
`wget http://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip`  
`unzip bst_all.zip`  
 
## USAGE:  
`get_bt_itp TCID YYYY MM DD HH [sep]`  
    argv1:  Target typhoon  
          -TCID: tropical cyclon number ID (TCID)")  
    argv2-5: Target date and time  
          -YYYY: year  
          -MM  : month  
          -DD  : day  
          -HH  : hour  
    argv6  : Separator for output (option)  
          -' ': space (default)")  
          -',': comma  
  
## OUTPUT: hourly interpolated data  
`YYYYMMDDHH  lon  lat  p`   
