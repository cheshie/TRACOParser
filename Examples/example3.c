#pragma omp parallel for
    for(i=0; i<N; i++)
    {
        A[i][j] = 5;
        for(j=0; j<N; j++)
            A[i][j] = 8;
    }