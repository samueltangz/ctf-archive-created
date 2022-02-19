#include <stdio.h>
#define n 1000000007

int _add(int a, int b) {
    int c = 0;
    for (int i = 0; i < a; i++) c += 1;
    for (int i = 0; i < b; i++) c += 1;

    return c;
}

int _sub(int a, int b) {    
    int c = 0;
    for (int i = 0; i < a; i++) c += 1;
    for (int i = 0; i < b; i++) c -= 1;
    
    return c;
}

int add(int a, int b) {
    int c = _add(a, b);
    if (c >= n) c = _sub(c, n);
    return c;
}

int mul(int a, int b) {
    int c = 0;
    for (int i = 0; i < b; i++) {
        c = add(c, a);
    }
    return c;
}

int pow(int a, int b) {
    int c = 1;
    for (int i = 0; i < b; i++) {
        c = mul(c, a);
    }
    return c;
}

int evaluate(int *polynomial, int degree, int x) {
    int c = 0;
    for (int i = 0; i < degree; i++) {
        c = add(c, mul(polynomial[i], pow(x, i)));
    }
    return c;
}

int main() {
    int polynomial[] = {77, 543680933, 779305823, 406010255, 852593453, 670940274, 400957584, 848777990, 534939184, 328847351, 616300066, 359055106, 161410101, 171509744, 155648929, 916365238, 18733844, 380452845, 509377978, 800691109, 908467961, 104753231, 181241660, 273070766, 93557074, 561221533, 449550761, 188262493, 915004277, 426375697, 665693795, 107906776, 665848870, 211169645, 53616008, 489964557, 908019215, 786707135, 573479073, 905263359, 938064888, 780724541, 361367421, 636367390, 816611492, 238098701, 596575814, 426971134, 943814120, 365926771, 929927764, 885597612, 895263918, 678662340, 387318491, 644785517, 566974198, 229009720, 874699826, 637234082, 673340960, 577186089, 903058253, 424604291, 663043221};
    int degree = sizeof polynomial / sizeof *polynomial;

    for (int x = 0; x < degree; x++) {
        printf("%c", evaluate(polynomial, degree, x));
        fflush(stdout);
    }
    return 0;
}

// gcc -s chall.c -o chall
// "-s" is used to strip the symbols