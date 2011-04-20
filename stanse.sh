#!/bin/sh -e

[ -r /usr/share/java-utils/java-functions ]
. /usr/share/java-utils/java-functions

# Set paths
CLASSPATH=$(build-classpath-directory /usr/share/stanse/lib)
CLASSPATH=$CLASSPATH:$(find-jar stanse)

export PATH=$PATH:/usr/share/stanse/data/bin

# Initialize STANSE_HOME
export STANSE_HOME=${STANSE_HOME:-"$HOME/.stanse"}
mkdir -p $STANSE_HOME
[ -e "$STANSE_HOME/bin" ] || ln -s /usr/share/stanse/bin $STANSE_HOME/bin
[ -e "$STANSE_HOME/data" ] || cp -a /usr/share/stanse/data $STANSE_HOME/data
[ -e "$STANSE_HOME/properties.xml" ] || cp -a /usr/share/stanse/properties.xml $STANSE_HOME/properties.xml

MAIN_CLASS=cz.muni.stanse.Stanse

exec run ${1:+"$@"}
