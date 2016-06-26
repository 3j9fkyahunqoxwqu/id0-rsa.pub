from itertools import cycle
from importlib import import_module

try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

caesar = import_module("32-caesar")
shift_cipher = caesar.shift_cipher
find_shift = caesar.find_shift


def autocorrelation(s, t):
    """Compute the autocorrelation of s:[int] with delay t:int."""
    correlation = 0
    for i in range(len(s) - t):
        if s[i] == s[i + t]:
            correlation += 1
    return correlation


ciphertext = "UHVGMEFNVCIAJPYPVGTKZYHYMIBPXFFCRPWYSCZALCSOEWCRIEELQCJSYLVBFRKZWNFLCTQCBNTLIQBRZDEIJNULXPJCBJAMSDKZSZFCRFWCJACHEWTFFCKCUTYPEZFFFCIRIEVMYJMSYTXZVTMTKCOEIPMKFAETHMOTVGILSERWPWLNFHLMXTFAVMOOLYGCUHRESLFTYPWMMUKTSLUHZDXGNEZDXFFKVJELENFHLCSEZDWMNEKPBRGRFXQMCYUTGINERYXGNERSEZPUKZJFFAITREPFYTWMGFZNIPTHRGMLHSZOIBUHVQYPUHVDXRPWZYHUBRUHEQTTZWPPBNXTREBHVLHMGTYPSRIEIMSYUSRNMPDUDDXYOCVMIQQERVMLHHFHTMUEEEEASENHEQQUCWMLHHZXXFPSVEMEFRPPPJPWTCIYUUIPWMGHZDWCFMVOEJMSKPIJBNUHLYMESZRCMIBPJGWEKCMNIADXIPTTYPCPPSVLRBGECWAGUHIPKSMAIDXPPKVDSDTTIPREUHNSMAIPVCMMEITLPJZSKLVRFDKSIZPAKLPMOGKSIUBTVCPGLERSSPJZFYXYMBLCWRCOZWIPPUKZJYNIJDMQTIGAMQUERXIPBSWZVDFDRWPYIWYZAYTSVPRNVLCTREUHVSEPQOFYICSORCLCIAUELPPWELWGEEYTWZMATVNYDKVEELEDZDTJBYVOLGTNRVIBDHVDXUJTYELCXHFWINBRKZJFJSSZHWBBFGIRIEXFRUBLVNPCBRCJGSUAXLMLTTKSIYMTVCRYUIERHCQRVDWGPNJZJRIENLXCSYYZVGAOEHLGMEREXFFOKSIPFNUZJRIESZERBHRMAGUHFYIYSMCTOCBFVYGCSSKSVMXNYLPDCATVAYSDZYXMUHVLMPBSZQXMDOLYXCSBRWELDERYCRFNUPRAZTFEVGQAYLFUBSJPILTTVLHGMYDLRYHIERLGTSKPIPJNXZEPBSZYERIOLDELEBFLXJPWVCMLHSVCIRIENSMRFWYLPCIAUESPOHZXEJMAKZRAFTYPSSUSKCIRDHVOEPNGRGIYQETFPGBRDZXGPNRYHRIEECIKBIEPHDJXVOAFJLVELCCOREWDJVVZEPTWVCIQFEEDMKVLKLRCPUJWCNFABPHZPAKLRBDRVHWYUMFEMMOLVDWMOTYPWCBIEDXYOTCJXFFTYCICTPIPEBCOREWGOTYPVCBRGLYQFDFYXFFIIHEWUHVHLYMEJSEBJRIPKSMAIWCQFTKWIBCOUTPWEONYMLUOKSIZMUVELSTGZGMLHNFOMQUAEEPWEIJNIPOISWIRPKVYSDUHVXSTFMVYXRIOLRLDSODSMQDLFDIPWITTRGUYRSEZIAUZFQFRMPHGUEMPVWNAEWSMLOLEEJPNXSMQPAIDGPJEUDXYSBLNORIOLBYCFQLPKQUAEOYNOIDMPWTPITREJNXFTMOTYPXPJAERYJBRILMQFDSZBGOTYPFMXTYPWYWAXPWRPOUPVCDTKSIPFAEOAGUHZYXCOSVWCCBGVCIWFSXLDCEOWQXMXAIOWRIEJASRXHVCIRIETSEQFHROPYTTSPILEEJNVGFDCTOCXIJPYNPNKSICYTIPQCTTVCRMGTYPFMBTNSIPFIKHEQBLJZXPJAERYJBRCJTJBTWZVKFDCPZCMWZELRIEXFRUBLVDXYSBLNOFJMJPPDXAJDICOCFZPJZAEOEBSOZEPWCACLRAJNXSMKTECQXMUHVUIPLIERXMTSZYKQPFYTWAIIGZJYDRRQXYODJTPCOTCJIWFIERXFFVRDXZMUVPCCPFKSIQFAEZXTFRPQEPEIJEELUFCLWITBFLXUBSRWWMMYZYKZSERELJFSJWCQUICWMRTCFXQYODVCVCDKCPWQMYJEELEIERYNPNKSIRPPFQXFFLFRKCSHVLHYTTFFXQPRKZJNPSKCSMUEUTRRIEBPIJBNUCMQJNXDSKFTNZJCFTRMSTFTYPPCWECZJRIEJEIPOPCLXDPRDTXGTUJPHDPRTLXAIIERXSSNJHMRITYPAFBLVWMLFIKDXMQIJYSRNOIPWNBCZZYQUHRYXFFPRWQMGADLRQIAEOELESKLRBJNXFTMOSLNLYCAJPEQUHREJJBSBDICNEUAIPDHVOERUHVXEQUHVLHMGSFXIQIIGHLGDHYLHQVNBESYMLSFXFFRKCYALSSFXJJTKWIIJNXASQUWRDWKBLCLRBTHFCXYODREXFFSRXIRJMVWMRULVVMLHPFDXUBSWFPJPFRWEPHERYHRBLCLQZJTZZRQPTYLXRIIJWSEHEISIYESKLRBQOZYXMGHZDHGEBPYSKFAEDWYUIJQCIJNXASQUITLRRTEVELPFEJPEQPFWEMNVSLAELPAIELCSERYHJFTDPSLUOKSERVPFYXFJSULKEPONTXFFIKSIPIAEOYNPNKSIEVNNLPCUOJEIYEYYTWUBYJHMDULPDPGEAWEELETYPRCSETEMLHHZXWCMFMZPSOTVPVCEHZDPMGTPDLMVLUPVQGOILTCEEJEEJ"


def find_key_length(ciphertext):
    """Determine Vigenere key length. The key length and multiples of it will have high autocorrelations."""
    delays = range(1, 100)
    correlations = [autocorrelation(ciphertext, t) for t in delays]
    plt.plot(delays, correlations)
    plt.show()
    corr_sort = sorted(zip(delays, correlations), key=lambda x: x[1], reverse=True)
    return corr_sort


def vigenere_shift(message, key):
    k = cycle(key)
    shifted = [shift_cipher(c, next(k)) for c in message]
    return "".join(shifted)


def decrypt_vigenere(ciphertext, t):
    """Find Vigenere key of length t by letter frequency analysis.
    Vigenere attack page 14, "Introduction to Modern Cryptography" by Katz, Lindell, 2nd edition.
    """
    streams = []
    for j in range(t):
        stream = [ciphertext[j + i * t] for i in range(len(ciphertext) // t)]
        streams.append(stream)

    key_inverse = [find_shift(stream)[0][0] for stream in streams]
    key = "".join([chr(ord('A') + (26 - k) % 26) for k in key_inverse])
    message = vigenere_shift(ciphertext, key_inverse)
    return message, key


# find_key_length(ciphertext)
message, key = decrypt_vigenere(ciphertext, 6)
