# GOParGenPy: A high throughput method to generate Gene Ontology data matrices

A fast python program, platform independent software tool to generate the binary data matrix showing the GO class membership, including parental classes, of a set of GO annotated genes. GOParGenPy is at least an order of magnitude faster than popular tools for Gene Ontology analysis and it can handle larger datasets than the existing tools. It can use any available version of the GO structure and allows the user to select the source of GO annotation. GO structure selection is critical for analysis, as we show that GO classes have rapid turnover between different GO structure releases. 

Additionally it can be customized to parse the directed acyclic graph (DAG) structure present in OBO (.obo) file of other ontologies such as human phenotype ontologies (HPO), Disease ontologies (DO), Plant ontologies (PO) etc.

# Publication:

  The details about the publication can be found here at:
  https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-14-242 
# Accessibility
The webpage and the original source code can be also be accessed here at:

    * http://ekhidna.biocenter.helsinki.fi/users/ajay/private/GOParGenPy.htm
Alternatively, the upadte version of GOParGenPy can also be accessed in this repository:

    * GO_anno_data/CODE/*.py (all the python source code)
    * GO_anno_data/CODE/README (Usage details with all different versions of GOParGenPy)
    * GO_annot_data/DATA/ (all different test data sets according to different formats)





