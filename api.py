# -*- coding: utf-8 -*-

import os
import json
from urllib import urlopen
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
#from urllib.request import urlopen, Request

# paginas com erros
# https://www.tuasaude.com/amoxilina-e-clavulanato-de-potassio/
# buscar forma de processar os resultados da pesquisa antes de retornas as informações do medicamento

app = Flask(__name__)

@app.route('/api/v1/medicine', methods=['GET'])

def getInformacoes():
    
    medicamento = []
    
    nome_medicamento = request.args.get('nome')
    
    print (nome_medicamento)
    
    html_doc = urlopen("https://www.tuasaude.com/{}/".format(nome_medicamento)).read()
    
    soup = BeautifulSoup(html_doc, "html.parser")
          
    nome = soup.find("h1", itemprop="name")
    
    if nome:
        resumo = soup.find("p")
        resumo2 = soup.find_all("p")[1]
        preco = soup.find_all("p")[2]
        indicacoes = soup.find_all("p")[3]
        #tem subtexto
        modo_de_uso = soup.find_all("p")[4]
        #tem subtexto
        efeitos = soup.find_all("p")[5]
        contraindicaoes = soup.find_all("p")[6]
        
        medicamento.append({
            'nome': nome.text,
            'resumo': resumo.text+' '+resumo2.text,
            'preço': preco.text,
            'indicações': indicacoes.text,
            'modo_de_uso': modo_de_uso.text,
            'efeitos_colaterais': efeitos.text,
            'contraindicações': contraindicaoes.text
        })
        
        return jsonify(informacoes = medicamento)
        
    else:
        return jsonify(informacoes = 'Sua busca não retornou resultados.')
        
  
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
