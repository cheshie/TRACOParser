  for (i=0; i<NMAX; i++) 
  {
    for (j=0; j<NMAX; j++) 
    {
      for (k=0; k<j-1; k++) 
      {
        c[i][k] += a[j][k] * b[i][j];
        c[i][j] += a[j][j] * b[i][j];
      }
      c[i][j] += a[j][j] * b[i][j];
    }
  }
