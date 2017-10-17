PRO read_fft, dnum,run,snapnum, fft_re, fft_im

; run = '0_0_0'
; dnum = 1, 2, etc.

snapstr = string(snapnum,format='(i03)')
base='/datascope/indra'+strn(dnum)+'/'+run

L=128L
PMGRID=640L
Lhalf=L/2

;fft_re  & fft_im  = [ z,x,y]
; x=[-L/2:L/2]  y =[-L/2,L/2]  z=[0:L/2]
;

fft_re=fltarr(Lhalf+1,L+1,L+1)
fft_im=fltarr(Lhalf+1,L+1,L+1)


fstr=base+'/FFT_DATA/FFT_128_'+snapstr+'.dat'
openr,1,fstr
time2=0.d0
readu,1,time2
readu,1,nsize
print,'time2:  ', time2
readu,1,fft_re
readu,1,fft_im
close,1



end
