# Installing packages required for text processing and rendering word cloud 
install.packages("tm") 
install.packages("wordcloud")

# Loading the packages to the library
library(tm)
library(wordcloud)

# Setting your working directory
setwd("<Your Directory Path>")

# Reading CSV file with text data
dataCsv <- read.csv("<Your File Name>.csv", header = TRUE, sep = ",")

# Pushing the text into a corpus
dataCorpus <- Corpus(VectorSource(dataCsv$tweets))

# Inspecting the corpus
inspect(dataCorpus)

# Word Cloud Function 
wordCloudF <- function(df){
  
# Processing the text by removing punctuations, stopwords, numbers,
# converting the characters to lowercase and creating a term document matrix
tDm <- as.matrix(TermDocumentMatrix(df,control = list(removePunctuation = TRUE,
                                           stopwords = stopwords("english"), 
                                           removeNumbers = TRUE, 
                                           tolower = TRUE)))

# Getting the word counts in descending order 
wordFreq <- sort(rowSums(tDm), decreasing = TRUE) 

# Creating a data frame with words and their frequencies
tDmDf <- data.frame( word = names(wordFreq), freq = wordFreq)

# To select the properties of word cloud
# To look at the available color palettes options in color brewer user -> "display.brewer.all()"
wordcloud(tDmDf$word, tDmDf$freq, random.order=FALSE, max.words = 100, 
          colors=brewer.pal(8, "Dark2"))
}

# To render the word cloud
wordCloudF(dataCorpus)
