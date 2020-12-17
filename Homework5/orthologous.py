from Bio import Entrez, SeqIO, Blast
import wget
from os.path import exists
import gzip
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML

blast = '/usr/local/ncbi/blast/bin/blastp'
name_cov = 'cov2.fasta.gz'
name_hpv = 'hpv.fasta.gz'
url_hpv = 'http://eng1.mu.edu.tr/~tugba/Bioinformatics/hpv.fasta.gz'
url_cov = 'http://eng1.mu.edu.tr/~tugba/Bioinformatics/cov2.fasta.gz'
result = 'results.xml'

if not exists(result):
    if not exists(name_hpv):
        print(name_hpv, 'file does not exists in path downloading...')
        file_hpv = wget.download(url_hpv)

    if not exists(name_cov):
        print(name_cov, 'file does not exists in path downloading...')
        file_cov = wget.download(url_cov)

    cov2 = SeqIO.parse(gzip.open(name_cov, 'rt'), format="fasta")
    hpv = SeqIO.parse(gzip.open(name_hpv, 'rt'), format="fasta")
    cmdline = NcbiblastpCommandline(cmd=blast, query=cov2, db=hpv, out=result)
    print(result, 'file does not exists in path re-generating...')
    stdout, stderr = cmdline()
else:
    print('reading', result)
    result_handle = open(result)
    print('searching in', result)
    for blast_result in NCBIXML.parse(result_handle):
        for alignment in blast_result.alignments:
            for hsp in alignment.hsps:
                if hsp.expect < 5e-3:
                    print()
                    print('COV2 sequence:', blast_result.query)
                    print('HPV sequence:', alignment.title)
                    print('COV2 sequence:', hsp.query[0:78])
                    print('HPV sequence:', hsp.sbjct[0:78])
                    # print(hsp.expect, hsp.score, hsp.positives, hsp.gaps)
