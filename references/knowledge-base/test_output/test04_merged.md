# COMP(2041|9044) 26T1 — Week 04 Weekly Test Questions

Test: 04

Source: https://cgi.cse.unsw.edu.au/~cs2041/26T1/test/04/questions

Final URL: F:\Codex\9044\test_html\test04_live.html

HTTP Status: 200

## Intro Sections

### Getting Started

test04 There are some provided files for this test which you can fetch with this command: If you're not working at CSE, you can download the provided files as a zip file or a tar file .

```
mkdir test04
cd test04
```

```
2041 fetch test04
```

#### Links

- [zip file](https://cgi.cse.unsw.edu.au/~cs2041/26T1/test/04/zip)
- [tar file](https://cgi.cse.unsw.edu.au/~cs2041/26T1/test/04/tar)

### Submission

give You can run give multiple times. Only your last submission will be marked. Don't submit any exercises you haven't attempted. If you are working at home, you may find it more convenient to upload your work via give's web interface . Remember you have until Week 5 Thursday 21:00:00 to complete this test. Automarking will be run by the lecturer several days after the submission deadline for the test, using test cases that you haven't seen: different to the test cases autotest runs for you. Hint: do your own testing as well as running autotest Test Marks After automarking is run by the lecturer you can view it here the resulting mark will also be available via via give's web interface or by running this command on a CSE machine: Each test is worth 1.7 marks, and will be automarked. Your total mark for the tests component is computed as a sum of your best 6 of 8 test marks.

```
2041 classrun -sturec
```

#### Links

- [give's web interface](https://cgi.cse.unsw.edu.au/~give/Student/give.php)
- [view it here](https://cgi.cse.unsw.edu.au/~cs2041/26T1/student/)
- [via give's web interface](https://cgi.cse.unsw.edu.au/~give/Student/sturec.php)

## Exercises

### weekly test question: Create A File of Integers In Shell

create_integers_file.sh

The first & second arguments will specify a range of integers.

The third argument will specify a filename.

Your program should create a file of this name containing the specified integers.

For example:

```
./create_integers_file.sh 40 42 fortytwo.txt
cat fortytwo.txt
40
41
42
./create_integers_file.sh 1 5 a.txt
cat a.txt
1
2
3
4
5
./create_integers_file.sh 1 1000 1000.txt
wc 1000.txt
1000 1000 3893 1000.txt
```

Make the first line of your shell-script #!/bin/dash

You are not permitted to use external programs such as grep , sort , uniq , .... In particular you are not permitted to use the external program: seq . You are permitted to use built-in shell arithmetic and other built-in shell features including: case cd exit for if pwd read shift test while [ Note most of the above built-in shell features features are not useful for this problem. You may not use non-POSIX-compatible shell features such as bash extensions. Your script must work when run by /bin/dash on a CSE system. You are not permitted to rely on the extra features provided by /bin/bash or /bin/sh . You can assume anything that works with the version of /bin/dash on CSE systems is POSIX compatible. You may not use Perl, C, Python, or any other language. No error checking is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest shell_create_integers_file
```

give

```
give cs2041 test04_shell_create_integers_file create_integers_file.sh
```

### weekly test question: Change the Suffix of HTML Files

.html

.htm

Write a POSIX-compatible shell script htm2html.sh which changes the name of all files with the suffix .htm in the current directory to have the suffix .html . For example:

```
touch index.htm small.htm large.htm
ls *.htm*
index.htm  large.htm  small.htm
./htm2html.sh
ls *.htm*
index.html  large.html  small.html
```

1

.html

```
touch andrew.htm andrew.html
./htm2html.sh 
andrew.html exists
```

You are permitted to use external programs such as mv . Make the first line of your shell-script #!/bin/dash You are permitted to use built-in shell features. You may not use non-POSIX-compatible shell features such as bash extensions. Your script must work when run by /bin/dash on a CSE system. You are not permitted to rely on the extra features provided by /bin/bash or /bin/sh . You can assume anything that works with the version of /bin/dash on CSE systems is POSIX compatible. You may not use Perl, C, Python, or any other language. No error checking other than described above is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest htm2html
```

give

```
give cs2041 test04_htm2html htm2html.sh
```

### weekly test question: Checking for Missing Include Files

Write a POSIX-comaptible shell script missing_include.sh which is give one of more filenames as argument. The files will contain C code.

missing_include.sh should print a message if any file included by the C program is not present in the current directory.

Reminder C include lines are of this form:

```
#include "file.h"
```

```
cat a.c
#include <stdio.h>

#include "a.h"
#include "b.h"
#include "input.h"

int a(void){
    return 42;
}
cat b.c
#include <stdio.h>

#include "b.h"
#include "c.h"
#include "d.h"
#include <string.h>
#include "global.h"

int b(void){
    return b.c;
}
./missing_include.sh a.c
a.h included into a.c does not exist
input.h included into a.c does not exist
./missing_include.sh b.c
c.h included into b.c does not exist
global.h included into b.c does not exist
./missing_include.sh a.c b.c
a.h included into a.c does not exist
input.h included into a.c does not exist
c.h included into b.c does not exist
global.h included into b.c does not exist
```

```
#include <stdio.h>
```

You can assume filenames do not contain whitespace or glob characters ( *[]? ). You are permitted to use external programs such as grep . Make the first line of your shell-script #!/bin/dash You are permitted to use built-in shell features. You may not use non-POSIX-compatible shell features such as bash extensions. Your script must work when run by /bin/dash on a CSE system. You are not permitted to rely on the extra features provided by /bin/bash or /bin/sh . You can assume anything that works with the version of /bin/dash on CSE systems is POSIX compatible. You may not use Perl, C, Python, or any other language. No error checking is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest missing_include
```

give

```
give cs2041 test04_missing_include missing_include.sh
```
