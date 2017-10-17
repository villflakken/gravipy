PRO read_sub, Base,num,TotNgroups,TotNids,M200,pos,$
              IDs,Sublen,Suboffset,loadIDs=loadIDs

;Base="/datascope/indra3/0_0_0/"

;num = 25 ; snapnum
if num ge 1000 then begin
   exts='0000'
   exts=exts+strcompress(string(Num),/remove_all)
   exts=strmid(exts,strlen(exts)-4,4)
endif else begin
   exts='000'
   exts=exts+strcompress(string(Num),/remove_all)
   exts=strmid(exts,strlen(exts)-3,3) ; snapnum string
endelse

skip = 0L
skip_sub = 0L
fnr = 0L

nnn=500000L
;mass_sub=fltarr(nnn)
;pos_sub=fltarr(3,nnn)
count=0L
count1=0L
count_sub = 0L

; First need total # subhalos, not saved like TotNgroups...
TotNSubs = 0L
repeat begin
   f = Base+"/postproc_"+exts+"/sub_tab_"+exts +"."$
       +strcompress(string(fnr),/remove_all)

   Ngroups = 0L
   TotNgroups = 0L
   Nids = 0L
   NTask = 0L
   NSubs = 0L

   openr,1,f
   readu,1, Ngroups, Nids, TotNgroups, NTask, NSubs
   close,1

   TotNSubs += NSubs

   fnr++
endrep until fnr eq NTask

fnr = 0L
SubLen = lonarr(TotNsubs)
SubOffset = lonarr(TotNsubs)

M200 = fltarr(totNgroups)
pos = fltarr(3,totNgroups)
repeat begin

   f = Base+"/postproc_"+exts+"/sub_tab_"+exts +"."$
       +strcompress(string(fnr),/remove_all)

   Ngroups = 0L
   TotNgroups = 0L
   Nids = 0L
   NTask = 0L

   openr,1,f
   readu,1, Ngroups, Nids, TotNgroups, NTask

;   print,'Ngroups = ', Ngroups
;   print,'TotNgroups = ', TotNgroups

   Nsubs = 0L
   readu,1,Nsubs

; Why would Nsubs be 0? ... in this certain file?
   IF Nsubs GT 0 THEN BEGIN

   NsubPerHalo = lonarr(Ngroups)
   FirstSubOfHalo = lonarr(Ngroups)
   locLen=lonarr(Nsubs)
   locOffset=lonarr(Nsubs)
   SubParentHalo= lonarr(Nsubs)

   readu,1, NsubPerHalo , FirstSubOfHalo, locLen, locOffset, SubParentHalo

      SubLen[skip:skip+Nsubs-1] = locLen[*]
      SubOffset[skip:skip+Nsubs-1] = locOffset[*]

      skip+= Nsubs

;   print,"Nsubs= ", Nsubs,total(loclen)

   Halo_M_Mean200 = fltarr(Ngroups)
   Halo_R_Mean200 = fltarr(Ngroups)
   Halo_M_Crit200 = fltarr(Ngroups)
   Halo_R_Crit200 = fltarr(Ngroups)
   Halo_M_TopHat200 = fltarr(Ngroups)
   Halo_R_TopHat200 = fltarr(Ngroups)

   readu,1, Halo_M_Mean200, Halo_R_Mean200 
   readu,1, Halo_M_Crit200, Halo_R_Crit200 
   readu,1, Halo_M_TopHat200, Halo_R_TopHat200

   M200[count:count+Ngroups-1] = Halo_M_Crit200

   SubPos = fltarr(3, Nsubs)
   SubVel = fltarr(3, Nsubs)
   SubVelDisp = fltarr(Nsubs)
   SubVmax = fltarr(Nsubs)
   SubSpin = fltarr(3, Nsubs)
   SubMostBoundID = lonarr(2, Nsubs)
   Subhalfmass=fltarr(Nsubs)

   readu,1, SubPos, SubVel, SubVelDisp, SubVmax, SubSpin, SubMostBoundID, $
     Subhalfmass

   pos[*,count:count+Ngroups-1] = subpos[*,firstsubofhalo]
   count += Ngroups

ENDIF; ELSE print,'nsubs = 0'

   close, 1

; Below running into indexing errors
;   ind=where(sublen gt 20)
;   if (ind[0] ne -1 ) then begin
;       num_chos=n_elements(ind)
;       mass_sub[count:count+num_chos-1L]=sublen[ind]
;       pos_sub[*,count:count+num_chos-1L]=subpos[*,ind]
;       count_sub=count_sub+num_chos
;   endif


;   mass_sub(count:count+ngroups-1L)=halo_m_mean200(*)
;   pos_sub(*,count:count+ngroups-1L)=subpos(*,firstsubofhalo)
;   count=count+ngroups
;   count1=count1+nsubs


   fnr++
endrep until fnr eq NTask

;mass_sub=mass_sub[0:count_sub-1L]
;pos_sub=pos_sub[*,0:count_sub-1L]



;print
;print, "TotNgroups   =", TotNgroups
;print
;print, "Largest group of length ", GroupLen(0)

;-------select the biggest subhalo in the first group -------------------------------------------

;-------load all of the IDs  --------------------------------------------------------------------

IF keyword_set(loadIDs) THEN BEGIN

skip = 0L
fnr = 0L

;length=grouplen(0)
;offset=groupoffset(0)

longid=1
repeat begin

   f = Base + "/postproc_" + exts +"/sub_ids_"+exts +"."$
       +strcompress(string(fnr),/remove_all)

   Ngroups = 0L
   TotNgroups = 0L
   Nids = 0L
   NTask = 0L

   openr,1,f
   readu,1, Ngroups,Nids, TotNgroups,NTask
;   print, "file=", fnr
;   print, "Ngroups=", Ngroups, "  TotNgroups=", TotNgroups, " Nids=", Nids,$
;          "  NTask=", NTask

   IF totNgroups GT 0 THEN totnids=total(Sublen,/double) ELSE totnids = 0.

   if fnr eq 0 AND TotNids GT 0 then begin
      IDs = lonarr(TotNids)
      IF (LONGID) then Ids=lon64arr(TotNids)
   endif

   if Nids gt 0 then begin
      locIDs =lonarr(Nids)
      IF (LONGID) then locIDs=lon64arr(Nids)
      readu,1, locIDs
;      IDs[skip:skip+Nids-1] = locIDs[*]
      ; looks like the same as IDs = [IDs,locIDs]...
; Remove the hash table info:
      IDs[skip:skip+Nids-1] = locIDs[*] AND (ishft(1LL,34)-1)
      skip+= Nids
   endif
   close, 1

   fnr++
;   if skip gt 1.01*length then goto, last 
endrep until fnr eq NTask

;particle IDs of halo N=10 
;N=10
;ids_group0=ids[groupoffset[N]:groupoffset[N]+grouplen[N]-1]

ENDIF


last:
end
