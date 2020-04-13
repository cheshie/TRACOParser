#pragma omp parallel for
    for(i=0; i<N; i++)
        for(j=0; j<N; j++)
            A[i][j] = 8;

