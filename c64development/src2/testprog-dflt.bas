100 if a=0 then a=1:load "bord2scrn",8,1
110 r$="result ":n$="dflt"
120 s$(0)="fail":s$(1)="pass"
130 open 4,4
140 print#4,n$;" start"
150 :
200 xp=14:ac=peek(53280) and 15 
210 if ac<>xp then 240
210 sys 49152:ac=peek(53281) and 15
220 print#4,r$;n$;".boot ";s$(-(xp=ac))
230 goto 300
240 print#4,"precondition error";xp;ac
250 print#4,r$;n$;".boot ";s$(0)
270 :
300 rem next
310 :
998 print#4,n$;" done"
999 close 4

