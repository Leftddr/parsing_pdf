import textract
import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers

if len(sys.argv) < 3:
    print('Usage : {}, filename wannabe word'.format(sys.argv[0]))
    sys.exit(1)

min_str_length = 15
process_title_list = []
final_dict = dict()
final_dict['blockchain'] = dict()
es = Elasticsearch('localhost:9200')

def textract_for_title(text):

    text = text.decode()
    title = True

    process_title = ''
    for index, tmp_text in enumerate(text):
        if index > 0 and text[index - 1] == '\n' and text[index] >= '1' and text[index] <= '9' and text[index + 1] == ' ' and text[index + 2] >= 'A' and text[index + 2] <= 'Z':
            title = True
        elif title and tmp_text == '\n':
            title = False
            process_title_list.append(process_title)
            process_title = ''
            
        if title:
            process_title += str(tmp_text)

def textract_to_split_dot(text):
    text = text.decode()

    process_dot = ''
    tmp_index = 0
    tmp_index_list = []

    for index, tmp_str_dot in enumerate(text):
        if tmp_str_dot == '.':
            tmp_index = index
            if index + 1 < len(text) and (text[index + 1] == ' ' or text[index + 1] == '\n'):
                if text[index - 1] == 'l' and text[index - 2] == 'a':
                    continue
                tmp_index_list.append(tmp_index)

    cur_pos = 0
    for index, tmp_str_dot in enumerate(text):
        if cur_pos < len(tmp_index_list) and index == tmp_index_list[cur_pos]:
            process_dot += '}'
            cur_pos += 1
        else:
            process_dot += tmp_str_dot 
    
    split_dot = process_dot.split('}')
    final_split_dot = []
    for tmp_split_dot in split_dot:
        if len(tmp_split_dot) < min_str_length:
            continue
        final_split_dot.append(tmp_split_dot.replace('\n', ' '))
    return final_split_dot

def textract_to_split_title(retval):
    for title_index, title in enumerate(process_title_list):
        #sentence_put = dict()
        cur_index = 0
        bool_put = False
        final_dict['blockchain'][title] = []
       
        for index, sentence in enumerate(retval):
            pos1 = sentence.find(title)
            pos2 = -1
            if title_index < len(process_title_list) - 1:
                pos2 = sentence.find(process_title_list[title_index + 1])
            
            if pos1 != -1:
                tmp_sentence = sentence.replace(title, "\n")
                retval[index] = tmp_sentence
                sentence_put = dict()
                sentence_put[title + '_'] = tmp_sentence
                final_dict['blockchain'][title].append(sentence_put)
                cur_index += 1
              
                bool_put = True
            elif pos2 != -1:
                break
            
            if bool_put:
                sentence_put = dict()
                sentence_put[title + '_'] = sentence
                final_dict['blockchain'][title].append(sentence_put)
                cur_index += 1
       
        #final_dict['blockchain'][title] = sentence_put
    
    #ft_json = json.dumps(final_dict, indent = 4, sort_keys = True)
    #print(ft_json)

def connect_to_elastic():
    es = Elasticsearch('localhost:9200')

def make_index(index_name):
    if es.indices.exists(index = index_name):
        es.indices.delete(index = index_name)
    es.indices.create(index = index_name)

if __name__ == '__main__':
    text = textract.process(sys.argv[1])
    textract_for_title(text)
    retval = textract_to_split_dot(text)
    textract_to_split_title(retval)

    # dictionary to json #
    ft_json = json.dumps(final_dict, indent = 4, sort_keys = True)
    # Temporary index_name #
    index_name = 'blockchain'
    connect_to_elastic()
    make_index(index_name)

    es.index(index = index_name, doc_type = 'example1', body = json.dumps(final_dict, indent = 4, sort_keys = True))
    es.indices.refresh(index = index_name)

    results = es.search(index = index_name, body = { 'query' : { 'bool' : { 'must' : [ { 'match' : { process_title_list[1] + '_' : sys.argv[2] }}]}}})
    #result2 = es.search(index = index_name, body = {'query' : {'match_all' : {}}})

    #print(json.dumps(results, indent = 4))
    for result in results['hits']['hits']:
        print('source : ', result['_source'])
    