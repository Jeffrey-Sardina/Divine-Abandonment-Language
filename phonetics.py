onsets = {
            "all": set(
                "s,z,th,dh,lh,l,x,gh, \
                k,g,m,mh,n,nh,ng,ngh, \
                sh,zh,w,wh,r,r*,t,d,tsh, \
                ts,ks,kx,smh,snh,sm,sn, \
                thwh,kth,ml,mr,mr*,nl,nr, \
                nr*".split(",")
            ),

            "voiced": set(
                "z,dh,k,gh,g,m,n, \
                ng,zh,w,r,r*".split(",")
            ),

            "stops": set(
                "t,d,k,g".split(",")
            ),

            "clusters": set(
                "ts,ks,kx,smh,snh,sm,sn, \
                thwh,kth,ml,mr,mr*,nl,nr, \
                nr*".split(",")
            ),

            "explosives": set(
                "".split(",")
            )
        }

codas = {
            "all": set(
                "lh,dh,m,nh,sh".split(",")
            ),

            "clusters": set(
                "".split(",")
            ),

            "voiced": set(
                "dh,m".split(",")
            )
    }

vowels = {
            "all": set(
                "ae,aei,a,ai,o,e,ii,i".split(",")
            ),

            "dipthong": set(
                "aei,ai".split(",")
            ),

            "monopthong": set(
                "ae,a,o,e,ii,i".split(",")
            )
        }

# get rid of all the spaces that are on the new lines in here
for phonetic_type in (onsets, codas, vowels):
    for subtype in phonetic_type:
        phonetic_type[subtype] = set(x.replace(" ", "") for x in  phonetic_type[subtype])

# now do logic to create a few more useful categories
codas["voiceless"] = codas["all"] - codas["voiced"]
codas["singles"] = codas["all"] - codas["clusters"]
codas["stops"] = codas["voiced"]

onsets["voiceless"] = onsets["all"] - onsets["voiced"]
onsets["nonplosive_voiceless_stops"] = onsets["stops"] - onsets["voiced"] - onsets["explosives"]
onsets["singles"] = onsets["all"] - onsets["clusters"]
