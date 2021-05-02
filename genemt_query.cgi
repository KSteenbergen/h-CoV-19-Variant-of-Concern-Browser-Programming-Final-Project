#!/usr/local/bin/python3
import jinja2
import mysql.connector

# Load Template
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('genes.html')          

def main():
    results = []
    reference = []

    conn = mysql.connector.connect(user='ksteenb1', password='Programming123!', 
        host='localhost', database='ksteenb1')
    
    #This query gets the variant gene information.
    curs = conn.cursor()
    qry = """ 
    SELECT gene, variant, country,
    mt_type as mutation, verbose as event
    FROM  variant
    ORDER BY gene, variant; 
    """ 
    curs.execute(qry)
    for(gene, variant, country, mutation, event) in curs:
        entry_dict= {'gene':gene, 'variant':variant, 'country':country, 'mutation':mutation, 'event':event }
        results.append(entry_dict)
    
    #This query gets the reference gene information.
    curs = conn.cursor()
    qry = """ 
    SELECT *
    FROM  reference
    ORDER BY begin; 
    """ 
    curs.execute(qry)

    for(gene, altname, begin, end, length, product, aa_length) in curs:
        gene_dict= {'gene':gene, 'altname':altname, 'begin':begin, 'end':end, 
        'length':length, 'product':product, 'aa_length':aa_length }
        reference.append(gene_dict)
    #Return Variant and Reference gene information to populate template
    #Sorting by gene occurs in the template
    return results, reference

    conn.commit()
    curs.close()

if __name__ == '__main__':
    results_list = main()

print("Content-Type: text/html\n\n")
print(template.render(gene_mutations = results_list[0], reference = results_list[1]))