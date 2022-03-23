
from datetime import date
from distutils.command.clean import clean
from pickle import EMPTY_SET, EMPTY_TUPLE
from queue import Empty
from turtle import clear, goto
from PyQt5 import QtWidgets, uic, QtGui
import threading
import sys
import mysql.connector
import pandas as pd
import win32com.client as win32
from PySide6.QtWidgets import QApplication, QWidget

numero_id = 0

#Connection by MySql Server localhost with XAMP to simulation 
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cadastro_crm"
)

def salvar_dados_editados():
    global numero_id #utilizando a variavel do Def Editar_dados que é o numero da linha clicada
    #print(numero_id)
     
     #declarando varible das lineEdit criado com o Qt Designer
    
    nome = tela_editar.lineEdit.text()
    cpf = tela_editar.lineEdit_2.text()
    telefone = tela_editar.lineEdit_3.text()
    data_nasc = tela_editar.lineEdit_4.text()
    e_mail = tela_editar.lineEdit_5.text()
    recebimento = tela_editar.lineEdit_6.text()
    
    #Utilizando o comando cursor com o "banco" MySql acima definido e útilizando as variaveis em seus locais e fazendo "UPDATE SET" ao banco
    
    cursor = banco.cursor()
    cursor.execute("UPDATE cadastro_promocao SET nome = '{}', cpf = '{}', telefone = '{}', data_nasc = '{}', e_mail = '{}', recebimento = '{}' WHERE cpf = {}".format(nome, cpf, telefone, data_nasc, e_mail, recebimento, numero_id))
    banco.commit()

    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()
    

def editar_dados():
    global numero_id
    
    #pegando a linha clicada com o comando "tableWinget.currentRow()"
    
    linha = segunda_tela.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT cpf FROM cadastro_promocao")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM cadastro_promocao WHERE cpf="+str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()
    numero_id = valor_id
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    tela_editar.lineEdit_6.setText(str(produto[0][5]))
    #

    print(produto[0][0])

    #tela_editar.lineEdit.setText(str(produto[0][0]))
    
    #banco.commit()
 

def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT cpf FROM cadastro_promocao")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    print(str(valor_id))
    cursor.execute("DELETE FROM cadastro_promocao WHERE cpf="+str(valor_id))
    banco.commit()
 

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2= formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    linha4 = formulario.dateEdit.text()
    linha5 = formulario.lineEdit_5.text()

    recebimento = ""

    if formulario.radioButton.isChecked():
        print("Email")
        Recebimento = "EMAIL"
    elif formulario.radioButton_2.isChecked():
        print("SMS")
        Recebimento = "SMS"
    else :
        print("Nao")
        Recebimento = "NAO"


    print("nome:",linha1)
    print("cpf:",linha2)
    print("telefone:",linha3)
    print("data_nasc:",linha4)
    print("e_mail:",linha5)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO cadastro_promocao (nome,cpf,telefone,data_nasc,e_mail,recebimento) VALUES (%s,%s,%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5), Recebimento)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_5.setText("")
    #formulario.dateEdit.setText("01/01/1990")


def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM cadastro_promocao"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    #print(dados_lidos)

    
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(6)
    
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            segunda_tela.tableWidget.setItem(i, j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            segunda_tela.tableWidget.setColumnWidth(0,250)
            segunda_tela.tableWidget.setColumnWidth(1,90)
            segunda_tela.tableWidget.setColumnWidth(2,90)
            segunda_tela.tableWidget.setColumnWidth(3,155)
            segunda_tela.tableWidget.setColumnWidth(4,200)
            segunda_tela.tableWidget.setColumnWidth(5,110)
 

app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
tela_editar=uic.loadUi("menu_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(excluir_dados)
segunda_tela.pushButton_2.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)


formulario.show()

app.exec()
