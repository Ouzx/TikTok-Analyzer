link_path = "link.txt"
driver_path = "scraper\driver\chromedriver.exe"

selectors = {
    "acc": ".ekmpd5l5",
    "acc_following": ".e1457k4r1:nth-child(1) strong",
    "acc_followers": ".e1457k4r1:nth-child(2) strong",
    "acc_likes": ".e1457k4r1:nth-child(3) strong",
    "acc_bio": ".e1457k4r3",

    "post": ".e1cg0wnj1",
    "post_like": ".edu4zum0:nth-child(1) .edu4zum2",
    "post_comment": ".edu4zum0:nth-child(2) .edu4zum2",
    "post_view": ".e148ts222",
    "post_name": ".e1yey0rl0 > img",
    "post_link": "a",
}

page_template = {
    "name": "",
    "following": "",
    "followers": "",
    "likes": "",
    "bio": "",
}

post_template = {
    "like": 0,
    "comment": 0,
    "view": 0,
    "name": "",
    "link": "",
}
