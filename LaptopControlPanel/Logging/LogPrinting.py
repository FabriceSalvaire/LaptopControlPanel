####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

####################################################################################################

import textwrap

####################################################################################################

def remove_enclosing_new_line(text):
    return text[1:-1]

####################################################################################################

class Filet(object):

    ##############################################

    def __init__(self,
                 horizontal, vertical,
                 top_left, top_right, bottom_left, bottom_right):

        self.horizontal, self.vertical = horizontal, vertical
        self.top_left, self.top_right = top_left, top_right
        self.bottom_left, self.bottom_right = bottom_left, bottom_right
        
####################################################################################################

empty_filet = Filet('', '', '', '', '', '')

solid_thin_filet = Filet(unichr(9472), unichr(9474),
                         unichr(9484), unichr(9488),
                         unichr(9492), unichr(9496))

solid_wide_filet = Filet(unichr(9473), unichr(9475),
                         unichr(9487), unichr(9491),
                         unichr(9495), unichr(9499))

dash_thin_filet = Filet(unichr(9476), unichr(9478),
                        unichr(9484), unichr(9488),
                        unichr(9492), unichr(9496))

dash_wide_filet = Filet(unichr(9477), unichr(9479),
                        unichr(9487), unichr(9491),
                        unichr(9495), unichr(9499))

solid_thin_doublefilet = Filet(unichr(9552), unichr(9553),
                               unichr(9556), unichr(9559),
                               unichr(9562), unichr(9565))

####################################################################################################

def format_frame(text,
                 filet=solid_thin_filet,
                 centered=False,
                 margin=False,
                 console_width=100):

    console_width_margin = 2
    lines = []
    for line in text.splitlines():
        sub_lines = textwrap.wrap(line, width=(console_width-console_width_margin))
        lines += [sub_lines[0]] + [' '*console_width_margin + sub_line for sub_line in sub_lines[1:]]
    width = max([len(line) for line in lines])
    if margin:
        width += 2
    rule = filet.horizontal*width
    empty_line = filet.vertical + ' '*width + filet.vertical + '\n'
    
    output_text = filet.top_left + rule + filet.top_right + '\n'
    if margin:
        output_text += empty_line
    for line in lines:
        if margin:
            line = ' ' + line + ' '
        if centered:
            line = line.center(width)
        else:
            line = line + ' '*(width - len(line))
        output_text += filet.vertical + line + filet.vertical + '\n'
    if margin:
        output_text += empty_line
    output_text += filet.bottom_left + rule + filet.bottom_right + '\n'
    
    return output_text

####################################################################################################

def format_message_header(text,
                          width=80,
                          centered=False,
                          margin=False,
                          filet=solid_wide_filet,
                          border=False,
                          bottom_rule=True,
                          newline=False):

    if not border:
        filet = empty_filet
    
    rule = filet.horizontal*width
    empty_line = filet.vertical + ' '*width + filet.vertical + '\n'

    output_text = ''
    if newline:
        output_text += '\n'
    output_text += filet.top_left + rule + filet.top_right + '\n'
    if margin:
        output_text += empty_line
        width_text = width - 2
    else:
        width_text = width
    for line in text.splitlines():
        if margin:
            line = ' ' + line + ' '
        if centered:
            line = line.center(width)
        else:
            line = line + ' '*(width - len(line))
        output_text += filet.vertical + line
        if bottom_rule:
            output_text += filet.vertical
        output_text += '\n'
    if margin:
        output_text += empty_line
    if bottom_rule:
        output_text += filet.bottom_left + rule + filet.bottom_right + '\n'

    return output_text

####################################################################################################
#
# End
#
####################################################################################################
