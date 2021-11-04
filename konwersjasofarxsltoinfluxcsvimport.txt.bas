Sub sofardata()
'
' sofardata Makro
' Makro konwertujÄ…ce dane pobrane z tygodniowych raportow do pliku tekstowego do importu bezposrednio do bazy fluxdb
'Zalgowac sie na home.solarman.cn -wejsc do szczegolow inwertera, w dolnej czesci nad wykresem wskazac zakres tygodniowy i pobrac dane.
'Pobrrany plik xls otwieramy w excel, zezwalamy na edycje, wchodzimy w zakladke developer i wybieramy edytor visualbasic (skrot Alt+F11)
'W edytoprze VB klikamy File->Import File lub skrĂłt Ctrl+M i wskazujemy ten plik
'Uruchamiamy makro sofardata -w wyniku utworzy nam siÄ™ plik tekstowy z taka sama nazwa i w tej samej sciezce jak excelowy plik ĹşrĂłdĹ‚owy, ale rozszerzeniem txt
'Ten plik importujemy do Bazy InfluxDB: Explore->WriteData (w gĂłrnej czesci okna), wskazujemy wlasciwa nazwe bazy np. SofarData. Pozostawiamy domyslna precyzje ns.


'Nie używane pola OutputPower_Reactive SolarTime_Today InverterCurrent_PV1CurrentSample DCInputCurrent_String1	DCInputCurrent_String2	DCInputCurrent_String3	DCInputCurrent_String4	DCInputCurrent_String5	DCInputCurrent_String6	DCInputCurrent_String7	DCInputCurrent_String8	DCInputVoltage_String1	DCInputVoltage_String2	DCInputVoltage_String3	DCInputVoltage_String4	DCInputVoltage_String5	DCInputVoltage_String6	DCInputVoltage_String7	DCInputVoltage_String8



    measurementname = "InverterData"
    timezone = "+01:00"
    nameNAM = Array(Array("PL", "EN", "fluxDB"), Array("Czas", "Time", "time"), Array("InwerterSN", "InverterSN", ""), Array("Data LoggerSN", "Data LoggerSN", ""), Array("Szczegóły alarmu", "Alert Details", ""), Array("Kod błędu", "Alert Code", ""), _
    Array("Napięcie DC PV1(V)", "DC Voltage PV1(V)", "SolarVoltage_PV1"), Array("Napięcie DC PV2(V)", "DC Voltage PV2(V)", "SolarVoltage_PV2"), _
    Array("Prąd DC1(A)", "DC Current1(A)", "SolarCurrent_PV1"), Array("Prąd DC2(A)", "DC Current2(A)", "SolarCurrent_PV2"), Array("Moc DC PV1(W)", "DC Power PV1(W)", "SolarPower_PV1"), Array("Moc DC PV2(W)", "DC Power PV2(W)", "SolarPower_PV2"), _
    Array("Napięcie AC R/U/A(V)", "AC Voltage R/U/A(V)", "OutputVoltage_L1"), Array("Napięcie AC S/V/B(V)", "AC Voltage S/V/B(V)", "OutputVoltage_L2"), Array("Napięcie AC T/W/C(V)", "AC Voltage T/W/C(V)", "OutputVoltage_L3"), _
    Array("Prąd AC R/U/A(A)", "AC Current R/U/A(A)", "OutputCurrent_L1"), Array("Prąd AC S/V/B(A)", "AC Current S/V/B(A)", "OutputCurrent_L2"), Array("Prąd AC T/W/C(A)", "AC Current T/W/C(A)", "OutputCurrent_L3"), Array("Całkowita moc czynna wyjściowa AC(W)", "AC Output Total Power (Active)(W)", "OutputPower_Active"), _
    Array("Częstotliwość wyjściowa AC R(Hz)", "AC Output Frequency R(Hz)", "OutputFreq_Frequency"), _
    Array("Dzienna produkcja (efektywna)(kWh)", "Daily Generation (Active)(kWh)", "SolarProduction_Today"), Array("Całkowita produkcja (efektywna)(kWh)", "Total Generation (Active)(kWh)", "SolarProduction_Total"), _
    Array("Całkowita moc użytkowa(W)", "Total Consumption Power (W)", ""), Array("Status mocy sieci", "Power Grid Status", ""), _
    Array("Moc całkowita sieci(W)", "Power Grid Total Power(W)", ""), Array("Temperatura inwertera(?)", "Inverter Temperature(?)", "InverterTemp_Inner"), Array("Temperatura Modułu(?)", "Module Temperature(?)", "InverterTemp_Module"), _
    Array("Prąd upływu(mA)", "Leaking Current(mA)", ""), Array("Łączna liczba godzin pracy(h)", "Total Operating Hours(h)", "SolarTime_Total"), _
    Array("Dystrybucja DC fazy A", "A-phase DC Distribution", ""), Array("Dystrybucja DC fazy B", "B-phase DC Distribution", ""), Array("Dystrybucja DC fazy C", "C-phase DC Distribution", ""), _
    Array("(W)", "CT power(W)", ""), Array("Napięcie magistrali(V)", "Bus voltage(V)", "InverterVoltage_Bus"), Array("Napięcie wejściowe rezerwowego procesora 1", "Vice CPU input voltage 1", "InverterVoltage_PV1VoltageSample"), _
    Array("Status inwertera", "Inverter Status", ""), Array("Okres wydajnośći(h)", "Performance Period(h)", ""), _
    Array("Impedancja izolacji Katoda-Ziemia", "Insulation impedance-Cathode to ground", "InverterInsulation_PV"), _
    Array("Wartość rezystancji izolacji PV1", "PV1 Insulation Resistance", "InverterInsulation_PV1"), Array("Wartość rezystancji izolacji PV2", "PV2 Insulation Resistance", "InverterInsulation_PV2"), _
    Array("Czas odliczania(h)", "Countdown Time(h)", ""), Array("Induktor 1 Prąd A(A)", "Inductor 1 Current A(A)", ""), _
    Array("", "Standby time", ""), Array("", "Total Standby time", ""), Array("", "Downtime", ""), _
    Array("", "Total Downtime", ""))
    
    Dim fsT As Object
    Set fsT = CreateObject("ADODB.Stream")
    fsT.Type = 2 'Specify stream type - we want To save text/string data.
    fsT.Charset = "utf-8" 'Specify charset For the source text data.
    fsT.Open 'Open the stream And write binary data To the object
    
    Dim namerow()
    namerow = Sheets("Sheet0").Range("4:4").FormulaLocal
    RowCount = Sheets("Sheet0").Cells(Rows.Count, 1).End(xlUp).Row
    For rowline = 5 To RowCount
        For x = 2 To UBound(namerow, 2)
            If Len(namerow(1, x)) = 0 Then
                Exit For
            End If
            For y = 2 To UBound(nameNAM)
                If (namerow(1, x) = nameNAM(y)(0) Or namerow(1, x) = nameNAM(y)(1)) And nameNAM(y)(2) <> "" Then
                    Value = Sheets("Sheet0").Cells(rowline, x).Value
                    If nameNAM(y)(2) = "SolarProduction_Today" Then
                        Value = Replace(Format(Val(Replace(Replace(Value, ",", Application.DecimalSeparator), ".", Application.DecimalSeparator)) * 1000, "0.00"), ",", ".")
                    End If
                    timed = Sheets("Sheet0").Cells(rowline, 1).Value
                    timesign = Str((timed - CDate("1970-01-01")) * 86400) + "000000000"
                    fsT.WriteText measurementname + "," + Chr(34) + "time" + Chr(34) + "=" + Replace(Str(timed), " ", "T") + ".000" + timezone + " " + nameNAM(y)(2) + "=" + Value + " " + timesign + vbLf
                    Exit For
                End If
            Next y
        Next x
        If x / 100 - x \ 100 = 0 Then
        a = a
        End If
        If Len(Sheets("Sheet0").Cells(rowline, 1).Value) < 10 Then
            Exit For
        End If
    Next rowline
    Const adSaveCreateOverWrite = 2
    fsT.SaveToFile ThisWorkbook.FullName + ".txt", adSaveCreateOverWrite 'Save binary data To disk
    ax = MsgBox("OK. Zamykam Arkusz bez zapisu", vbOK)
    ActiveWorkbook.Close savechanges:=False
    ActiveWorkbook.Close False
End Sub





