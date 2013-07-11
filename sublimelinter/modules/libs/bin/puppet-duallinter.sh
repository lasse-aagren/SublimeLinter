#!/bin/sh
PUPPET=`which puppet`
PUPPETLINT=`which puppet-lint`

if [ $1 = '-v' ]; then
	exit 0
fi

if [ $PUPPET ]; then
	$PUPPET parser validate --color=false "$1"
	PUPPETEXIT=$?
fi

if [ $PUPPETLINT ]; then
	$PUPPETLINT --no-autoloader_layout-check "$1"
	PUPPETLINTEXIT=$?
fi

if [ $PUPPETEXIT -ne 0 ]; then
	exit $PUPPETEXIT
fi

if [ $PUPPETLINTEXIT -ne 0 ]; then
	exit $PUPPETLINTEXIT
fi

exit 0