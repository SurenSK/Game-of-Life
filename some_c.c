#include <stdio.h>
#include <stdlib.h>

//C:\Users\kumar\PythonProjects\GameofLife

#define P_0 0.5
#define TOROIDAL_ENV 1
#define BOARD_WIDTH 5
#define BOARD_HEIGHT 5

#define ROW_LEN (BOARD_WIDTH+TOROIDAL_ENV*2)
#define COL_LEN (BOARD_WIDTH+TOROIDAL_ENV*2)
#define THRESHOLD RAND_MAX * P_0

void init_array();
void disp_array_full();
void disp_array(int);
void iter_array(int);

int arr[2][COL_LEN][ROW_LEN];

int main(){
	init_array();
	disp_array_full();
}

void init_array(){
	for(int i = 0; i < COL_LEN; i++){
		for(int j = 0; j < ROW_LEN; j++){
			arr[0][i][j] = (rand() > THRESHOLD)?0:1;
			arr[1][i][j] = (rand() > THRESHOLD)?0:1;
		}
	}
}

void disp_array_full(){
	for(int i = 0; i < COL_LEN; i++){
		for(int j = 0; j < ROW_LEN; j++){
			printf("%d %d ", arr[0][i][j], arr[1][i][j]);
		}
		printf("\n");
	}
}

void disp_array(int active_layer){
	for(int i = 1; i < COL_LEN-1; i++){
		for(int j = 1; j < ROW_LEN-1; j++){
			printf("%d ", arr[active_layer][i][j]);
		}
		printf("\n");
	}
}

void wrap_array(int src){
	for(int i = 0; i < COL_LEN; i++){
		arr[src][i][0] = arr[src][i][ROW_LEN-2];
		arr[src][i][ROW_LEN-1] = arr[src][i][1];
	}
	for(int j = 0; j < ROW_LEN; j++){
		arr[src][0][j] = arr[src][COL_LEN-2][j];
		arr[src][COL_LEN-1][j] = arr[src][1][j];
	}
}

void iter_array(int dst){
	int count;
	int src = dst==0?1:0;
	wrap_array(src);
	for(int i = 1; i < COL_LEN-1; i++){
		for(int j = 1; j < ROW_LEN-1; j++){
			count = arr[src][i-1][j-1]+arr[src][i-1][j]+arr[src][i-1][j+1]+
					arr[src][i+1][j-1]+arr[src][i+1][j]+arr[src][i+1][j+1]+
					arr[src][i][j-1]+arr[src][i][j+1];
			switch(count){
				case 2: arr[dst][i][j] = arr[src][i][j]; break;
				case 3: arr[dst][i][j] = 1; break;
				default: arr[dst][i][j] = 0; break;
			}
		}
	}
}