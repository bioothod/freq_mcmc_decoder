# freq_mcmc_decoder
Implementation of the Hastings-Metropolis and simple ngram-based decoder for substitution ciphers

### original message
> last week, the social media company first made the announcement about saying that the label provides more transparency
into the companys process for reducing the reach of hateful tweets. restricting the reach of tweets helps reduce binary
leave up versus take down content moderation decisions and supports our freedom of speech vs freedom of reach approach, the company said at that time. 


### encrypted message
> ajmu-a3pprha-fpauno,mja9pv,maon90m?kai,cu-a9mvpa-fpam??ne?op9p?-am7ne-aumk,?1a-fm-a-fpajm7pja0cnx,vpua9ncpa-cm?u0mcp?
oka,?-na-fpaon90m?kua0cnopuuaincacpveo,?1a-fpacpmofaniafm-pieja-3pp-u!acpu-c,o-,?1a-fpacpmofania-3pp-uafpj0uacpveopa7,?
mckajpmxpae0axpcueua-mrpavn3?aon?-p?-a9nvpcm-,n?avpo,u,n?uam?vaue00nc-uanecaicppvn9aniau0ppofaxuaicppvn9aniacpmofam00cnmofha
-fpaon90m?kaum,vam-a-fm-a-,9p!a


### decrypted message with ngram-frequency method: ngram=1
> fant yee.v tre nosdaf meuda somlahg cdint maue tre ahhowhsemeht a,owt nagdhb trat tre fa,ef liopduen 
moie tiahnlaiehsg dhto tre somlahgn liosenn coi ieuwsdhb tre ieasr oc ratecwf tyeetnk ientidstdhb tre 
ieasr oc tyeetn refln ieuwse ,dhaig feape wl peinwn ta.e uoyh sohteht moueiatdoh uesdndohn ahu nwlloitn 
owi cieeuom oc nleesr pn cieeuom oc ieasr allioasrv tre somlahg nadu at trat tdmek 

accuracy: **0.52**

### decrypted message with Hastings-Metropolis algorithm
> last weev, the social media company first made the announcement about saying that the label prokides 
more transparency into the companys process for reducing the reach of hateful tweets. 
restricting the reach of tweets helps reduce binary leake up kersus tave down content moderation decisions and 
supports our freedom of speech ks freedom of reach approach, the company said at that time. 

accuracy: **0.98**
This method takes much more time to complete (a few minutes on a CPU) and essentially is a 'guided' permutation update towards the best match solution.
