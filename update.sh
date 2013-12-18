#! /bin/bash

####################################################################################################

html_build="../laptop-control-panel/doc/sphinx/build/html"

####################################################################################################

rm -rf static images

rsync --delete -av --exclude-from=rsync-filter.txt  ${html_build}/ .

mv _static static
mv _images images
find . -name "*.html" -exec sed -e 's/_images/images/g;' -i {} \;
find . -name "*.html" -exec sed -e 's/_static/static/g;' -i {} \;

####################################################################################################
# 
# End
# 
####################################################################################################
