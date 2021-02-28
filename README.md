# AntiAFK
Program to prevent PC from going to sleep.

I created this to prevent _Skype for Business_ from showing me as "Away" every five minutes per the domain rules. Take a bathroom break? Get up to stretch? Reading a document on a page?
AWAY, with massive popup that says "Joe Vincent is Away"

Well no more.

This program, written in Python and utilizing QT, determines if the user is afk (using a multithreaded process to check for mouse movement or key presses). If so, it simply presses 'F13' on the keyboard at the user-defined interval. (Default of 10 seconds).
