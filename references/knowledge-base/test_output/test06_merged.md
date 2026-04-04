# COMP(2041|9044) 26T1 — Week 06 Weekly Test Questions

Test: 06

Source: https://cgi.cse.unsw.edu.au/~cs2041/26T1/test/06/questions

Final URL: F:\Codex\9044\test_html\test06_live.html

HTTP Status: 200

## Intro Sections

### Getting Started

test06

```
mkdir test06
cd test06
```

### Submission

give You can run give multiple times. Only your last submission will be marked. Don't submit any exercises you haven't attempted. If you are working at home, you may find it more convenient to upload your work via give's web interface . Remember you have until Week 7 Thursday 21:00:00 to complete this test. Automarking will be run by the lecturer several days after the submission deadline for the test, using test cases that you haven't seen: different to the test cases autotest runs for you. Hint: do your own testing as well as running autotest Test Marks After automarking is run by the lecturer you can view it here the resulting mark will also be available via via give's web interface or by running this command on a CSE machine: Each test is worth 1.7 marks, and will be automarked. Your total mark for the tests component is computed as a sum of your best 6 of 8 test marks.

```
2041 classrun -sturec
```

#### Links

- [give's web interface](https://cgi.cse.unsw.edu.au/~give/Student/give.php)
- [view it here](https://cgi.cse.unsw.edu.au/~cs2041/26T1/student/)
- [via give's web interface](https://cgi.cse.unsw.edu.au/~give/Student/sturec.php)

## Exercises

### weekly test question: Remove the vowels from a file

Write a POSIX-compatible shell script devowel_file.sh , which takes one command line argument, the name of a file.

devowel_file.sh should remove vowels from the file.

Your program can assume vowels are {'a', 'e', 'i', 'o', 'u'} and their upper-case equivalents {'A', 'E', 'I', 'O', 'U'}

Your program should not print anything to stdout. The only thing it should do is change the file.

For example:

```
cat frost.txt
I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I --
I took the one less traveled by,
And that has made all the difference.
./devowel_file.sh frost.txt
cat frost.txt
 shll b tllng ths wth  sgh
Smwhr gs nd gs hnc:
Tw rds dvrgd n  wd, nd  --
 tk th n lss trvld by,
nd tht hs md ll th dffrnc.
```

devowel_file.sh

Make sure your program does this.

Your program can assume it is given one argument which is the name of a file. Your program can assume the file exists. Your program should print nothing to stdout. You are permitted to create temporary files. You are permitted to use these and only these external programs: basename cat chmod cmp cp cut diff dirname echo expr false find grep head ls mkdir mktemp mv printf pwd rev rm rmdir sed seq sort stat strings tac tail tee test touch tr true uniq wc xargs You are permitted to use any built-in shell features including: case cd exit for if pwd read shift test while [ You may not use non-POSIX-compatible Shell. You are not permitted to use /bin/bash or /bin/sh . You can assume anything that works with the version of /bin/dash on CSE systems is POSIX compatible. You may not use Perl, C, Python, or any other language. No error checking is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest shell_devowel_file
```

give

```
give cs2041 test06_shell_devowel_file devowel_file.sh
```

### weekly test question: Create Copies of a File

n_copies.sh

The first command line argument will be a filename file

The second command-line argument will be a positive integer n

Your script n_copies.sh should create n copies of file named file .1 , file .2 ... file . n

For example:

```
echo hello COMP2041 and COMP9041 >message
cat message
hello COMP2041 and COMP9041
ls message*
message
./n_copies.sh message 3
ls message*
message
message.1
message.2
message.3
cat message.2
hello COMP2041 and COMP9041
```

```
seq 6 10 >five_numbers.txt
cat five_numbers.txt
6
7
8
9
10
ls five_numbers.txt*
five_numbers.txt
./n_copies.sh five_numbers.txt 11
ls five_numbers.txt*
five_numbers.txt
five_numbers.txt.1
five_numbers.txt.10
five_numbers.txt.11
five_numbers.txt.2
five_numbers.txt.3
five_numbers.txt.4
five_numbers.txt.5
five_numbers.txt.6
five_numbers.txt.7
five_numbers.txt.8
five_numbers.txt.9
cat five_numbers.txt.10
6
7
8
9
10
```

You can assume the filename supplied as the first argument to your script exists. You can assume the files to be created by your script do not exist. You can assume the integer supplied as a second argument to your script is greater than zero. You are not permitted to create temporary files. You are permitted to use these and only these external programs: basename cat chmod cmp cp cut diff dirname echo expr false find grep head ls mkdir mktemp mv printf pwd rev rm rmdir sed seq sort stat strings tac tail tee test touch tr true uniq wc xargs You are permitted to use any built-in shell features including: case cd exit for if pwd read shift test while [ You may not use non-POSIX-compatible Shell. You are not permitted to use /bin/bash or /bin/sh . You can assume anything that works with the version of /bin/dash on CSE systems is POSIX compatible. You may not use Perl , C , Python , or any other language. You may not use awk . No error checking is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest shell_n_copies
```

give

```
give cs2041 test06_shell_n_copies n_copies.sh
```

### weekly test question: Three vowel echo

three_vowel_echo.sh

echo

Your program can assume vowels are there are 5 vowel {'a', 'e', 'i', 'o', 'u'} and their upper-case equivalents {'A', 'E', 'I', 'O', 'U'}

```
./three_vowel_echo.sh Pompeii Rome Aeolian Florence
Pompeii Aeolian
./three_vowel_echo.sh an anxious bedouin beauty booed an ancient zoologist
anxious bedouin beauty booed
./three_vowel_echo.sh 

./three_vowel_echo.sh abstemiously adenocarcinomatous Hawaiian Eoanthropus
abstemiously Hawaiian Eoanthropus
./three_vowel_echo.sh aaa aata EEE EETEE TeeE aEo aeteituu
aaa EEE TeeE aEo
```

Your shell script should produce only 1 line of output. Your shell script may produce an extra space at the end of the line. You are not permitted to create temporary files. You are permitted to use these and only these external programs: basename cat chmod cmp cp cut diff dirname echo expr false find grep head ls mkdir mktemp mv printf pwd rev rm rmdir sed seq sort stat strings tac tail tee test touch tr true uniq wc xargs You are permitted to use any built-in shell features including: case cd exit for if pwd read shift test while [ You may not use non-POSIX-compatible Shell. You are not permitted to use /bin/bash or /bin/sh . You can assume anything that works with the version of /bin/dash on CSE systems is POSIX compatible. You may not use Perl , C , Python , or any other language. You may not use awk . No error checking is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest shell_three_vowel_echo
```

give

```
give cs2041 test06_shell_three_vowel_echo three_vowel_echo.sh
```
