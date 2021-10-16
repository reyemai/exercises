#include <iostream>
#include <string>
#include <cstring>
#include <time.h> 
#include "QueueUserThread.h"
#include "PriorityQueue.h"

using namespace std;

#define N_READING_THREADS 3
#define N_WRITING_THREADS 3
#define READERS_READING_N_VALUES 10
#define WRITERS_WRITING_N_VALUES 10

int main()
{
    vector<QueueUserThread> tReads;
    vector<QueueUserThread> tWrites;
    vector<string> names;

    srand (time(NULL));

    // Instantiating the queue:
    // Parameters: 
    //     - Size 20 values
    //     - low_threshold  = 10% (float 0.1)
    //     - high_threshold = 90% (float 0.9)
    PriorityQueue q = PriorityQueue(20,0.1,0.9);

    // Define READERS Threads
    for(int i=0; i < N_READING_THREADS; i++)
    {
        names.push_back("READER"+to_string(i));
        QueueUserThread r = QueueUserThread(names.back(),&q,READERS_READING_N_VALUES,true);
        tReads.push_back(r);
    }

    // Define WRITING Threads
    for(int i=0; i < N_WRITING_THREADS; i++)
    {
        names.push_back("WRITER"+to_string(i));
        QueueUserThread w = QueueUserThread(names.back(),&q,WRITERS_WRITING_N_VALUES,false);
        tWrites.push_back(w);
    }

    // Start all threads
    for(int i=0; i < N_READING_THREADS; i++)
        tReads[i].start();

    for(int i=0; i < N_WRITING_THREADS; i++)
        tWrites[i].start();

    // Wait to finish:
    for(int i=0; i < N_READING_THREADS; i++)
    {
        tReads[i].join();
        cout << "RETURN READER " << i << endl;
    }

    for(int i=0; i < N_WRITING_THREADS; i++)
    {
        tWrites[i].join();
        cout << "RETURN WRITER " << i << endl;
    }
  
    return 0;
}