#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//C:\Users\kumar\PythonProjects\GameofLife

#define P_0 0.3
#define BOARD_W 10000
#define BOARD_H 10000
#define TOROIDAL_ENV 1
#define THRESHOLD RAND_MAX * P_0
#define ROW_LEN (BOARD_W+TOROIDAL_ENV*2)
#define COL_LEN (BOARD_W+TOROIDAL_ENV*2)

void init_array();
void disp_array();
void iter_array();

unsigned short arr[2][COL_LEN][ROW_LEN];
unsigned short lut[10][2] = {{0,0},{0,0},{0,0},{1,1},{0,1},{0,0},{0,0},{0,0},{0,0},{0,0}};
char* line_break;
int required_frames = 100;

int main(){
	printf("Starting...\n");
	init_array();
	disp_array();
	clock_t start = clock();
	for(int i = 1; i <= required_frames; i++){
		iter_array();
	}
	clock_t end = clock();
	printf("Runtime : %fs\n", (double)(end - start)/CLOCKS_PER_SEC);
}

void init_array(){
	for(int i = 0; i < COL_LEN; i++){
		for(int j = 0; j < ROW_LEN; j++){
			arr[0][i][j] = (rand() > THRESHOLD)?0:1;
		}
	}
	int strlen_req = -1+2*BOARD_W;
	line_break = malloc(strlen_req*sizeof(char));
	line_break[strlen_req] = '\0';
	for(int i = 0; i < strlen_req; i++){
		line_break[i] = '-';
	}
}

void disp_array(){
	for(int i = 1; i < COL_LEN-1; i++){
		for(int j = 1; j < ROW_LEN-1; j++){
			printf("%d ", arr[0][i][j]);
		}
		printf("\n");
	}
	printf("%s\n", line_break);
}

void wrap_array(){
	//Try wrapping with pointers?
	//Think possible to just wrap once then
	for(int i = 0; i < COL_LEN; i++){
		arr[0][i][0] = arr[0][i][ROW_LEN-2];
		arr[0][i][ROW_LEN-1] = arr[0][i][1];
	}
	for(int j = 0; j < ROW_LEN; j++){
		arr[0][0][j] = arr[0][COL_LEN-2][j];
		arr[0][COL_LEN-1][j] = arr[0][1][j];
	}
}

void iter_array(){
	wrap_array();
	for(int i = 0; i < COL_LEN; i++){
		for(int j = 1; j < ROW_LEN-1; j++){
			arr[1][i][j] = arr[0][i][j-1] + arr[0][i][j] + arr[0][i][j+1];
		}
	}
	for(int i = 1; i < COL_LEN-1; i++){
		for(int j = 1; j < ROW_LEN-1; j++){
			arr[0][i][j] = lut[arr[1][i-1][j] + arr[1][i][j] + arr[1][i+1][j]][arr[0][i][j]];
		}
	}
}