Sub sofardata()
'
' sofardata Makro
' Makro konwertujące dane pobrane z tygodniowych raportow do pliku tekstowego do importu bezposrednio do bazy fluxdb
'Zalgowac sie na home.solarman.cn -wejsc do szczegolow inwertera, w dolnej czesci nad wykresem wskazac zakres tygodniowy i pobrac dane.
'Pobrrany plik xls otwieramy w excel, zezwalamy na edycje, wchodzimy w zakladke developer i wybieramy edytor visualbasic (skrot Alt+F11)
'W edytoprze VB klikamy File->Import File lub skrót Ctrl+M i wskazujemy ten plik 
'Uruchamiamy makro sofardata -w wyniku utworzy nam się plik tekstowy z taka sama nazwa i w tej samej sciezce jak excelowy plik źródłowy, ale rozszerzeniem txt 
'Ten plik importujemy do Bazy InfluxDB: Explore->WriteData (w górnej czesci okna), wskazujemy wlasciwa nazwe bazy np. SofarData. Pozostawiamy domyslna precyzje ns.


'
    Sheets.Add After:=ActiveSheet
    Range("A1").Select
    ActiveCell.FormulaR1C1 = "time"
    Range("B1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String1"
    Range("C1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String2"
    Range("D1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String3"
    Range("E1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String4"
    Range("F1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String5"
    Range("G1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String6"
    Range("H1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String7"
    Range("I1").Select
    ActiveCell.FormulaR1C1 = "DCInputCurrent_String8"
    Range("J1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String1"
    Range("K1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String2"
    Range("L1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String3"
    Range("M1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String4"
    Range("N1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String5"
    Range("O1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String6"
    Range("P1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String7"
    Range("Q1").Select
    ActiveCell.FormulaR1C1 = "DCInputVoltage_String8"
    Range("R1").Select
    ActiveCell.FormulaR1C1 = "InverterCurrent_PV1CurrentSample"
    Range("S1").Select
    ActiveCell.FormulaR1C1 = "InverterInsulation_PV"
    Range("T1").Select
    ActiveCell.FormulaR1C1 = "InverterInsulation_PV1"
    Range("U1").Select
    ActiveCell.FormulaR1C1 = "InverterInsulation_PV2"
    Range("V1").Select
    ActiveCell.FormulaR1C1 = "InverterTemp_Inner"
    Range("W1").Select
    ActiveCell.FormulaR1C1 = "InverterTemp_Module"
    Range("X1").Select
    ActiveCell.FormulaR1C1 = "InverterVoltage_Bus"
    Range("Y1").Select
    ActiveCell.FormulaR1C1 = "InverterVoltage_PV1VoltageSample"
    Range("Z1").Select
    ActiveCell.FormulaR1C1 = "OutputCurrent_L1"
    Range("AA1").Select
    ActiveCell.FormulaR1C1 = "OutputCurrent_L2"
    Range("AB1").Select
    ActiveCell.FormulaR1C1 = "OutputCurrent_L3"
    Range("AC1").Select
    ActiveCell.FormulaR1C1 = "OutputFreq_Frequency"
    Range("AD1").Select
    ActiveCell.FormulaR1C1 = "OutputPower_Active"
    Range("AE1").Select
    ActiveCell.FormulaR1C1 = "OutputPower_Reactive"
    Range("AF1").Select
    ActiveCell.FormulaR1C1 = "OutputVoltage_L1"
    Range("AG1").Select
    ActiveCell.FormulaR1C1 = "OutputVoltage_L2"
    Range("AH1").Select
    ActiveCell.FormulaR1C1 = "OutputVoltage_L3"
    Range("AI1").Select
    ActiveCell.FormulaR1C1 = "SolarCurrent_PV1"
    Range("AJ1").Select
    ActiveCell.FormulaR1C1 = "SolarCurrent_PV2"
    Range("AK1").Select
    ActiveCell.FormulaR1C1 = "SolarPower_PV1"
    Range("AL1").Select
    ActiveCell.FormulaR1C1 = "SolarPower_PV2"
    Range("AM1").Select
    ActiveCell.FormulaR1C1 = "SolarProduction_Today"
    Range("AN1").Select
    ActiveCell.FormulaR1C1 = "SolarProduction_Total"
    Range("AO1").Select
    ActiveCell.FormulaR1C1 = "SolarTime_Today"
    Range("AP1").Select
    ActiveCell.FormulaR1C1 = "SolarTime_Total"
    Range("AQ1").Select
    ActiveCell.FormulaR1C1 = "SolarVoltage_PV1"
    Range("AR1").Select
    ActiveCell.FormulaR1C1 = "SolarVoltage_PV2"
    Range("A2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C="""","""",(Sheet0!R[3]C))"
    Selection.NumberFormat = "dd/mm/yy h:mm;@"
    Range("S2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[15]="""","""",Sheet0!R[3]C[15])"
    Range("T2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[18]="""","""",Sheet0!R[3]C[18])"
    Range("U2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[18]="""","""",Sheet0!R[3]C[18])"
    Range("V2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[3]="""","""",Sheet0!R[3]C[3])"
    Range("W2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[3]="""","""",Sheet0!R[3]C[3])"
    Range("X2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[9]="""","""",Sheet0!R[3]C[9])"
    Range("Y2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[10]="""","""",Sheet0!R[3]C[10])"
    Range("Z2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-11]="""","""",Sheet0!R[3]C[-11])"
    Range("AA2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-11]="""","""",Sheet0!R[3]C[-11])"
    Range("AB2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-11]="""","""",Sheet0!R[3]C[-11])"
    Range("AC2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-10]="""","""",Sheet0!R[3]C[-10])"
    Range("AD2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-12]="""","""",Sheet0!R[3]C[-12])"
    Range("AF2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-20]="""","""",Sheet0!R[3]C[-20])"
    Range("AG2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-20]="""","""",Sheet0!R[3]C[-20])"
    Range("AH2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-20]="""","""",Sheet0!R[3]C[-20])"
    Range("AI2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-27]="""","""",Sheet0!R[3]C[-27])"
    Range("AJ2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-27]="""","""",Sheet0!R[3]C[-27])"
    Range("AK2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-27]="""","""",Sheet0!R[3]C[-27])"
    Range("AL2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-27]="""","""",Sheet0!R[3]C[-27])"
    Range("AM2").Select
    ActiveCell.FormulaR1C1 = _
        "=IF(Sheet0!R[3]C[-19]="""","""",SUBSTITUTE(SUBSTITUTE(Sheet0!R[3]C[-19],""."","","")*1000,"","","".""))"
    Range("AN2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-19]="""","""",Sheet0!R[3]C[-19])"
    Range("AP2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-14]="""","""",Sheet0!R[3]C[-14])"
    Range("AQ2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-37]="""","""",Sheet0!R[3]C[-37])"
    Range("AR2").Select
    ActiveCell.FormulaR1C1 = "=IF(Sheet0!R[3]C[-37]="""","""",Sheet0!R[3]C[-37])"
    Range("AX2").Select
    ActiveCell.FormulaR1C1 = _
        "=IF(RC[-49]="""","""",""InverterData,""&R1C[-30]&""=""&RC[-30]&"" ""&R1C[-29]&""=""&RC[-29]&"" ""&R1C[-28]&""=""&RC[-28]&"" ""&R1C[-26]&""=""&RC[-26]&"" ""&R1C[-25]&""=""&RC[-25]&"" ""&R1C[-24]&""=""&RC[-24]&"" ""&R1C[-23]&""=""&RC[-23]&"" ""&R1C[-22]&""=""&RC[-22]&"" ""&R1C[-21]&""=""&RC[-21]&"" ""&R1C[-20]&""=""&RC[-20]&"" ""&R1C[-27]&""=""&RC[-27]&"" ""&R1C[-18]&" & _
        """=""&RC[-18]&"" ""&R1C[-17]&""=""&RC[-17]&"" ""&R1C[-16]&""=""&RC[-16]&"" ""&R1C[-15]&""=""&RC[-15]&"" ""&R1C[-14]&""=""&RC[-14]&"" ""&R1C[-13]&""=""&RC[-13]&"" ""&R1C[-12]&""=""&RC[-12]&"" ""&R1C[-11]&""=""&RC[-11]&"" ""&R1C[-10]&""=""&RC[-10]&"" ""&R1C[-8]&""=""&RC[-8]&"" ""&R1C[-7]&""=""&RC[-7]&"" ""&R1C[-6]&""=""&RC[-6]&"" ""&R1C[-31]&""=""&RC[-31]&"" ""&""  """ & _
        "&(RC[-49]-DATE(1970,1,1))*86400)" & _
        ""
    Range("AY2").Select
    ActiveCell.FormulaR1C1 = ""
    Range("AZ2").Select
    ActiveCell.FormulaR1C1 = ""
    Range("BA2").Select
    ActiveCell.FormulaR1C1 = _
        "=RC[-1]&IF(RC1="""","""",""InverterData,""&CHAR(34)&""time""&CHAR(34)&""=""&TEXT(RC1,""rrrr:mm:ddTgg:mm:ss;@"")&"".000+01:00""&""  ""&R1C[-34]&""=""&IF(RC[-34]="""",0,RC[-34])&"" ""&(RC1-DATE(1970,1,1))*86400&""000000000""&CHAR(10))"
    Range("BA2").Select
    Selection.AutoFill Destination:=Range("BA2:BZ2"), Type:=xlFillDefault
    Rows("2:2").Select
    Range("V2").Activate
    Selection.Copy
    Rows("2:6000").Select
    ActiveSheet.Paste
    Range("BZ2").Select
    Application.CutCopyMode = False
    Rowv = 2
    wartosc = "zaczynamy"
    While wartosc <> ""
        wartosc = Range(Replace("BZ" + Str(Rowv), " ", "")).Value
        If wartosc <> "" Then wynik = wynik + wartosc + Chr(10)
        Rowv = Rowv + 1
    Wend
    Const adSaveCreateOverWrite = 2
    With CreateObject("ADODB.Stream")
        .Charset = "utf-8"
        .Open
        .WriteText wynik
        .SaveToFile ThisWorkbook.FullName + ".txt", adSaveCreateOverWrite
    End With
End Sub

