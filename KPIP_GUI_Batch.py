#!/usr/bin/env python

import sys
import os
import glob
import re
import argparse
from datetime import date
from gooey import Gooey, GooeyParser

@Gooey(program_name='Kmer Pathogen Identification Pipeline', 
        default_size=(720, 900))


def main():

    now = date.today()
    local_path = os.path.dirname(os.path.realpath(__file__))
    #print(local_path)
    db_path = os.path.expanduser(f"~/KPIP/db")
    
    mash_parser = f"{local_path}/mash_screen_parser.py"
    kma_parser= f"{local_path}/kma_screen_parser.py"

    parser = GooeyParser(description="Determine Pathogen Identity and Antibiotic Profile")
    io_box = parser.add_argument_group("Input Output", gooey_options={'show_border': True, 'columns': 1})
    io_box.add_argument('-i', '--InputFolder', help="Input folder containing fasta, fastq, or fasta.gz/fastq.gz file", required=True, widget='DirChooser')
    io_box.add_argument('-o', '--OutputFolder', help=f"Output Folder. Default is ~/KPIP_results/pathogen_id_{now}", required=False, default=f"~/KPIP_results/pathogen_id_{now}")

    options_box = parser.add_argument_group("Options", gooey_options={'show_border': True, 'columns': 2})

    options_box.add_argument('-t', '--threads', help="Use x threads. More is faster if your computer can support it", type=int, required=False, default=4)
    options_box.add_argument('-n', '--top_id', help="Display top N matches", type=int, required=False, default=5)
    
    method = options_box.add_mutually_exclusive_group("File Type", gooey_options={'show_border': True})
    method.add_argument('--Illumina', help = 'Low Error Short Reads such as Illumina', action='store_true')
    method.add_argument('--Nanopore', help = 'High Error Long Reads such as Nanopore', action='store_true')
    method.add_argument('--LongSequence', help = 'Long Sequences such as Assembly or PacBioCCS', action='store_true')

    db = parser.add_argument_group("Databases", gooey_options={'show_border': True, 'columns': 1})
    db.add_argument('-rg', '--Pathogen_DB', help=f"Kmer Pathogen Library. Default is {db_path}/refseq.genomes.k21s1000.msh", required=False, default=f"{db_path}/refseq.genomes.k21s1000.msh", widget = 'FileChooser')
    db.add_argument('-rp', '--Plasmid_DB', help=f"Kmer Pathogen Library. Default is {db_path}/refseq.plasmid.k21s1000.msh", required=False, default=f"{db_path}/refseq.plasmid.k21s1000.msh", widget = 'FileChooser')
    db.add_argument('-ra', '--AMR_DB', help=f"Antibiotic Resistance Database. Default is {db_path}/resfinder_res/resistance.name", required=False, default=f"{db_path}/resfinder_res/resistance.name", widget='FileChooser')
    
    args = parser.parse_args()

    AMR_DB = os.path.splitext(args.AMR_DB)[0]
    AMR_DB = os.path.splitext(AMR_DB)[0]

    files = sorted([f for f in glob.glob(args.InputFolder+"/**", recursive = True) if re.search(r'(.*)\.((fastq|fq|fasta|fna)(|\.gz))$', f)])

    OutputFolder = os.path.expanduser(args.OutputFolder)
    #os.system(f"mkdir -p {OutputFolder}/results")


    for i in range(0, len(files)):

        base = os.path.splitext(os.path.basename(files[i]))[0]
        base = os.path.splitext(base)[0]
        os.system(f"mkdir -p {OutputFolder}/results_{base}")

        mashscreen_cmd = f"mash screen -w -p {args.threads} {args.Pathogen_DB} {files[i]} | sort -gr > {OutputFolder}/results_{base}/pathogen_id.out"
        mash_pathogen_parser_cmd = f"{mash_parser} -i {OutputFolder}/results_{base}/pathogen_id.out -o {OutputFolder}/summary_{base}.txt -n {args.top_id} -m 'Pathogen Identification:'"
        mashscreen_plasmid_cmd = f"mash screen -w -p {args.threads} {args.Plasmid_DB} {files[i]} | sort -gr > {OutputFolder}/results_{base}/plasmid_id.out"
        mash_plasmid_parser_cmd = f"{mash_parser} -i {OutputFolder}/results_{base}/plasmid_id.out -o {OutputFolder}/summary_{base}.txt -n {args.top_id} -m 'Plasmid Identification:'"

        if(args.Illumina):
            kma_cmd=f"kma -i {files[i]} -o {OutputFolder}/results_{base}/res -t_db {AMR_DB} -1t1"
        elif(args.Nanopore):
            kma_cmd=f"kma -i {files[i]} -o {OutputFolder}/results_{base}/res -t_db {AMR_DB} -bcNano -bc 0.7"
        elif(args.LongSequence):
            kma_cmd=f"kma -i {files[i]} -o {OutputFolder}/results_{base}/res -t_db {AMR_DB}"
        kma_ar_parser_cmd = f"{kma_parser} -i {OutputFolder}/results_{base}/res.res -o {OutputFolder}/summary_{base}.txt -m 'Antibiotic Resistance Identification:'"
    
        os.system(mashscreen_cmd)
        os.system(mash_pathogen_parser_cmd)
        os.system(mashscreen_plasmid_cmd)
        os.system(mash_plasmid_parser_cmd)
        os.system(kma_cmd)
        os.system(kma_ar_parser_cmd)

        f=open(f"{OutputFolder}/cmd_{base}.log", 'w+')
        f.write(mashscreen_cmd+'\n')
        f.write(mashscreen_plasmid_cmd+'\n')
        f.write(kma_cmd+'\n')
        f.close()


if __name__ == "__main__":
    sys.exit(main())
