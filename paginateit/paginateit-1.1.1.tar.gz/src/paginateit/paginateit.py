"""Main module."""

# Paginateit

''' Module help us get the right values while creating API calls using pagination method.


pg.page(1700, 8) --> Max records availabe in all pages is 1700 and are creating 8 threads / loops (We see skip[1-9] values)
pg.page(90005, 6) --> Max records availabe in all pages is 90005 and are creating 6 threads / loops (We see skip[1-7] values)
pg.page(5025) --> Max records availabe in all pages is 1700 and are creating 8 threads /loops (We see skip[1-3] values)

pg.page(count, max_workers) # max_workers defaults to 2 unless specified

--> Access the dynamic calculated variables as shown below:

pg.skip1, pg.skip3, pg.limit2, pg.flimit4, pg.count2

'''


def page(count, max_workers=2):
    ndiv = int(count/max_workers)
    sk = 0
    lm = ndiv
    # Loop based on count and calcuates the end values required for pagination
    for mw in range(1, (max_workers+2)):
        globals()[f"skip{mw}"] = sk
        globals()[f"limit{mw}"] = lm
        globals()[f"flimit{mw}"] = str(lm)[1:].lstrip("0")
        globals()[f"count{mw}"] = lm - sk
        sk = sk + ndiv
        lm = lm + ndiv
