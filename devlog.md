# Date: 9/23/2025, Time- 12:05 PM

THIS IS MY FIRST SESSION! I plan on using Python as my chosen programming langauge, because that is the only language I have used frequently in the past few months, other than SQLite. I will work on the Encryption Program first, before worrying about the other two programs. It doesn't seem too bad, after all this is my first time dealing with encryption. But, I hope I'll do my best! Hopefully, I get this encryption program completed by the end of today. If not, by tomorrow. 


# Date: 9/23/2025, Time- 9:52 PM
The encryption program is pretty much done. I may add some minor tweaks later on, but as for now, it's good. The only difficult thing was implementing the logic for the encryption and decryption. I had to watch 
a couple of Youtube videos to get the gist of it. The next program I will work on is the "logger". I felt using a class in the program fits the theme of encryption if we want the passkey to be hidden! Plus, I honestly felt more organized using a class. I'll work on it later this week, if I have time of course. 

# Date: 9/23/2025, Time- 10:29 PM

The logger program is basically completed. Honestly, this was the easiest part of this whole project. Just like the encryption program, I will probably have to perform some minor changes to the logger program, so that it can work with the driver's program. For instance, instead of I need to change connect the standard I/O with pipes in mind. But as of now, it can work by itself! I took CS 4377 (Linux) back in the spring semester of 2025. I was never good with pipes, especially in C (the most painful programming language I had to learn in college). I haven't use pipes in Python as well. So before I even begin implementing my driver's program. I will watch some Youtube videos to freshen up my mind! 


# Date 9/25/2025, Time- 8:14 PM   

Game plan today is to finally work on the driver's program. I believe this is last thing I will have to work on, other than making some minor changes to the other 2 programs. I've watched some Youtube videos to get an idea of piping with Python's subprocess module, and I feel pretty comfortable with it! Firstly, I will work on the user interface (won't take me a long time to implement), and then worry about piping. I plan on finishing this either by tomorrow or the day after that. 

# Date 9/26/2024, Time- 11:20 PM

I finally completed the project! I was struggling because I realize that entering a passkey won't be retained throughout the whole runtime of the driver's program. Thus, it made it impossible to encrypt and decrypt the plain text.
So I looked up online how to make the encryption process persistent! Got it to work, thankfully. I also implemented the history feature in driver.py. Another issue I came across was the program freezing up everytime I tried to create a new process for the encryption. It seems that the problem was that I wasn't flushing out standard input, which cause the whole program to freeze up. That is all I have to say, thanks for listening!