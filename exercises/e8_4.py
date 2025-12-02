import taichi as ti
import taichi.math as tm

import numpy as np
import matplotlib.pyplot as plt

ti.init(ti.cpu, default_fp=ti.f64, default_ip=ti.i64)

# dekorator data_oriented nam umozni definovat pole a kernely
# uvnitr tridy
@ti.data_oriented
class Mandelbrot:
    def __init__(self, N):
        self.m = ti.field(dtype=ti.i64, shape=(N, N))

    # taichi funkce, kterou je mozno volat jedine z taichi kernelu
    @ti.func
    def conv(self, c_re: ti.f64, c_im: ti.f64, k_max: ti.i64 = 200) -> ti.i64:
        # nemame complexni cisla jak ve standardnim Pythonu
        # manipulaci s komplexnimi cislami musime udelat rucne
        z_re = 0.0
        z_im = 0.0
        kret = ti.i64(-1) # tohle budeme vracet
        # defaultne vnejsi smycky bezi paralelne
        # timhle nasledujici smycku serialuzjeme
        ti.loop_config(serialize=True)
        for k in range(k_max):
            tmp = z_re 
            z_re = z_re*z_re - z_im*z_im + c_re
            z_im = 2*tmp*z_im + c_im
            # smycku musime serializovat, protoze vypocet z
            # zavisi od predchozich iteraci a v paralelni smycke
            # nemuzeme pouzit break
            if z_re**2 + z_im**2 > 4:
                break
            kret += 1
        return kret

    #jen pro default hodnoty rozsahu
    #kernely nepodporuju defaultne hodnoty
    def spocti(self, xmin=-2, xmax=1, ymin=-1, ymax=1):
        self.extent = [xmin, xmax, ymin, ymax]
        self._spocti(xmin, xmax, ymin, ymax)

    # samotni kernel, ktery mnozinu spocita
    @ti.kernel
    def _spocti(self, xmin: ti.f64, xmax: ti.f64, ymin: ti.f64, ymax: ti.f64):
        # vnejsi smycka bezi paralelne
        Dx = xmax - xmin
        Dy = ymax - ymin
        for i, j in self.m:
            c_re = float(j)/N*Dx + xmin
            c_im = float(i)/N*Dy + ymin
            self.m[i,j] = self.conv(c_re, c_im, 100)

    
N = 2000
M = Mandelbrot(N)
# cela mnozina
# M.spocti()
# pekny kousek
M.spocti(-0.435, -0.4, 0.585, 0.615)

fig, ax = plt.subplots()
# to_numpy() nam premeni ti.field na standardni numpy pole
ax.imshow(M.m.to_numpy(), extent=M.extent, origin='lower')
plt.show()