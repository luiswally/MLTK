import metapy
import pytoml

class Ranker:
    # Constructor method of Ranker
    def __init__(self, tempInput):
        self.tempInput = tempInput
        self.tempInternalField = None
        self.foo() # set internal field to whatever it needs to be via foo()

    
    # implement BM25 out-of-box ranker then try training with weighed meta data
    def foo(self):
        pass

    
    
