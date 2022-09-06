#include <vector>
#include <string>

using namespace std;

#ifdef _MSC_VER
    #define EXPORT_SYMBOL __declspec(dllexport)
#else
    #define EXPORT_SYMBOL
#endif

#ifdef __cplusplus
extern "C" {
#endif


// EXPORT_SYMBOL float cppmult(int int_param, float float_param);

class TradingFW
{
    vector<vector<string>> data;
    string csv_name;
    int a;
public:
    TradingFW();
    int get();
    char* get_csv_name(char * dest);
    void set(int);
    void read_csv(char* file_name,int max_lines);
    char* get_value(char * dest,int c, int r);
    int cols();
    int rows();
    void add_value(int row, int col, char * value);
};

#ifdef __cplusplus
}
#endif
