#!/bin/sh

CLASSPATH=$(build-classpath-directory /usr/share/java/stanse):$(find-jar stanse)
export CLASSPATH
STANSE_HOME=${STANSE_HOME:-"$HOME/.stanse"}
export STANSE_HOME
mkdir -p $STANSE_HOME

java cz.muni.stanse.Stanse $@
