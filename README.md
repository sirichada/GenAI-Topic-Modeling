# AN OVERVIEW OF RESEARCH & RESEARCHERS: Topic Modeling GenAI Ethics
*Paper researched by Sirichada (Tingting)*

With the emergence of new technology, ethical principles must be established to guide research, interest, and investment towards beneficial yet moral purposes. In the space of generative artificial intelligence, a literature review must be done to assess areas of research that are in alignment with the public’s ethical considerations, such as originality and the value of self-expression. 

The purpose of this paper is to map out where the most value and research have been done on the ethics of AI that address people’s concerns– such as creatives, consumers, and businesses– and to lay a foundation for future research directions in these fields. 

## guide to repo structure
- **data:** includes data extracted from Crossref API and its iterations into cleaned the processed data
  - **reference graph data:** final node and edge data for reference graph. node refers to the paper while edge is the citation from a paper to another.
  - **topic graph data:** final node and edge data for topic graph. node refers to the topic while edge is the simliarity between the topics.
 - **figures:** graphs and figures from the paper
 - **gephi files:** gephi files of topic and reference graph for data visualization
 - **topic models:** original jupyter notebooks of different topic modeling algorithms used (BERTopic, LDA, and Top2Vec)
