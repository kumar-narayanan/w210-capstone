with open('./data/v1_hotel/test/seq.in') as f1, open('./data/v1_hotel/dev/seq.out') as f2:
    while True: 
        line1 = f1.readline()
        line2 = f2.readline()
        if not line1:
            break
        inp = len(line1.strip().split())
        outp = len(line2.strip().split())
        
        if inp != outp:
            print(line1)
            print(line2)
