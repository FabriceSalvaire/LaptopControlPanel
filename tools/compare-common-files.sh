#! /bin/bash

project1=$HOME/home/unison-osiris/git-python
project2=$PWD

for i in \
  doc/sphinx/Makefile.sphinx \
  doc/sphinx/make-html \
  tools/check-license.sh \
  tools/clean \
  tools/generate-rst \
  tools/replace \
  tools/RstFactory.py \
  tools/update-tags \
  ; do
  echo Compare File $i
  diff -Naur $project1/$i $project2/$i
done

# End
