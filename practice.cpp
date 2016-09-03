#include <iostream>
#include <stdio.h>

using namespace std;

class Parent{
public:
	Parent(){
		cout << "call parent constructor" << endl;
	}
	virtual ~Parent(){
		cout << "call parent destructor" << endl;
	}
	void func(void){
		cout << "this is a base-class method." << endl;
	}

};

class Child : public Parent{
public:
	Child(){
		cout << "call child constructor" << endl;
	}
	~Child(){
		cout << "call child destructor" << endl;
	}
	//orverride method
	void func(void){
		cout << "this is a derrived-class method." << endl;
	}
};


int main(int argc, char** argv)
{
	Child* chi = new Child();
	delete chi;
	Parent* par = new Child();
	delete par;

	printf("num of args = %d\n",argc);
	for(int i=0;i<argc;i++){
		printf("args of %d = %s\n",i,argv[i]);
	}
  	return 0;

}