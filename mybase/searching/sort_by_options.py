
class SortBy:
    RELEVANCE = 1
    NEWEST = 2
    MOST_VIEWED = 3
    MOST_LIKED = 4

    def fromStr(s):
        strMatching = {
            "relevance": SortBy.RELEVANCE,
            "newest": SortBy.NEWEST,
            "most_liked": SortBy.MOST_LIKED,
            "most_viewed": SortBy.MOST_VIEWED
        }
        return strMatching.get(s, None)
