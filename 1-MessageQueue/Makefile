# Makefile
 
# *****************************************************
# Variables to control Makefile operation
SRCS = *.cpp
CC = g++
CFLAGS = -pthread -g
MAIN = TestPriorityQueue
 
# ****************************************************
# Targets needed to bring the executable up to date
 
main: 
	$(CC) $(CFLAGS) $(SRCS) -o $(MAIN)

.PHONY: clean

clean:
	$(RM) *.o *~ $(MAIN)
