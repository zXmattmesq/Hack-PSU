import PyPDF2
import os
import openai

# Open the PDF file in read-binary mode
infilename = 'Frontiers___Relationship_Between_Putative_eps_Genes_and_Production_of_Exopolysaccharide_in_Lactobacillus_casei_LC2W'
with open(infilename + '.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Save number of pages in pdf to num_pages
    num_pages = len(pdf_reader.pages)

    outfilename = infilename + '_summary' + '.txt'
    outputFile = open(outfilename, "w")

    openai.api_key = "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"

    # Read the text from each page, put into input.txt
    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        page_text = page.extract_text()
        
        prompt = "list the 5 most relevant topics within this text, please disregard any links:" + page_text

        outputMessage = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = [{"role": "user", "content": prompt}])
        out = outputMessage.choices[0].message.content

        outputFile.write(f"Page {page_number + 1}:\n{out}\n")

# Remember to replace 'your_file.pdf' with the path to your PDF file
