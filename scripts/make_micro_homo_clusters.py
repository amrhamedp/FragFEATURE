import cPickle as pickle
from load_directorypaths import *
from load_datafiles import load_resatm_KB_ann, load_seqclusterid
from microenvironment_types import types
import cPickle as pickle

def main():
    prot_clusters = load_seqclusterid('95') 
    print 'File loaded'
    micro_clusters = cluster_micros(prot_clusters)
    outfile = 'micro_clusters.pvar'
    outfile = open(outfile,'w')
    pickle.dump(micro_clusters, outfile)

    return

################################################################################
def invert_dict(dict_by_prot):    

    dict_by_cluster = {}
    for prot, cluster_ID in dict_by_prot.iteritems():
        if cluster_ID not in dict_by_cluster:
            dict_by_cluster[cluster_ID] = [prot]
        else:
            dict_by_cluster[cluster_ID].append(prot)

    return dict_by_cluster

################################################################################
def cluster_micros(dict_by_tag):

    micro_clusters = {}
    for resatm in types:
        type_clusters = {}
        anndata = load_resatm_KB_ann(resatm)
        print "loaded annotations for %s" % (resatm)
        for micro_num, micro_ann in enumerate(anndata):
            # look up the protein the micro belongs to with micro.tag
            # then look up the cluster that protein belongs to
            try:
                clusterID = dict_by_tag[micro_ann.tag] 
                #print "%s %s with tag %s belongs to cluster %s" % (resatm, str(micro_num), micro_ann.tag, str(clusterID))
                if clusterID not in type_clusters:
                    #assign the micro line number to the cluster
                    type_clusters[clusterID] = [micro_num]
                else:
                    type_clusters[clusterID].append(micro_num)
            except KeyError:
                print "%s %s with tag %s has no cluster" % (resatm, str(micro_num), micro_ann.tag)
        # put the dictionary for this micro type into the master dictionary
        micro_clusters[resatm] = type_clusters

    return micro_clusters


################################################################################
if __name__ == "__main__":
    main()
