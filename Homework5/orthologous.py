from Bio import SeqIO
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline
from os.path import exists
import wget
import gzip

blast = '/usr/local/ncbi/blast/bin/blastp'
name_query = 'cov2.fasta.gz'
name_subject = 'hpv.fasta.gz'
url_hpv = 'http://eng1.mu.edu.tr/~tugba/Bioinformatics/hpv.fasta.gz'
url_cov = 'http://eng1.mu.edu.tr/~tugba/Bioinformatics/cov2.fasta.gz'
result = 'results.xml'
format = 'fasta'
mode = 'rt'
literal_query = name_query.split('.')[0].upper()
literal_subject = name_subject.split('.')[0].upper()

if not exists(result):
    if not exists(name_subject):
        print(name_subject, 'file does not exists in path downloading...')
        file_hpv = wget.download(url_hpv)

    if not exists(name_query):
        print(name_query, 'file does not exists in path downloading...')
        file_cov = wget.download(url_cov)

    cov2 = SeqIO.parse(gzip.open(name_query, mode), format=format)
    hpv = SeqIO.parse(gzip.open(name_subject, mode), format=format)
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
                    print(f'{literal_query} sequence:', blast_result.query)
                    print(f'{literal_subject} sequence:', alignment.title)
                    print(f'{literal_query} sequence:', hsp.query[0:78])
                    print(f'{literal_subject} sequence:', hsp.sbjct[0:78])
                    # print(hsp.expect, hsp.score, hsp.positives, hsp.gaps)
