# -*- coding: utf-8 -*-

class verbose_converter(object):

    currencies = {
        'LVL': ('lats', 'lati', 'santīms', 'santīmi'),
        'USD': ('dolārs', 'dolāri', 'cents', 'centi'),
        'EUR': ('eiro', 'eiro', 'cents', 'centi'),
        }

    digits = [
        'nulle',
        'viens',
        'divi',
        'trīs',
        'četri',
        'pieci',
        'seši',
        'septiņi',
        'astoņi',
        'deviņi'
        ]

    starters = [
        None,
        '*',
        'div*',
        'trīs*',
        'četr*',
        'piec*',
        'seš*',
        'septiņ*',
        'astoņ*',
        'deviņ*'    
        ]

    specials = {
        'teens': 'padsmit',
        'tens': 'desmit',
        'hundreds': 'i simti',
        'hundreds_for_3': ' simti',
        'eleven': 'vienpadsmit',
        'ten': 'desmit',
        'one_hundred': 'viens simts'
        }

    enumerated_endings = [
        None,
        'tūkstoši',       
        'miljoni',
        'miljardi',
        'triljoni',
        'kvadriljoni',
        'kvintiljoni',
        ]

    enumerated_endings_singular = [
        None,
        'tūkstotis',
        'miljons',
        'miljards',
        'triljons',
        'kvadriljons',
        'kvintiljons',
        ]

    def _cc(self, str1, str2):
        if len(str1) and len(str2):
            return str1 + ' ' + str2
        else:
            return str1 + str2
        
    def _get_triad(self, triad):
        res = ''
        triad = triad[::-1]
        if len(triad) == 3 and triad[2] != '0':
            if triad[2] == '1':
                res = self.specials['one_hundred']
            else:
                zz = int(triad[2])
                if zz == 3:
                    res = self.starters[zz].replace('*',
                                                  self.specials['hundreds_for_3'])
                else:                    
                    res = self.starters[zz].replace('*',
                                                  self.specials['hundreds']) 

        if len(triad) > 1 and triad[1] != '0':
            if triad[1] == '1':                
                if triad[0] == '0':
                    res = self._cc(res, self.specials['ten'])
                elif triad[0] == '1':
                    res = self._cc(res, self.specials['eleven'])
                else:
                    res = self._cc(res, self.starters[int(triad[0])].replace('*',
                                                          self.specials['teens']))
            else:
                res = self._cc(res, self.starters[int(triad[1])].replace('*',
                                                          self.specials['tens']))

                if triad[0] != '0':
                    res = self._cc(res, self.digits[int(triad[0])])
        else:
            if triad[0] != '0':
                res = self._cc(res, self.digits[int(triad[0])])            
            
        return res

    def _convert_triad(self, triad, num):
        triad = self._get_triad(triad)
        if (num > 0 and len(triad)):
            if triad.endswith(self.digits[1]):
                triad = self._cc(triad, self.enumerated_endings_singular[num])
            else:
                triad = self._cc(triad, self.enumerated_endings[num])
        return triad        

    def verbose_num(self, num, capitalize=True):
        snum = str(num)
        res = []
        triad_num = 0
        i = len(snum)
        for i in range(len(snum) - 3, 0, -3):
            t = snum[i:i+3]
            res.append(self._convert_triad(t, triad_num))
            triad_num += 1
        if i > 0:
            res.append(self._convert_triad(snum[0:i], triad_num))
        res.reverse()
        res = filter(None, res)
        res = ' '.join(res)
        if (not len(res)):
            res = self.digits[0]
        res = unicode(res, 'utf-8')
        if capitalize:
            res = res[0].upper() + res[1:]
        return res

    def verbose_currency(self, num, currency):
        curr = (self.currencies.get(currency) or 
                (currency, currency, '', ''))
        
        intNum = int(num)
        rest = int((num - intNum) * 100)

        oneIntNum = str(intNum).endswith('1') and not str(intNum).endswith('11')
        oneRest = str(rest).endswith('1') and not str(rest).endswith('11')        
        numStr = self.verbose_num(intNum)

        res = numStr + ' ' + unicode(oneIntNum and curr[0] or curr[1], 'utf-8') + ' un %0*d ' % (2, rest) + \
            unicode(oneRest and curr[2] or curr[3], 'utf-8')
        return res
                
vc = verbose_converter()

def convert(num):
    global vc
    return vc.verbose_num(num)


def convert_currency(num, currency):
    global vc
    return vc.verbose_currency(num, currency)

