# folder with 1000s of PDFs
dest <- "C:/Users/alokg/Desktop/BLM"

# make a vector of PDF file names
myfiles <- list.files(path = dest, pattern = "pdf",  full.names = TRUE)

# convert each PDF file that is named in the vector into a text file 
# text file is created in the same directory as the PDFs
exe <- "D:\\Downloads\\xpdfbin-win-3.04\\bin32\\pdftotext.exe"

lapply(myfiles, function(i) system(paste(exe, paste0('"', i, '"')), wait = FALSE))
