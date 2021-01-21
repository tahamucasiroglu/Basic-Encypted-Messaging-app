from textwrap import wrap


def constant_time_power(base, power, MOD):
    result = 1
    while power > 0:
        # constant-time conditional copy
        sBit = power % 2 == 1
        result = ((result * base) % MOD) * sBit + (1 - sBit) * result

        # Divide the power by 2
        power = power // 2
        # Multiply base to itself
        base = (base * base) % MOD

    #print('RESULT IS:\n', result)
    return result


def textToDeci(inPlain):
    s = inPlain
    n = ' '.join(str(ord(c)) for c in s)

    # Starting with a two digit ASCII character results in deleting the padded zero because it has no value in "int" space
    # As a solution i added the ASCII character "126" which is "~" at the start of every message
    
    n = ascii(126) + " " + n

    return "".join([num.zfill(3) for num in n.split(" ")])


def deciToText(inDeci):
    h = inDeci

    chunked = ' '.join(wrap(h, 3))

    inted = [int(i) for i in chunked.split(' ')]

    text = [chr(i) for i in inted]

    str = ""
    strtext = str.join(text)

    # print('Shorter code for decode', ''.join(chr(int(s)) for s in chunked.split()))

    return strtext


#if __name__ == '__main__':
    # constant_time_power_with_conditional_copy(69696969,163512196775020195634439829827433199362533323535701820525095275149769126926296561491830018739593888146286297468152518650603122835002603367446461383634174137156212929113999152958931253775202070117570810753069887892844889264442158235963617130581339989679614000597239457747500741932845680984309944721240001669001,23520263619691607532359450235906939519638550014554531754555876198744756078152793573292513937358864285257544106713208814537169171262653938738230608960857682745912770664470909864730911343831838999659198642791070340555106688483077053527668141415735760343072434112517202945056725683223470499327281398049586892264275550458312360678689959092087757327816060643280172097903301620120474296678324351681959534538171229630482381800665378832041706368568750629170313907480025886547336303562148116983998304539626081580361638415858459409798328471436554013374129609612896858517767879582524655202080709394857492718483681687762363543873)
 #   print(textToDeci('Hello test is it working??? tesstttt'))
  #  print(deciToText('072101108108111032116101115116032105115032105116032119111114107105110103063063063032116101115115116116116116'))

