# Sorta
Sorta is a tool to help you sort your files

## What's that?
Have you ever had a folder where lots of files pile up, and at the end it takes ages to tidy them up? Well, Sorta is the solution.

Create a Sorta drop folder, create some sorting rules, and all the files will magically be placed in the right place.

## Installation
Just follow these three steps:

1. clone this repository : `git clone https://github.com/loics2/sorta`
2. go into the sorta folder : `cd ./sorta`
3. install : `python3 setup.py install`

## How-to
Let's take an example : your download folder. You save files there, because you don't want to browse your filesystem everytime you download something.

First, init the drop folder :

    cd ~/download/
    sorta init

Next, we need to add some sorting rules. There are 2 types of rules:
* prefix rules : the destination of the file is defined by a prefix in the name of the file. A delimiter is used to separate the prefix and the file name (`--` by default)
* extension rules : the destination is defined by the extension of the file.

The prefixes are used first, then the extensions.

    sorta add prefix img ~/images/
    sorta add prefix doc ~/documents/

    sorta add ext mp3 ~/music/
    sorta add ext jpeg ~/images/

Finally, launch Sorta :

    sorta sort

Everything file matching one of your rules will be moved. In this case, the file `doc--cv.pdf` will be moved at `~/documents/cv.pdf`, or `friday.mp3` at `~/music/friday.mp3`.

## The config file
The rules (and other options) are stored in the `.sortaconfig` file at the root of the drop folder.
You can edit it manually (some options are not modifiable with the cli tool), but it needs to follow this structure :

    [core]
    delimiter = --          # this is the delimiter for the prefix
    polling = 60.0          # this is the polling time for the daemon

    [prefix]                # here come the prefix rules
    asdf = /home/user/asdf  # following the notation <prefix> = <path>

    [extension]             # here come the extension rules
    mp3 = /mnt/docs/music   # following the notation <extension> = <path>
    jpeg = /mnt/docs/images

## Compatibility
Sorta has been tested on Fedora 23, but should work on most of the platforms, no exotic libraries have been used.

## Contributions
Every contribution is accepted, feel free to make a pull request and I will happily look at it!
