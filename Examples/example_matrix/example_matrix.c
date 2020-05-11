// Example with matrix multiplication
// Taken from: https://www.programiz.com/cpp-programming/examples/matrix-multiplication
// Matrix mult is the result of multiplying a * b
for(i = 0; i < r1; i++)
    for(j = 0; j < c2; j++)
        for(k = 0; k < c1; k++)
        {
            mult[i][j] += a[i][k] * b[k][j];
        }