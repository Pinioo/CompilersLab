# control flow instruction

k = 10;
N = 10;
M = 20;
for i = 1:10 {
    for j = i:50 {
        print i, j;
    }
}

while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;   
    else
        i = 3;
    
    k = k - 1;
    print(k);
}