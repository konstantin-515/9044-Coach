# COMP(2041|9044) 26T1 — Week 07 Weekly Test Questions

Test: 07

Source: https://cgi.cse.unsw.edu.au/~cs2041/26T1/test/07/questions

Final URL: F:\Codex\9044\test_html\test07_live.html

HTTP Status: 200

## Intro Sections

### Getting Started

test07

```
mkdir test07
cd test07
```

### Submission

give You can run give multiple times. Only your last submission will be marked. Don't submit any exercises you haven't attempted. If you are working at home, you may find it more convenient to upload your work via give's web interface . Remember you have until Week 8 Thursday 21:00:00 to complete this test. Automarking will be run by the lecturer several days after the submission deadline for the test, using test cases that you haven't seen: different to the test cases autotest runs for you. Hint: do your own testing as well as running autotest Test Marks After automarking is run by the lecturer you can view it here the resulting mark will also be available via via give's web interface or by running this command on a CSE machine: Each test is worth 1.7 marks, and will be automarked. Your total mark for the tests component is computed as a sum of your best 6 of 8 test marks.

```
2041 classrun -sturec
```

#### Links

- [give's web interface](https://cgi.cse.unsw.edu.au/~give/Student/give.php)
- [view it here](https://cgi.cse.unsw.edu.au/~cs2041/26T1/student/)
- [via give's web interface](https://cgi.cse.unsw.edu.au/~give/Student/sturec.php)

## Exercises

### weekly test question: Unique Echo

Write a Python program uniq_echo.py that prints its command-line argument to standard output, similar to echo command in Shell, except only the first occurrence of any argument should be printed, Repeat occurrences should not be printed.

```
./uniq_echo.py echo echo echo
echo 
./uniq_echo.py bird cow bird cow fish bird cow fish bird
bird cow fish 
./uniq_echo.py how much wood would a woodchuck chuck
how much wood would a woodchuck chuck 
./uniq_echo.py d c b d c a a d
d c b a 
./uniq_echo.py
```

Your answer must be Python only. You can not use other languages such as Shell, Perl or C. You may not run external programs.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest uniq_echo
```

give

```
give cs2041 test07_uniq_echo uniq_echo.py
```

### weekly test question: Snap N

Write a Python program snap_n.py which reads lines from its input until it reads an line that has been entered n times.

Your program should then print "Snap: " followed by the line.

Your program will be given n as a command line argument. Your program should print nothing if the end-of-input is reached before any line is repeated n times.

```
./snap_n.py 2
hi
how
are
you
hi
Snap: hi
```

```
./snap_n.py 2
hi
hi hi
hi hi hi
hi hi hi hi
hi hi
Snap: hi hi
```

```
./snap_n.py 4
Hello World
Line 2
Hello World
Line 3
Hello World
Line 4
Hello World
Snap: Hello World
```

You can assume input lines are ASCII, you should not assume anything else about input lines. Your answer must be Python only. You can not use other languages such as Shell, Perl or C. You may not run external programs. No error checking is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest snap_n
```

give

```
give cs2041 test07_snap_n snap_n.py
```

### weekly test question: Print the Line(s) from Stdin With the Largest Number

Write a Python program largest_numbered_line.py that read lines from standard input until end-of-input. It should then print the line(s) which contained the largest number.

Lines may contain multiple numbers and they may contain any number of any character between the numbers.

If the largest number occurs on multiple lines you should print all of the lines in the order they occurred.

If no line contains a number, your program should print nothing.

```
./largest_numbered_line.py
I spent $ 15.50 for
3.3 kg apples yesterday.
2000 is a leap year.

2000 is a leap year.
```

```
./largest_numbered_line.py
two2 four4 eight8 sixteen16
1 sixteen-and-half 16.5  1
11 12 13

1 sixteen-and-half 16.5  1
```

```
./largest_numbered_line.py
the quick brown f42ox
4 9 42 2 4
1 2 3 4 42.0
no forty two
last 42

the quick brown f42ox
4 9 42 2 4
1 2 3 4 42.0
last 42
```

```
./largest_numbered_line.py
a 0.01
b .5
c -0.9

b .5
```

```
./largest_numbered_line.py
a -.5
b -5
c --90--

a -.5
```

```
./largest_numbered_line.py
I love programming in Shell.
but I like Python better.
```

You can assume numbers do not contain white space, commas or other extra characters. You can assume numbers are only in decimal format . You can assume numbers are not in scientific/exponential format. You can assume input is only ASCII. Your answer must be Python only. You can not use other languages such as Shell, Perl or C. You may not run external programs. No error checking is necessary.

When you think your program is working you can autotest to run some simple automated tests:

```
2041 autotest largest_numbered_line
```

give

```
give cs2041 test07_largest_numbered_line largest_numbered_line.py
```
