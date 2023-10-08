
def search_sentence(redis, pattern):
    title_keys= redis.keys("title*")
    author_keys = redis.keys("author*")
    preface_keys = redis.keys("preface*")
 
    match_list = []

    for title_key in title_keys:
        key = title_key.decode()
        id = key.replace("title","")

        titleValue = redis.get(key)
        authorValue = redis.get("author" + id)
        prefaceValue = redis.get("preface" + id)

        if pattern in titleValue.decode():
            match_list.append(key)
        elif pattern in authorValue.decode():
            match_list.append(key)
        elif pattern in prefaceValue.decode():
            match_list.append(key)
    
    return match_list
