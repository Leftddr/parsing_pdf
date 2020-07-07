import textract
import sys

if len(sys.argv) < 2:
    print('Usage : {}, filename'.format(sys.argv[0]))
    sys.exit(1)

if __name__ == '__main__':
    text = textract.process(sys.argv[1])
    text = text.decode()
    title = True

    process_title_list = []
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


        
    for tmp_title in process_title_list:
        print(tmp_title)    
  
