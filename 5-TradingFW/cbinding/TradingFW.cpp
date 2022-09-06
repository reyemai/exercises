#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <new>
#include "TradingFW.hpp"
#include <string.h>

using namespace std;

int TradingFW::get(){return this->a;}
void TradingFW::set(int a){this->a = a;}


TradingFW::TradingFW(){
    data.clear();
}

char* TradingFW::get_value(char * dest,int c, int r){
    strcpy(dest,data[c][r].c_str());
    return dest;
}

int TradingFW::cols(){return data[0].size();}
int TradingFW::rows(){return data.size();}


void TradingFW::add_value(int row, int col, char * value){
    if (col > data[0].size()-1){
        for(int i=0;i<data.size();i++){
            data[i].push_back("");
        }
    }
    data[row][col] = value;
}

char* TradingFW::get_csv_name(char * dest){
    strcpy(dest,csv_name.c_str());
    return dest;
}

void TradingFW::read_csv(char* file_name,int max_lines) {
    csv_name = file_name;
    fstream fin(file_name);

    string line, word, temp;
    int i = 0;
    while (fin >> line) {
        if((max_lines != 0) && (i == max_lines+1))
            break;

        vector<string> row;

        // used for breaking words
        istringstream s(line);

        while (std::getline(s, word, ',')) {
            row.push_back(word);
        }

        data.push_back(row);
        i++;
    }
}


extern "C"
{
    void * NewTradingFW( void ){return new(std::nothrow) TradingFW;}
    void DeleteTradingFW (void *ptr){delete(reinterpret_cast<TradingFW *>(ptr));}

    int get(void *ptr){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        return ref->get();
    }

    void set(void *ptr,int a){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        return ref->set(a);
    }

    void read_csv(void *ptr, char* file_name,int max_lines){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        ref->read_csv(file_name,max_lines);
    }

    char* get_value(void *ptr,char * dest,int c, int r){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        return ref->get_value(dest,c,r);
    }

    char* get_csv_name(void *ptr,char * dest){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        return ref->get_csv_name(dest);
    }

    int cols(void *ptr){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        return ref->cols();
    }

    int rows(void *ptr){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        return ref->rows();
    }

    void add_value(void *ptr,int row, int col, char * value){
        TradingFW * ref = reinterpret_cast<TradingFW *>(ptr);
        return ref->add_value(row,col,value);
    }
}
