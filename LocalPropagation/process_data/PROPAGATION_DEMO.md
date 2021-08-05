# Propagation - explanation

- Fourier timeshifting:
```
exp(i*2*pi * (kx*dx + ky*dy + kz*dz - w*dt))
```

- Our study confines to `dx=0`, `dy=0`, `dz=z`. We also have `t = z`. Therefore:

```
exp(i*2*pi * (kz*dz - w*dz))
```

- Data scales are uniform: `w/k = 1`.
- Dispersion relation:

```
w = sqrt(kx**2 + ky**2 + kz**2)
kz**2 = w**2 - kx**2 - ky**2
```

- Therefore the timeshift argument becomes:

```
exp(i*2*pi * dz * (kz - w))
```

- However:

sqrt(w**2 - kx**2 - ky**2) - w ~= w(1 - ( 0.5*kx**2 -0.5*ky**2 )/w**2 - 1) --> -0.5(kx**2 + ky**2)/w  
 
--> exp(-i*pi * ((kx**2 + ky**2)/w )
