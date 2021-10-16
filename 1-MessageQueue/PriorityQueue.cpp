//#include <iostream>
//#include <bits/stdc++.h>
#include <cstring>
#include "PriorityQueue.h"

// Constructor Base
QueueInterface::QueueInterface(int maxMessages,float lowThreshold,float highThreshold)
{
    this->maxMessages = maxMessages;
    this->lowThreshold = maxMessages * lowThreshold;
    this->highThreshold = maxMessages * highThreshold;
}

// Constructor Derived
PriorityQueue::PriorityQueue(int maxMessages,float lowThreshold,float highThreshold)
    : QueueInterface(maxMessages,lowThreshold,highThreshold)
{
    if (pthread_mutex_init(&lock_, NULL) != 0) {
        // Raise exception
    }
}

// Destructor
PriorityQueue::~PriorityQueue()
{
    pthread_mutex_lock(&lock_);
    while(queue_.size() > 0){
        MESSAGE_TYPE* message = queue_.back().message;
        queue_.pop_back();
        delete[] message;
    }
    pthread_mutex_unlock(&lock_);

    pthread_mutex_destroy(&lock_);
}

// Insert a new element
//  Return true if successfull enqueue
bool PriorityQueue::enqueue(MESSAGE_TYPE *message, int priority)
{
    Item newItem;
    newItem.message = new MESSAGE_TYPE[MESSAGE_SIZE];
    memcpy(newItem.message,message,MESSAGE_SIZE*sizeof(MESSAGE_TYPE));
    newItem.priority = priority;
    int size;
    bool success = false;

    pthread_mutex_lock(&lock_);
    size = queue_.size();
    if (size < maxMessages)
    {
        if (size == 0){
            // Add as a first element
            queue_.emplace_front(newItem);
        } else {
            if (priority > queue_.back().priority){
                queue_.insert(queue_.end(),newItem);
            } else {
                list<Item>::iterator q = queue_.begin();
                for (; q != queue_.end(); q++){ 
                    if (priority <= q->priority) {
                        queue_.insert(q,newItem);
                        break;
                    }
                    advance(q,1);
                }
            }
        }
        if (size+1 >= highThreshold) {
            callFullCB();
        }
        success = true;
    }
    pthread_mutex_unlock(&lock_);


    return success;
}

  
// Pop highest priority
//  Returns false in queue was empty
bool PriorityQueue::dequeue(MESSAGE_TYPE *dest)
{
    bool success = false;
    MESSAGE_TYPE* message;
    int size;
    pthread_mutex_lock(&lock_);
    size = queue_.size();
    if (size > 0)
    {
        MESSAGE_TYPE* message = queue_.back().message;
        memcpy(dest,message,MESSAGE_SIZE*sizeof(MESSAGE_TYPE));
delete[] message;
        queue_.pop_back();
        success = true;

        if (size-1 <= lowThreshold) {
            callEmptyCB();
        }
    }
    pthread_mutex_unlock(&lock_);

    return success;
}


void PriorityQueue::callEmptyCB()
{
    cout << "EVENT: below empty threshold. Queue Size:" << queue_.size() << endl;
    for(auto &i : emptyCBs)
    {
        i.cb(i.obj);
    }
}

void PriorityQueue::callFullCB()
{
    cout << "EVENT: above full threshold. Queue Size:" << queue_.size() << endl;
    for(auto &i : fullCBs)
    {
        i.cb(i.obj);
    }
}
void PriorityQueue::connectFullCB(void (*cb)(void *),void* obj)
{
    cbtd n;
    n.cb = cb;
    n.obj = obj;
    fullCBs.emplace_front(n);
}

void PriorityQueue::connectEmptyCB(void (*cb)(void *),void* obj)
{
    cbtd n;
    n.cb = cb;
    n.obj = obj;
    emptyCBs.emplace_front(n);
}