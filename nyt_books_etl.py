# import requests, pickle, pathlib, re, time, and csv modules
import requests, pickle, pathlib, re, time, csv, os

# API process
API_KEY = os.environ['NYT_API_KEY']  # set this in your environment; never commit a real key
base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
# using the params parameter from the requests.get() method to pass in the API key and query
parameters={'q':'mental health','api-key':API_KEY}
response=requests.get(base_url,params=parameters)
# updating parameters
d_sn_filter='document_type:("article") AND section_name:("Books")'
# updating the value to the fq key in the parameters
parameters['fq']=d_sn_filter
# creating and adding date range parameters
parameters['begin_date']='20000101'
parameters['end_date']='20201231'
# adding a page parameter
parameters['page']=0
# printing out the parameters
print(parameters)

# testing the parameters
response=requests.get(base_url,params=parameters)
content=response.json()
# printing the number of hits
print(content['response']['meta']['hits'])

# creates directory to store keyword pickle files and processed data
nytimes_mental_health_keywords = pathlib.Path.cwd()/"nytimes_mental_health_keywords"
nytimes_mental_health_keywords.mkdir(exist_ok=True)

# iterating over the pages
# for loop where the range sets the number of pages to hit (10 articles/page)
for i in range(65):
    # try block to break the loop in the event that an error occurs
    try:
        pg_num=i
        file_name=f"keywords_pg{pg_num}"
        parameters['page']=i
        response=requests.get(base_url,params=parameters)
        content=response.json()
        # for loops where the keywords are extracted and saved to a pickle file when there is a page hit
        for d in content['response']['docs']:
            # creates a list for the keywords
            kw_list=[]
            for k in d['keywords']:
                # appends the value to the list kw_list
                kw_list.append(k['value'])
                with open(f"nytimes_mental_health_keywords/{file_name}",'wb') as p_file:
                    pickle.dump(kw_list,p_file)
        # timer set to 7 seconds to ensure the API doesn't block the repeated requests
        time.sleep(7)
    # breaks the loop and prints "Something went wrong" if an error occurs
    except:
        print("Something went wrong")
    
# creates a list for all the keywords
kw_list_all=[]
# gets the current working directory
cwd=pathlib.Path.cwd()
nytimes_kw_dir=cwd/"nytimes_mental_health_keywords"
# for loop with iterdir() function that iterates over all the files in the directory
for i in nytimes_kw_dir.iterdir():
    # opens/loads each file
    with open(i,'rb') as kw_file:
        kws=pickle.load(kw_file)
        # the list's values are iterated and appended to the list kw_list_all
        for kw in kws:
            kw_list_all.append(kw)

# prints the kw_list_all list             
# print(kw_list_all)
 
# creates a list for book inputs
book_inputs=[]
# for loop that searchs through the list kw_list_all
for kw in kw_list_all:
    # re.search looks for the pattern "(Book)"
    if re.search('\(Book\)',kw):
        # when it finds "(Book)", the find() locates where "(Book)" starts
        substring_end=kw.find("(Book)")
        # strips the book names of unwanted characters and appends them to the book_inputs list
        book_inputs.append(kw[:substring_end].strip())

# prints the book_inputs list
# print(book_inputs)

# API process
API_KEY = os.environ['NYT_API_KEY']  # set this in your environment; never commit a real key
base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
# using the params parameter from the requests.get() method to pass in the API key and query
parameters={'q':'mental health','api-key':API_KEY}
response=requests.get(base_url,params=parameters)
# updating parameters
d_sn_filter='document_type:("article") AND section_name:("Books")'
# updating the value to the fq key in the parameters
parameters['fq']=d_sn_filter
# creating and adding date range parameters
parameters['begin_date']='20000101'
parameters['end_date']='20201231'
# adding a page parameter
parameters['page']=0

# creates the function hit_counts which returns the number of hits each book has
def hit_counts(book_name):
    parameters['q']=book_name
    response_new=requests.get(base_url,parameters)
    content_new=response_new.json()
    return content_new['response']['meta']['hits']

# creates a list for the results
book_results = []
# for loop that iterates over every keyword
for b in book_inputs:
    b_dict = {}
    # sets the book names to the key book_name
    b_dict['book_name']=b
    # sets the number of hits to the key hit_count
    b_dict['hit_count']=hit_counts(b)
    # appends b_dict to the list book_results
    book_results.append(b_dict)
    # timer set to 7 seconds to ensure the API doesn't block the repeated requests
    time.sleep(7)

# creates a path within the nytimes_mental_health_keywords path
results_file = nytimes_kw_dir/"book_results.csv"

# opens results_file and calls 2 columns book_name and hit_count
# writes the book names in the first column and the number of hits in the second column
with results_file.open(mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['book_name', 'hit_count'])
    writer.writeheader()
    writer.writerows(book_results)