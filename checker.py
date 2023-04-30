from pbkdf2 import PBKDF2
from hashlib import pbkdf2_hmac, sha1, md5
from binascii import a2b_hex, b2a_hex
import hmac



class HC22000_Checker:
    # Source: https://nicholastsmith.wordpress.com/2016/11/15/wpa2-key-derivation-with-anaconda-python/

    @staticmethod
    def PRF(key, A, B):
        nByte = 64
        i = 0
        R = b''
        while(i <= ((nByte * 8 + 159) / 160)):
            hmacsha1 = hmac.new(key, A + chr(0x00).encode() + B + chr(i).encode(), sha1)
            R = R + hmacsha1.digest()
            i += 1
        return R[0:nByte]



    @staticmethod
    def MakeAB(aNonce, sNonce, apMac, cliMac):
        A = b"Pairwise key expansion"
        B = min(apMac, cliMac) + max(apMac, cliMac) + min(aNonce, sNonce) + max(aNonce, sNonce)
        return (A, B)



    @staticmethod
    def MakeMIC(pwd, ssid, A, B, data):
        pmk = pbkdf2_hmac('sha1', pwd.encode('ascii'), ssid.encode('ascii'), 4096, 32)
        ptk = HC22000_Checker.PRF(pmk, A, B)
        mic = hmac.new(ptk[0:16], data, sha1).digest()
        return (mic, ptk, pmk)



    def RunTest(psk, handshake):
        if(handshake.split("*")[0] == "WPA"):
            ssid = bytes.fromhex(handshake.split("*")[5]).decode('utf-8')
            aNonce = a2b_hex(handshake.split("*")[6])
            sNonce = a2b_hex(handshake.split("*")[7][34:(34+64)])
            apMac = a2b_hex(handshake.split("*")[3]) 
            cliMac = a2b_hex(handshake.split("*")[4]) 

            mic1 = handshake.split("*")[2]
            data1 = a2b_hex(handshake.split("*")[7])
            A, B = HC22000_Checker.MakeAB(aNonce, sNonce, apMac, cliMac)
            mic, ptk, pmk = HC22000_Checker.MakeMIC(psk, ssid, A, B, data1)

            
            if(handshake.split("*")[1] == "01"):
                pmkid = handshake.split("*")[2]
                predictedPMKID = hmac.new(pmk, b'PMK Name' + apMac + cliMac, sha1).digest().hex()[:32]
                if(predictedPMKID == pmkid):
                    print('MATCH')
                    return True

            elif(handshake.split("*")[1] == "02"):
                if(b2a_hex(mic).decode().upper()[:-8] == mic1.upper()):
                    print('MATCH')
                    return True
        return False




password = "vanagas123"
handshake = "WPA*02*4cb5dd3b660d7936940be82911be3b94*7669d957e8ca*a4c6f023fce8*546f6d61736950686f6e65*7f6a7bbf9fd95423e74da1d36a7135e4a5b5589642077c40333009dde6ea9d17*0203007502010a001000000000000000018a2115d422a2281d1bbcd1ed8868aee3f4c083d41321a4514c7431e89fc0d343000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001630140100000fac040100000fac040100000fac020c00*02"
HC22000_Checker.RunTest(password, handshake)

