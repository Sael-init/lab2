#include <iostream>
#include<fstream>
#include<cstdio>
#include <map>
using namespace std;

struct Record
{
    char nombre[30];
    char carrera[20];
    int ciclo;

    void setData() {
        cout << "Alumno:";
        cin >> nombre;
        cout << "Carrera: ";
        cin >> carrera;
        cout << "Ciclo: ";
        cin >> ciclo;
    }

    void showData() {
        cout << "\nNombre: " << nombre;
        cout << "\nCarrera: " << carrera;
        cout << "\nCiclo : " << ciclo;
    }

    string getKey(){
        return nombre;
    }
    
};

class RandomFile {
private:
    string fileName;
    string indexName;
    //map: mantiene ordenado las entradas
    map<string, long> index;

public:
    RandomFile(string _fileName) {
        this->fileName = _fileName + ".dat";
        this->indexName = _fileName + "_ind"+".dat";
        readIndex();
    }

    ~RandomFile(){
        
        writeIndex();
    }
 //
 //   /*
 //   * leer el indice desde disco
 //   */
    void readIndex()
    {
        
        
        ifstream file;
        file.open(fileName, ios::binary);
         Record obj;
        while (file.read((char *) &obj, sizeof(obj))){
            int ubicacion = file.tellg();
            index.insert({obj.getKey(),ubicacion});
        }
        
        file.close();
    }
 //
 //   /*
 //   * Regresa el indice al disco
 //   */
        void writeIndex(){
            ofstream dataFile;
            
            dataFile.open(this->indexName, ios::app | ios::binary);
            for (auto i = index.begin(); i != index.end(); ++i) {
                dataFile.write((char*)&i->first, sizeof(i->first));
                dataFile.write((char*)&i->second, sizeof(i->second));   
            }
            
            
            dataFile.close();
       }
 //
 //   /*
 //   * Escribe el registro al final del archivo de datos. Se actualiza el indice.
 //   */
    void write_record(Record record) {
        ofstream dataFile;
        dataFile.open(this->fileName, ios::app | ios::binary);
        long posFisica = dataFile.tellp();
        dataFile.write((char*)&record, sizeof(Record));
        this->index[record.getKey()] = posFisica;
        dataFile.close();
    }
 //
 //
 //   /*
 //   * Busca un registro que coincida con la key
 //   */
    Record search(string key) {
        Record result;
        ifstream file;
        file.open(fileName, ios::binary);
         for (auto i = index.begin(); i != index.end(); ++i) {
                if(i->first == key){
                file.seekg(i->second);
                file.read((char*) &result, sizeof(Record));
                break;
                }
            }

        file.close();
       return result;
    }
 //
 //   /*
 //  * Muestra todos los registros de acuerdo como fueron insertados en el archivo de datos

    void scanAll() {
        ifstream file;
        file.open(fileName, ios::binary);
        
         Record obj;
        while (file.read((char *) &obj, sizeof(obj))){
            obj.showData();
            cout<<endl;
        }
        file.close();
    }    
    
 //
 //   /*
 //  * Muestra todos los registros de acuerdo a como estan ordenados en el indice
 //  */
    void scanAllByIndex() {
        ifstream file;
        
        
        Record obj;
        
        for (auto i = index.begin(); i != index.end(); ++i) {
            file.open(fileName, ios::binary);        
                
                file.seekg(i->second);
                file.read((char*) &obj, sizeof(Record));
                obj.showData(); 
                file.seekg(0, ios::beg);
            file.close();
            cout<<endl;
            }            
        
        

    }
 //
};