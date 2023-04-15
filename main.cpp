#include "RandomFile.h"
#include <iostream>
using namespace std;

void writeFile(string filename){
    RandomFile file(filename);
    Record record;
    for (int i = 0; i < 2; i++)
    {
        record.setData();
        file.write_record(record);
    }
}

void readFile(string filename){
    RandomFile file(filename);
    cout<<"--------- show all data -----------\n";
    file.scanAll();
    cout<<"--------- show all sorted data -----------\n";
    file.scanAllByIndex();
}

int main(){
    writeFile("/home/salvador/Documents/BD II/lab2/datos1");

    readFile("datos1");
    RandomFile RF("datos1");
    cout<<"--------- show data search -----------\n";
    RF.search("salvadorgit").showData();
    cout<<endl;
    return 0;
}