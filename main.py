class branching:
    def __init__(self,l,r):
        self.lt = l
        self.rt = r
    def __str__(self):
        """
        Essentialy, the print method will return the current branching, and all
        subsequent branchings, in the newick format. This will make integration
        with other packages easier.
        """
        if hasattr(self.lt,'lt'):
            ltxt = self.lt.__str__()
        else:
            ltxt = self.lt
        if hasattr(self.rt,'rt'):
            rtxt = self.rt.__str__()
        else:
            rtxt = self.rt
        s = '('+ltxt+','+rtxt+')'
        return s
    def has_spe(self,spe):
        """
        Find if a species is in the current branching and the
        current branching is a leaf
        ---
        Return the branching where the species was found
        """
        if (self.lt == spe) or (self.rt == spe):
            return self
        else:
            rt_res = None
            lt_res = None
            if hasattr(self.rt,'rt'):
                rt_res = self.rt.has_spe(spe)
                if not rt_res is None:
                    return rt_res
            if hasattr(self.lt,'rt'):
                lt_res = self.lt.has_spe(spe)
                if not lt_res is None:
                    return lt_res
    def update(self,anc,nbr):
        """
        Update a branching by replacing a species with another new
        branching
        """
        if self.lt == anc:
            self.lt = nbr
        else:
            self.rt = nbr
    def remove(self,spe):
        """
        Remove a species from a branching
        """
        if hasattr(self.rt,'lt'):
            if self.rt.lt == spe:
                self.rt = self.rt.rt
                return 1
            elif self.rt.rt == spe:
                self.rt = self.rt.lt
                return 1
            else:
                self.rt.remove(spe)
        if hasattr(self.lt,'lt'):
            if self.lt.rt == spe:
                self.lt = self.lt.lt
                return 1
            elif self.lt.lt == spe:
                self.lt = self.lt.rt
                return 1
            else:
                self.lt.remove(spe)
        return 0

class PhyloTree:
    def __init__(self,ancname='anc'):
        """
        create a new tree with a root and an ancestral species named ancname
        """
        self.struct = branching('root',ancname)
    def __str__(self):
        """
        We use the print method of the branching object
        """
        s = self.struct.__str__()
        return s
    def speciate(self,anc,off):
        self.struct.has_spe(anc).update(anc,branching(anc,off))
    def extinct(self,spe):
        self.struct.remove(spe)

iTree = PhyloTree('0')
iTree.speciate('0','0_0')
iTree.extinct('0')
iTree.speciate('root','1')
iTree.speciate('1','2')
iTree.speciate('0_0','3')
iTree.extinct('1')
print iTree
