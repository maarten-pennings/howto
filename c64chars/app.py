from PIL import Image,ImageDraw,ImageFont
import functools

# image format (source and destination)
num_cx= 16          # num characters in x direction
num_cy= 16          # num characters in y direction
num_pix= 8          # num pixels in x and y in a character (on the C64)

# destination image
dst_dot=6           # pixels in a dot (same in x and y) in destination image 
dst_dotsep=1        # pixels between dots in destination image
dst_charsepx=32     # pixels between chars in destination image in x-direction
dst_charsepy=3      # pixels between chars in destination image in y-direction
dst_marginx=32      # margin for labels at left hand side (for row number)
dst_marginy0=96     # margin for labels at the top (for headings and column number)
dst_marginy1=32     # margin for labels at the bottom (for foornote)
dst_offsetx=16      # offset of the labels in x
dst_offsety=5       # offset of the labels in y
dst_font_ascii=20   # font size for ascii
dst_font_labels=32  # font size for labels
            
dst_charbx= dst_dot*num_pix+dst_dotsep*(num_pix-1) # bare character size x
dst_charby= dst_dot*num_pix+dst_dotsep*(num_pix-1) # bare character size y
dst_charx= dst_charbx + dst_charsepx               # character pitch x 
dst_chary= dst_charby + dst_charsepy               # character pitch y
dst_colbg= (150,140,255)
dst_colfg= (0,0,0)
dst_col0 = (62,50,162)
dst_col1 = (124,113,218)
dst_labels = ImageFont.truetype("consolab", dst_font_labels)
dst_ascii = ImageFont.truetype("consolab", dst_font_ascii)

# Note
#   ^ control
#   # shift
#   € commodore

# 0x00                  ^@                
# 0x01                  ^A                          
# 0x02                  ^B                          
# 0x03 stop             ^C, RUN/STOP
# 0x04                  ^D                          
# 0x05 white            ^E, ^2
# 0x06                  ^F                          
# 0x07                  ^G                          
# 0x08 disable €#       ^H                          
# 0x09 enable €#        ^I                          
# 0x0A                  ^J                          
# 0x0B                  ^K                          
# 0x0C                  ^L                          
# 0x0D return           ^M, RETURN
# 0x0E charset-lo       ^N                          
# 0x0F                  ^O                          
# 0x10                  ^P                          
# 0x11 cursor down      ^Q, CRSR^v
# 0x12 reverse on       ^R, ^9                  
# 0x13 home             ^S, CLR/HOME  
# 0x14 delete           ^T, INST/DEL
# 0x15                  ^U                          
# 0x16                  ^V                          
# 0x17                  ^W                          
# 0x18                  ^X                          
# 0x19                  ^Y                          
# 0x1A                  ^Z                          
# 0x1B                  ^:
# 0x1C red              ^£, ^3 
# 0x1D cursor right     ^;, CRSR<>
# 0x1E green            ^↑, ^6
# 0x1F blue             ^=, ^7
# 
# 0x80                  
# 0x81 orange           €1
# 0x82                  
# 0x83 run              #RUN/STOP
# 0x84                  
# 0x85 F1               f1/f2
# 0x86 F3               f3/f4
# 0x87 F5               f5/f6
# 0x88 F7               f7/f8
# 0x89 F2               #f1/f2
# 0x8A F4               #f3/f4
# 0x8B F6               #f5/f6
# 0x8C F8               #f7/f8
# 0x8D #return          #RETURN
# 0x8E charset-hi
# 0x8F                  
# 0x90 black            ^1
# 0x91 cursor up        #CRSR^v
# 0x92 reverse off      ^0
# 0x93 clear            #CLR/HOME
# 0x94 insert           #INST/DEL
# 0x95 brown            €2
# 0x96 pink             €3
# 0x97 dark grey        €4
# 0x98 grey             €5
# 0x99 light green      €6
# 0x9A light blue       €7
# 0x9B light grey       €8
# 0x9C purple           ^5
# 0x9D cursor left      #CRSR<>
# 0x9E yellow           ^8
# 0x9F cyan             ^4


class Charset:
  def __init__(self,filename,charsetname) :
    self.img= Image.open(filename)
    self.name= charsetname
    if self.img.size[0] != num_cx*num_pix : raise Exception("unexpected width")
    if self.img.size[1] != num_cy*num_pix : raise Exception("unexpected height")
  def name(self) :
    return self.charsetname
  def getpixel(self,pokecode,px,py) :
    cx = pokecode // num_cx
    cy = pokecode % num_cx
    dot= self.img.getpixel( (cx*num_pix + px, cy*num_pix + py) )
    return dot<128
  def char_str(self,pokecode) :
    result = ""
    for py in range(num_pix):
      for px in range(num_pix):
        result += "#" if self.getpixel(pokecode,px,py) else "-"
      result += "\n"
    return result
  @functools.cache # compute the nums only once
  def char_num(self,pokecode) :
    result = 0;
    for py in range(num_pix):
      for px in range(num_pix):
        result = 2*result + int(self.getpixel(pokecode,px,py))
    return result
  def duplicates(self) :
    result = []
    for p1 in range(256) :
      for p2 in range(p1) :
        n1= self.char_num(p1)
        n2= self.char_num(p2)
        if n1==n2 : result.append((p2,p1))
    return result
  def wrongrvs(self) :
    result = []
    for p in range(128) :
        n1= self.char_num(p)
        n2= self.char_num(p+128)
        n3= 2**64-1 - n2
        if n1!=n3 : result.append(p)
    return result


def demo() :
  charset = Charset("c64fontromhi.pbm","charset uppercase")
  print( charset.name )
  pokecode=0x06
  print(charset.char_str(pokecode))
  num=charset.char_num(pokecode)
  print(num)
  num64= ("0"*64 + bin(num)[2:])[-64:]
  print("0b"+num64)
  for i in range(num_pix) : print( num64[i*8:(i+1)*8] )
  # print( charset.duplicates() )
  print("duplicates ",end="");
  for p1,p2 in charset.duplicates() :
    print( f"({p1:02X},{p2:02X})", end="" )
  print()
  #print( charset.wrongrvs() )
  print("wrongrvs ",end="");
  for p in charset.wrongrvs() :
    print( f"{p:02X}", end=" " )
  print()

def circle(draw,pokecode,color,label) :
  width= dst_charsepy # bice default
  cx = pokecode // num_cx
  cy = pokecode % num_cx
  dst_px = dst_marginx + dst_charsepx + cx*dst_charx 
  dst_py = dst_marginy0 + dst_charsepy + cy*dst_chary
  shape = [(dst_px-width,dst_py-width),(dst_px+dst_charbx+width-1,dst_py+dst_charby+width-1)]
  draw.rectangle(shape,outline=color,width=width)
  draw.text( (dst_px + dst_charbx + 3,dst_py + dst_charby - dst_font_ascii*3 + 3), label, color, font=dst_ascii)


def table(charset) :
    # setup dest
    dst_dim= (dst_marginx + dst_charsepx + num_cx*dst_charx , dst_marginy0 + dst_charsepy + num_cy*dst_chary + dst_marginy1)
    dst_img = Image.new('RGB', dst_dim, dst_colbg )
    dst_draw = ImageDraw.Draw(dst_img)  
    # draw pixels
    for cx in range(num_cx) :
      for cy in range(num_cy) :
        dst_cx = dst_marginx + dst_charsepx + cx*dst_charx
        dst_cy = dst_marginy0 + dst_charsepy + cy*dst_chary
        for dx in range(num_pix):
          for dy in range(num_pix):
            # create a dot in destination
            dst_dx= dst_cx+dx*dst_dot + dx*dst_dotsep
            dst_dy= dst_cy+dy*dst_dot + dy*dst_dotsep
            shape = [(dst_dx,dst_dy),(dst_dx+dst_dot-1,dst_dy+dst_dot-1)]
            if charset.getpixel( cx*16+cy,dx,dy ) :
              dst_draw.rectangle(shape,fill=dst_col0)
            else :
              dst_draw.rectangle(shape,fill=dst_col1)
    # chrset name
    dst_cx = dst_marginx + dst_charsepx + 0*dst_charx
    dst_cy = dst_offsety + 1*dst_font_labels
    dst_draw.text( (dst_cx,dst_cy), charset.name, dst_colfg, font=dst_labels)
    # draw row of labels
    for cx in range(num_cx) :
      dst_cx = dst_marginx + dst_charsepx + cx*dst_charx
      dst_cy = dst_offsety + 2*dst_font_labels
      dst_draw.text( (dst_cx,dst_cy), f"{cx%16:X}–", dst_colfg, font=dst_labels)
    # draw col of labels
    for cy in range(num_cy) :
      dst_cx = dst_offsetx
      dst_cy = 0 + dst_marginy0 + dst_charsepy + cy*dst_chary + dst_chary/2 - dst_font_labels/2
      dst_draw.text( (dst_cx,dst_cy), f"–{cy%0x100:X}", dst_colfg, font=dst_labels)
    for ascii in range(256) :
      shift=1
      if     0 <= ascii <= 31: pokecode= ascii+128
      elif  32 <= ascii <= 63: pokecode= ascii
      elif  64 <= ascii <= 95: pokecode= ascii-64
      elif  96 <= ascii <=127: pokecode= ascii-32
      elif 128 <= ascii <=159: continue # pokecode= ascii; shift=2
      elif 160 <= ascii <=191: pokecode= ascii-64
      elif 192 <= ascii <=254: pokecode= ascii-128; shift=2
      elif 255 <= ascii <=255: pokecode= ascii-161; shift=3
      cx = pokecode // num_cx
      cy = pokecode % num_cx
      dst_px = dst_marginx + dst_charsepx + cx*dst_charx + dst_charbx + 3
      dst_py = dst_marginy0 + dst_charsepy + cy*dst_chary + dst_charby - dst_font_ascii*shift + 3
      dst_draw.text( (dst_px,dst_py), f"{ascii:02X}", dst_colfg, font=dst_ascii)
    return dst_img

        
def patchdot(draw,pokecode,col,dx,dy) :
  cx = pokecode // num_cx
  cy = pokecode % num_cx
  # upper left pixel of char cx,cy
  dst_cx = dst_marginx + dst_charsepx + cx*dst_charx
  dst_cy = dst_marginy0 + dst_charsepy + cy*dst_chary
  # upper left pixel of char cx,cy its dot dx,dy
  dst_dx= dst_cx+dx*dst_dot + dx*dst_dotsep
  dst_dy= dst_cy+dy*dst_dot + dy*dst_dotsep
  # form shape
  d=1
  shape = [(dst_dx+d,dst_dy+d),(dst_dx+dst_dot-1-d,dst_dy+dst_dot-1-d)]
  draw.rectangle(shape,fill=col)


def patchdots(draw,pokecode,col,dots) :
  for dx,dy in dots : patchdot(draw,pokecode,col,dx,dy)
      

def main(charset,basename) :
  img= table(charset)
  
  plain=img.copy()
  draw = ImageDraw.Draw(plain)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "Dark blue means pixel active. Small black numbers are the associated ASCII code in hex.", dst_colfg, font=dst_ascii)
  plain.save(basename+'-1plain.png')

  dups=img.copy()
  draw= ImageDraw.Draw(dups)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - duplicates", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "Char 60 is likely non-breaking space (20). All other are due to C64 \"doubling\" of pixels (wrt VIC-20), here dotted.", dst_colfg, font=dst_ascii)
  dupslist=[ (0x40,0x43),(0x42,0x5D),(0x20,0x60),(0x67,0x6A),(0x65,0x74),(0xC0,0xC3),(0xC2,0xDD),(0xA0,0xE0),(0xE7,0xEA),(0xE5,0xF4) ] 
  if dupslist!=charset.duplicates() : raise Exception("duplicates mismatch")
  for dup in dupslist :
    circle(draw,dup[0],"red",f"{dup[1]:02X}")
    circle(draw,dup[1],"red",f"{dup[0]:02X}")
  patchdots(draw,0x40,dst_col1, [(x,3) for x in range(num_pix)] ); patchdots(draw,0x43,dst_col1, [(x,4) for x in range(num_pix)] )
  patchdots(draw,0x42,dst_col1, [(4,y) for y in range(num_pix)] ); patchdots(draw,0x5D,dst_col1, [(3,y) for y in range(num_pix)] )
  # (0x20,0x60) also in VIC-20
  patchdots(draw,0x67,dst_col1, [(6,y) for y in range(num_pix)] );  # 0x6A
  patchdots(draw,0x65,dst_col1, [(1,y) for y in range(num_pix)] );  # 0x74
  patchdots(draw,0xC0,dst_col0, [(x,3) for x in range(num_pix)] ); patchdots(draw,0xC3,dst_col0, [(x,4) for x in range(num_pix)] )
  patchdots(draw,0xC2,dst_col0, [(4,y) for y in range(num_pix)] ); patchdots(draw,0xDD,dst_col0, [(3,y) for y in range(num_pix)] )
  # (0xA0,0xE0) also in VIC-20
  patchdots(draw,0xE7,dst_col0, [(6,y) for y in range(num_pix)] );  # 0xEA
  patchdots(draw,0xE5,dst_col0, [(1,y) for y in range(num_pix)] );  # 0xF4
  dups.save(basename+'-2dups.png')

  wrongrvs=img.copy()
  draw= ImageDraw.Draw(wrongrvs)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - mismatching reverse", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "Char 00 is the only one where the RVS ON is not a true pixel flip (see dotted pixel).", dst_colfg, font=dst_ascii)
  wrongrvslist=[ 0 ] 
  if wrongrvslist!=charset.wrongrvs() : raise Exception("wrongrvs mismatch")
  for wrong in charset.wrongrvs() :
    circle(draw,wrong,"red",f"{wrong+128:02X}")
    circle(draw,wrong+128,"red",f"{wrong:02X}")
  patchdots(draw,0x80,dst_col0, [(5,5)] ); 
  wrongrvs.save(basename+'-3wrongrvs.png')
  
  blocks=img.copy()
  draw= ImageDraw.Draw(blocks)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - block graphics", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "A set of characters for low resolution (80×50) monochrome graphics.", dst_colfg, font=dst_ascii)
  for ix,block in enumerate([32,126,124,226,123,97,255,236,108,127,225,251,98,252,254,160]) :
    circle(draw,block,"red",f"#{ix}")
  blocks.save(basename+'-4blocks.png')
  
  verfill=img.copy()
  draw= ImageDraw.Draw(verfill)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - vertical fill", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "Bars to make vertical pixel-accurate gauge.", dst_colfg, font=dst_ascii)
  for ix,block in enumerate([0x20,0x64,0x6F,0x79,0x62,0xF8,0xF7,0xE3,0xA0]) :
    circle(draw,block,"red",f"#{ix}")
  verfill.save(basename+'-5verfill.png')

  horfill=img.copy()
  draw= ImageDraw.Draw(horfill)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - horizontal fill", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "Bars to make horizontal gauge (with the C64 double pixels causing some jumps, see dotted pixels).", dst_colfg, font=dst_ascii)
  for ix,block in enumerate([0x20,0x65,0x74,0x75,0x61,0xF6,0xEA,0x67,0xA0]) :
    circle(draw,block,"red",f"#{ix}")
  patchdots(draw,0x67,dst_col1, [(6,y) for y in range(num_pix)] );
  patchdots(draw,0x65,dst_col1, [(1,y) for y in range(num_pix)] );
  horfill.save(basename+'-6horfill.png')

  verwave=img.copy()
  draw= ImageDraw.Draw(verwave)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - vertical wave", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "Bars to make vertical wave (with the C64 double pixels missing a start and end, see dotted pixels).", dst_colfg, font=dst_ascii)
  for ix,block in enumerate([0x65,0x74,0x54,0x47,0x42,0x48,0x59,0x6A,0x67]) :
    circle(draw,block,"red",f"#{ix}")
  patchdots(draw,0x67,dst_col1, [(6,y) for y in range(num_pix)] );
  patchdots(draw,0x65,dst_col1, [(1,y) for y in range(num_pix)] );
  verwave.save(basename+'-7verwave.png')
  
  horwave=img.copy()
  draw= ImageDraw.Draw(horwave)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - horizontal wave", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "Characters for a pixel accurate wave.", dst_colfg, font=dst_ascii)
  for ix,block in enumerate([0x64,0x6F,0x52,0x46,0x43,0x44,0x45,0x77,0x63]) : 
    circle(draw,block,"red",f"#{ix}")
  horwave.save(basename+'-8horwave.png')

  midframe=img.copy()
  draw= ImageDraw.Draw(midframe)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - mid cell frames", dst_colfg, font=dst_labels)
  draw.text( (dst_marginx+dst_charsepx,dst_marginy0+dst_charsepy+num_cy*dst_chary+dst_offsety), "In red two types of corners, in orange the interconnect.", dst_colfg, font=dst_ascii)
  for ix,block in enumerate([0x70,0x6E,0x6D,0x7D,0x55,0x49,0x4A,0x4B]) :
    circle(draw,block,"red",f"")
  for ix,block in enumerate([0x71,0x72,0x73,0x6B,0x5B,0x40,0x42]) :
    circle(draw,block,"orange",f"")
  midframe.save(basename+'-9midframe.png')

  outerframe=img.copy()
  draw= ImageDraw.Draw(outerframe)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - outer frames", dst_colfg, font=dst_labels)
  for ix,block in enumerate([0x4F,0x50,0x4C,0x7A,0x77,0x6F,0x65,0x67]) :
    circle(draw,block,"red",f"")
  outerframe.save(basename+'-10outerframe.png')

  symbols=img.copy()
  draw= ImageDraw.Draw(symbols)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - various symbols", dst_colfg, font=dst_labels)
  for ix,block in enumerate([0x41,0x53,0x58,0x5A, 0x51,0x57,0x5E,0x1E,0x1F,0x56,0x5B]) :
    circle(draw,block,"red",f"")
  symbols.save(basename+'-11symbols.png')

  diagonal=img.copy()
  draw= ImageDraw.Draw(diagonal)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - diagonal characters", dst_colfg, font=dst_labels)
  for ix,block in enumerate([0x4D,0x4E,0x56,0x5F,0x69]) :
    circle(draw,block,"red",f"")
  diagonal.save(basename+'-12diagonal.png')

  dither=img.copy()
  draw= ImageDraw.Draw(dither)  
  draw.text( (dst_marginx+dst_charsepx,dst_offsety), "Commodore 64 pokecodes - dithering", dst_colfg, font=dst_labels)
  for ix,block in enumerate([0x5C,0x66,0x68]) :
    circle(draw,block,"red",f"")
  dither.save(basename+'-13dither.png')

if __name__ == "__main__":
  #demo()
  charset = Charset("c64fontromhi.pbm","charset uppercase")
  main(charset, "c64fontromhi")
