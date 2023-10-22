import PyPDF2
import os
import openai
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

fileName = ""
alreadyUsedFiles = []

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        
        if not event.is_directory:
            
            fileName = str(os.path.basename(event.src_path))
            split = fileName.rfind('.')
            formatting = fileName[split:]
            subFileName = fileName[0:split]

            print(f'Name: {fileName}\ntype: {formatting}\nsubName: {subFileName}')
            
            if(formatting==".pdf"):
                
                if fileName in alreadyUsedFiles:
                    print("file already shortened")
                    
                else:
                    
                    alreadyUsedFiles.append(fileName)
                    with open(fileName, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        num_pages = len(pdf_reader.pages)

                        for page_number in range(num_pages):
                            
                            page = pdf_reader.pages[page_number]
                            page_text = page.extract_text()
                            outfilename = subFileName + str(page_number+1) + '.txt'
                            outputFile = open(outfilename, "w")
                            outputFile.write(f"Page {page_number + 1}:\n{page_text}\n")
                            
                counter = 0
                outputFile = open(subFileName+"big"+'.txt', "a+")

                notDone = True
                while notDone:
                    counter = counter + 1
                    try:
                        testCounter = counter+1
                        inp = subFileName+str(testCounter)+'.txt'
                        inputFile = open(inp, "r")
                    except:
                        notDone = False

                    inp = subFileName+str(counter)+'.txt'
                    inputFile = open(inp, "r")

                    prompt = "list the 5 most relevant topics within this text, please disregard any links:" + inputFile.read()
                    inputFile.close()

                    openai.api_key = "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"

                    outputMessage = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [{"role": "user", "content": prompt}])
                    out = outputMessage.choices[0].message.content

                    outputFile.write("page "+str(counter) + "\n"+out+"\n")

                outputFile.close()
                    
            else:
                print("please only use pdf files")
                

            

            #with open(event.src_path, 'r') as file:
                  #content = file.read()
                  #print(f'File contents: \n{content}')



if __name__ == "__main__":
    folder_to_watch = "C:\\Users\\chnyz\\AppData\\Local\\Programs\\Python\\Python311"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path = folder_to_watch, recursive = False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop

    observer.join()
