for idx, c in enumerate(self.cells[:9]):
    if self.issolved() ==True:
        break
    if c.value is None:

        options = list(c.options)
        for a in options:
            print idx,c,a

            success = self.test(idx, a)
            print success
            if success==True:
                continue



def option_count(cells):
    return sum([ c.options.__len__() if isinstance(c.options, list) else 0  for c in cells] )