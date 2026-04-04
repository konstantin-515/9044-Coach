# COMP(2041|9044) 26T1 — Week 07 Laboratory Exercises

Lab: 07

Source: https://cgi.cse.unsw.edu.au/~cs2041/26T1/lab/07/questions

## Intro Sections

### Objectives

Objectives Getting used to Python programing. Practice text processing in Python. Practice using regex in Python.

### Preparation

Preparation Before the lab you should re-read the relevant lecture slides and their accompanying examples.

### Getting Started

Getting Started Set up for the lab by creating a new directory called lab07 and changing to this directory. mkdir lab07 cd lab07 There are some provided files for this lab which you can fetch with this command: 2041 fetch lab07 If you're not working at CSE, you can download the provided files as a zip file or a tar file .

#### Code Blocks

```
mkdir lab07
cd lab07
```

```
2041 fetch lab07
```

#### Links

- [zip file](https://cgi.cse.unsw.edu.au/~cs2041/26T1/lab/07/zip)
- [tar file](https://cgi.cse.unsw.edu.au/~cs2041/26T1/lab/07/tar)

## Exercises

### Exercise: How many Orcas in that File?

A citizen science project monitoring whale populations has files of containing large numbers of whale observations. Each line in these files contains:

- the date the observation was made
- the number of whales in the pod ("pod" is the collective number for a group of whales)
- the species of whale

```
head whales0.txt
18/01/18  9 Pygmy right whale
01/09/17 21 Southern right whale
16/02/18  4 Striped dolphin
02/07/17  4 Common dolphin
19/02/18  4 Blue whale
21/02/18 38 Dwarf sperm whale
14/06/17 29 Southern right whale
20/06/17  3 Spinner dolphin
22/07/17 34 Indo-Pacific humpbacked dolphin
20/03/18  7 Long-finned pilot whale
```

Write a Python program orca.py which prints a count of the number of observations of Orcas in the files.

Your program should take 1 or more filenames as command line arguments.

```
./orca.py whales0.txt
1245 Orcas reported
./orca.py whales0.txt whales1.txt whales2.txt
3150 Orcas reported
```

Note: each line records one pod of whales Your program should print the number of individual Orca observed - it needs to sum each pod of Orcas.

#### Notes

Your answer must be Python only. You can not use other languages such as Shell, Perl or C.

Make the first line of your script #!/usr/bin/env python3

You may not run external programs.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest orca
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Tuesday 07 April 2026 12:00 (midday) (2026-04-07 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab07_orca orca.py
```

### Exercise: Printing A summary of All Whale Species

Write a Python program whale_summary.py which take one or more files on the command line.

whale_summary.py should print for, every whale species in the file, how many pods were seen and how many total whales were seen of that species.

Whale species should be listed in alphabetic order.

All whale names should be converted to lower case.

All whale names should be converted to singular form - assume this can be done safely by deleting a trailing 's' if it is present.

```
./whale_summary.py whales0.txt
blue whale observations: 51 pods, 1171 individuals
bryde's whale observations: 47 pods, 1023 individuals
coastal bottlenose dolphin observations: 53 pods, 1169 individuals
common dolphin observations: 62 pods, 1232 individuals
dwarf minke whale observations: 49 pods, 1080 individuals
dwarf sperm whale observations: 58 pods, 1272 individuals
fin whale observations: 65 pods, 1251 individuals
humpback whale observations: 55 pods, 1071 individuals
indo-pacific humpbacked dolphin observations: 43 pods, 897 individuals
long-finned pilot whale observations: 50 pods, 996 individuals
orca observations: 53 pods, 1245 individuals
pygmy right whale observations: 59 pods, 1260 individuals
pygmy sperm whale observations: 57 pods, 1346 individuals
sei whale observations: 55 pods, 929 individuals
short-finned pilot whale observations: 68 pods, 1344 individuals
southern right whale observations: 55 pods, 1252 individuals
spinner dolphin observations: 52 pods, 1118 individuals
striped dolphin observations: 68 pods, 1337 individuals
./whale_summary.py messy_whales0.txt
blue whale observations: 2 pods, 27 individuals
dwarf minke whale observations: 6 pods, 132 individuals
orca observations: 2 pods, 48 individuals
```

#### Notes

Your answer must be Python only. You can not use other languages such as Shell, Perl or C.

Make the first line of your script #!/usr/bin/env python3

You may not run external programs.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest whale_summary
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Tuesday 07 April 2026 12:00 (midday) (2026-04-07 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab07_whale_summary whale_summary.py
```

### Exercise: Find the sum of all numbers in a file

Write a Python program summing_numbers.py which given a file as a command line argument, prints the sum of all the numbers in the file.

A number for the purposes of this exercise is any sequence of consecutive digits.

Note only the digits 0-9 are considered parts of numbers. The characters '.' and '-' are not considered part of numbers.

For example, the string the "It was -42.5C outside" should be treated as containing the numbers 42 and 5 .

```
./summing_numbers.py A-Tale-of-Two-Cities.txt
7104
./summing_numbers.py Pride-and-Prejudice.txt
46520
```

#### Notes

You might find re.findall useful.

Your answer must be Python only. You can not use other languages such as Shell, Perl or C.

Make the first line of your script #!/usr/bin/env python3

You may not run external programs.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest summing_numbers
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Tuesday 07 April 2026 12:00 (midday) (2026-04-07 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab07_summing_numbers summing_numbers.py
```

### Challenge Exercise: A Python Program that Prints Python

Write a Python program python_print.py which is given a single argument. It should output a Python program which when run, prints this string. For example:

```
./python_print.py "hello world, how are you?" | python3 
hello world, how are you?
./python_print.py "I'm So Meta, Even This Acronym" > new_program.py
chmod +x new_program.py
./new_program.py
I'm So Meta, Even This Acronym
```

#### Notes

You can assume the string contains only ASCII characters.

You can not make other assumptions about the characters in the string.

Your answer must be Python only. You can not use other languages such as Shell, Perl or C.

Make the first line of your script #!/usr/bin/env python3

You may not run external programs.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest python_print
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Tuesday 07 April 2026 12:00 (midday) (2026-04-07 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab07_python_print python_print.py
```

### Challenge Exercise: A Python Program that Prints Python that Prints Python that ...

Write a Python program python_print_n.py which is given a two arguments, an integer n and a string.

If n is 1 it should output a Python program which prints the string.

If n is 2 it should output a Python program which prints a Python program which prints the string.

If n is 3 it should output a Python program which prints a Python program which prints a Python program which prints the string.

And so on for any value of n .

```
./python_print_n.py 1 "hello world, how are you?" | python3
hello world, how are you?
./python_print_n.py 2 "hello world, how are you?" | python3 | python3
hello world, how are you?
./python_print_n.py 3 "hello world, how are you?" | python3 | python3 | python3
hello world, how are you?
./python_print_n.py 10 "Now that's a lot of python" | python3 | python3 | python3 | python3 | python3 | python3 | python3 | python3 | python3 | python3
Now that's a lot of python
```

#### Notes

You can assume n is a positive integer.

You can assume the string contains only ASCII characters.

You can not make other assumptions about the characters in the string.

Your answer must be Python only. You can not use other languages such as Shell, Perl or C.

Make the first line of your script #!/usr/bin/env python3

You may not run external programs.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest python_print_n
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Tuesday 07 April 2026 12:00 (midday) (2026-04-07 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab07_python_print_n python_print_n.py
```

### Challenge Exercise: A Python Program that Prints itself forever

Write a Python program python_print_inf.py which prints it's own soruce code.

The program can not use the open function. The program can not use the inspect module.

```
./python_print_inf.py > new_program.py
diff -s python_print_inf.py new_program.py
Files python_print_inf.py and new_program.py are identical
chmod +x new_program.py
./new_program.py > second_order_program.py
diff -s python_print_inf.py second_order_program.py
Files python_print_inf.py and second_order_program.py are identical
./python_print_inf.py | python3 | python3 | python3 | python3 | python3 > nth_program.py
diff -s python_print_inf.py nth_program.py
Files python_print_inf.py and nth_program.py are identical
```

#### Notes

Your answer must be Python only. You can not use other languages such as Shell, Perl or C.

Make the first line of your script #!/usr/bin/env python3

You may not run external programs.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest python_print_inf
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Tuesday 07 April 2026 12:00 (midday) (2026-04-07 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab07_python_print_inf python_print_inf.py
```
