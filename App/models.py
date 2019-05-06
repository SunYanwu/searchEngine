class Doc:
    docId = 0
    tf = 0
    lf = 0

    def __init__(self,docId,tf,lf):
        self.docId = docId
        self.tf = tf
        self.lf = lf

    def __repr__(self):
        return(str(self.docId) + '\t' + str(self.tf) + '\t' + str(self.lf))

    def __str__(self):
        return(str(self.docId) + '\t' + str(self.tf) + '\t' + str(self.lf))
