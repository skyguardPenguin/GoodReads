import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def getIndexContent(template):
    titleKeys = r.keys("title*")
    content = ""
    for titleKey in titleKeys:
        titleKey = titleKey.decode()
        id = titleKey.replace("title","")
        authorKey = f"author{id}"
        title = r.get(titleKey).decode()
        author= r.get(authorKey).decode()
        content += getIndexArticle(id, title,author) 
    return template.replace("@content",content)


def getBookContent(template, id):
    title = r.get(f"title{id}").decode()
    author = r.get(f"author{id}").decode()
    preface = r.get(f"preface{id}").decode()
    return template.replace("@content", getBookSection(title,author,preface))

def getSearchContent(template, match_list):#match list contiene los title keys de los libros cuya información coincidió con el patrón de búsqueda.
    content = ""
    for titleKey in match_list:
        id = titleKey.replace("title","")
        authorKey = f"author{id}"
        title = r.get(titleKey).decode()
        author= r.get(authorKey).decode()
        content += getIndexArticle(id, title,author) 
    return template.replace("@content", content)






def getIndexArticle(id, title, author):
    return f"""
            <article class="art-libro" id="art-libro-{id}">
               <h2 class="art-libro__title"><a href="books/{id}">{title}</a></h2>
               <p class="art-libro__author">{author}</p>
            </article> 
            """

def getBookSection(title, author, preface):
    return  f"""
        <section class="book-section">
            <h2>{title}</h2>
            <p>{author}</p>
            <p>
               {preface}
            </p>
        </section>
            """
