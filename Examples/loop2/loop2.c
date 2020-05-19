for(i=1; i<N; i++)
#pragma omp parallel for
 for(j=1; j<N; j++)
  for(k=1; k<N; k++)
   a[i][j] = a[i][j] + 2;