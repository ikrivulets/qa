"""Utility functions for working with spacy.
"""

import re
import spacy
from spacy.tokenizer import Tokenizer


def create_tokenizer(nlp):
    # The following way of definining unicode characters that should be
    # tokenized is super ugly and I would hope that it can be improved.
    # But it is better than not doing it because spacy's tokenizer won't break
    # on these  weird characters when it should.
    # To get this list, I scraped the train dataset for all unicode-looking
    # things.
    unicode_patterns = "|\U0001000a" + "|\U0001000d" + "|\U0001001a" + "|\U0001001e" + "|\U000120b5" + "|\U00012111" + "|\U000121b3" + "|\U0001222a" + "|\U00012292" + "|\U00012295" + "|\U00012326" + "|\U0002053b" + "|\U0002a6a5" + "|\U0002a736" + "|\u0100" + "|\u0101" + "|\u0103" + "|\u0105" + "|\u0106" + "|\u0107" + "|\u010b" + "|\u010c" + "|\u010d" + "|\u010e" + "|\u010f" + "|\u0110" + "|\u0111" + "|\u0112" + "|\u0113" + "|\u0117" + "|\u0119" + "|\u011b" + "|\u011d" + "|\u011f" + "|\u0120" + "|\u0121" + "|\u0126" + "|\u0127" + "|\u012b" + "|\u012d" + "|\u0130" + "|\u0131" + "|\u013c" + "|\u0141" + "|\u0142" + "|\u0144" + "|\u0146" + "|\u0148" + "|\u014b" + "|\u014c" + "|\u014d" + "|\u014f" + "|\u0151" + "|\u0152" + "|\u0153" + "|\u0159" + "|\u015a" + "|\u015b" + "|\u015e" + "|\u015f" + "|\u0160" + "|\u0161" + "|\u0163" + "|\u0165" + "|\u0169" + "|\u016b" + "|\u016d" + "|\u016f" + "|\u0175" + "|\u017a" + "|\u017b" + "|\u017c" + "|\u017d" + "|\u017e" + "|\u01a1" + "|\u01b0" + "|\u01bf" + "|\u01c0" + "|\u01c1" + "|\u01c2" + "|\u01c3" + "|\u01ce" + "|\u01d0" + "|\u01d2" + "|\u01d4" + "|\u01da" + "|\u01dc" + "|\u01e5" + "|\u01f5" + "|\u0219" + "|\u021b" + "|\u0250" + "|\u0251" + "|\u0252" + "|\u0254" + "|\u0255" + "|\u0256" + "|\u0259" + "|\u025b" + "|\u025c" + "|\u0261" + "|\u0262" + "|\u0263" + "|\u0264" + "|\u0265" + "|\u0266" + "|\u0268" + "|\u026a" + "|\u026b" + "|\u026d" + "|\u026f" + "|\u0273" + "|\u0275" + "|\u0278" + "|\u0279" + "|\u027e" + "|\u0280" + "|\u0281" + "|\u0282" + "|\u0283" + "|\u0288" + "|\u028a" + "|\u028c" + "|\u028e" + "|\u028f" + "|\u0292" + "|\u0294" + "|\u0295" + "|\u0298" + "|\u02b0" + "|\u02b1" + "|\u02b2" + "|\u02b7" + "|\u02bb" + "|\u02bc" + "|\u02be" + "|\u02bf" + "|\u02c0" + "|\u02c7" + "|\u02c8" + "|\u02cc" + "|\u02d0" + "|\u02d1" + "|\u02da" + "|\u02e4" + "|\u02e5" + "|\u02e7" + "|\u02e8" + "|\u02e9" + "|\u02ed" + "|\u0300" + "|\u0301" + "|\u0303" + "|\u0304" + "|\u030c" + "|\u030d" + "|\u031e" + "|\u0320" + "|\u0324" + "|\u0325" + "|\u0327" + "|\u0329" + "|\u032a" + "|\u032f" + "|\u0361" + "|\u0391" + "|\u0392" + "|\u0393" + "|\u0394" + "|\u0395" + "|\u0397" + "|\u0398" + "|\u0399" + "|\u039a" + "|\u039b" + "|\u039c" + "|\u039d" + "|\u03a0" + "|\u03a1" + "|\u03a3" + "|\u03a4" + "|\u03a5" + "|\u03a6" + "|\u03a7" + "|\u03a8" + "|\u03ac" + "|\u03ad" + "|\u03ae" + "|\u03af" + "|\u03b1" + "|\u03b2" + "|\u03b3" + "|\u03b4" + "|\u03b5" + "|\u03b6" + "|\u03b7" + "|\u03b8" + "|\u03b9" + "|\u03ba" + "|\u03bb" + "|\u03bc" + "|\u03bd" + "|\u03be" + "|\u03bf" + "|\u03c0" + "|\u03c1" + "|\u03c2" + "|\u03c3" + "|\u03c4" + "|\u03c5" + "|\u03c6" + "|\u03c7" + "|\u03c8" + "|\u03c9" + "|\u03cc" + "|\u03cd" + "|\u03ce" + "|\u0404" + "|\u0408" + "|\u0410" + "|\u0411" + "|\u0412" + "|\u0413" + "|\u0414" + "|\u0415" + "|\u0417" + "|\u0418" + "|\u041a" + "|\u041b" + "|\u041c" + "|\u041d" + "|\u041e" + "|\u041f" + "|\u0420" + "|\u0421" + "|\u0422" + "|\u0424" + "|\u0425" + "|\u0430" + "|\u0431" + "|\u0432" + "|\u0433" + "|\u0434" + "|\u0435" + "|\u0436" + "|\u0437" + "|\u0438" + "|\u0439" + "|\u043a" + "|\u043b" + "|\u043c" + "|\u043d" + "|\u043e" + "|\u043f" + "|\u0440" + "|\u0441" + "|\u0442" + "|\u0443" + "|\u0444" + "|\u0445" + "|\u0446" + "|\u0447" + "|\u0448" + "|\u0449" + "|\u044a" + "|\u044b" + "|\u044c" + "|\u044d" + "|\u044e" + "|\u044f" + "|\u0451" + "|\u0456" + "|\u0457" + "|\u045e" + "|\u0463" + "|\u0467" + "|\u0469" + "|\u046b" + "|\u046d" + "|\u0473" + "|\u0475" + "|\u04b3" + "|\u04b6" + "|\u04b7" + "|\u053c" + "|\u0540" + "|\u054a" + "|\u0561" + "|\u0562" + "|\u056b" + "|\u056f" + "|\u0570" + "|\u0575" + "|\u0576" + "|\u057d" + "|\u057f" + "|\u0580" + "|\u0581" + "|\u05b0" + "|\u05b4" + "|\u05b5" + "|\u05b7" + "|\u05b8" + "|\u05b9" + "|\u05bc" + "|\u05bf" + "|\u05c1" + "|\u05c2" + "|\u05d0" + "|\u05d1" + "|\u05d2" + "|\u05d3" + "|\u05d4" + "|\u05d5" + "|\u05d6" + "|\u05d7" + "|\u05d8" + "|\u05d9" + "|\u05da" + "|\u05dc" + "|\u05dd" + "|\u05de" + "|\u05df" + "|\u05e0" + "|\u05e1" + "|\u05e2" + "|\u05e4" + "|\u05e5" + "|\u05e6" + "|\u05e7" + "|\u05e8" + "|\u05e9" + "|\u05ea" + "|\u05f2" + "|\u0621" + "|\u0623" + "|\u0625" + "|\u0626" + "|\u0627" + "|\u0628" + "|\u0629" + "|\u062a" + "|\u062b" + "|\u062c" + "|\u062d" + "|\u062e" + "|\u062f" + "|\u0630" + "|\u0631" + "|\u0633" + "|\u0634" + "|\u0635" + "|\u0636" + "|\u0638" + "|\u0639" + "|\u0640" + "|\u0641" + "|\u0642" + "|\u0643" + "|\u0644" + "|\u0645" + "|\u0646" + "|\u0647" + "|\u0648" + "|\u0649" + "|\u064a" + "|\u064d" + "|\u064e" + "|\u064f" + "|\u0650" + "|\u0651" + "|\u0652" + "|\u0654" + "|\u067e" + "|\u06af" + "|\u06cc" + "|\u0710" + "|\u071d" + "|\u0722" + "|\u0729" + "|\u072a" + "|\u0903" + "|\u0906" + "|\u0908" + "|\u0915" + "|\u0916" + "|\u0917" + "|\u0920" + "|\u0921" + "|\u0923" + "|\u0924" + "|\u0926" + "|\u0927" + "|\u0928" + "|\u092a" + "|\u092c" + "|\u092e" + "|\u092f" + "|\u0930" + "|\u0937" + "|\u0938" + "|\u093e" + "|\u093f" + "|\u0941" + "|\u094a" + "|\u094d" + "|\u099c" + "|\u09aa" + "|\u09ae" + "|\u09af" + "|\u09b0" + "|\u09b2" + "|\u09b8" + "|\u09be" + "|\u09cd" + "|\u0c95" + "|\u0c9a" + "|\u0c9c" + "|\u0caa" + "|\u0cae" + "|\u0caf" + "|\u0cb0" + "|\u0cb2" + "|\u0cb6" + "|\u0cb8" + "|\u0cbe" + "|\u0cbf" + "|\u0cc1" + "|\u0ccd" + "|\u0e02" + "|\u0e07" + "|\u0e14" + "|\u0e19" + "|\u0e21" + "|\u0e22" + "|\u0e23" + "|\u0e25" + "|\u0e27" + "|\u0e28" + "|\u0e2a" + "|\u0e2d" + "|\u0e32" + "|\u0e34" + "|\u0e35" + "|\u0e40" + "|\u0e41" + "|\u0e42" + "|\u0e43" + "|\u0e44" + "|\u0f0b" + "|\u0f51" + "|\u0f56" + "|\u0f7c" + "|\u1014" + "|\u101e" + "|\u102c" + "|\u1038" + "|\u1202" + "|\u120b" + "|\u122a" + "|\u123b" + "|\u1261" + "|\u1273" + "|\u1295" + "|\u13a0" + "|\u13a3" + "|\u13a6" + "|\u13a8" + "|\u13a9" + "|\u13b0" + "|\u13b3" + "|\u13b9" + "|\u13be" + "|\u13cd" + "|\u13cf" + "|\u13d4" + "|\u13ef" + "|\u13f1" + "|\u1d7b" + "|\u1da2" + "|\u1e0c" + "|\u1e0d" + "|\u1e17" + "|\u1e24" + "|\u1e25" + "|\u1e31" + "|\u1e37" + "|\u1e43" + "|\u1e45" + "|\u1e47" + "|\u1e5b" + "|\u1e62" + "|\u1e63" + "|\u1e6d" + "|\u1e92" + "|\u1e93" + "|\u1ea3" + "|\u1ea5" + "|\u1ebf" + "|\u1ec1" + "|\u1ec5" + "|\u1ec9" + "|\u1ed1" + "|\u1ed3" + "|\u1edb" + "|\u1edd" + "|\u1ee5" + "|\u1eed" + "|\u1eef" + "|\u1f00" + "|\u1f01" + "|\u1f04" + "|\u1f08" + "|\u1f0c" + "|\u1f10" + "|\u1f11" + "|\u1f14" + "|\u1f18" + "|\u1f19" + "|\u1f21" + "|\u1f2d" + "|\u1f30" + "|\u1f31" + "|\u1f34" + "|\u1f35" + "|\u1f36" + "|\u1f38" + "|\u1f40" + "|\u1f50" + "|\u1f51" + "|\u1f60" + "|\u1f70" + "|\u1f72" + "|\u1f76" + "|\u1f78" + "|\u1fc6" + "|\u1fd6" + "|\u1fe6" + "|\u1ff6" + "|\u2009" + "|\u200b" + "|\u200c" + "|\u200d" + "|\u200e" + "|\u2011" + "|\u2013" + "|\u2014" + "|\u2018" + "|\u2019" + "|\u201a" + "|\u201c" + "|\u201d" + "|\u2022" + "|\u2026" + "|\u202f" + "|\u2032" + "|\u2033" + "|\u203a" + "|\u2044" + "|\u204a" + "|\u2082" + "|\u20a4" + "|\u20a5" + "|\u20ac" + "|\u20af" + "|\u20b9" + "|\u2116" + "|\u211b" + "|\u2153" + "|\u2192" + "|\u2205" + "|\u2208" + "|\u2212" + "|\u2216" + "|\u2217" + "|\u221a" + "|\u221d" + "|\u2248" + "|\u2261" + "|\u2265" + "|\u22c5" + "|\u25cc" + "|\u2646" + "|\u2660" + "|\u266f" + "|\u2764" + "|\u27e8" + "|\u27e9" + "|\u2c8f" + "|\u2c93" + "|\u2c99" + "|\u2cac" + "|\u3000" + "|\u3002" + "|\u300a" + "|\u300b" + "|\u301c" + "|\u3044" + "|\u3055" + "|\u305f" + "|\u3064" + "|\u3066" + "|\u306e" + "|\u306f" + "|\u3072" + "|\u3075" + "|\u3076" + "|\u3080" + "|\u3089" + "|\u308a" + "|\u308b" + "|\u308d" + "|\u30a1" + "|\u30a4" + "|\u30ab" + "|\u30ad" + "|\u30af" + "|\u30b0" + "|\u30b3" + "|\u30b7" + "|\u30b8" + "|\u30b9" + "|\u30bb" + "|\u30bc" + "|\u30bf" + "|\u30c0" + "|\u30c1" + "|\u30c3" + "|\u30c7" + "|\u30c8" + "|\u30d1" + "|\u30d4" + "|\u30d5" + "|\u30d7" + "|\u30de" + "|\u30df" + "|\u30e1" + "|\u30e2" + "|\u30e3" + "|\u30e5" + "|\u30e9" + "|\u30ea" + "|\u30eb" + "|\u30ec" + "|\u30ed" + "|\u30ef" + "|\u30f3" + "|\u30fc" + "|\u34fe" + "|\u4e01" + "|\u4e03" + "|\u4e09" + "|\u4e0a" + "|\u4e0b" + "|\u4e0d" + "|\u4e1a" + "|\u4e1c" + "|\u4e2d" + "|\u4e39" + "|\u4e3b" + "|\u4e49" + "|\u4e4b" + "|\u4e66" + "|\u4e89" + "|\u4e8b" + "|\u4e8c" + "|\u4e91" + "|\u4e94" + "|\u4e9c" + "|\u4ea7" + "|\u4eac" + "|\u4eba" + "|\u4eca" + "|\u4ecb" + "|\u4ed4" + "|\u4ed5" + "|\u4ed6" + "|\u4ee3" + "|\u4eea" + "|\u4f10" + "|\u4f1a" + "|\u4f1d" + "|\u4f2f" + "|\u4f50" + "|\u4f53" + "|\u4f55" + "|\u4f6c" + "|\u4f86" + "|\u4f8d" + "|\u4fc4" + "|\u4fe1" + "|\u5019" + "|\u50cf" + "|\u5143" + "|\u5148" + "|\u5149" + "|\u514b" + "|\u514d" + "|\u5165" + "|\u516b" + "|\u516c" + "|\u5175" + "|\u5178" + "|\u51b6" + "|\u51f9" + "|\u5206" + "|\u5207" + "|\u5218" + "|\u5229" + "|\u5236" + "|\u524d" + "|\u524e" + "|\u5251" + "|\u5287" + "|\u5289" + "|\u529b" + "|\u52a8" + "|\u5305" + "|\u5317" + "|\u5320" + "|\u533a" + "|\u5341" + "|\u5343" + "|\u5345" + "|\u534c" + "|\u5357" + "|\u535a" + "|\u536b" + "|\u5370" + "|\u5398" + "|\u53c8" + "|\u53cc" + "|\u53d1" + "|\u53d7" + "|\u53e0" + "|\u53e3" + "|\u53e4" + "|\u53ea" + "|\u53ef" + "|\u53f8" + "|\u5408" + "|\u5409" + "|\u540e" + "|\u5410" + "|\u5463" + "|\u5477" + "|\u548a" + "|\u548c" + "|\u5510" + "|\u5514" + "|\u554f" + "|\u559c" + "|\u56cd" + "|\u56db" + "|\u56e3" + "|\u56fd" + "|\u56fe" + "|\u570b" + "|\u5715" + "|\u5716" + "|\u571f" + "|\u5730" + "|\u5757" + "|\u5764" + "|\u576a" + "|\u57ce" + "|\u57df" + "|\u57e0" + "|\u57fa" + "|\u5802" + "|\u584a" + "|\u5883" + "|\u58eb" + "|\u5909" + "|\u590d" + "|\u5927" + "|\u5929" + "|\u5937" + "|\u5949" + "|\u5950" + "|\u5973" + "|\u5974" + "|\u5979" + "|\u59b9" + "|\u5a4e" + "|\u5aa0" + "|\u5b50" + "|\u5b57" + "|\u5b66" + "|\u5b81" + "|\u5b83" + "|\u5b87" + "|\u5b88" + "|\u5b89" + "|\u5b97" + "|\u5bb6" + "|\u5be7" + "|\u5be9" + "|\u5bf9" + "|\u5bfc" + "|\u5c06" + "|\u5c09" + "|\u5c0e" + "|\u5c0f" + "|\u5cf6" + "|\u5ddd" + "|\u5dde" + "|\u5de1" + "|\u5de5" + "|\u5df4" + "|\u5e03" + "|\u5e1d" + "|\u5e25" + "|\u5e2b" + "|\u5e38" + "|\u5e73" + "|\u5e81" + "|\u5e86" + "|\u5e93" + "|\u5e9c" + "|\u5eab" + "|\u5eb7" + "|\u5eda" + "|\u5ef7" + "|\u5efa" + "|\u5eff" + "|\u5f00" + "|\u5f18" + "|\u5f35" + "|\u5f53" + "|\u5f81" + "|\u5f8c" + "|\u5f92" + "|\u5f9e" + "|\u5fa1" + "|\u5fd2" + "|\u601d" + "|\u603b" + "|\u6062" + "|\u606f" + "|\u60e1" + "|\u60f0" + "|\u611b" + "|\u6182" + "|\u61f8" + "|\u6210" + "|\u6218" + "|\u6226" + "|\u6230" + "|\u624b" + "|\u624d" + "|\u6279" + "|\u6280" + "|\u628a" + "|\u6297" + "|\u6298" + "|\u62c9" + "|\u62ff" + "|\u6309" + "|\u6311" + "|\u6368" + "|\u63d0" + "|\u63f4" + "|\u64ab" + "|\u652f" + "|\u653f" + "|\u6559" + "|\u6587" + "|\u6597" + "|\u65ac" + "|\u65af" + "|\u65b0" + "|\u65b9" + "|\u65bc" + "|\u65cf" + "|\u65e5" + "|\u65e7" + "|\u6607" + "|\u660e" + "|\u661f" + "|\u6642" + "|\u666e" + "|\u66f2" + "|\u66f8" + "|\u66f9" + "|\u66ff" + "|\u6708" + "|\u6709" + "|\u671d" + "|\u6728" + "|\u672f" + "|\u6731" + "|\u674e" + "|\u675c" + "|\u6765" + "|\u676d" + "|\u6771" + "|\u6777" + "|\u677e" + "|\u6787" + "|\u6797" + "|\u6821" + "|\u6848" + "|\u6853" + "|\u694a" + "|\u696d" + "|\u69d0" + "|\u69d8" + "|\u6a02" + "|\u6a19" + "|\u6a80" + "|\u6b21" + "|\u6b4c" + "|\u6b66" + "|\u6bcb" + "|\u6bd4" + "|\u6c11" + "|\u6c34" + "|\u6c35" + "|\u6c49" + "|\u6c5f" + "|\u6c76" + "|\u6c90" + "|\u6c96" + "|\u6cb3" + "|\u6cc9" + "|\u6cd5" + "|\u6ce5" + "|\u6d1e" + "|\u6d32" + "|\u6d41" + "|\u6d4e" + "|\u6d59" + "|\u6d66" + "|\u6d77" + "|\u6de8" + "|\u6dee" + "|\u6e05" + "|\u6e08" + "|\u6e23" + "|\u6e24" + "|\u6e56" + "|\u6e96" + "|\u6ed1" + "|\u6f22" + "|\u6f33" + "|\u6f6e" + "|\u6f84" + "|\u706b" + "|\u707e" + "|\u7089" + "|\u70cf" + "|\u722d" + "|\u7231" + "|\u7236" + "|\u7247" + "|\u7260" + "|\u7279" + "|\u732e" + "|\u737b" + "|\u738b" + "|\u73b0" + "|\u73ca" + "|\u7406" + "|\u7435" + "|\u7436" + "|\u745a" + "|\u74e6" + "|\u74e9" + "|\u7528" + "|\u752b" + "|\u7530" + "|\u756a" + "|\u7570" + "|\u767d" + "|\u7684" + "|\u7686" + "|\u7687" + "|\u76db" + "|\u7763" + "|\u77e5" + "|\u77f3" + "|\u793b" + "|\u793e" + "|\u7942" + "|\u7950" + "|\u795e" + "|\u7985" + "|\u798f" + "|\u79c0" + "|\u79e3" + "|\u7a0b" + "|\u7adc" + "|\u7ae0" + "|\u7af9" + "|\u7bc0" + "|\u7bc6" + "|\u7c72" + "|\u7c73" + "|\u7c81" + "|\u7cce" + "|\u7cfb" + "|\u7d04" + "|\u7d05" + "|\u7d10" + "|\u7d2b" + "|\u7d39" + "|\u7d71" + "|\u7da0" + "|\u7dad" + "|\u7dcf" + "|\u7dd1" + "|\u7de3" + "|\u7de9" + "|\u7e23" + "|\u7e3d" + "|\u7e54" + "|\u7ea2" + "|\u7ecd" + "|\u7ecf" + "|\u7edf" + "|\u7ef4" + "|\u7f8e" + "|\u7fa9" + "|\u7fbd" + "|\u7fd2" + "|\u8003" + "|\u8036" + "|\u803f" + "|\u8089" + "|\u80e1" + "|\u8150" + "|\u8179" + "|\u81ba" + "|\u81e3" + "|\u81e8" + "|\u8208" + "|\u820d" + "|\u822a" + "|\u8239" + "|\u826f" + "|\u8282" + "|\u82cf" + "|\u82d7" + "|\u82f1" + "|\u8349" + "|\u83e9" + "|\u83ef" + "|\u8428" + "|\u84b2" + "|\u8543" + "|\u85a9" + "|\u85cd" + "|\u85cf" + "|\u85e9" + "|\u866b" + "|\u8700" + "|\u8774" + "|\u8776" + "|\u885b" + "|\u8868" + "|\u897f" + "|\u8986" + "|\u898b" + "|\u89aa" + "|\u8a00" + "|\u8a5e" + "|\u8a66" + "|\u8a71" + "|\u8a9e" + "|\u8aac" + "|\u8b70" + "|\u8b80" + "|\u8ba9" + "|\u8bd5" + "|\u8bdd" + "|\u8bed" + "|\u8c46" + "|\u8c4a" + "|\u8c54" + "|\u8d77" + "|\u8d8a" + "|\u8d99" + "|\u8ecd" + "|\u901a" + "|\u9038" + "|\u904e" + "|\u9053" + "|\u9091" + "|\u90a3" + "|\u90ce" + "|\u90e8" + "|\u90fd" + "|\u9134" + "|\u91c1" + "|\u91cd" + "|\u91d1" + "|\u91dd" + "|\u9296" + "|\u92ea" + "|\u94fa" + "|\u9577" + "|\u957f" + "|\u9580" + "|\u958f" + "|\u95a9" + "|\u95dc" + "|\u95e8" + "|\u95ee" + "|\u95fd" + "|\u964b" + "|\u9662" + "|\u9673" + "|\u9675" + "|\u967d" + "|\u96b6" + "|\u96b8" + "|\u96c6" + "|\u96cd" + "|\u96d9" + "|\u96e8" + "|\u96f2" + "|\u9707" + "|\u9752" + "|\u97d3" + "|\u97e9" + "|\u97f3" + "|\u9813" + "|\u984c" + "|\u986f" + "|\u987f" + "|\u9898" + "|\u98ce" + "|\u98df" + "|\u9928" + "|\u9a37" + "|\u9a57" + "|\u9a8c" + "|\u9ad4" + "|\u9ad8" + "|\u9b31" + "|\u9b42" + "|\u9b44" + "|\u9b4f" + "|\u9bae" + "|\u9c7b" + "|\u9c81" + "|\u9c9c" + "|\u9f49" + "|\u9f8d" + "|\u9f98" + "|\u9fa2" + "|\ua015" + "|\ua723" + "|\uace0" + "|\uad50" + "|\uad6d" + "|\uadf8" + "|\uae30" + "|\ub098" + "|\ub300" + "|\ub3c4" + "|\ub3c5" + "|\ub3d9" + "|\ub77c" + "|\ub78c" + "|\ub798" + "|\ub824" + "|\ub85c" + "|\ub984" + "|\ub9ac" + "|\ubb3c" + "|\ubc29" + "|\ubcf4" + "|\ubd80" + "|\ube44" + "|\uc0ac" + "|\uc120" + "|\uc18c" + "|\uc218" + "|\uc288" + "|\uc2a4" + "|\uc2e0" + "|\uc544" + "|\uc608" + "|\uc744" + "|\uc774" + "|\uc778" + "|\uc791" + "|\uc7a5" + "|\uc7c1" + "|\uc804" + "|\uc870" + "|\uc871" + "|\ucef4" + "|\ud070" + "|\ud1b5" + "|\ud30c" + "|\ud37c" + "|\ud558" + "|\ud55c" + "|\ud569" + "|\ud574" + "|\ud604" + "|\ud68c" + "|\ufb01" + "|\ufb02" + "|\ufe18" + "|\ufeff" + "|\uff0c" + "|\uff5e" + "|\ufffd" + "|\xa1" + "|\xa2" + "|\xa3" + "|\xa5" + "|\xa7" + "|\xb0" + "|\xb1" + "|\xb2" + "|\xb4" + "|\xb5" + "|\xb6" + "|\xb7" + "|\xbc" + "|\xbd" + "|\xbf" + "|\xc1" + "|\xc2" + "|\xc4" + "|\xc5" + "|\xc6" + "|\xc7" + "|\xc9" + "|\xcd" + "|\xce" + "|\xd3" + "|\xd4" + "|\xd5" + "|\xd6" + "|\xd7" + "|\xd8" + "|\xda" + "|\xdc" + "|\xdf" + "|\xe0" + "|\xe1" + "|\xe2" + "|\xe3" + "|\xe4" + "|\xe5" + "|\xe6" + "|\xe7" + "|\xe8" + "|\xe9" + "|\xea" + "|\xeb" + "|\xec" + "|\xed" + "|\xee" + "|\xef" + "|\xf0" + "|\xf1" + "|\xf2" + "|\xf3" + "|\xf4" + "|\xf5" + "|\xf6" + "|\xf7" + "|\xf8" + "|\xf9" + "|\xfa" + "|\xfb" + "|\xfc" + "|\xfd" + "|\xfe" + "|\xff"
    infix_pattern = "[-~.,'?;!@#$%^&*():]" + unicode_patterns
    prefix_pattern = "^[-\"'[(]"
    suffix_pattern = "[-\"'\])]$"
    infix_re = re.compile(infix_pattern)
    prefix_re = re.compile(prefix_pattern)
    suffix_re = re.compile(suffix_pattern)
    tokenizer = Tokenizer(vocab=nlp.vocab, infix_finditer=infix_re.finditer,
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search)
    return tokenizer