#!/bin/sh

CLASSPATH=$(build-classpath-directory /usr/share/java/stanse):$(find-jar stanse)
echo $CLASSPATH
export CLASSPATH
export STANSE_HOME=$HOME/.stanse
java cz.muni.stanse.Stanse -gui
