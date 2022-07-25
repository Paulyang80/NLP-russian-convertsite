from multiprocessing import context
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
import pandas as pd
import time
import os
import spacy
import csv
import ru_core_news_sm
# Create your views here.
def convert_view(request):
    print(request.POST)
    text_list = []
    pos_list = []
    lemma_list = []
    opos_list = []
    # file = request.POST.get('input_csv', False)
    try:
        file = request.FILES['input_csv']
    except MultiValueDictKeyError:
        file = False
    nlp = spacy.load("ru_core_news_sm")
    try:
        df = pd.read_csv(file, encoding='utf-8')
        ru_text = df['text']
        ru_list = []
        for sen in ru_text:
            ru_list.append(sen)
        for text in ru_list:
            sen = nlp(text)
            text_list.append(text)
            pos_sen = ""
            pos_wr = ""
            lemma_sen = ""
            for s in sen:
                pos_sen = pos_sen + s.text + '(' + s.pos_ +') '
            for s in sen:
                pos_wr = pos_wr + s.pos_ + " "
            for s in sen:
                if s.text != s.lemma_:
                    lemma_sen = lemma_sen + s.text + '('+ s.lemma_ + ') '
                else:
                    lemma_sen = lemma_sen + s.text + " "
            pos_list.append(pos_sen)
            opos_list.append(pos_wr)
            lemma_list.append(lemma_sen)
    except ValueError:
        print('')

    content = [{'text' : text,'pos' : pos,'opos':opos,'lemma':lemma} for text, pos, opos, lemma in zip(text_list, pos_list, opos_list, lemma_list)]
    context = {'content':content}
    return render(request, "index.html",context)