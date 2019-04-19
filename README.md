OPENNLP statistični modeli za:
- prepoznavanje pojavnic, tj. besed in ločil (tokenizacija)
- oblikoslovnem označevanju besed (*POS tagging*)
- določanje osnovne oblike besed (lematizacija)
- prepoznavanje stavkov (segmentacija)
- prepoznavanje imenovanih entitet (*named entities recognition*)

### Uporaba

#### Ustvarite podmape

`mkdir data\dl`
`mkdir models`

#### Dolpoteg korpusov

`python dl.py`

#### Priprava OPENNLPju prijaznih podatkov

`python ner.py`

`python okrajsave.py`

#####Treniranje modelov

*Tokenizacija*

`opennlp TokenizerTrainer.conllu -model models\sl-token.bin -alphaNumOpt False -lang sl -data data/sl_ssj-ud_v2.4-train.conllu -encoding UTF-8`

*Oblikoslovno oblikovanje*

`opennlp POSTaggerTrainer.conllu -model models\sl-pos.bin  -lang sl -data data\sl_ssj-ud_v2.4-train.conllu -encoding UTF-8 -tagset u`

*Segmentacija*

`opennlp SentenceDetectorTrainer.conllu -model models\sl-sentence.bin  -lang sl -data data/sl_ssj-ud_v2.4-train.conllu -encoding UTF-8  -abbDict data/okr.xml -sentencesPerSample 15`

*Lematizacija*

`opennlp LemmatizerTrainerME.conllu -model models\sl-lemmatizer.bin -lang sl -data data/sl_ssj-ud_v2.4-train.conllu -encoding UTF-8 -tagset u`

*Imenovane entitete*

`opennlp TokenNameFinderTrainer -model models\sl-ner.bin -lang sl -data data\ner.txt -encoding UTF-8`

Vsi modeli se nahajajo v podmapi `models`. 
Parametri so privzeti; za več njih se posvetujte z [dokumentacijo](http://opennlp.apache.org/docs/1.9.1/manual/opennlp.html#tools.cli).

####SOLR

Kopirajte modele iz mape `models` v podmapo `opennlp` vašega SOLR jedra. Primer :

```
C:\{pot do solr}\SOLR-8.0.0\SERVER\SOLR\{CORE}
│   core.properties
├───conf
│   │   schema.xml
│   │   solrconfig.xml
│   └───opennlp
│           sl-lemmatizer.bin
│           sl-pos.bin
│           sl-sentence.bin
│           sl-token.bin
├───data
└───lib
        lucene-analyzers-opennlp-8.0.0.jar
        opennlp-tools-1.9.1.jar
        solr-analysis-extras-8.0.0.jar
```

V shemi uporabite: 
```xml

<analyzer type="index|query|...">
    <!-- drugi filtri-->
    <tokenizer  class="solr.OpenNLPTokenizerFactory"
             sentenceModel="opennlp\sl-sentence.bin"
             tokenizerModel="opennlp\sl-token.bin"/>
    <!-- drugi filtri -->
    <filter class="solr.OpenNLPPOSFilterFactory" posTaggerModel="opennlp\sl-pos.bin"/>
    <filter class="solr.OpenNLPLemmatizerFilterFactory" lemmatizerModel="opennlp\sl-lemmatizer.bin"/>
</analyzer>
```

Več v [dokumentaciji](https://lucene.apache.org/solr/guide/7_7/language-analysis.html#opennlp-integration).