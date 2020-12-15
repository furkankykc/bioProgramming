from urllib.request import urlretrieve

import Bio.PDB
import Bio.PDB.PDBParser
from Bio.PDB import PDBList, Select

pdbl = PDBList()
# Use QUIET=True to avoid lots of warnings...
parser = Bio.PDB.PDBParser(QUIET=True)
# In[ ]:
pdbs = ["2WFJ", "2GW2"]
[urlretrieve(f'http://files.rcsb.org/download/{pdb}.pdb', f'{pdb}.pdb') for pdb in pdbs]

structure1 = parser.get_structure("2WFJ", "2WFJ.pdb")
structure2 = parser.get_structure("2GW2", "2GW2.pdb")
ppb = Bio.PDB.PPBuilder()
# In[ ]:

# Manually figure out how the query and subject peptides correspond...
# query has an extra residue at the front
# subject has two extra residues at the back
query = ppb.build_peptides(structure1)[0][1:]
target = ppb.build_peptides(structure2)[0][:-2]

query_atoms = [r['CA'] for r in query]
target_atoms = [r['CA'] for r in target]
# In[ ]:

superimposer = Bio.PDB.Superimposer()
superimposer.set_atoms(query_atoms, target_atoms)

print("Query and subject superimposed, RMS:", superimposer.rms)
superimposer.apply(structure2.get_atoms())


# In[ ]:
# class NotW(Select):
#     def accept_residue(self, residue):
#         return not residue.id[0] == "W"


# In[ ]:

# Write modified structures to one file
outfile = open("2GW2-modified.pdb", "w")
io = Bio.PDB.PDBIO()
io.set_structure(structure2)
io.save(outfile)
outfile.close()
