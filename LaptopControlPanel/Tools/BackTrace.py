####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

####################################################################################################

def html_highlight_backtrace(backtrace_text):

    lines = [x for x in backtrace_text.split('\n') if x]

    backtrace_highlighted = '<h3>' + lines[0] + '</h3>'

    for line in lines[1:-1]:
        line = line.replace('<', '(')
        line = line.replace('>', ')')
        if 'File' in line:
            line = '<font color="blue"><h6>' + line + '</h6>'
        else:
            line = '<font color="black"><code>' + line + '</code>'
        backtrace_highlighted += line

    backtrace_highlighted += '<font color="blue"><h4>' + lines[-1] + '</h4>'

    return backtrace_highlighted

####################################################################################################
#
# End
#
####################################################################################################
