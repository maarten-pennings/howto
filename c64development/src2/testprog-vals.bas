100 if a=0 then a=1:load "bord2scrn",8,1
110 r$="result ":n$="vals"
120 s$(0)="fail":s$(1)="pass"
130 open 4,4
140 print#4,n$;" start"
150 :
200 xp=1
210 poke 53280,xp:sys 49152:ac=peek(53281) and 15
220 print#4,r$;n$;".std ";s$(-(xp=ac))
230 :
300 xp=0
310 poke 53280,xp:sys 49152:ac=peek(53281) and 15
320 print#4,r$;n$;".min ";s$(-(xp=ac))
330 :
400 xp=15
410 poke 53280,xp:sys 49152:ac=peek(53281) and 15
420 print#4,r$;n$;".max ";s$(-(xp=ac))
430 :
998 print#4,n$;" done"
999 close 4
