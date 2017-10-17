PRO read_indra_snap, dnum,run,snapnum, pos, id, vel=vel, nosort=nosort

  snapstr = string(snapnum,format='(i03)')
; run = '0_0_0'
; dnum = 1, 2, etc. or 0 for ICs

;  fstart = '/home/wangjie/data/test/snapdir_'+snapstr+'/snapshot_'+snapstr+'.'
;  numsnap = 32

;  fstart = '/home/wangjie/Indra/IC/0_0_1/indra_Gpc_ics_'+snapstr+'.'
;  fstart = '/home/wangjie/Indra/V2/DATA/0_0_0/snapdir_'+snapstr+'/snapshot_'$
;    +snapstr+'.'
;  numsnap = 128

  fstart = '/datascope/indra'+strn(dnum)+'/'+run+'/snapdir_'+snapstr+$
    '/snapshot_'+snapstr+'.'
  numsnap = 256

; Read first snapshot file:
  npart = lonarr(6)
  massarr = dblarr(6)
  time = 0.0D
  redshift = 50.0D
  bytesleft = 256-6*4 - 6*8 - 8 - 8
  la = intarr(bytesleft/2)
     
  openr,1,fstart+'0',/f77_unformatted
  readu,1,npart,massarr,time,redshift,la

  n = npart[1]                  ; dark matter only
  pos = fltarr(3,n)
  vel = fltarr(3,n)
  id = lon64arr(n)

  readu,1,pos
  readu,1,vel
  readu,1,id
  close,1

  print,'z = '+strn(redshift)
;stop

; Read the rest of the snapshot files:
  FOR i=1,numsnap-1 DO BEGIN

     npart = lonarr(6)
     massarr = dblarr(6)
     time = 0.0D
     redshift = 50.0D
     bytesleft = 256-6*4 - 6*8 - 8 - 8
     la = intarr(bytesleft/2)

     openr,1,fstart+strn(i),/f77_unformatted

     readu,1,npart,massarr,time,redshift,la

;     print,npart,massarr,redshift
;     print,total(npart)

     n = npart[1] ; dark matter only
     thispos = fltarr(3,n)
     thisvel = fltarr(3,n)
     thisid = lon64arr(n)

     readu,1,thispos
     readu,1,thisvel
     readu,1,thisid

     close,1

     pos = [[pos],[thispos]]
;     vel = [[vel],[thisvel]]
     id = [id,thisid]


  ENDFOR

;stop

IF NOT keyword_set(nosort) THEN BEGIN
    pos = pos[*,sort(id)]
    id = sort(id) ; index of sorted id!
ENDIF



END
