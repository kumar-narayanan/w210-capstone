import json

transaction_cnt = 0
hotel_cnt = 0
restaurant_cnt = 0
rail_train_cnt = 0

for i in range(1, 18):
    if 1 <= i <= 9:
        num_str = "00" + str(i)
    else:
        num_str = "0" + str(i)
    filename = "/code/workflows/multiwoz/data/MultiWOZ_2.2/train/" + "dialogues_" + num_str + ".json"

    with open(filename, "r") as fp:
        mwoz_dialog_list = json.load(fp)

    for j in mwoz_dialog_list:
        if "hotel" in j["services"]:
            hotel_cnt += 1
        if "restaurant" in j["services"]:
            restaurant_cnt += 1
        if "train" in j["services"]:
            rail_train_cnt += 1
            
    transaction_cnt += len(mwoz_dialog_list)

    if i == 2 or i == 14 or i == 17:
        if i == 2:
            print("DEV counts")
        if i == 14:
            print("TRAIN counts")
        if i == 17:
            print("TEST counts")
        print("      Transaction count:", transaction_cnt)
        print("      Hotel count:", hotel_cnt)
        print("      Restaurant count:", restaurant_cnt)
        print("      Rail-train count:", rail_train_cnt)
        transaction_cnt = 0
        hotel_cnt = 0
        restaurant_cnt = 0
        rail_train_cnt = 0



