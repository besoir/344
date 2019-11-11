#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct item {
	char *name;
	int quantity;
	int empty;
} tempItem;

void createItem() {
	tempItem.name = malloc(sizeof(char) * 70);
	fprintf(stdout, "%s", "Enter a name:\n");
	fgets(tempItem.name, 70, stdin);
	fprintf(stdout, "%s", "Enter the quantity:\n");
	scanf("%d", &tempItem.quantity);
	fseek(stdin,0,SEEK_END);
}

void printList(struct item **listOfItems, int numColumn, int numRow) {
	for(int x = 0; x < numRow; x++) {
		for(int y = 0; y < numColumn; y++) {
			if(listOfItems[x][y].empty == 0)
				printf("Item Name: %sQuantity: %d\n", listOfItems[x][y].name, listOfItems[x][y].quantity);
		}
	}
}

void clearList(struct item **listOfItems, int numColumn, int numRow) {
	for(int x = 0; x < numRow; x++) {
		for(int y = 0; y < numColumn; y++) {
			if(listOfItems[x][y].empty == 0) {
				free(listOfItems[x][y].name); 
				listOfItems[x][y].quantity = 0;
				listOfItems[x][y].empty = 1;
				listOfItems[x][y].name = malloc(70 * sizeof(char));
			}
		}
	}
}


int main(void) {
	MAXCHARACTERS = 500;
	str[MAXCHARACTERS];
	File *f;
	


	fprintf(stdout, "%s", "Enter the number of columns:\n");
	int numColumn;
	scanf("%d", &numColumn);
	fseek(stdin,0,SEEK_END);
	fprintf(stdout, "%s", "Enter the number of rows:\n");
	int numRow;
	scanf("%d", &numRow);
	fseek(stdin,0,SEEK_END);

	struct item **listOfItems = malloc(numRow * sizeof(struct item));
	for(int i = 0; i < numRow; i++) {
		listOfItems[i] = malloc(numColumn * sizeof(struct item));
		for(int j = 0; j < numColumn; j++) {
			listOfItems[i][j].name = malloc(70 * sizeof(char));
			listOfItems[i][j].empty = 1;
		}
	}

	char cmd[60];
	const char del[1] = "\0";
	char *token;
	printf("%s", "Enter add, print, clear, or quit:\n");
	scanf("%s", cmd);
	token = strtok(cmd, del);
	fseek(stdin,0,SEEK_END);
	
	while(strcmp(token, "quit") != 0) {
		if(strcmp(token, "add") == 0) {
			fprintf(stdout, "%s", "Enter the column position of the item:\n");
			int tempColumn;
			scanf("%d", &tempColumn);
			fseek(stdin,0,SEEK_END);
			fprintf(stdout, "%s", "Enter the row position of the item:\n");
			int tempRow;
			scanf("%d", &tempRow);
			fseek(stdin,0,SEEK_END);
			createItem();
			strcpy(listOfItems[tempRow][tempColumn].name, tempItem.name);
			listOfItems[tempRow][tempColumn].quantity = tempItem.quantity;
			listOfItems[tempRow][tempColumn].empty = 0;
		}

		if(strcmp(token, "print") == 0) {
			printList(listOfItems, numColumn, numRow);
		}
		if(strcmp(token, "clear") == 0) {
			clearList(listOfItems, numColumn, numRow);
		}
		printf("%s", "Enter add, print, clear, or quit:\n");
		scanf("%s", cmd);
		token = strtok(cmd, del);
		fseek(stdin,0,SEEK_END);
	}
}