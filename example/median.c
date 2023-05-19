#include <stdio.h>
#include <stdlib.h>

double findMedianSortedArrays(int* nums1, int nums1Size, int* nums2,int nums2Size){
    int totallen = nums1Size+nums2Size;
    int i,index1,index2,now,prior,top1,top2,is10,is20;
    i=index1=index2=now=prior=top1=top2=is10=is20= 0;
    if (nums1Size == 0) {top1 = 1;is10 = 1;int nums1[2]={1000000,1000000};};
    if (nums2Size == 0) {top2 = 1;is20 = 1;int nums2[2]={1000000,1000000};};
    int count =totallen/2+1;
    for (i=0;i<count;i++){
        if (is10) {prior = now;
            now = nums2[index2];
            index2++;}
        else if (is20){
            prior = now;
            now = nums1[index1];
            index1++;
        }
        else if ((nums1[index1]<=nums2[index2] && top1==0)||top2 == 1){
            prior = now;
            now = nums1[index1];
            index1++;
            if (index1==nums1Size) {top1 = 1;index1--;};
        } else if ((nums1[index1]>=nums2[index2] && top2==0)||top1 == 1) {
            prior = now;
            now = nums2[index2];
            index2++;
            if (index2==nums2Size) {top2 = 1;index2--;};
        };
    };
    double ans;
    if (totallen % 2 == 0){
        ans = ((double)prior+(double)now)/2;
        return ans;
    } else {
        ans = now;
        return ans;
    };
}

int read_file(char *filename, int *numbers) {
    FILE *fp;
    int i = 0;

    fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Error opening file");
        return -1;
    }

    while (fscanf(fp, "%d", &numbers[i]) == 1) {
        i++;
    }

    fclose(fp);
    return i;
}



int main(){

    double r;

    int numbers1[100000];
    
    int numbers2[100000];
    

    read_file("input1.txt", numbers1);
    read_file("input2.txt", numbers2);


    r = findMedianSortedArrays(numbers1,100000,numbers2,100000);
    printf("result = %lf\n", r);
    return 0;
}