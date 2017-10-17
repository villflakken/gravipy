PRO read_group, Base,num,TotNgroups,TotNids,ids,grouplen,groupoffset

; NOTE: groupoffset appears to be wrong for some groups, but can
; calculate using grouplen: groupoffset[N] = total(grouplen[0:N-1])

;Base="/home/wangjie/data/test"
;base = 'datascope/indra5/test/2_0_0_A/'

;num = 25 ; snapnum

if num ge 1000 then begin
   exts='0000'
   exts=exts+strcompress(string(Num),/remove_all)
   exts=strmid(exts,strlen(exts)-4,4)
endif else begin
; gets snapnum string in range '000' to '064'
   exts='000'
   exts=exts+strcompress(string(Num),/remove_all)
   exts=strmid(exts,strlen(exts)-3,3) ; snapnum string
endelse

skip = 0L
skip_sub = 0L
fnr = 0L

repeat begin

   f = Base+"/snapdir_"+exts+"/group_tab_"+exts +"."$
       +strcompress(string(fnr),/remove_all)

   Ngroups = 0L
   TotNgroups = 0L
   Nids = 0L
   NTask = 0L

   openr,1,f
   readu,1, Ngroups, Nids, TotNgroups, NTask

   if fnr eq 0 AND TotNgroups GT 0 then begin
      GroupLen = lonarr(TotNgroups)
      GroupOffset = lonarr(TotNgroups)
   endif

   if Ngroups gt 0 then begin
      
      locLen = lonarr(Ngroups)
      locOffset = lonarr(Ngroups)

      readu,1, loclen 
      readu,1, locOffset

      GroupLen[skip:skip+Ngroups-1] = locLen[*]
      GroupOffset[skip:skip+Ngroups-1] = locOffset[*]

      skip+= Ngroups
   endif

   close, 1

   fnr++
endrep until fnr eq NTask


;print
;print, "TotNgroups   =", TotNgroups
;print
;print, "Largest group of length ", GroupLen(0)

;-------select the biggest subhalo in the first group -------------------------------------------

;-------load all of the IDs  --------------------------------------------------------------------

skip = 0L
fnr = 0L

;length=grouplen(0)
;offset=groupoffset(0)

longid=1

repeat begin

   f = Base + "/snapdir_" + exts +"/group_ids_"+exts +"."$
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

   IF totNgroups GT 0 THEN totnids=total(grouplen,/double) ELSE totnids = 0.

   if fnr eq 0 AND TotNids GT 0 then begin
      IDs = lonarr(TotNids)
      IF (LONGID) then Ids=lon64arr(TotNids)
   endif

   if Nids gt 0 then begin
      
      locIDs =lonarr(Nids)
;      locIDs =lonarr(Nids*2)

      IF (LONGID) then locIDs=lon64arr(Nids)

      readu,1, locIDs

;      IDs[skip:skip+Nids-1] = locIDs[*]
      ; looks like the same as IDs = [IDs,locIDs]...
;      IDs[skip:skip+Nids-1] = locIDs[indgen(Nids)*2]
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

last:
end
