/*
Daryl Lim (1625608) (DISM/FT/2B/22)
Lim Chun Yu (1625273) (DISM/FT/2B/22)

Author: Daryl Lim

How to compile:
Normal mode: cc myencode.c -o myencode
Debug mode: cc -D DEBUG myencode.c -o myencode

Updates:
Decoding requires file to be read 3 times. No longer requires to.
Once to check if number of characters excluding break lines is even.
Once to check if characters are from [0-9A-F] by using a for loop.
Once to actually decode.
Solved by running once, decoding and placing in variable and validating. If file is not valid, it won't print to file.
Checks for any non-printable characters.

Bugs:
Stress test by decoding a 8MB file.
Theorectical time of completion is 32 times longer than encoding, however, it took longer.
Possible problems, using strcat and storing about 4MB of data in a variable.
Possible fixes, Using malloc to allocate more memory.

Debug mode:
Prints out in status of program

Logic flow of program
main:
	if exactly 3 arguments are supplied:
		if file exists:
			if file is empty:
				print file is empty
		else:
			print file does not exist
		if argv[1] is -e:
			check if file extension is .txt
			encode file by converting character to hex and swapping positions
			write to file as filename.txt.xeh
		elif argv[1] is -d:
			check if file extension is .xeh
			if file content contains invalid characters, file content contains odd number of characters and decoded into readable characters:
				print invalid content
			else:
				decode file by swapping positions of hex and converting them to characters
				write to file as filename.txt
		else:
			print usage
	else:
		print usage
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <regex.h>

// Define debug colours
#define BLUE "\x1B[96m"
#define RED "\x1B[91m"
#define GREEN "\x1B[92m"
#define YELLOW "\x1B[93m"
#define END "\x1B[0m"

// Declare functions
void usage();
void invalidExt();
void invalidCont();
void empty();
void notExist();
void fileExt();
int regSearch();
long length();
void encode();
void decode();

// Print usage
void usage() {
	#ifdef DEBUG
		printf(RED "Fail!\n" END);
	#endif
	printf(BLUE "Usage:\n");
	printf("myencode <-e | -d> <textfile>\n\n");
	printf("myencode\t:\tCommand name\n");
	printf("-e\t\t:\tOption to encode\n");
	printf("-d\t\t:\tOption to decode\n");
	printf("textfile\t:\tThe name of the text file to be encoded or decoded\n" END);
	#ifdef DEBUG
		printf(RED "Program aborted!\n" END);
	#endif
	exit(0);
}

// Prints invalid file extension
void invalidExt(char filename[], char function[]) {
	#ifdef DEBUG
		printf(RED "Fail!\n" END);
	#endif
	printf(BLUE "Invalid file name '%s' for %s. Please try again.\n"END ,filename,function);
	#ifdef DEBUG
		printf(RED "Program aborted!\n" END);
	#endif
	exit(0);
}

// Prints invalid file content
void invalidCont(int type) {
	if (type) {
		printf(BLUE "Invalid file content, decoding is aborted.\n" END);
	} else {
		printf(BLUE "Invalid file content, encoding is aborted.\n" END);
	}
	#ifdef DEBUG
		printf(RED "Program aborted!\n" END);
	#endif
	exit(0);
}

// Prints empty input file content
void empty() {
	#ifdef DEBUG
		printf(RED "Fail!\n" END);
	#endif
	printf(BLUE "Input file is empty! Please try again.\n" END);
	#ifdef DEBUG
		printf(RED "Program aborted!\n" END);
	#endif
	exit(0);
}

// Prints input file does not exist
void notExist(char filename[]) {
	#ifdef DEBUG
		printf(RED "Fail!\n" END);
	#endif
	printf(BLUE "File '%s' does not exist! Please try again.\n" END ,filename);
	#ifdef DEBUG
		printf(RED "Program aborted!\n" END);
	#endif
	exit(0);
}

// Check if file extension is correct for encoding and decoding respectively
void fileExt(int type, char filename[]) {
	#ifdef DEBUG
		printf(YELLOW "File extension valid: " END);
	#endif
	char * extension = &filename[strlen(filename) - 4]; // Stores the file extension
	// Compares file extension for encoding and decoding respectively
	if (type) {
		if (strcmp(extension, ".txt") != 0) {
			char function[] = "encoding";
			invalidExt(filename, function);
		}
	} else {
		if (strcmp(extension, ".xeh") != 0) {
			char function[] = "decoding";
			invalidExt(filename, function);
		}
	}
	#ifdef DEBUG
		printf(GREEN "Pass!\n" END);
	#endif
}

// Regex search
// A regex routine in C from a web page.
int regSearch(const char *str) {
	const char * pattern = "[^A-F0-9\n]";
    regex_t re;
    int ret;
    if (regcomp(&re, pattern, REG_EXTENDED) != 0) {
        return 0;
    }
    ret = regexec(&re, str, (size_t) 0, NULL, 0);
    regfree(&re);
    if (ret == 0) {
        return 1;
    } else {
    	return 0;
    }
}

long length(char filename[]) {
	FILE * read = fopen(filename,"r"); // Opens file to read
	fseek(read,0,SEEK_END); // Goes to end of file
	long length = ftell(read); // Checks length of file including break lines
	fclose(read);
	return length;
}

// Check if character is printable or not
int readableChar(int decimal) {
	if ((decimal >= 32) && (decimal <= 126) || decimal == 0) {
		return 1;
	} else {
		return 0;
	}
}

// Encoding process
void encode(char filename[], long length) {
	#ifdef DEBUG
		int lines = 0;
		printf(YELLOW "Encoding file...\n" END);
	#endif
	int c;
	int decimal;
	FILE * read = fopen(filename,"r"); // Opens file to read
	char hex[3],swap[3];
	char buffer[length*2+1];
	strcpy(buffer,"");
	strcat(filename,".xeh"); // Adds .xeh to filename
	while ((c = fgetc(read)) != EOF) { // Gets characters as long as it's not end of file
		if (c != '\n') {
			sprintf(hex,"%02X",c); // Converts character into hex
			decimal = strtol(hex,NULL,16);
			if(!readableChar(decimal)) {
				#ifdef DEBUG
					printf(RED "Non-readable characters detected!\n" END);
				#endif
				fclose(read);
				invalidCont(0);
			}
			sprintf(swap,"%c%c",hex[1],hex[0]); // Swaps the first and second characters around
			strcat(buffer,swap);
		} else {
			#ifdef DEBUG
				lines++;
				if (lines % 1000 == 0) {
					printf(YELLOW "%d lines encoded.\n" END,lines);
				}
			#endif
			strcat(buffer,"\n");
		}
	}
	FILE * write = fopen(filename,"w"); // Creates new file to write to
	fprintf(write,"%s",buffer);
	// Close files
	fclose(write);
	fclose(read);
	#ifdef DEBUG
		printf(YELLOW "%d lines encoded.\n" END,lines);
		printf(GREEN "Done!\n" END);
	#endif
	printf(BLUE "Encoded file saved as '%s'\n" END,filename);
	#ifdef DEBUG
		printf(GREEN "Program ended with no problems\n" END);
	#endif
}

// Decoding process
void decode(char filename[], long length) {
	#ifdef DEBUG
		int lines = 0;
		printf(YELLOW "Decoding file...\n" END);
	#endif
	long size = length;
	char * text = malloc(size + 1);
	int n = 1;
	char * buffer = (char*)malloc((n+1) * sizeof(char)); // Allocates memory for one character
	strcpy(buffer,"");
	char hex[3], ascii[2];
	int decimal;
	FILE * read = fopen(filename,"r");
	fread(text,size,1,read);
	if (!regSearch(text)) {
		int count = 0;
		int i = 0;
		int char1, char2;
		while (count < size) {
			if (text[i] != '\n') {
				if (count % 2 == 0) {
					char1 = text[i];
				} else {
					char2 = text[i];
					sprintf(hex,"%c%c",char2,char1); // Swap characters
					decimal = strtol(hex,NULL,16);
					if(readableChar(decimal)) { // Check for printable characters
						sprintf(ascii, "%c", (char)decimal); // Conversion from hex to ascii
						strcat(buffer,ascii); // Concatenate characters
					} else {
						#ifdef DEBUG
							printf(RED "Non-readable characters detected!\n" END);
						#endif
						fclose(read);
						free(text);
						free(buffer);
						invalidCont(1);
					}
				}
				count++;
			} else {
				#ifdef DEBUG
					lines++;
					if (lines % 1000 == 0) {
						printf(YELLOW "%d lines decoded.\n" END,lines);
					}
				#endif
				strcat(buffer,"\n");
				length--;
			}
			i++;
			n++;
			buffer = (char*)realloc(buffer,n * sizeof(char)); // Allocates memory for n number of characters
		}
	} else {
		#ifdef DEBUG
			printf(RED "Invalid hex values\n" END);
		#endif
		fclose(read);
		free(text);
		free(buffer);
		invalidCont(1);
	}
	if (length % 2) {
		#ifdef DEBUG
			printf(RED "Odd number of characters found\n" END);
		#endif
		fclose(read);
		free(text);
		free(buffer);
		invalidCont(1);
	}
	char * ptr = filename;
	ptr[strlen(ptr)-4] = 0; // Removes last 4 characters of filename changing .txt.xeh to .txt
	FILE * write = fopen(filename,"w");
	fprintf(write,"%s",buffer); // Writes to file
	// Close files and free memory
	fclose(write);
	fclose(read);
	free(text);
	free(buffer);
	#ifdef DEBUG
		printf(YELLOW "%d lines decoded.\n" END,lines);
		printf(GREEN "Done!\n" END);
	#endif
	printf(BLUE "Decoded file saved as '%s'\n"END,filename);
	#ifdef DEBUG
		printf(GREEN "Program ended with no problems\n" END);
	#endif
}

int main(int argc, char * argv[]) {
	long charsInFile;
	// Validates arguments
	#ifdef DEBUG
		printf(GREEN "Debug mode\n" END);
		printf(YELLOW "Checking arguments: " END);
	#endif
	if (argc == 3) { // Exactly 3 arguments
		#ifdef DEBUG
			printf(GREEN "Pass!\n" END);
			printf(YELLOW "Checking if file exists: " END);
		#endif
		if (access(argv[2],F_OK) != -1) { // Checks if file exists
			#ifdef DEBUG
				printf(GREEN "Pass!\n" END);
				printf(YELLOW "Checking if file is not empty: " END);
			#endif
			if ((charsInFile = length(argv[2])) == 0) { // Checks if file is empty
				empty();
			}
			#ifdef DEBUG
				printf(GREEN "Pass!\n" END);
				printf(YELLOW "Characters in file: " GREEN "%ld.\n" YELLOW, charsInFile);
				printf("Function selected: " END);
			#endif
		} else {
			notExist(argv[2]);
		}
		if (strcmp(argv[1],"-e") == 0) { // Encoding selected
			#ifdef DEBUG
				printf(GREEN "Encoding.\n" END);
			#endif
			fileExt(1, argv[2]); // Check if file extension is .txt
			encode(argv[2],charsInFile);
		} else if (strcmp(argv[1],"-d") == 0) { // Decoding selected
			#ifdef DEBUG
				printf(GREEN "Decoding.\n" END);
			#endif
			fileExt(0, argv[2]); // Check if file extension is .xeh
			decode(argv[2],charsInFile);
		} else {
			usage();
		}
	} else {
		usage();
	}
	return 0;
}
