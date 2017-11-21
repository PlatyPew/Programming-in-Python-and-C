/*
Daryl Lim (P1625608)
Lim Chun Yu (P1625273)


author:Lim Chun Yu (P1625273)

basic logic flow
- open file
- read in line by line
- strtok to separate each line
- check lines that are needed(likes,gender,age)
- add accordingly according to gender
- adjust max and min accordingly if a bigger/smaller number appears
- calculate accordingly
	- total=add likes continuously
	- avg=addlikes and divide by total valid entries
	- add each median in order (already arranged.)
- calculate median by storing only unique likes and the amount of each unique like(prevent running out of memory)
	- find "middle mark" of valid entries for each gender
	- add amount of each likes until it reaches the mid mark
	- if the number is between 2 unique numbers, it calculates the average.
- printout results
- end
*/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

typedef struct node
{
int data;//unique number of likes
int quan;//quatity for each like
 struct node*next;//next pointer
}node;
typedef node fNode;//female struct

void add(node**s,int num)//adding in ascending order
{
node*temp;
	if(*s==NULL||num<(*s)->data)//check if node is null(first number/start) or if the new number is lesser than the front node
	{
		temp=(node*)malloc(sizeof(node));//allocate new space for new node
		temp->data=num;
		temp->quan=1;//set number of unique number to 1
		temp->next=*s;//next
		*s=temp;
	}
	else
	{
		temp=*s;
		while(temp!=NULL)//while it is not last
		{
			if(temp->data==num)//if like is not unique, add one for the quantity of likes
			{
				temp->quan=temp->quan+1;
				return;
			}else{
				if(temp->data<=num&&(temp->next==NULL || temp->next->data>num))//if like is the current biggest number.
				{
				node*temp1=(node*)malloc(sizeof(node));//creates new node to accomodate for new unique value
				temp1->data=num;
				temp1->quan=1;//set quantity as one as this is the first of its kind
				temp1->next=temp->next;
				temp->next=temp1;
				return;
				}
			}
			temp=temp->next;//moves to next
		}
	}
}

void printresult(int totalppl,int max,int min,int totallikes,float median){//prints out results
	printf("Valid entries count :\t\t%d\n",totalppl);
	printf("Highest likes received count :\t%d\n",max);
	printf("Lowest likes received count :\t%d\n",min);
	printf("Likes received count total :\t%d\n",totallikes);
	printf("Likes received count average :\t%.2f\n",(float)totallikes/totalppl);
	printf("Likes received count median :\t%.2f\n",median);
}
int half(int totalppl){//finds the middle number for total users
	if(totalppl%2==1){//if total ppl is odd
		return ((totalppl/2)+1);
	}else{//even
		return(totalppl/2);
	}
}
int traverses(node*s,int total)//adds first few quantity until it is more than the half mark for total ppl for each gender.
{
	node*prv=NULL;
	int liked=0;
	while(s!=NULL&&liked<half(total))//list through linked list
	{
		liked+=s->quan;//adds each value
		if(liked==half(total)){//if equal, find mean
			return(float)(s->data+prv->data)/2;
		}
		prv=s;
		s=s->next;//moves to next
	}
	return prv->data;
}
int main(){
	node*n=NULL;//male likes linked list
	fNode*fn=NULL;//female likes linked list
	const char tab[2]="\t";//tab for strtok
	FILE *stream;
	char *line = NULL;
	size_t len = 0;
	ssize_t read;
 	int i=1;
	int age=0;//for checking age
	//males	
	int max=0;//max for males
	int min=2000;//min for males
	int totallikes=0;//total male likes
	int totalppl=0;//total applicable male
	//female
	int fmax =0;//max for female
	int fmin =2000;//min for female
	int ftotallikes =0;//total likes for female
	int ftotalppl=0;//total appplicable female
	char *strtokfind;
	stream = fopen("pseudo_facebook.tsv", "r");
	if (stream == NULL)
		exit(EXIT_FAILURE);
	while ((read = getline(&line, &len, stream)) != -1) {
		i=1;
		strtokfind = strtok(line,tab);
		int likes;
		int check=0;
		while(strtokfind!=NULL&&i<=15){
			switch(i){
				case 2:
					age=atoi(strtokfind);//check that age is between 13 and 90
					if(age>=13&&age<=90)
						check+=1;
				break;
				case 6:
					if(strcmp(strtokfind,"female")==0)//check that gender is female or male
						check+=1;
					else if(strcmp(strtokfind,"male")==0)
						check+=4;//makes sure this will provide a number that will show it is correct
					
				break;
				case 11:
					likes=atoi(strtokfind);//check that likes is more than 0 and an integer
					if(likes>0)
						check+=1;
				break;
				default:
				break;
			}
		strtokfind = strtok(NULL, tab);
		i++;
		}
		if(check==3){//female - check through calculation
			ftotalppl+=1;
			fmax=(fmax>likes)?fmax:likes;//checks if it is the biggest number
			fmin=(fmin<likes)?fmin:likes;//checks if it is the smallest 
			ftotallikes+=likes;
			add(&fn,likes);
		}else if(check==6){//male - check through calculation
			totalppl+=1;
			max=(max>likes)?max:likes;//checks if it is the biggest number
			min=(min<likes)?min:likes;//checks if it is the smallest 
			totallikes+=likes;
			add(&n,likes);
		}
		
	}
float median=traverses(n,totalppl);//finds the mid of the total numbers
float fmedian=traverses(fn,ftotalppl);
printf("Statistic Summary\n");
printf("Male Users\n");
printresult(totalppl,max,min,totallikes,median);//prints results in format
printf("\nFemale Users\n");
printresult(ftotalppl,fmax,fmin,ftotallikes,fmedian);//prints results in format
fclose(stream);
exit(EXIT_SUCCESS);
}



