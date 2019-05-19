#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = 'Ricarda_Erhart'


##
##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:

    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)

        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"

    def annotate_vcf_file(self):
        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))

                if counter >= 899:
                    break

        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'

        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')

        ## TODO now do something with the 'annotation_result'
        dic_annotation_results=json.loads(annotation_result)
        return dic_annotation_results  ## return the data structure here


    def get_list_of_genes(self, dic_annotation_results):
        genenames=[]
        for vcf in dic_annotation_results:
            if 'snpeff' in vcf:
                for annotation in vcf['snpeff']['ann']:
                    if isinstance(annotation, dict) == True:
                        if annotation['genename'] not in genenames:
                            genenames.append(annotation['genename'])
            if 'dbnsfp' in vcf:
                if 'genename' in vcf['dbnsfp']:
                    if vcf['dbnsfp']['genename'] not in genenames:
                        genenames.append(vcf['dbnsfp']['genename'])
            if 'cadd' in vcf:
                if 'gene' in vcf['cadd']:
                    for annotation in vcf['cadd']['gene']:
                        if 'genename' in annotation:
                            if isinstance(annotation, dict) == True:
                                if annotation['genename'] not in genenames:
                                    genenames.append(annotation['genename'])
        print('Names of genes in Annotation: ', genenames)


    def get_num_variants_modifier(self, dic_annotation_results):
        vcf_mod=0
        for vcf in dic_annotation_results:
            if 'snpeff' in vcf:
                for annotation in vcf['snpeff']['ann']:
                    if isinstance(annotation, dict) == True:
                        if annotation['putative_impact'] == "MODIFIER":
                            vcf_mod+=1
                            break
        print('Number of variants with putative_impact "MODIFIER": ', vcf_mod)



    def get_num_variants_with_mutationtaster_annotation(self, dic_annotation_results):
        mutationtaster=0
        for vcf in dic_annotation_results:
            if 'dbnsfp' in vcf:
                if 'mutationtaster' in vcf['dbnsfp']:
                    mutationtaster+=1
        print("Number of variants with a 'mutationtaster' annotation: ", mutationtaster)


    def get_num_variants_non_synonymous(self, dic_annotation_results):
        nsyn=0
        for vcf in dic_annotation_results:
            if 'cadd' in vcf:
                if vcf['cadd']['consequence'] == "NON_SYNONYMOUS":
                    nsyn+=1
        print("Number of variants with 'consequence' 'NON_SYNONYMOUS': ", nsyn)


    def view_vcf_in_browser(self):
        ## Document the final URL here
        print("URL for vcf in ibio: https://vcf.iobio.io/?species=Human&build=GRCh38")


    def print_summary(self):
        print("Print all results here")
        dic_annotation_results = self.annotate_vcf_file()
        self.get_list_of_genes(dic_annotation_results)#
        self.get_num_variants_modifier(dic_annotation_results)
        self.get_num_variants_with_mutationtaster_annotation(dic_annotation_results)
        self.get_num_variants_non_synonymous(dic_annotation_results)
        self.view_vcf_in_browser()


def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")


if __name__ == '__main__':
    main()
