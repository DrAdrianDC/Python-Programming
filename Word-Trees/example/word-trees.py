#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 22:55:59 2024

@author: adriandominguezcastro
"""

# Word Trees using Python

print("*************************************") 
print("**                                 **") 
print("**                                 **") 
print("**        WORD TREES               **")
print("**                                 **") 
print("**                                 **") 
print("*************************************") 


import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

#text = 'Machine learning is the art of turning data into insight, transforming complexity into simplicity.'

text = input("Insert the phrase: ")

# Generate word cloud
wordcloud = WordCloud(
    width=800, height=500, 
    background_color='white', 
    colormap='viridis', 
    max_words=100, 
    stopwords=STOPWORDS
).generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
#plt.title('Python Word Cloud', fontsize=20)
plt.savefig('figure.png', dpi=300)  # Save with better resolution
plt.show()
