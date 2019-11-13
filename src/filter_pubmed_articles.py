#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 10:20:46 2019

@author: antonio
"""

import xml.etree.ElementTree as ET
import copy
import pandas as pd

path = '/home/antonio/Documents/Projects/Tasks/CodiEsp/Mesh2ICD10/'
filename = 'data/pubmed_result.xml'

def filter_pubmed_results(path_to_file, output_filename):
    ## Keep only Pubmed results with Mesh terms and Abstract
    ## Why abstract??? We want free full text, right??
    ## Or are we supplying only the abstract?
    
    root = ET.parse(path_to_file).getroot()
    root_new = ET.Element('root')
    
    # Keep results with abstract and Mesh terms
    count = 0
    for child in root:
        all_subel_tags = list(map(lambda x: x.tag, list(child.iter())))
        if (('MeshHeadingList' in all_subel_tags) & ('Abstract' in all_subel_tags)):
            # Create a copy
            member2 = copy.deepcopy(child)
            # Append the copy 
            root_new.append(member2)
            
            # count
            count += 1
                    
    tree = ET.ElementTree(root_new)
    tree.write(output_filename)

def get_mesh_terms(path_to_file, output_filename):
    ## Create CSV with Pubmed IDs and Mesh terms associated to that article
    
    root = ET.parse(path_to_file).getroot()
    
    colnames = ['PubMedID', 'Mesh_descriptor_ID', 'Mesh_descriptor_text',
                               'Mesh_qualifier_ID', 'Mesh_qualifier_text']
    c = 0
    df = pd.DataFrame(columns=colnames)
    for child in root:
        c = c + 1
        for element in child.iter():
            if element.tag == 'PMID':
                pubmedID = (element.text)
            if element.tag == 'MeshHeadingList':
                for header in element.iter():
                    if header.tag == 'MeshHeading':
                        desc_ui = header.find('DescriptorName').attrib['UI']
                        desc_text = header.find('DescriptorName').text
                        df = df.append(pd.Series([pubmedID, desc_ui, desc_text, '', ''],
                                                index=colnames), ignore_index=True)
                        qual_ui = []
                        qual_text = []
                        for qual in header.findall('QualifierName'):
                            qual_ui.append(qual.attrib['UI'])
                            qual_text.append(qual.text)
                            df = df.append(pd.Series([pubmedID, desc_ui, desc_text, qual.attrib['UI'], qual.text],
                                                index=colnames), ignore_index=True)
                            
        if c == 1000:
            print(c)
            c = 0
                            
    df.to_csv(output_filename, sep=';', header=colnames, index=False)
    
def get_all_mesh_terms(path_to_csv, output_filename):
    ## Get unique MeSH terms in our results and create a txt with them.
    df = pd.read_csv(path_to_csv, header=0, sep=';')
    mesh_terms = df['Mesh_descriptor_ID'].unique()
    pd.DataFrame(mesh_terms).to_csv(output_filename, index=False, header=False)


def main():
    filter_pubmed_results(path + filename, path + 'docs/filtered_results.xml')
    get_mesh_terms(path + 'docs/filtered_results.xml', path + 'docs/filtered_results.csv')
    get_all_mesh_terms(path + 'docs/filtered_results.csv', path + 'docs/mesh-codes.txt')

if __name__ == '__main__':
    main()
