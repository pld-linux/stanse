#!/bin/sh -e

# Set paths

CLASSPATH=$(build-classpath-directory /usr/share/stanse/lib)
CLASSPATH=$CLASSPATH:$(find-jar stanse)
export CLASSPATH

PATH=$PATH:/usr/share/stanse/data/bin
export PATH

# Initialize STANSE_HOME

STANSE_HOME=${STANSE_HOME:-"$HOME/.stanse"}
export STANSE_HOME
mkdir -p $STANSE_HOME
[ -e "$STANSE_HOME/bin" ] || ln -s /usr/share/stanse/bin $STANSE_HOME/bin
[ -e "$STANSE_HOME/data" ] || cp -a /usr/share/stanse/data $STANSE_HOME/data
[ -e "$STANSE_HOME/properties.xml" ] || cp -a /usr/share/stanse/properties.xml $STANSE_HOME/properties.xml

java cz.muni.stanse.Stanse $@
