//#include <iostream>
//#include <bits/stdc++.h>
#include <pthread.h>
#include <unistd.h>
#include <cstring>
#include <stdlib.h>
#include "QueueUserThread.h"

QueueUserThread::QueueUserThread(string tName, PriorityQueue *queue, const int executions,bool isReader)
{
    this->tName = tName;
    this->queue = queue;
    this->executions = executions;
    this->isReader = isReader;
    this->stop_ = false;

    if(!isReader)
    {
        // Writer
        queue->connectFullCB(pause,this);
        queue->connectEmptyCB(resume,this);
    }
}

void QueueUserThread::start()
{
    int error = pthread_create(&thread_,NULL,&this->threadLoopHelper, this);
    if (error != 0)
    {
        // TODO: Raise Exception
        //printf("\nThread can't be created :[%s]",strerror(error));
    }
}

QueueUserThread::~QueueUserThread()
{
    pthread_mutex_destroy(&lock_);
}

void QueueUserThread::pause(void* _this)
{
    QueueUserThread* t = (QueueUserThread*) _this;
    pthread_mutex_lock(&(t->lock_));
    t->stop_ = true;
    pthread_mutex_unlock(&(t->lock_));
}

void QueueUserThread::resume(void* _this)
{
    QueueUserThread* t = (QueueUserThread*) _this;
    pthread_mutex_lock(&(t->lock_));
    t->stop_ = false;
    pthread_mutex_unlock(&(t->lock_));
}

void QueueUserThread::join()
{
    int res = pthread_join(thread_, NULL);
    if (res != 0)
    {
        //TODO raise exception
        // (avoided in order to be called multiple times)
    }
}

void* QueueUserThread::threadLoopHelper(void *_this)
{
    QueueUserThread* t = (QueueUserThread*) _this;
    return t->threadLoop();
}


void* QueueUserThread::threadLoop()
{
    bool _stop;
    bool readStatus;
    bool writeStatus;
    unsigned int _waitms;
    int priority;
    MESSAGE_TYPE message[MESSAGE_SIZE];
    string s;
    int i = 0;

    while(i<executions)
    {
        pthread_mutex_lock(&lock_);
        _stop = this->stop_;
        pthread_mutex_unlock(&lock_);

        _waitms = rand() % MAX_RAND_DELAY_MS;
        usleep(_waitms);

        if (!_stop)
        {
            if(isReader)
            {
                // READER
                readStatus = queue->dequeue(message);
                if (readStatus)
                {
                    cout << "READ  < " << tName << " received: '"<< message << "'" << endl;
                }
                i++;
            } else
            {
                // WRITER
                priority = rand() % MAX_PRIORITY;
                s = "Thread " + tName + " sending with priority: " + to_string(priority);
                s = s.substr(0,MESSAGE_SIZE-1);
                memcpy(message,s.data(),s.length());
                message[s.length()] = 0;
                writeStatus = queue->enqueue(message,priority);
                if (writeStatus){
                    cout << "WRITE > " << tName << " sent:     '"<< message << "'" << endl;
                }
                i++;
            }
        }
    }

    return 0;
}