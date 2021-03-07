from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class NewDonation(BaseModel):
    name: str = Field(None, example="Fake Todd")
    email: str = Field(None, example="fake@example.com")
    count: int = Field(None, example=5)
    message: Optional[str] = Field(
        None, example="Great tutorials but this is a test message."
    )
    link: str = Field(None, example="https://buymeacoffee.com/hackersslackers/c/fake")
    coffee_id: int = Field(None, example=3453543)

    class Config:
        schema_extra = {
            "name": "Fake Todd",
            "email": "fake@example.com",
            "count": 1,
            "message": "Great tutorials but this is a test message.",
            "link": "https://buymeacoffee.com/hackersslackers",
            "coffee_id": 405127,
        }


class NewComment(BaseModel):
    post_id: str = Field(None, example="5dc42cb812c9ce0d63f5bf96")
    post_slug: str = Field(None, example="python-virtualenv-virtualenvwrapper")
    user_id: str = Field(None, example="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385")
    user_name: Optional[str] = Field(None, example="Todd Birchard")
    user_avatar: Optional[str] = Field(
        None, example="https://avatars3.githubusercontent.com/u/2747442?v=4"
    )
    user_email: str = Field(None, example="person@example.com")
    user_role: Optional[str] = Field(None, example=None)
    body: Optional[str] = Field(None, example="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385")
    created_at: str = Field(None, example="2020-12-15T04:52:03.928Z")

    class Config:
        schema_extra = {
            "comment_id": 999,
            "post_id": "5dc42cb812c9ce0d63f5bf96",
            "post_slug": "python-virtualenv-virtualenvwrapper",
            "post_url": "https://hackersandslackers.com/python-virtualenv-virtualenvwrapper/",
            "user_avatar": "https://avatars3.githubusercontent.com/u/2747442?v=4",
            "user_email": "toddbirchard@gmail.com",
            "user_id": "8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385",
            "user_name": "Fake Name",
            "user_role": None,
            "body": "hello",
            "created_at": "2020-12-12T05:26:14.794Z",
        }


class UpvoteComment(BaseModel):
    comment_id: int = Field(None, example=1)
    user_id: str = Field(None, example="8c06d6d7-2b02-4f4f-b8df-2ca5d16c0385")
    vote: bool = Field(None, example=True)


class Role(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class Author(BaseModel):
    id: str = Field(None, example=1)
    name: str = Field(None, example="Todd Birchard")
    slug: str = Field(None, example="todd")
    email: Optional[str] = Field(None, example="fake@example.com")
    profile_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/authors/todd@2x.jpg",
    )
    cover_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/2020/03/fantasticmrfox.jpg",
    )
    bio: Optional[str] = Field(
        None,
        example="Engineer with an ongoing identity crisis. Breaks everything before learning best practices. Completely normal and emotionally stable.",
    )
    website: Optional[str] = Field(None, example="https://toddbirchard.com")
    location: Optional[str] = Field(None, example="New York City")
    twitter: Optional[str] = Field(None, example="@ToddRBirchard")
    status: str = Field(None, example="active")
    tour: str = Field(None, example='["upload-a-theme","getting-started"]')
    last_seen: str = Field(None, example="2020-12-20 10:54:20")
    created_at: datetime = Field(None, example="2019-11-07 14:38:35")
    updated_at: datetime = Field(None, example="2020-12-20 10:54:20")
    roles: List[Role] = Field(
        None,
        example=[
            {
                "id": "5dc42c6b4b25bc0d13674448",
                "name": "Administrator",
                "description": "Administrators",
                "created_at": "2019-11-07T14:38:35.000Z",
                "updated_at": "2019-11-07T14:38:35.000Z",
            }
        ],
    )
    url: Optional[str] = Field(None, example="fake@example.com")


class Tag(BaseModel):
    id: str = Field(None, example="5dc42cb712c9ce0d63f5bf4f")
    name: str = Field(None, example="Python")
    slug: str = Field(None, example="python")
    description: Optional[str] = Field(
        None,
        example="Let us feed your endless Python addiction!",
    )
    feature_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/2020/05/python.png",
    )
    visibility: str = Field(None, example="public")
    meta_title: Optional[str] = Field(
        None, example="Python Tricks, Hacks, and Snippets"
    )
    meta_description: Optional[str] = Field(
        None,
        example="Let us feed your endless Python addiction!",
    )
    created_at: datetime = Field(None, example="2017-11-17 20:44:09")
    updated_at: datetime = Field(None, example="2020-08-03 05:21:42")
    og_title: Optional[str] = Field(None, example="Python Tricks, Hacks, and Snippets")
    og_description: Optional[str] = Field(
        None,
        example="Let us feed your endless Python addiction!",
    )
    og_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/2020/05/python.png",
    )
    twitter_title: Optional[str] = Field(
        None, example="Python Tricks, Hacks, and Snippets"
    )
    twitter_description: Optional[str] = Field(
        None,
        example="Let us feed your endless Python addiction!",
    )
    twitter_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/2020/05/python.png",
    )
    accent_color: Optional[str] = Field(None, example="#4B8BBE")
    canonical_url: Optional[str] = None


class BasePost(BaseModel):
    id: str = Field(None, example="5dc42cb812c9ce0d63f5bf8e")
    uuid: str = Field(None, example="84d9b616-db30-44f3-9ef3-cfc035ae71f9")
    title: Optional[str] = Field(None, example="Welcome to Hackers and Slackers")
    slug: str = Field(None, example="welcome-to-hackers-and-slackers")
    mobiledoc: Optional[str] = Field(
        None,
        example='{"version":"0.3.1","atoms":[],"cards":[],"markups":[["a",["href","http://hackersandslackers.com"]]],"sections":[[1,"p",[[0,[],0,"Welcome to the Hackers and Slackers blog, the official counterpart to "],[0,[0],1,"hackersandslackers.com"],[0,[],0,"."]]],[1,"p",[[0,[],0,"H+S is a tightly knit community of of people who code dope shit as a means to an end. While we may not all be developers per se, we like to blow stuff up and make an impact. If we get to pick up a few programming languages in the process, so be it."]]],[1,"p",[[0,[],0,"While we keep most of our knowledge tucked into our confluence instance, this blog is intended to be the public facing fruits of our labor. When we manage to stumble upon making things that are actually useful, this will be our medium for communicating that."]]],[1,"p",[[0,[],0,"If you\'re somebody who likes to learn and be casually badass, maybe you should join us."]]]]}',
    )
    html: Optional[str] = Field(
        None,
        example='<p>Welcome to the Hackers and Slackers blog, the official counterpart to <a href="http://hackersandslackers.com">hackersandslackers.com</a>.</p><p>H+S is a tightly knit community of of people who code dope shit as a means to an end. While we may not all be developers per se, we like to blow stuff up and make an impact. If we get to pick up a few programming languages in the process, so be it.</p><p>While we keep most of our knowledge tucked into our confluence instance, this blog is intended to be the public facing fruits of our labor. When we manage to stumble upon making things that are actually useful, this will be our medium for communicating that.</p><p>If you\'re somebody who likes to learn and be casually badass, maybe you should join us.</p>',
    )
    comment_id: str = Field(None, example="5a0f4699e38d612cc8261306")
    plaintext: Optional[str] = Field(None, example="5dc42cb712c9ce0d63f5bf4f")
    feature_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/2017/11/welcome.jpg",
    )
    featured: bool = Field(None, example=False)
    status: str = Field(None, example="published")
    visibility: str = Field(None, example="public")
    email_recipient_filter: Optional[str] = Field(None, example=None)
    created_at: datetime = Field(None, example="2017-11-17T20:29:13.000Z")
    updated_at: datetime = Field(None, example="2019-10-26T06:52:53.000Z")
    published_at: str = Field(None, example="2017-11-13T20:37:00.000Z")
    custom_excerpt: Optional[str] = Field(None, example="Technology for badasses.")
    authors: List[Author] = Field(None, example=[Author.schema()])
    tags: Optional[List[Tag]] = Field(None, example=[Tag.schema()])
    primary_author: Author = Field(None, example=Author.schema())
    primary_tag: Optional[Tag] = Field(None, example=Tag.schema().get("example"))
    url: Optional[str] = Field(
        None, example="https://hackersandslackers.com/welcome-to-hackers-and-slackers/"
    )
    excerpt: Optional[str] = Field(None, example="Technology for badasses.")
    reading_time: int = Field(None, example=1)
    send_email_when_published: bool = Field(None, example=False)
    og_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/2017/11/welcome.jpg",
    )
    og_title: Optional[str] = Field(None, example="Welcome to Hackers and Slackers")
    og_description: Optional[str] = Field(None, example="Technology for badasses")
    twitter_image: Optional[str] = Field(
        None,
        example="https://cdn.hackersandslackers.com/2017/11/welcome.jpg",
    )
    twitter_title: Optional[str] = Field(
        None, example="Welcome to Hackers and Slackers"
    )
    twitter_description: Optional[str] = Field(None, example="Technology for badasses")
    meta_title: Optional[str] = Field(None, example="Welcome to Hackers and Slackers")
    meta_description: Optional[str] = Field(None, example="Technology for badasses")


class Post(BaseModel):
    current: BasePost
    previous: Optional[Dict[str, Any]]


class PostUpdate(BaseModel):
    post: Post

    class Config:
        schema_extra = {
            "post": {
                "current": {
                    "id": "5e5cbed04965476b6cd6f16d",
                    "uuid": "242bc890-4537-453b-a85c-690fabf4b6f2",
                    "title": "Lynx Roundup, March 4th 2020",
                    "slug": "lynx-roundup-march-4th-2020",
                    "mobiledoc": '{"version":"0.3.1","atoms":[],"cards":[["bookmark",{"type":"bookmark","url":"https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064","metadata":{"url":"https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064","title":"Dijkstra’s Shortest Path Algorithm in Python","description":"From GPS navigation to network-layer link-state routing, Dijkstra’s Algorithm powers some of the most taken-for-granted modern services. Utilizing some basic data structures, let’s get an…","author":"Micah Shute","publisher":"Cantor’s Paradise","thumbnail":"https://miro.medium.com/max/1200/1*UEBb_0AUZf1QxVOHY71xRA.png","icon":"https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"}}],["bookmark",{"type":"bookmark","url":"https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace","metadata":{"url":"https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace","title":"Turn Python Scripts into Beautiful ML Tools","description":"In my experience, every nontrivial machine learning project is eventually stitched together with bug-ridden and unmaintainable internal tools. These tools — often a patchwork of Jupyter Notebooks…","author":"Adrien Treuille","publisher":"Towards Data Science","thumbnail":"https://miro.medium.com/freeze/max/640/1*Mbn2SxozueUkGKPW1NJkOw.gif","icon":"https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"}}],["bookmark",{"type":"bookmark","url":"https://github.com/jyhjinghwang/SegSort","metadata":{"url":"https://github.com/jyhjinghwang/SegSort","title":"jyhjinghwang/SegSort","description":"SegSort: Segmentation by Discriminative Sorting of Segments - jyhjinghwang/SegSort","author":"jyhjinghwang","publisher":"GitHub","thumbnail":"https://avatars3.githubusercontent.com/u/7334548?s=400&v=4","icon":"https://github.githubassets.com/favicon.ico"}}]],"markups":[["a",["href","https://docs.python-guide.org/writing/tests/"]],["a",["href","https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled"]],["a",["href","https://lectures.quantecon.org/_downloads/pdf/py/Quantitative%20Economics%20with%20Python.pdf"]]],"sections":[[10,0],[10,1],[10,2],[1,"p",[[0,[0],1,"https://docs.python-guide.org/writing/tests/"]]],[1,"p",[[0,[1],1,"https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled"]]],[1,"p",[[0,[2],1,"https://lectures.quantecon.org/_downloads/pdf/py/Quantitative Economics with Python.pdf"]]]]}',
                    "html": '<figure class="kg-card kg-bookmark-card"><a class="kg-bookmark-container" href="https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064"><div class="kg-bookmark-content"><div class="kg-bookmark-title">Dijkstra’s Shortest Path Algorithm in Python</div><div class="kg-bookmark-description">From GPS navigation to network-layer link-state routing, Dijkstra’s Algorithm powers some of the most taken-for-granted modern services. Utilizing some basic data structures, let’s get an…</div><div class="kg-bookmark-metadata"><img class="kg-bookmark-icon" src="https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"><span class="kg-bookmark-author">Micah Shute</span><span class="kg-bookmark-publisher">Cantor’s Paradise</span></div></div><div class="kg-bookmark-thumbnail"><img src="https://miro.medium.com/max/1200/1*UEBb_0AUZf1QxVOHY71xRA.png"></div></a></figure><figure class="kg-card kg-bookmark-card"><a class="kg-bookmark-container" href="https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace"><div class="kg-bookmark-content"><div class="kg-bookmark-title">Turn Python Scripts into Beautiful ML Tools</div><div class="kg-bookmark-description">In my experience, every nontrivial machine learning project is eventually stitched together with bug-ridden and unmaintainable internal tools. These tools — often a patchwork of Jupyter Notebooks…</div><div class="kg-bookmark-metadata"><img class="kg-bookmark-icon" src="https://cdn-images-1.medium.com/fit/c/152/152/1*8I-HPL0bfoIzGied-dzOvA.png"><span class="kg-bookmark-author">Adrien Treuille</span><span class="kg-bookmark-publisher">Towards Data Science</span></div></div><div class="kg-bookmark-thumbnail"><img src="https://miro.medium.com/freeze/max/640/1*Mbn2SxozueUkGKPW1NJkOw.gif"></div></a></figure><figure class="kg-card kg-bookmark-card"><a class="kg-bookmark-container" href="https://github.com/jyhjinghwang/SegSort"><div class="kg-bookmark-content"><div class="kg-bookmark-title">jyhjinghwang/SegSort</div><div class="kg-bookmark-description">SegSort: Segmentation by Discriminative Sorting of Segments - jyhjinghwang/SegSort</div><div class="kg-bookmark-metadata"><img class="kg-bookmark-icon" src="https://github.githubassets.com/favicon.ico"><span class="kg-bookmark-author">jyhjinghwang</span><span class="kg-bookmark-publisher">GitHub</span></div></div><div class="kg-bookmark-thumbnail"><img src="https://avatars3.githubusercontent.com/u/7334548?s=400&amp;v=4"></div></a></figure><p><a href="https://docs.python-guide.org/writing/tests/">https://docs.python-guide.org/writing/tests/</a></p><p><a href="https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled">https://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled</a></p><p><a href="https://lectures.quantecon.org/_downloads/pdf/py/Quantitative%20Economics%20with%20Python.pdf">https://lectures.quantecon.org/_downloads/pdf/py/Quantitative Economics with Python.pdf</a></p>',
                    "comment_id": "5e5cbed04965476b6cd6f16d",
                    "plaintext": "Dijkstra’s Shortest Path Algorithm in PythonFrom GPS navigation to\nnetwork-layer\nlink-state routing, Dijkstra’s Algorithm powers some of the most\ntaken-for-granted modern services. Utilizing some basic data structures, let’s\nget an…Micah ShuteCantor’s Paradise\n[https://medium.com/cantors-paradise/dijkstras-shortest-path-algorithm-in-python-d955744c7064]\nTurn Python Scripts into Beautiful ML ToolsIn my experience, every nontrivial\nmachine learning project is eventually stitched together with bug-ridden and\nunmaintainable internal tools. These tools — often a patchwork of Jupyter\nNotebooks…Adrien TreuilleTowards Data Science\n[https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace]\njyhjinghwang/SegSortSegSort: Segmentation by Discriminative Sorting of Segments\n- jyhjinghwang/SegSortjyhjinghwangGitHub\n[https://github.com/jyhjinghwang/SegSort]\nhttps://docs.python-guide.org/writing/tests/\n\nhttps://www.bloomberg.com/news/features/2019-09-25/polypropylene-plastic-can-finally-be-recycled\n\nhttps://lectures.quantecon.org/_downloads/pdf/py/Quantitative Economics with\nPython.pdf\n[https://lectures.quantecon.org/_downloads/pdf/py/Quantitative%20Economics%20with%20Python.pdf]",
                    "feature_image": "https://cdn.hackersandslackers.com/roundup/125.jpg",
                    "featured": False,
                    "status": "published",
                    "visibility": "public",
                    "email_recipient_filter": "none",
                    "created_at": "2020-03-02T08:07:44.000Z",
                    "updated_at": "2020-03-06T03:48:11.000Z",
                    "published_at": "2020-03-04T12:00:00.000Z",
                    "custom_excerpt": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "authors": [
                        {
                            "id": "5dc42cb612c9ce0d63f5bf39",
                            "name": "Mister Man",
                            "slug": "man",
                            "email": "fake@example.com",
                            "profile_image": "https://cdn.hackersandslackers.com/authors/mattavi@2x.jpg",
                            "cover_image": "https://cdn.hackersandslackers.com/2020/03/lynxy.jpg",
                            "bio": "Supervillain in somebody's action hero movie. Experienced a radioactive freak accident at a young age which rendered him part-snake and strangely adept at Python.\n\n",
                            "website": "https://github.com/mattalhonte",
                            "location": "Center of the Universe",
                            "twitter": "@MisterMan",
                            "status": "active",
                            "tour": '["getting-started"]',
                            "last_seen": "2020-11-20T05:32:19.000Z",
                            "created_at": "2018-04-16T03:42:48.000Z",
                            "updated_at": "2020-11-20T05:32:19.000Z",
                            "roles": [
                                {
                                    "id": "5dc42c6b4b25bc0d13674448",
                                    "name": "Administrator",
                                    "description": "Administrators",
                                    "created_at": "2019-11-07T14:38:35.000Z",
                                    "updated_at": "2019-11-07T14:38:35.000Z",
                                }
                            ],
                            "url": "https://hackersandslackers.app/author/matt/",
                        }
                    ],
                    "tags": [
                        {
                            "id": "5dc42cb712c9ce0d63f5bf54",
                            "name": "Roundup",
                            "slug": "roundup",
                            "description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "visibility": "public",
                            "meta_title": "Data Science News Daily Roundup",
                            "meta_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "created_at": "2018-04-16T23:26:05.000Z",
                            "updated_at": "2020-08-04T22:14:59.000Z",
                            "og_title": "Data Science News Daily Roundup",
                            "og_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "twitter_title": "Data Science News Daily Roundup",
                            "twitter_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                            "accent_color": "#897ecb",
                            "url": "https://hackersandslackers.app/tag/roundup/",
                        }
                    ],
                    "primary_author": {
                        "id": "5dc42cb612c9ce0d63f5bf39",
                        "name": "Mister Man",
                        "slug": "man",
                        "email": "fake@example.com",
                        "profile_image": "https://cdn.hackersandslackers.com/authors/mattavi@2x.jpg",
                        "cover_image": "https://cdn.hackersandslackers.com/2020/03/lynxy.jpg",
                        "bio": "Supervillain in somebody's action hero movie. Experienced a radioactive freak accident at a young age which rendered him part-snake and strangely adept at Python.\n\n",
                        "website": "https://github.com/mattalhonte",
                        "location": "Center of the Universe",
                        "twitter": "@MisterMan",
                        "status": "active",
                        "tour": '["getting-started"]',
                        "last_seen": "2020-11-20T05:32:19.000Z",
                        "created_at": "2018-04-16T03:42:48.000Z",
                        "updated_at": "2020-11-20T05:32:19.000Z",
                        "roles": [
                            {
                                "id": "6dc42c6b4b25bc0d1367444c",
                                "name": "Owner",
                                "description": "Blog Owner",
                                "created_at": "2019-11-07T14:38:35.000Z",
                                "updated_at": "2019-11-07T14:38:35.000Z",
                            }
                        ],
                        "url": "https://hackersandslackers.app/author/matt/",
                    },
                    "primary_tag": {
                        "id": "5dc42cb712c9ce0d63f5bf54",
                        "name": "Roundup",
                        "slug": "roundup",
                        "description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "visibility": "public",
                        "meta_title": "Data Science News Daily Roundup",
                        "meta_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "created_at": "2018-04-16T23:26:05.000Z",
                        "updated_at": "2020-08-04T22:14:59.000Z",
                        "og_title": "Data Science News Daily Roundup",
                        "og_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "twitter_title": "Data Science News Daily Roundup",
                        "twitter_description": "Subscribe to our daily roundups of top data science news articles, slimmed down to only the good stuff.",
                        "accent_color": "#897ecb",
                        "url": "https://hackersandslackers.app/tag/roundup/",
                    },
                    "url": "https://hackersandslackers.app/lynx-roundup-march-4th-2020/",
                    "excerpt": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "reading_time": 2,
                    "send_email_when_published": False,
                    "og_title": "Lynx Roundup, March 4th 2020",
                    "og_description": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "twitter_title": "Lynx Roundup, March 4th 2020",
                    "twitter_description": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                    "meta_title": "Lynx Roundup, March 4th 2020",
                    "meta_description": "Quantum economics with Python! Turn Python scripts into ML tools!  Dijkstra’s 'shortest path' algorithm in Python!",
                },
                "previous": {},
            }
        }


class NetlifyUserMetadata(BaseModel):
    avatar_url: Optional[str] = Field(None, example="https://example.com/dsfdsf.jpg")
    full_name: str = Field(None, example="Fake Name")
    signupSource: Optional[str] = Field(None, example="react-netlify-identity-widget")


class NetlifyUserAppMetadata(BaseModel):
    provider: Optional[str] = Field(None, example="google")


class NetlifyAccount(BaseModel):
    id: str = Field(None, example="4e7c4f1b-e51a-4abb-8a58-105483724713")
    aud: Optional[str] = Field(None, example=None)
    role: Optional[str] = Field(None, example=None)
    email: str = Field(None, example="fake@example.com")
    confirmation_sent_at: Optional[str] = Field(None, example="2021-03-04T07:06:54Z")
    app_metadata: NetlifyUserAppMetadata
    user_metadata: NetlifyUserMetadata
    created_at: datetime = Field(None, example="2019-11-07 14:38:35")
    updated_at: datetime = Field(None, example="2020-12-20 10:54:20")


class NetlifyUserEvent(BaseModel):
    event: str = Field(None, example="signup")
    instance_id: str = Field(None, example="dc76yfi-94b8-4b0f-8d45-gdffg76i")
    user: NetlifyAccount


class Member(BaseModel):
    id: Optional[str] = Field(None, example="604393b784657849344434dfe31d")
    uuid: Optional[str] = Field(None, example="e34567d5-5ac5-234e-4356-02f624cd3bbd")
    email: Optional[str] = Field(None, example="fake@example.com")
    name: Optional[str] = Field(None, example="Name")
    note: Optional[str] = Field(None, example="")
    subscribed: Optional[bool] = Field(None, example=True)
    created_at: Optional[datetime] = Field(None, example="2021-03-06T14:37:42.846Z")
    updated_at: Optional[datetime] = Field(None, example="2021-03-06T14:37:42.846Z")
    labels: Optional[List[Optional[str]]] = Field([], example=[])
    avatar_image: Optional[str] = Field(
        None, example="https://gravatar.com/avatar/c611f62ef"
    )
    comped: Optional[bool] = Field(bool, example=False)
    email_count: Optional[int] = Field(bool, example=0)
    email_opened_count: Optional[int] = Field(bool, example=0)

    class Config:
        schema_extra = {
            "current": {
                "id": "604393b65d4a222434dfe31d",
                "uuid": "e90320d5-5ac5-490e-9814-02f624cd3bbd",
                "email": "toddbirchard+fakeinfo@gmail.com",
                "name": "Fake Name",
                "subscribed": True,
                "created_at": "2021-03-06T14:37:42.846Z",
                "updated_at": "2021-03-06T14:37:42.846Z",
                "labels": [],
                "avatar_image": "https://gravatar.com/avatar/c611f62ef75d2fafe58ffb61661b22e0?s=250&d=blank",
                "comped": False,
                "email_count": 0,
                "email_opened_count": 0
            },
            "previous": {}
        }


class NewGhostMember(BaseModel):
    current: Optional[Member]
    previous: Optional[Member]


class GhostMemberEvent(BaseModel):
    member: NewGhostMember


class SubscriptionWelcomeEmail(BaseModel):
    from_email: str = Field(None, example="fake@example.com")
    to_email: str = Field(None, example="recipient@example.com")
    subject: str = Field(None, example="Welcome to Hackers & Slackers")
    template: str = Field(None, example="This is an email")

    class Config:
        schema_extra = {
            "from_email": "fake@example.com",
            "to_email": "recipient@example.com",
            "subject": "Welcome to Hackers & Slackers",
            "template": "This is an email",
        }


class SMS:
    phone_recipient: str = Field(None, example="+5556461738")
    phone_sender: str = Field(None, example="+5553451738")
    date_sent: str = Field(None, example="2021-03-06T14:37:42.846Z")
    message: str = Field(None, example="u up?")

    class Config:
        schema_extra = {
            "phone_recipient": "5554201738",
            "phone_sender": "5551738420",
            "date_sent": "2020-12-02T02:59:13.642Z",
            "message": "u up?",
        }


class GithubIssue:
    issue: Dict[str, Any]

    class Config:
        schema_extra = {
            "issue": {
                "time": "2020-12-02T02:59:13.642Z",
                "status": "open",
                "trigger": {
                    "type": "github",
                    "repo": "toddbirchard/jamstack-api",
                    "title": "Jamstack API",
                    "user": "fakeuser",
                    "action": "opened",
                },
            },
        }


class PostBulkUpdate(BaseModel):
    inserted: dict = Field(None)
    updated: dict = Field(None)

    class Config:
        schema_extra = {
            "inserted": {"count": 0, "posts": []},
            "updated": {
                "count": 0,
                "posts": {
                    "tags_meta_og_image.sql": 0,
                    "tags_meta_og_description.sql": 0,
                    "lynx_plaintext_https.sql": 0,
                    "tags_meta_twitter_title.sql": 0,
                    "feature_image_cdn_urls.sql": 0,
                    "title_escape_quotes.sql": 0,
                    "description_escape_quotes.sql": 0,
                    "plaintext_cdn_urls.sql": 0,
                    "tags_meta_twitter_description.sql": 0,
                    "tags_meta_twitter_image.sql": 0,
                    "email_unset_newsletter.sql": 0,
                    "tags_meta_og_title.sql": 0,
                    "lynx_html_https.sql": 0,
                    "html_cdn_urls.sql": 0,
                },
            },
        }
