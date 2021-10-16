#ifndef QUEUEUSERTHREAD_H
#define QUEUEUSERTHREAD_H

#include <pthread.h>
#include "PriorityQueue.h"

#define MAX_RAND_DELAY_MS 200
#define MAX_PRIORITY 200

using namespace std;

// Base Class
class QueueUserThread
{
    bool isReader;
    int executions;
    string tName;
    pthread_t thread_;
    PriorityQueue *queue;
    bool stop_;
    void *threadLoop();
    static void *threadLoopHelper(void *arg);
public:
    pthread_mutex_t lock_;
    QueueUserThread(string tName, PriorityQueue *queue,const int executions,bool isReader);
    ~QueueUserThread();
    void start();
    static void pause(void*);
    static void resume(void*);
    void join();
};


#endif