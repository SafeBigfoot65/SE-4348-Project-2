# Date: 10/20/2025; Time: 1:46 PM

This is the start of this project. From what I understood of the instructions, I'm just creating a program that shows the interactions between the customers, 3 bank tellers, and the manager. My plan is to basically work on each entity (manager, teller, customer) and figure out their attributes and functions associated with them. Then I will work on using Semaphores to the entities interact with others. This will take me a bit of time of to do since I have only using Sempaphores once in my entire life. That's all I have planned out for now!

# Date: 10/26/2025; Time: 11:10 PM

Yo, yo, yo! I have completed the teller class. Might have to make some adjustments later on, but I basically went ahead and implemented the actions of teller when dealing with a customer and the manager. I also gave out some restrictions such as there only being 3 teller threads in total, and that a teller can only assist ONE customer at a time. Next, I plan on working on the Customer class, and then finally testing out the interactions between these two classes. So far, I'm splitting up the work in 2-3 python files, just to make it easier to read for our sakes. I believe the 3rd file will just act as the main for now. Until next time!

# Date: 10/26/2025; Time: 1:47 PM
PS, I forgot to push my commit to the main branch...Doing it now.

# Date: 10/28/2025; Time: 2:12 PM

Made some changes to teller.py. In this file, I implemented the algorithm of logging the outputs in a text file called "log.txt". The reason why I put in a text file rather than displaying them in the terminal is because there are at least 1000 lines of outputs in regards to all of the actions taken and events. So, when the program runs, I won't be able to view all of them, especially the outputs that are shown at the very beginning. I also added it to a file called "customer.py", but I won't push it yet since I'm not done with it. It will probably either be pushed later this night, or by tomorrow morning. There are two additional files, one being the main and the other being the logger. Logger is almost completed, whereas I have only gotten started on the main file. The main file will take me some time to push, due to testing the program, and make any additional changes to the other files. If there is one thing that concerns me for the main file, it would be ending up in a deadlock 🙁. customer.py is very similar to teller.py, in terms of the attributes and the functions within the Teller and Customer classes, but of course there are few things that make each class unique, such as the customers having a random choice for the transaction type, and the tellers being the only ones to get approval from the manager and enter the safe. Until next time!!!

# Date: 10/28/2025; Time: 10:07 PM

I've completed customer.py. This file may need some adjustments later, but it seems good for now. I also wrote another script, that handles the logging aspect of this program. Next up is the main file, which will serve as the platform in regards to the interactions between the customers, tellers, and the shared resources (e.g., manager and safe). This part won't take me long to do, hopefully...Until next time!!!
