def algo(ori_p, user_p, time_diff):
    
    ori_p_words = ori_p.split(" ")
    user_p_words = user_p.split(" ")

    matched_words = 0

    print(ori_p_words)
    print(user_p_words)

    for i in range(len(user_p_words)):
        print(ori_p_words[i])
        print(user_p_words[i])

        if(ori_p_words[i] == user_p_words[i]):
            matched_words += 1

    wpm = matched_words / (time_diff /60)

    return int(wpm)
