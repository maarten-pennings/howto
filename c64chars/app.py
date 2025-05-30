from PIL import Image,ImageDraw,ImageFont

def main(file,sets) :
    # get source
    src_img= Image.open(file+'.pbm')
    num_cx= 16*sets     # num characters in x direction in source and destination image
    num_cy= 16          # num characters in y direction in source and destination image 
    num_pix= 8          # num pixels in x and y in a character (on the C64)
    src_dot= 3          # pixels in a dot (same in x and y) in source image 
    src_char= src_dot*8 # pixels in a char (same in x and y) in source image 
    # check source
    if src_img.size[0] != num_cx*src_char : print("error x")
    if src_img.size[1] != num_cy*src_char : print("error y")
    # setup dest
    dst_dot=6           # pixels in a dot (same in x and y) in destination image 
    dst_dotsep=1        # pixels between src_dots in destination image
    dst_charsepx=32     # pixels between chars in destination image
    dst_charsepy=3      # pixels between chars in destination image
    dst_marginx=32      # margin on left and top for labels
    dst_marginy=96      # margin on left and top for labels
    dst_offsetx=16      # offset of the labels in x
    dst_offsety=5       # offset of the labels in y
    dst_font_ascii=20   # font size for ascii
    dst_font_labels=32  # font size for labels
    dst_charx= dst_dot*num_pix+dst_dotsep*(num_pix-1)+dst_charsepx
    dst_chary= dst_dot*num_pix+dst_dotsep*(num_pix-1)+dst_charsepy
    dst_dim= (dst_marginx + dst_charsepx + num_cx*dst_charx , dst_charsepy + num_cy*dst_chary + dst_marginy)
    dst_colbg= (150,140,255)
    dst_colfg= (0,0,0)
    dst_col0 = (62,50,162)
    dst_col1 = (124,113,218)
    dst_img = Image.new('RGB', dst_dim, dst_colbg )
    dst_draw = ImageDraw.Draw(dst_img)  
    dst_labels = ImageFont.truetype("consolab", dst_font_labels)
    dst_ascii = ImageFont.truetype("consolab", dst_font_ascii)
    # draw pixels
    for cx in range(num_cx) :
      for cy in range(num_cy) :
        dst_cx = dst_marginx + dst_charsepx + cx*dst_charx
        dst_cy = dst_marginy + dst_charsepy + cy*dst_chary
        for dx in range(num_pix):
          for dy in range(num_pix):
            # get value `dot` of pixel dx,dy in char cx,cy
            src_dx= cx*src_char + dx*src_dot 
            src_dy= cy*src_char + dy*src_dot
            dot= src_img.getpixel( (src_dx,src_dy) )
            # create a dot in destination
            dst_dx= dst_cx+dx*dst_dot + dx*dst_dotsep
            dst_dy= dst_cy+dy*dst_dot + dy*dst_dotsep
            shape = [(dst_dx,dst_dy),(dst_dx+dst_dot-1,dst_dy+dst_dot-1)]
            if dot>128 :
              dst_draw.rectangle(shape,fill=dst_col0)
            else :
              dst_draw.rectangle(shape,fill=dst_col1)
    # set header
    dst_cx = dst_marginx + dst_charsepx + 0*dst_charx
    dst_cy = dst_offsety + 0*dst_font_labels
    dst_draw.text( (dst_cx,dst_cy), "Commodore 64 poke codes [light-blue=on] [ASCII in small]", dst_colfg, font=dst_labels)
    dst_cx = dst_marginx + dst_charsepx + 0*dst_charx
    dst_cy = dst_offsety + 1*dst_font_labels
    dst_draw.text( (dst_cx,dst_cy), "upper case set", dst_colfg, font=dst_labels)
    dst_cx = dst_marginx + dst_charsepx + 16*dst_charx
    dst_cy = dst_offsety + 1*dst_font_labels
    dst_draw.text( (dst_cx,dst_cy), "lower case set", dst_colfg, font=dst_labels)
    # draw row of labels
    for cx in range(num_cx) :
      dst_cx = dst_marginx + dst_charsepx + cx*dst_charx
      dst_cy = dst_offsety + 2*dst_font_labels
      dst_draw.text( (dst_cx,dst_cy), f"{cx%16:X}–", dst_colfg, font=dst_labels)
    # draw col of labels
    for cy in range(num_cy) :
      dst_cx = dst_offsetx
      dst_cy = 0 + dst_marginy + dst_charsepy + cy*dst_chary + dst_chary/2 - dst_font_labels/2
      dst_draw.text( (dst_cx,dst_cy), f"–{cy%0x100:X}", dst_colfg, font=dst_labels)
    for ascii in range(256) :
      if     0 <= ascii <= 31: continue
      elif  32 <= ascii <= 63: poke= ascii
      elif  64 <= ascii <= 95: poke= ascii-64
      elif  96 <= ascii <=127: poke= ascii-32
      elif 128 <= ascii <=159: continue
      elif 160 <= ascii <=191: poke= ascii-64
      elif 192 <= ascii <=254: continue # poke= ascii-128
      elif 255 <= ascii <=255: continue # poke= ascii-161
      cx = poke // 16
      cy = poke % 16
      dst_cx = dst_marginx + dst_charsepx + cx*dst_charx + dst_dot*num_pix+dst_dotsep*(num_pix-1) + 2
      dst_cy = dst_marginy + dst_charsepy + cy*dst_chary + dst_dot*num_pix+dst_dotsep*(num_pix-1) - dst_font_ascii
      dst_draw.text( (dst_cx,dst_cy), f"{ascii:02X}", dst_colfg, font=dst_ascii)
        
    dst_img.show()
    dst_img.save(file+'.png')

if __name__ == "__main__":
  main("c64fontrom1",1)
  main("c64fontrom2",2)
