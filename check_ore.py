import pandas as pd
from pandas.tseries.offsets import *
from datetime import timedelta
from flask import render_template, url_for

def controlla_ore():

    filename = 'static/downloads/Timbrature_sett.xlsx'
#    filename = 'static/downloads/Timbrature_ott.xlsx'
    tables = []
    strings = ['na']

    df = pd.read_excel(filename, skiprows=1)
    # print(df.head())

    df['DOW'] = df['Data'].str.rpartition(',')[0]
    df['Cal'] = df['Data'].str.rpartition(',')[2]

    # merge colonne cal e orario
    df['GiornoOra'] = df['Cal'] + ' ' + df['Orario']
    # converte colonna giornoOra in datetime
    df['GiornoOra'] = pd.to_datetime(df['GiornoOra'], format=' %d-%m-%Y %H:%M:%S')
    # riorganizza la tabella
    df = df[['GiornoOra', 'Descrizione', 'DOW']]

    def calcola_giorno(this_day):
        this_day.reset_index(inplace=True, drop=True) # reinizializza l'index a 0, inplace
        print this_day
        table = this_day.to_html(classes = 'table table-condensed', header=False, index=False, border=0)
        outstring = ''
    
        if this_day.GiornoOra.count() == 2:	 # entrata e uscita
            totOreGiorno = this_day.GiornoOra[1] - this_day.GiornoOra[0]
            print 'Ore Lorde: ', totOreGiorno 
            print 'Ore nette (int. mensa): ', totOreGiorno - timedelta(minutes=30)
            outstring = 'Ore Lorde: ' + str(totOreGiorno) + ' Ore nette (int. mensa): ' + str(totOreGiorno - timedelta(minutes=30))
        
        elif this_day.GiornoOra.count() == 4:  # TODO: distinguere con e senza inizio pausa
            ore_mattino = this_day.GiornoOra[1] - this_day.GiornoOra[0]
            ore_pomeriggio = this_day.GiornoOra[3] - this_day.GiornoOra[2]
            totOreGiorno = ore_mattino + ore_pomeriggio
            print 'Ore Lorde: ', totOreGiorno 
            print 'Ore nette (int. mensa): ', totOreGiorno
            outstring = 'Ore Lorde: ' + str(totOreGiorno) + ' Ore nette (int. mensa): ' + str(totOreGiorno)
        
        elif this_day.GiornoOra.count() == 6:  # Anomalia, calcolo e/u a coppie
            ore_1 = this_day.GiornoOra[1] - this_day.GiornoOra[0]
            ore_2 = this_day.GiornoOra[3] - this_day.GiornoOra[2]
            ore_3 = this_day.GiornoOra[5] - this_day.GiornoOra[4]
            print ore_1, ore_2, ore_3
            totOreGiorno = ore_1 + ore_2 + ore_3
            print 'Ore Lorde: ', totOreGiorno 
            print 'Ore nette (int. mensa): ', totOreGiorno
            outstring = 'Ore Lorde: ' + str(totOreGiorno) + ' Ore nette (int. mensa): ' + str(totOreGiorno)
    
        else:  # ogni altro caso
            print(" ----- Numero di timbrature ANOMALO ----- ")
            outstring = " ----- Numero di timbrature ANOMALO ----- "
        
        return table, outstring


    start_date = df.GiornoOra[0]  # primo giorno della prima timbratura
    start_date = start_date.replace(hour=7, minute=0, second=0, microsecond=0)	# setto le 7:00
    day_count = df.GiornoOra[0].days_in_month  # quanti giorni ci sono nel mese del foglio

    for single_date in (start_date + timedelta(n) for n in range(day_count)):
        # print(single_date)
        end_date = single_date + DateOffset(days=1)
        mask = (df.GiornoOra >= single_date) & (df.GiornoOra < end_date)
        tddf = df.loc[mask]
        if not tddf.empty: # giorno con timbrature
            t, os = calcola_giorno(tddf)
            tables.append(t)
            strings.append(os)
        else:  # giorno senza trimbrature
            print('######', single_date.strftime(format='%Y-%m-%d'), '######')
            tables.append('')
            strings.append('######' + single_date.strftime(format='%Y-%m-%d') + '######')
        # break
        
#    return(df.to_html(classes = 'table table-condensed', header=False, index=False, border=0))
    return(tables, strings)
#    return render_template('home.html')
    

if __name__ == '__main__':
    tables, strings = controlla_ore()
    # print strings