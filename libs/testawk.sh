:
# testawk - test awk features (stv, 5/98)
# $Id: testawk.sh,v 1.5 2003/01/30 03:02:29 heiner Exp $
#
# usage: testawk [awk_path ...]
#
# Thanks to
#     Raffaele Guide Della Valle <valle@aronte.fci.unibo.it>
#     Ian P. Springer <ips@fpk.hp.com>
# for feature tests and bug reports

email="heiner.steven@shelldorado.com"
PN=`basename "$0"`			# Program name
LOGFILE=/tmp/testawk.log			# Default log file

if [ $# -gt 0 ]
then
    AWKList="$@"
else
    AWKList=" "
    for path in `echo "$PATH" | sed 's|^:|./ |;s|:$| ./|;s|:| |g'`
    do
	for awk in "$path"/*awk*
	do
	    case "$awk" in
		*.exe|*.com|*.bat)	;;	# DOS/Windows
		*.*)	continue	;;	# ignore "script.awk"
	    esac
	    [ X"$awk" = X"$path/*awk*" ] && continue	# no awk found
	    [ X"`basename \"$awk\"`" = X"$PN" ] && continue
	    if [ -x "$awk" ]
	    then
	    	case "$AWKList" in
		    *" $awk "*) ;;		# awk already in list
		    *) AWKList="${AWKList}$awk " ;;
		esac
	    fi
	done
    done
    [ -z "$AWKList" ] &&
    	exec echo "no AWK found - please specify a path on the command line"
fi

Script="${TMPDIR:=/tmp}/scr$$.awk"		# Temporary AWK script
Input="$TMPDIR/in$$"				# AWK input (a newline)
Output="$TMPDIR/out$$"				# Resulting output
Result="$TMPDIR/res$$"

# Automatically remove temporary files at program termination
trap 'rm -f "$Script" "$Input" "$Output" "$Result" >/dev/null 2>&1' 0
trap "exit 2" 1 2 3 13 15

uname -a > "$Result"

for AWK in $AWKList
do
    Status="$AWK	-v option"

    #
    # check for "-v" command line argument
    #

    echo > "$Input"
    cat <<-! > "$Script"
	{
	    print variable
	}
	!

    echo >&2 "-v option"
    if TZ= "$AWK" -v variable=A -f "$Script" "$Input" > "$Output" 2>/dev/null
    then
        if [ -s "$Output" ] && [ X`cat "$Output"` = X"A" ]
	then
	    Status="$Status	+"
	    echo >&2 "	$AWK +"
	else
	    Status="$Status	-"
	    echo >&2 "	$AWK -"
	fi
    else
	Status="$Status	-"
    	echo >&2 "	$AWK -"
    fi

    echo "$Status" >> "$Result"

    #
    # Check if variable=value pairs work on the command line
    #

    Status="$AWK	var=val pairs"
    echo >&2 "variable=value arguments"

    if TZ= "$AWK" -f "$Script" variable=A "$Input" > "$Output" 2>/dev/null
    then
        if [ -s "$Output" ] && [ X`cat "$Output"` = X"A" ]
	then
	    Status="$Status	+"
	    echo >&2 "	$AWK +"
	else
	    Status="$Status	-"
	    echo >&2 "	$AWK -"
	fi
    else
	Status="$Status	-"
    	echo >&2 "	$AWK -"
    fi
    echo "$Status" >> "$Result"

    #
    # User defined functions
    #

    Status="$AWK	functions"
    echo >&2 "functions"

    echo 1 > "$Input"
    cat <<-! > "$Script"
    	function mydouble(x) { return 2*x }
	{
	    print mydouble(\$0)
	}
	!


    if TZ= "$AWK" -f "$Script" "$Input" > "$Output" 2>/dev/null
    then
        if [ -s "$Output" ] && [ X`cat "$Output"` = X"2" ]
	then
	    Status="$Status	+"
	    echo >&2 "	$AWK +"
	else
	    Status="$Status	-"
	    echo >&2 "	$AWK -"
	fi
    else
	Status="$Status	-"
    	echo >&2 "	$AWK -"
    fi
    echo "$Status" >> "$Result"

    #
    # exit() function
    #

    Status="$AWK	exit()"
    echo >&2 "exit()"
    "$AWK" '{ exit(99) }' "$Input" 2>/dev/null
    if [ $? -eq 99 ]
    then
    	Status="$Status	+"
	echo >&2 "	$AWK +"
    else
    	Status="$Status	-"
	echo >&2 "	$AWK -"
    fi
    echo "$Status" >> "$Result"
done

# Test the listed features.
# Format:
#	string_to_print<TAB>awk_command<TAB>expected_output

for func in 								\
	'ARGIND	if ( !ARGIND ) exit (1)'				\
	'ERRNO	getline s < "/"; if ( !ERRNO ) exit (1)'		\
	'ENVIRON	if ( !ENVIRON["PATH"] ) exit (1)'		\
	'IGNORECASE	IGNORECASE = 1; if ( !("A" ~ "a") ) exit (1)'	\
	'\x escapes	if ( "\x41" != "A" ) exit (1)'			\
	'assignment to $0	$0 = "a b"; print $2	b'		\
	'array delete elem	a[1]=1; delete a[1]; if (a[1]!=0) exit (1)' \
	'array delete	a[1]=1; delete a; if (a[1]!=0) exit (1)'	\
	'array "in"	i="x"; a[i]="1"; if (! (i in a)) exit (1)'	\
	'assoc array	a ["i"] = "x"; print a ["i"]	x'		\
	'atan2()	print atan2 (0, 1)	0'			\
	'cos()	print cos(0)	1'					\
	'exp()	print exp(0)	1'					\
	'getline	"echo 1" | getline; if ( $0 != "1" ) exit (1)'	\
	'int()	print int(1.5)	1'					\
	'index()	print index("AB", "B")	2'			\
	'length()	print length("A")	1'			\
	'log()	print log(1)	0'					\
	'gensub()	print gensub (/u/, "x", "g", "uu")	xx'	\
	'gsub()	s = "AB"; gsub(/./, "X", s); print s	XX'		\
	'match()	print match("ab", /b/)	2'			\
	'operator **	print 2**2	4'				\
	'operator ^	print 2^2	4'				\
	'printf()	printf("%s\n", "X")	X'			\
	'rand()	print rand()'						\
	'sin()	print sin(0)	0'					\
	'split()	print split ("A B", a, " ")	2'		\
	'sprintf()	print sprintf("%.1s", "AB")	A'		\
	'sqrt()	print sqrt(1)	1'					\
	'srand()	srand()'					\
	'sub()	s = "AB"; sub(/./, "X", s); print s	XB'		\
	'substr()	print substr ("AB", 2, 1)	B'		\
	'system()	system (":")'					\
	'systime()	print systime()'				\
	'strftime()	print strftime("%d.%m.%y", 0)	01.01.70'	\
	'conditional exp	a=(1)?("y"):("n"); print a	y'	\
	'toupper()	print toupper("a")	A'			\
	'tolower()	print tolower("A")	a'			\
	'var regexp	r="x"; if ( "x" ~ r ) print "yes"	yes'
do
    OIFS="$IFS"
    IFS="	" export IFS
    set -- $func
    IFS="$OIFS"

    case "$#" in
    	2)  msg="$1"; func="$2"; result=;;
	3)  msg="$1"; func="$2"; result="$3";;
	*)  echo >&2 "invalid awk test: $*"
	    exit 2;;
    esac

    echo >&2 "$msg"
    echo > "$Input"	

    cat <<-EOT > "$Script"
	{
	    $func
	}
	EOT

    for AWK in $AWKList
    do
    	Status="$AWK	$msg"
	if TZ= "$AWK" -f "$Script" "$Input" > "$Output" 2>&1
	then					# AWK returned success
	    if [ -n "$result" ]
	    then				# Check result string
	    	if [ -s "$Output" ]
		then
		    if [ X"$result" = X"`cat $Output`" ]
		    then
		    	Status="$Status	+"
			echo >&2 "	$AWK +"
		    else
		    	Status="$Status	!"
			echo >&2 "	$AWK - (expected <$result>, got <`cat $Output`>)"
		    fi
		else
		    Status="$Status	-"
		    echo >&2 "	$AWK did not produce output"
		fi
	    else
		Status="$Status	+"
		echo >&2 "	$AWK +"
	    fi
	else
	    Status="$Status	-"
	    echo >&2 "	$AWK -"
	fi
	echo "$Status" >> "$Result"
    done
done

if [ -s "$Result" ]
then
    # Create a table containing all results

    sort < "$Result" |
    awk -F'	' '
	NF != 3 { print "	! " $0 }
	NF == 3 {
	    if ( awks [$1] == "" ) {
		awks [$1] = $1
		if ( Header == "" ) Header = "   "
		Header = Header "	" $1
	    }
	    if ( F [$2] != "" ) F [$2] = F [$2] "	"
	    F [$2] = F [$2] $3
	}
	END {
	    print Header
	    for ( i in F ) {
		print i "	" F [i]
	    }
	}
    ' |
    sort |
    tee "$LOGFILE"
fi

echo >&2 "
A copy of the test results were written to the file
	$LOGFILE

Please send an e-mail with the contents of the file to the 
following address:

	$email
"

exit 0
