from watson_developer_cloud import ToneAnalyzerV3 as TA
from flask import Flask, render_template, request
from nltk import Nonterminal, nonterminals, Production, CFG

# Add you API here
WATSON = {"password": "MFQ2QZexuGwa","username": "3f15db62-2795-45bc-824d-b7f6c6704958", "version": "2017-03-21"}  
# ^ API key
app = Flask(__name__)
senti_model = None
nt1 = Nonterminal('NP')
nt2 = Nonterminal('VP')
nt1.symbol()
nt1 == Nonterminal('NP')
nt1 == nt2
S, NP, VP, PP = nonterminals('S, NP, VP, PP')
N, V, P, DT = nonterminals('N, V, P, DT')
prod1 = Production(S, [NP, VP])
prod2 = Production(NP, [DT, NP])
prod1.lhs()
prod1.rhs()
prod1 == Production(S, [NP, VP])
prod1 == prod2
grammar=CFG.fromstring((open("english.txt")).read())
from nltk.parse import RecursiveDescentParser
rd = RecursiveDescentParser(grammar)

def analyse(data):
    try:
        senti_model = TA(**WATSON)
    except:
        print "Watson Not reachable"
    if senti_model is None:
        return {}
    return senti_model.tone(text=data)
    # ^This is the analysis part

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/senti', methods = ['GET', 'POST'])
def senti():
    global data
    result = request.form
    data = result['data']
    #^ gets data from form
    senti_dict = analyse(data) 
    data = str(data).split() 
    processed_text=[]
    for t in rd.parse(data):
        processed_text.append(t)                     
    return render_template('senti.html', line = str(processed_text).replace('Tree','-->'), list=senti_dict['document_tone']['tone_categories'])   
    #^renders senti.html present in templates

if __name__ == "__main__":
    app.run(port=5000)
