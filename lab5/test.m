## UNKNOWN_TERM with MATRIX ##
a = [
    [1, 2, 3],
    [4, 5, 6]
];

b = a[1, 5];
c = b[1, 2, 3];
d = c;

e = a[1+2, 3+4];
f = e;
g = e + e;

## UNKNOWN_TERM with ARRAY ##
a = [1, 2, 3, 4, 5];

b = a[10 / 2];
c = b[2];
d = b + [100];
d = b + 100;
print d;

## UNKNOWN_ARRAY ##
a = [1, 2, 3, 4, 5];

b = a[1+2 : 3+4];
c = b[10:100];
d = b[5 * 2];
e2 = b + d;
return e2;

## RANGE
a = [1, 2, 3, 4, 5];
b = a[1:4];
c = b[2];
d = b[100:1000];
e = a[2.2:4.5];