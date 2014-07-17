Tail.py
=======

This is a small `tail` like program that should be system independent (should work on Windows, Linux and Mac).

Currently it simply outputs last line of file and observes the file continuously until your press `CTRL+C`.

Usage
-----
```bash
tail.py your_file.log  
```

Note. The scripts where tested on Python 2.6 and should work on any above.

If it doesn't work for you - please file a bug.

Why this script?
----------------

Because when you redirect output on Windows command line to a file you will NOT be able to observer it's output. Probably because flushing issues.

Here are some [other ways to observer file on Windows](http://www.stackify.com/11-ways-to-tail-a-log-file-on-windows-unix/) (note that I tested most of them and they didn't work for redirected output).
