from Bio import SeqIO
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline, NcbimakeblastdbCommandline
from os.path import exists
from os import remove
import wget
import gzip
import shutil

blast = '/usr/local/ncbi/blast/bin/blastp'
makeblast = '/usr/local/ncbi/blast/bin/makeblastdb'
name_query = 'cov2.fasta.gz'
name_subject = 'hpv.fasta.gz'
subject = '.'.join(name_subject.split('.')[:-1])
query = '.'.join(name_query.split('.')[:-1])
subject_out = subject + '.out'
query_out = query + '.out'
url_hpv = 'http://eng1.mu.edu.tr/~tugba/Bioinformatics/hpv.fasta.gz'
url_cov = 'http://eng1.mu.edu.tr/~tugba/Bioinformatics/cov2.fasta.gz'
result = 'results.xml'
format = 'fasta'
mode = 'rt'
literal_query = name_query.split('.')[0].upper()
literal_subject = name_subject.split('.')[0].upper()


def unzip(filename):
    with gzip.open(filename, 'rb') as f_in:
        with open('.'.join(filename.split('.')[:-1]), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


if not exists(result):
    if not exists(name_subject):
        print(name_subject, 'file does not exists in path downloading...')
        file_hpv = wget.download(url_hpv)

    if not exists(name_query):
        print(name_query, 'file does not exists in path downloading...')
        file_cov = wget.download(url_cov)

    unzip(name_subject)
    unzip(name_query)
    subject_cline = NcbimakeblastdbCommandline(cmd=makeblast, dbtype="prot", input_file=subject,
                                               out=subject_out)
    query_cline = NcbimakeblastdbCommandline(cmd=makeblast, dbtype="prot", input_file=query,
                                             out=query_out)
    print(subject_cline)
    s_stdout, s_stderr = subject_cline()
    q_stdout, q_stderr = query_cline()

    # cov2 = SeqIO.parse(gzip.open(name_query, mode), format=format)
    # hpv = SeqIO.parse(gzip.open(name_subject, mode), format=format)
    result_cline = NcbiblastpCommandline(cmd=blast, query=query, db=subject_out, out=result, num_threads=4,
                                         evalue=0.005, outfmt=5)
    print(result, 'file does not exists in path re-generating...')
    print(result_cline)
    r_stdout, r_stderr = result_cline()
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
