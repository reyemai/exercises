

Author: Marco Bettoni
Data: 2021/06/20

Title:
	Code for "Message queue with priorities"

Description:
	Check description.txt

Content:
	.\main.cpp            - Main + test
	.\Makefile            - makefile
	.\PriorityQueue.cpp   - Priority Queue implementation
	.\PriorityQueue.h     - 
	.\QueueUserThread.cpp - Classes for case testing
	.\QueueUserThread.h   - 
	.\readme.txt          - this file

How to BUILD:
	$ cd $this_folder
	$ Make

	Otherwise:
	$ g++ -pthread -g *.cpp -o TestPriorityQueue

How to RUN:
	The binary can run with some basic values
	$ ./TestPriorityQueue

Additional compile time parameters:
	- Message size:
		Please edit PriorityQueue.h for:
			#define MESSAGE_SIZE 512
			#define MESSAGE_TYPE unsigned char
		Which will set the size and the formar of the Message
	- Queue Full/Empty Threshold:
		Please initialize the queue with the following paramenters:
			PriorityQueue(int maxMessages,float lowThreshold,float highThreshold)
	- N Threads:
		You can change main.c to modify the sample test:
			#define N_READING_THREADS 3
			#define N_WRITING_THREADS 3
			#define READERS_READING_N_VALUES 10
			#define WRITERS_WRITING_N_VALUES 10

Testing Environment:
	- gcc version 9.3.0
	- Ubuntu 20.04.2 LTS