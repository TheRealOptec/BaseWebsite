
class SearchIn:
    TOPICS_IX = 0
    POSTS_IX = 1

    TOPICS = lambda: 1 << SearchIn.TOPICS_IX
    POSTS = lambda: 1 << SearchIn.POSTS_IX
    ALL = lambda: SearchIn.TOPICS() | SearchIn.POSTS()

    def getVal(val, ix):
        return val & (1 << ix)


