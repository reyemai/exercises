#ifndef PRIOQ_H
#define PRIOQ_H

#include <pthread.h>
#include <list>
#include <iostream>
#include <random>

#ifndef MESSAGE_SIZE
#define MESSAGE_SIZE 512
#endif

#define MESSAGE_TYPE unsigned char

using namespace std;

// Base Interface Class
class QueueInterface
{
protected:
    typedef struct Item {
        MESSAGE_TYPE *message;
        int priority;
    } Item;
    int maxMessages;
    int lowThreshold;
    int highThreshold;
public:
    QueueInterface(int maxMessages,float lowThreshold,float highThreshold);
    virtual bool enqueue(MESSAGE_TYPE *message, int priority) = 0;
    virtual bool dequeue(MESSAGE_TYPE* dest) = 0;
    virtual void connectFullCB(void (*cb)(void *),void* obj) = 0;
    virtual void connectEmptyCB(void (*cb)(void *),void* obj) = 0;
};

// Derived Class
class PriorityQueue: public QueueInterface
{
    typedef struct cbtd {
        void (*cb)(void*);
        void* obj;
    } cbtd;
    list<Item> queue_;
    pthread_mutex_t lock_;
    list<cbtd> fullCBs;
    list<cbtd> emptyCBs;
    void callEmptyCB();
    void callFullCB();
public:
    PriorityQueue(int maxMessages,float lowThreshold,float highThreshold);
    ~PriorityQueue();
    bool enqueue(MESSAGE_TYPE *message, int priority);
    bool dequeue(MESSAGE_TYPE* dest);
    void connectFullCB(void (*cb)(void *),void* obj);
    void connectEmptyCB(void (*cb)(void *),void* obj);
};

#endif