10 if a=1 then 60:rem restart
20 print "load 'border-sub' at c000"
30 a=1: load "border-sub",8,1
40 rem load will do run
50 :
60 print "call sub at c000"
70 sys 49152
80 print "back in basic."
90 end
