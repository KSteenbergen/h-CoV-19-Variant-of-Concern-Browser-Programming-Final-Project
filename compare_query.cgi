#!/usr/local/bin/python3
import jinja2
import mysql.connector
import cgi

#Instantiate a FieldStorage object
form = cgi.FieldStorage()
varA = form.getvalue('VarA')
varB = form.getvalue('VarB')

#Load template
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('compare.html')          

def main():
    #Create an error message if the variants chosen are the same (Avoids 500 error)
    if varA == varB:
        err = "Try Again: Choose two DIFFERENT variants to compare"
        return err

    shared_mt = []
    varA_list = []
    varB_list = []

    conn = mysql.connector.connect(user='ksteenb1', password='Programming123!', 
        host='localhost', database='ksteenb1')
    
    curs = conn.cursor()
    qry = """ 
    SELECT   v.variant,  r.gene,  r.product, r.aa_length,  v.mt_type as mutation, 
    v.concise as event, count(mt_code) as count, v.country      
    FROM   variant v        
    JOIN reference r ON v.gene = r.gene      
    WHERE   v.variant = %s OR v.variant = %s 
    GROUP BY   v.mt_code      
    ORDER BY r.begin;
    """
    curs.execute(qry, (varA, varB,))
    #Place the query results into a dictionary entry
    for(variant, gene,  product, aa_length,  mutation, event, count, country) in curs:
        unique_dict= {'variant':variant, 'gene':gene, 'product':product, 'aa_length':aa_length, 
        'mutation':mutation, 'event':event, 'count':count, 'country':country }
        #Separate the shared mutations and append to shared list
        if unique_dict.get('count') > 1:
            shared_mt.append(unique_dict)
        #Separate the unique mutations and append to appropriate variant lists
        elif unique_dict.get('count') == 1:
            if unique_dict.get('variant') == varA:
                countryA = unique_dict.get('country')
                varA_list.append(unique_dict)
            elif unique_dict.get('variant') == varB:
                varB_list.append(unique_dict)
                countryB = unique_dict.get('country')
    #Return values needed to populate template file          
    return shared_mt, varA_list, varB_list, varA, varB, countryA, countryB

    conn.commit()
    curs.close()

if __name__ == '__main__':
    results_list = main()

err = "Try Again: Choose two DIFFERENT variants to compare"

print("Content-Type: text/html\n\n")
if results_list == err:
    print(template.render(message = results_list))
else:
    print(template.render(shared_list = results_list[0], varA_list = results_list[1], 
varB_list = results_list[2], variantA = results_list[3], variantB = results_list[4],
countryA = results_list[5], countryB = results_list[6]))