# sorta
Sorta is a tool to help you sort your files

## How does it work?
Sorta will check your drop folder and first look for prefixes, then for extensions.

You can add prefixes or extensions with the following commands :

    sorta.py add prefix <your prefix> <destination of the files containing the prefix> 
    sorta.py add ext <your extension> <destination of the files containing the extension>

By default, no prefix or extension is configured, and the delimiter for the prefix is `--`. 
You can change all of this by hand by modifying the `.sortaconfig` file in the root of your drop folder.

For more information, take a look at the help with the command `sorta.py -h`.

## Bugs, ameliorations and compatibility
Sorta has been test on Fedora 23, but it should work on every platform because no specific library has been used.

There's no bug for now, I count on the bug hunters!

Although I didn't found any bugs, they're some limitations due to the code : 

* when a file is in the drop folder, there's no check to see if it's open by another application. Sorta will copy it anyway, 
but the original will stay in the drop folder until it's closed.
* the daemon mode works by polling the state of the drop folder, it could be better to work with file system events (maybe?) 

## Contributions
Every contribution is accepted, feel free to make a pull request and I will happily look at it!