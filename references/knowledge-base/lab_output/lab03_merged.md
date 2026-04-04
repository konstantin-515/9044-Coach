# COMP(2041|9044) 26T1 — Week 03 Laboratory Exercises

Lab: 03

Source: https://cgi.cse.unsw.edu.au/~cs2041/26T1/lab/03/questions

## Intro Sections

### Objectives

Objectives Understanding shell scripting

### Preparation

Preparation Before the lab you should re-read the relevant lecture slides and their accompanying examples.

### Getting Started

Getting Started Set up for the lab by creating a new directory called lab03 and changing to this directory. mkdir lab03 cd lab03 There are no provided files for this lab.

#### Code Blocks

```
mkdir lab03
cd lab03
```

## Exercises

### Exercise: Balancing numbers

Write a POSIX-compatible shell script, balancing_numbers.sh , that reads from standard input and writes to standard output. It should:

- map all digit characters whose values are less than 5 into the character ' < '.
- map all digit characters whose values are greater than 5 into the character ' > '.
- leave the digit character '5', and all non-digit characters, unchanged.

```
Sample Input Data | 1 234 5 678 9 | I can think of 100's of other things I'd rather be doing than these 5 questions | A line with lots of numbers: 123456789123456789123456789 A line with all zeroes 000000000000000000000000000 A line with blanks at the end 1 2 3 | Input with absolutely 0 digits in it Well ... apart from that 1 ... | 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536
Corresponding Output | < <<< 5 >>> > | I can think of <<<'s of other things I'd rather be doing than these 5 questions | A line with lots of numbers: <<<<5>>>><<<<5>>>><<<<5>>>> A line with all zeroes <<<<<<<<<<<<<<<<<<<<<<<<<<< A line with blanks at the end < < < | Input with absolutely < digits in it Well ... apart from that < ... | < < < > <> << >< <<> <5> 5<< <<<< <<<> <<>> ><>< <><>< <<>>> >55<>
```

#### Notes

Make the first line of your shell-script #!/bin/dash

tr(1) will be very useful.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest balancing_numbers
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Monday 09 March 2026 12:00 (midday) (2026-03-09 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab03_balancing_numbers balancing_numbers.sh
```

### Exercise: Can you hear my echo

Write a POSIX-compatible shell script called echon.sh which given exactly two arguments, an integer n and a string, prints the string n times.

For example:

```
./echon.sh 1 goodbye
goodbye
./echon.sh 5 hello
hello
hello
hello
hello
hello
./echon.sh 0 nothing
```

Your script should print exactly the error message below if it is not given exactly 2 arguments:

```
./echon.sh 
Usage: ./echon.sh <number of lines> <string>
./echon.sh 1 2 3
Usage: ./echon.sh <number of lines> <string>
```

Your script should print exactly the error message below if its first argument isn't a non-negative integer:

```
./echon.sh hello world
./echon.sh: argument 1 must be a non-negative integer
./echon.sh -42 lines
./echon.sh: argument 1 must be a non-negative integer
```

Although its better practice to print your error messages to stderr its OK to print your error messages to stdout for this exercise.

#### Notes

Make the first line of your shell-script #!/bin/dash

You will need to use:

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest echon
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Monday 09 March 2026 12:00 (midday) (2026-03-09 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab03_echon echon.sh
```

### Exercise: Categorising sizes

Write a POSIX-compatible shell script, file_sizes.sh , which prints the names of the files in the current directory splitting them into three categories:

- small if the file contains less than 10 lines
- medium-sized if the file contains between 10 and 100 lines
- large if the file contains 100 or more lines

Your script should always print exactly three lines of output. Files should be listed in alphabetic order on each line. Your shell-script should match character-for-character the output shown in the example below. Notice the creation of a separate directory for testing and the use of the script from the last question to produce test files. You could also produce test files manually using an editor.

```
mkdir test
cd test
../echon.sh 5 text > a
../echon.sh 505 text > bbb
../echon.sh 17 text > cc
../echon.sh 10 text > d
../echon.sh 1000 text > e
../echon.sh 0 text > empty
ls -l
total 24
-rw-r--r-- 1 andrewt andrewt   25 Mar 24 10:37 a
-rw-r--r-- 1 andrewt andrewt 2525 Mar 24 10:37 bbb
-rw-r--r-- 1 andrewt andrewt   85 Mar 24 10:37 cc
-rw-r--r-- 1 andrewt andrewt   50 Mar 24 10:37 d
-rw-r--r-- 1 andrewt andrewt 5000 Mar 24 10:37 e
-rw-r--r-- 1 andrewt andrewt    0 Mar 24 10:37 empty
../file_sizes.sh 
Small files: a empty
Medium-sized files: cc d
Large files: bbb e
rm cc d
../echon.sh 10000 . > lots_of_dots
ls -l
total 36
-rw-r--r-- 1 andrewt andrewt    25 Mar 24 10:37 a
-rw-r--r-- 1 andrewt andrewt  2525 Mar 24 10:37 bbb
-rw-r--r-- 1 andrewt andrewt  5000 Mar 24 10:37 e
-rw-r--r-- 1 andrewt andrewt     0 Mar 24 10:37 empty
-rw-r--r-- 1 andrewt andrewt 20000 Mar 24 10:39 lots_of_dots
../file_sizes.sh
Small files: a empty
Medium-sized files:
Large files: bbb e lots_of_dots
```

#### Notes

Make the first line of your shell-script #!/bin/dash

You can use the command wc(1) to discover how many lines are in a file. You probably want to use a subshell $() , if statements, and the [(1) ( test(1) ) command.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest file_sizes
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Monday 09 March 2026 12:00 (midday) (2026-03-09 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab03_file_sizes file_sizes.sh
```

### Exercise: Scraping JSON APIs with the shell

Write a POSIX-compatible shell script, scraping_courses.sh , which prints a list of UNSW postgraduate & undergraduate courses with the given prefix by extracting them from the UNSW handbook webpages.

In 2019 UNSW changed to much prettier format but also added an API that scripts can extract information from. (It's probably not really meant for our scripts, but they haven't blocked us yet)

In 2024 UNSW added rate limiting to the API, but we have ways around that.

For this exercise we'll use the 2019-2026 handbook pages via the API

For example:

```
./scraping_courses.sh 2021 OPTM
OPTM2133 The Clinical Environment
OPTM2190 Introduction to Clinical Optometry
OPTM2233 Optical Dispensing
OPTM2291 Primary Care Optometry
OPTM3105 Disease Processes of the Eye 1
OPTM3111 Optometry 3A
OPTM3131 Ocular Disease 3A
OPTM3133 Vision Science in the Consulting Room
OPTM3201 Ocular Imaging & Applied Vision Science
OPTM3205 Disease Processes of the Eye 2
OPTM3211 Optometry 3B
OPTM3231 Ocular Disease 3B
OPTM3233 Working in the Clinical Environment
OPTM4110 Optometry 4A
OPTM4131 Clinical Optometry 4A
OPTM4151 Ocular Therapeutics 4A
OPTM4211 Optometry 4B
OPTM4231 Clinical Optometry 4B
OPTM4251 Ocular Therapeutics 4B
OPTM4271 Professional Optometry
OPTM4291 Optometry, Medicine and Patient Management
OPTM5111 Clinical Optometry 5A
OPTM5131 Specialist Clinical Optometry 5A
OPTM5151 Clinical Ocular Therapeutics 5A
OPTM5171 Research Project 5A
OPTM5211 Clinical Optometry 5B
OPTM5231 Specialist Clinical Optometry 5B
OPTM5251 Clinical Ocular Therapeutics 5B
OPTM5271 Research Project 5B
OPTM6400 Optometric Preclinical Practice
OPTM6411 Contact Lenses
OPTM6412 Clinical Optometry 4A
OPTM6413 Anterior Eye Therapeutics
OPTM6421 Binocular Vision, Paediatrics and Low Vision
OPTM6422 Clinical Optometry 4B
OPTM6423 Therapeutics and the Posterior Eye
OPTM6424 Professional Optometry
OPTM7001 Introduction to Community Eye Health
OPTM7002 Epidemiology & Biostatistics for Needs Assessment
OPTM7003 Epidemiology of Blinding Eye Diseases
OPTM7004 Advocacy and Education in Community Eye Health
OPTM7005 Eye Health Economics and Sustainability
OPTM7006 Eye Care Program Management
OPTM7007 Community Eye Health Project
OPTM7103 Behavioural Optometry 1
OPTM7104 Advanced Contact Lens Studies 1
OPTM7107 Ocular Therapy 1
OPTM7108 Research Skills in Optometry
OPTM7115 Visual Neuroscience
OPTM7117 Ocular Therapy 2
OPTM7203 Behavioural Optometry 2
OPTM7205 Specialty Contact Lens Studies
OPTM7208 Research Skills in Optometry
OPTM7213 Ocular Therapy
OPTM7218 Research Project
OPTM7301 Advanced Clinical Optometry
OPTM7302 Evidence Based Optometry
OPTM7308 Research Project
OPTM7444 Business Skills in Optometry
OPTM7511 Advanced Ocular Disease 1
OPTM7521 Advanced Ocular Disease 2
OPTM7611 Introduction to Myopia
OPTM7612 Myopia Management
OPTM7621 Clinical Myopia Management
OPTM8511 Clinical Paediatrics, Low Vision and Colour Vision
OPTM8512 Clinical Optometry 5A
OPTM8513 Clinical Ocular Therapy 5A
OPTM8514 Optometry Research Project
OPTM8518 Optometry Research Project A
OPTM8521 Clinical Contact Lenses
OPTM8522 Clinical Optometry 5B
OPTM8523 Clinical Ocular Therapy 5B
OPTM8528 Optometry Research Project B
./scraping_courses.sh 2020 MATH | wc
    125     601    5029
./scraping_courses.sh 2019 COMP | grep -F "Soft"
COMP1531 Software Engineering Fundamentals
COMP2041 Software Construction: Techniques and Tools
COMP3141 Software System Design and Implementation
COMP3431 Robotic Software Architecture
COMP4161 Advanced Topics in Software Verification
COMP6447 System and Software Security Assessment
COMP6452 Software Architecture for Blockchain Applications
COMP9044 Software Construction: Techniques and Tools
COMP9322 Software Service Design and Engineering
COMP9323 Software as a Service Project
COMP9434 Robotic Software Architecture
./scraping_courses.sh 2023 MINE | grep -F "Rock"
MINE3630 Rock Breakage
MINE5010 Fundamentals of Rock Behaviour for Underground Mining
MINE5030 Mining Excavations in Rock
```

Your script should print exactly the error message below if it is not given exactly 2 arguments:

```
./scraping_courses.sh
Usage: ./scraping_courses.sh <year> <course-prefix>
```

Also get your script to print this error message if its first argument isn't in the allowable range:

```
./scraping_courses.sh 2000 COMP
./scraping_courses.sh: argument 1 must be an integer between 2019 and 2026
```

Your script must access the handbook API and extract the information from the returned JSON data.

#### Notes

Making too many requests to the API in a short period of time may result in your IP being blocked for a short period of time.

You should test your script intermittently, and not run it multiple times in quick succession.

autotest will make many requests to the API in quick succession.

You should manually test your script with a few different prefixes before running autotest.

You should wait at least 2 minutes between each time you run autotest.

If your script starts failing randomly, it's likely that your IP has been blocked.

wait 5 minutes without running your script before trying again.

Make the first line of your shell-script #!/bin/dash

The program curl can be used to access the API, by running it as curl -sL <url> or The program wget can be used to access the API, by running it as wget -qO- <url>

This task is tricky just using line-based tools such as, sort , and uniq .

An extra tool called jq can make the task much easier.

But you'll need to figure out how to use jq - understanding new tools is a skill worth developing!

The following URL will return all Courses, Programs, and Specialisations available in 2020: https://handbook-proxy.cse.unsw.edu.au/current/api/search-all?searchType=advanced&siteId=unsw-prod-pres&query=&siteYear=2020

Any sequence of whitespace characters in the course title should be replaced with a single space.

Make sure courses which occur in both postgraduate & undergraduate handbooks aren't repeated.

We are only interested in postgraduate & undergraduate courses, not research courses, programs, or specialisations.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest scraping_courses
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Monday 09 March 2026 12:00 (midday) (2026-03-09 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab03_scraping_courses scraping_courses.sh
```

### Challenge Exercise: Scraping Badly Designed JSON APIs with the shell

Write a POSIX-compatible shell script, advanced_scraping_courses.sh , which works exactly the same as scraping_courses.sh but can also retrieve data from the legacy handbook.

In 2005-2018 the handbook uses a different API so you will need to write a new (and more complicated) jq command.

The legacy handbook API returns a lot of extra information. We only want undergraduate and postgraduate courses.

Same as the non-challenge exercise, your script should print a suitable error message when necessary.

#### Notes

Making too many requests to the API in a short period of time may result in your IP being blocked for a short period of time.

You should test your script intermittently, and not run it multiple times in quick succession.

autotest will make many requests to the API in quick succession.

You should manually test your script with a few different prefixes before running autotest.

You should wait at least 2 minutes between each time you run autotest.

If your script starts failing randomly, it's likely that your IP has been blocked.

wait 5 minutes without running your script before trying again.

Make the first line of your shell-script #!/bin/dash

You can still use the same curl command curl -sL <url> or You can still use the same wget command wget -qO- <url>

You can find the legacy handbook API here (eg, for all courses (and more) in 2005): https://handbook-proxy.cse.unsw.edu.au/legacy/api/search/2005data.json

If a course doesn't have a course code listed perhaps there is another way to get this information

If a course doesn't have a course title listed it should simply be left blank.

Any sequence of whitespace characters in the course title should be replaced with a single space.

Remember we only want to print the course code and course title of undergraduate and postgraduate courses.

Opening the API URL in firefox will give a nice interface for you to examine the returned data (other browsers might provide similar functionality with extensions).

Your script should work for all years from 2005 to 2026.

#### Autotest

When you think your program is working, you can use autotest to run some simple automated tests:

```
2041 autotest advanced_scraping_courses
```

#### Submission

When you are finished working on this exercise, you must submit your work by running give :

before Monday 09 March 2026 12:00 (midday) (2026-03-09 12:00:00) to obtain the marks for this lab exercise.

```
give cs2041 lab03_advanced_scraping_courses advanced_scraping_courses.sh
```
