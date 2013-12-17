####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

about = """
@ProjectDescription@..
"""

####################################################################################################

system_information_message_pattern = """
<h2>LaptopControlPanel %(software_version)s</h2>
<h2>Host %(node)s</h2>
<h3>Hardware</h3>
<ul>
<li>Machine: %(machine)s</li>
<li>Architecture: %(architecture)s</li>
<li>CPU: %(cpu)s</li>
<li>Number of cores: %(number_of_cores)u</li>
<li>Memory Size: %(memory_size_mb)u MB</li>
</ul>
<h3>OpenGL</h3>
<ul>
<li>Render: %(gl_renderer)s</li>
<li>Version: %(gl_version)s</li>
<li>Vendor: %(gl_vendor)s</li>
</ul>
<h3>Software Versions</h3>
<ul>
<li>OS: %(os)s %(distribution)s</li>
<li>Python %(python_version)s</li>
<li>Qt %(qt_version)s</li>
<li>PyQt %(pyqt_version)s</li>
</ul>
"""

####################################################################################################
# 
# End
# 
####################################################################################################
