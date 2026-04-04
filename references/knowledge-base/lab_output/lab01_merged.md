# COMP(2041|9044) 26T1 — Week 01 Laboratory Exercises

Lab: 01

Source: https://cgi.cse.unsw.edu.au/~cs2041/26T1/lab/01/questions

## Intro Sections

### Objectives

Objectives Understanding regular expressions Understanding use of UNIX filters (grep)

### Preparation

Preparation Before the lab you should re-read the relevant lecture slides and their accompanying examples.

### Getting Started

Getting Started Set up for the lab by creating a new directory called lab01 and changing to this directory. mkdir lab01 cd lab01 There are some provided files for this lab which you can fetch with this command: 2041 fetch lab01 If you're not working at CSE, you can download the provided files as a zip file or a tar file .

#### Links

- [zip file](https://cgi.cse.unsw.edu.au/~cs2041/26T1/lab/01/zip)
- [tar file](https://cgi.cse.unsw.edu.au/~cs2041/26T1/lab/01/tar)

## Exercises

### Exercise: grep-ing a Dictionary

#### Files

- `dictionary.txt`
- `dictionary_answers.txt`

#### Intro

You have been given a file named

The autotest scripts depend on the format of

On most Unix systems you will find one or more dictionaries containing many thousands of words:

We've created an example dictionary named

#### Questions

##### Q1

Write a

**Hint**

It should print:

```
almner
almners
calmness
calmnesses
```

**Check / Autotest**

The COMP2041 class account contains a script named

Once you have entered your answer you can check it like this:

##### Q2

Write a

**Hint**

It should print:

```
aqueous
archaeoastronomer
archaeoastronomers
archaeoastronomical
archaeoastronomies
archaeoastronomy
banlieue
beauish
blooie
cooee
cooeed
cooeeing
cooees
enqueue
epigaeous
epopoeia
epopoeias
euoi
euois
euouae
euouaes
flooie
giaour
giaours
gooier
gooiest
guaiac
guaiacol
guaiacols
guaiacs
guaiacum
guaiacums
guaiocum
guaiocums
hawaiians
homoiousian
homoiousians
hypoaeolian
hypogaeous
loaiasis
looie
looies
louie
louies
maieutic
maieutical
maieutics
meoued
meouing
metasequoia
metasequoias
miaou
miaoued
miaouing
miaous
mythopoeia
mythopoeias
nonaqueous
obloquious
obsequious
obsequiously
obsequiousness
obsequiousnesses
onomatopoeia
onomatopoeias
palaeoanthropic
palaeoanthropological
palaeoanthropologies
palaeoanthropologist
palaeoanthropologists
palaeoanthropology
palaeoecologic
palaeoecological
palaeoecologies
palaeoecologist
palaeoecologists
palaeoecology
palaeoethnologic
palaeoethnological
palaeoethnologist
palaeoethnologists
palaeoethnology
pharmacopoeia
pharmacopoeial
pharmacopoeian
pharmacopoeias
plateaued
plateauing
prosopopoeia
prosopopoeial
prosopopoeias
queue
queued
queueing
queueings
queuer
queuers
queues
queuings
radioautograph
radioautographic
radioautographies
radioautographs
radioautography
radioiodine
radioiodines
reliquiae
rhythmopoeia
saouari
saouaris
scarabaeoid
scarabaeoids
sequoia
sequoias
subaqueous
tenuious
terraqueous
zoaea
zooea
zooeae
zooeal
zooeas
zoogloeae
zoogloeoid
zooier
zooiest
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q3

Write a

The words may contain more than 5 vowels but they must contain "aeiou" in that order.

**Hint**

It should print:

```
abstemious
abstemiously
abstemiousness
abstemiousnesses
abstentious
adenocarcinomatous
adventitious
adventitiously
adventitiousness
adventitiousnesses
aeruginous
amentiferous
androdioecious
andromonoecious
anemophilous
antenniferous
antireligious
arenicolous
argentiferous
arsenious
arteriovenous
asclepiadaceous
autoecious
autoeciously
bacteriophagous
caesalpiniaceous
caesious
cavernicolous
chaetiferous
facetious
facetiously
facetiousness
facetiousnesses
flagelliferous
garnetiferous
haemoglobinous
hamamelidaceous
lateritious
paroecious
quadrigeminous
sacrilegious
sacrilegiously
sacrilegiousness
sacrilegiousnesses
sarraceniaceous
supercalifragilisticexpialidocious
ultrareligious
ultraserious
valerianaceous
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q4

Write a

**Hint**

It should print:

```
abstemious
abstemiously
abstentious
arsenious
caesious
facetious
facetiously
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

#### Footer

When you are finished working on this exercise, you must submit your work by running

before

### Exercise: grep-ing Federal Parliament

#### Files

- `parliament.txt`
- `parliament_answers.txt`

#### Intro

You have been given a file named

The autotest scripts depend on the format of

In this exercise you will analyze a file named

#### Questions

##### Q1

Write a

**Hint**

It should print:

```
Hon Scott Buchholz: Member for Wright, Queensland
Hon Tony Burke: Member for Watson, New South Wales
Hon Stephen Jones: Member for Whitlam, New South Wales
Mr Peter Khalil: Member for Wills, Victoria
Mr Llew O'Brien: Member for Wide Bay, Queensland
Ms Allegra Spender: Member for Wentworth, New South Wales
Ms Anne Stanley: Member for Werriwa, New South Wales
Ms Zali Steggall OAM: Member for Warringah, New South Wales
Hon Dan Tehan: Member for Wannon, Victoria
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q2

Write a

**Hint**

It should print:

```
Dr Andrew Charlton: Member for Parramatta, New South Wales
Hon Andrew Gee: Member for Calare, New South Wales
Hon Andrew Giles: Member for Scullin, Victoria
Hon Andrew Hastie: Member for Canning, Western Australia
Hon Dr Andrew Leigh: Member for Fenner, Australian Capital Territory
Mr Andrew Wallace: Member for Fisher, Queensland
Mr Andrew Wilkie: Member for Clark, Tasmania
Mr Andrew Willcox: Member for Dawson, Queensland
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q3

Write a

**Hint**

It should print:

```
Ms Angie Bell: Member for Moncrieff, Queensland
Mr Sam Birrell: Member for Nicholls, Victoria
Mr Matt Burnell: Member for Spence, South Australia
Mr Julian Hill: Member for Bruce, Victoria
Mr Brian Mitchell: Member for Lyons, Tasmania
Mr Rob Mitchell: Member for McEwen, Victoria
Ms Zali Steggall OAM: Member for Warringah, New South Wales
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q4

Write a

**Hint**

It should print:

```
Ms Peta Murphy: Member for Dunkley, Victoria
Mr Rowan Ramsey: Member for Grey, South Australia
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q5

Write a

**Hint**

It should print:

```
Hon Dr Anne Aly: Member for Cowan, Western Australia
Hon Linda Burney: Member for Barton, New South Wales
Ms Kate Chaney: Member for Curtin, Western Australia
Hon Pat Conroy: Member for Shortland, New South Wales
Hon Milton Dick: Member for Oxley, Queensland
Hon Ed Husic: Member for Chifley, New South Wales
Hon Bob Katter: Member for Kennedy, Queensland
Hon Ged Kearney: Member for Cooper, Victoria
Hon Michelle Landry: Member for Capricornia, Queensland
Hon Sussan Ley: Member for Farrer, New South Wales
Mr Sam Lim: Member for Tangney, Western Australia
Mrs Melissa McIntosh: Member for Lindsay, New South Wales
Ms Louise Miller-Frost: Member for Boothby, South Australia
Ms Peta Murphy: Member for Dunkley, Victoria
Mr Llew O'Brien: Member for Wide Bay, Queensland
Hon Tanya Plibersek: Member for Sydney, New South Wales
Mr Rowan Ramsey: Member for Grey, South Australia
Hon Michelle Rowland: Member for Greenway, New South Wales
Ms Anne Stanley: Member for Werriwa, New South Wales
Ms Kylea Tink: Member for North Sydney, New South Wales
Mr Aaron Violi: Member for Casey, Victoria
Hon Anika Wells: Member for Lilley, Queensland
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q6

Write a

**Hint**

It should print:

```
Mr Luke Gosling OAM: Member for Solomon, Northern Territory
Hon Andrew Hastie: Member for Canning, Western Australia
Hon Catherine King: Member for Ballarat, Victoria
Hon Madeleine King: Member for Brand, Western Australia
Mr Jerome Laxale: Member for Bennelong, New South Wales
Dr Monique Ryan: Member for Kooyong, Victoria
Hon Bill Shorten: Member for Maribyrnong, Victoria
Mr Terry Young: Member for Longman, Queensland
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q7

Write a

**Hint**

It should print:

```
Hon Anthony Albanese: Member for Grayndler, New South Wales
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

##### Q8

Write a

**Hint**

It should print:

```
Hon Barnaby Joyce: Member for New England, New South Wales
Hon Kristy McBain: Member for Eden-Monaro, New South Wales
Mr Llew O'Brien: Member for Wide Bay, Queensland
Hon Matt Thistlethwaite: Member for Kingsford Smith, New South Wales
Ms Kylea Tink: Member for North Sydney, New South Wales
Hon Jason Wood: Member for La Trobe, Victoria
```

**Check / Autotest**

Once you have entered your answer you can check it like this:

#### Footer

When you are finished working on this exercise, you must submit your work by running

before

### Challenge Exercise: Exploring Regular Expressions

#### Files

- `ab_answers.txt`
- `input.txt`

#### Intro

You have been given a file named

The autotest scripts depend on the format of

Use

We've provided a set of test cases in

#### Questions

##### Q1

Write a

Once you have entered your answer you can check it like this:

##### Q2

Write a

In other words if there is pair of

Once you have entered your answer you can check it like this:

##### Q3

Write a

Once you have entered your answer you can check it like this:

#### Footer

When you are finished working on this exercise, you must submit your work by running

before
