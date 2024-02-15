from background_task import background
from logging import getLogger
from . import models
from .functions import pdf_grid, image_grid, add_symbol, Berlin_time
import os
import sys
from PIL import Image
import pandas as pd
import math
import config
from django.conf import settings
sys.path.insert(0, os.path.join(config.AUTOBAT_PATH, 'autoBat'))
from BaumgrassGating import BaumgrassGating
from AutoBatWorkflow import AutoBatWorkflow
from Data import Data
from Reporting import Reporting
from Report import Report
import flowkit as fk
from django.shortcuts import get_object_or_404
import traceback
logger = getLogger(__name__)


       
#@background(queue='autoBat-queue-save', schedule=10)
def save_pdf(pdf_path, pdf_list, analysisMarker_id, analysis_type=None):
    pdf_list.reverse()
    
    if analysis_type == "AutoGrat":
        new_pdf_list = pdf_list
    else:
        new_pdf_list = []
        new_pdf_list.append(pdf_list) #the function pdf_grid is expecting a list of lists

    #image_grid(pdf_list, pdf_path, analysis_type)
    pdf_grid(new_pdf_list, pdf_path, analysis_type)
    
    # Save pdf plot to database
    PDFresults_instance = models.AnalysisFiles(file_path=pdf_path, file_type="PDF")
    PDFresults_instance.analysisMarker_id_id = int(analysisMarker_id)
    PDFresults_instance.save()
    
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Ready")
    end_time = Berlin_time()
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_end_time=end_time)

@background(queue='autoBat-queue-process-files', schedule=10)
def proccess_files(analysis_id):
    sample_obj = models.ExperimentFiles.objects.values_list('file_id', 'file').filter(analysis_id = analysis_id)

    for sample in sample_obj:
        file_id = sample[0]
        file_path = sample[1]
        filename = fk.Sample(file_path) 
        dataO = Data(filetype="FCS", filename = file_path)
        data = dataO.getData()
        meta = data.get_metadata()
        for m in meta:
            Label = m
            value = meta[m]
            if len(value) < 200:
                value = value
            else:
                value = None

            meta_obj = models.MetaData(
                                    labels = Label,
                                    values = value,
                                    )
        
            meta_obj.file_id_id = int(file_id)
            meta_obj.save()

        pnnLabels = filename.pnn_labels
        xform = fk.transforms.LogicleTransform('asinh', param_t=1024, param_w=0.5, param_m=4.5, param_a=0)
        filename.apply_transform(xform)
        content = filename.as_dataframe(source='xform', col_names=pnnLabels)
        raw_fcs_val = content.to_dict()
        for label in pnnLabels:
            labels = f"{label}_mean"
            try:
                values = math.ceil((sum(raw_fcs_val[label].values())) / len(raw_fcs_val[label]) * 100) / 100
            except:
                values=0
            mean_obj = models.MeanRawData(
                                    labels = labels,
                                    values = values,
                                    )
            mean_obj.file_id_id = int(file_id)
            mean_obj.save()

@background(queue='autoBat-queue-analysis', schedule=10)
def run_analysis_autobat_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, condition,
                        chosen_z1, chosen_z1_lable, chosen_y1, chosen_y1_lable, chosen_z2, device, outputPDFname, pathToData, pathToExports, 
                        pathToOutput, pathToGatingFunctions, rPath, manualThresholds, xMarkerThreshhold, yMarkerThreshold, z1MarkerThreshold, analysis_type_version, user_id
                    ):

    start_time = Berlin_time()
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_start_time=start_time)
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="In Progress")

    sample_obj = models.ExperimentFiles.objects.values_list('file_id', 'file', 'file_name','allergen', 'control').filter(analysis_id = analysis_id)
    

    nrFiles = len(sample_obj)
    reports = [None]*nrFiles
    info = [None]*nrFiles 
    algList = [None]*nrFiles
    files_list = []
    usName = ''
    posFileName = ''
    posTwoFileName= ''
    chosen_x = ""
    chosen_x_label = ""
    chosen_z2_lable = "CD32"
    quality_messages = []
    #info_messages = ""
    i = 0
    try:
        for sample in sample_obj:
            file_id = sample[0]
            file_path = sample[1]
            file_name = sample[2]
            allergen = sample[3]
            algList[i] = allergen

            control = sample[4]
            if control == 'Primary Positive control':
                posFileName = file_name
            elif control == 'Secondary Positive control':
                posTwoFileName = file_name

            elif control == 'Negative control':
                usName = file_name
        
            if panel_name in ['full-panel', 'grat-panel']:
                if condition:
                    pathToExports = (f'/home/abusr/autoBatWeb/auto-BAT-Web/media/FCS_fiels/{bat_name}/{donor_name}/{panel_name}/{condition}/')
                else:
                    pathToExports = (f'/home/abusr/autoBatWeb/auto-BAT-Web/media/FCS_fiels/{bat_name}/{donor_name}/{panel_name}/')
                files_list.append(pathToExports + file_name)

                reports[i] = Report(id = file_name.lower())
                try:
                    total_cells = get_object_or_404(models.MetaData.objects.filter(file_id=file_id, labels='tot').values_list('values', flat=True))
                except:
                    total_cells = 0
                reports[i].setCellTotal(total_cells)
                reports[i].setDebrisPerc(0) 
                reports[i].setFirstDoubPerc(0)
                reports[i].setSecDoubPerc(0)
                info[i]= ["For this panel no automatic pregating is done"]
                i += 1
            
            else:
                baumgrassgater = BaumgrassGating(
                                file_path,            
                                pathToGatingFunctions, 
                                device, 
                                pathToExports,
                                report_Id = i)

                #reports[i] = baumgrassgater.runbaumgrassgating()
                reports[i], info[i] = baumgrassgater.runbaumgrassgating()
                files_list.append(pathToExports + file_name)
                #info_messages = str(reports[i][1])
                i += 1
         
        autoworkflow = AutoBatWorkflow(files_list,
                                    pathToData,
                                    pathToExports,
                                    pathToOutput,
                                    outputPDFname,
                                    pathToGatingFunctions,
                                    device,
                                    chosen_x,   
                                    chosen_y1,  
                                    chosen_z1,
                                    chosen_z2,
                                    chosen_x_label,
                                    chosen_y1_lable,
                                    chosen_z1_lable,
                                    chosen_z2_lable,
                                    str(usName),
                                    str(posFileName),
                                    str(posTwoFileName),
                                    '',
                                    rPath,
                                    webapp="Yes")
    
        
        if manualThresholds:
            df, SSCA, FCR, CD63, info_bg = autoworkflow.updateBatResultswithManualThresholds(xMarkerThreshhold, yMarkerThreshold, z1MarkerThreshold)
            manual_check = True
            plot_symbol = 'ok'
        else:
            df, SSCA, FCR, CD63, info_bg = autoworkflow.runCD32thresholding()
            plot_symbol = None

        
        #df, SSCA, FCR, CD63, info_bg, plot_symbol = autoworkflow.runCD32Bat()
        quality_messages.append(info_bg)
        print("\n -- This is the dataframe from first part of reporting: \n")
        print(df)
        #results = autoworkflow.runCD32thresholding()
        # check out folder set as output folder for results
        # check out folder set as output folder for results
        
        # check out folder set as output folder for results
        algList.insert(0, 'NA')
        df.insert(0, 'ID', algList, True) # I somehow needed this row

        info_cellQ4 = []

        for i in range(len(reports)):       
            reports[i].setZMarker('NA')
            reports[i].setRed(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["redQ4"]))
            reports[i].setBlack(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["blackQ2"]))
            reports[i].setBlackQ3(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["blackQ3"]))
            reports[i].setBlackQ4(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["blackQ4"]))
            reports[i].setZmean(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["zmeanQ4"]))
            reports[i].setZ1Min(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["Z1_min"]))
            reports[i].setZ1max(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["Z1_max"]))
            reports[i].setMsiY(float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["msi_Y"]))
            reports[i].cellQ3 = float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["cellQ3"])
            reports[i].cellQ4 = float(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["cellQ4"])
            reports[i].setResult(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["result"].values[0])
            reports[i].setResponder(df[df['filename'].str.contains(reports[i].filename.lower(), regex=False)]["responder"].values[0])
            reports[i].setPlotSympol(plot_symbol)
            if int(reports[i].cellTotal) < 100000:
                reports[i].setPlotSympol('unclear')
            if reports[i].cellQ4  < 350:
                reports[i].setPlotSympol('unclear')

                print("\n The number of events in Q4 (basophils) is smaller than 350. This might result in problems with the analysis and the results must be handled with care. \n")
                info_cellQ4 = ["The number of events in Q4 (basophils) is smaller than 350. This might result in problems with the analysis and the results must be handled with care."]
        ###==========================================================================================================================###
        # filling the quality messages column with the file specific error messages and
        # also applying the thresholds for responder/nonresponder in the controls

        if "us" in reports[i].filename.lower():               # bei der negativen Kontrolle kann ich auch die Thresholding Infos anfügen
            try:
                us_info = info[0]
            except:
                us_info = []
            reports[i].setQualityMessages(us_info + info_bg + info_cellQ4) 
            reports[i].setYThreshold(FCR)  
            reports[i].setZ1Threshold(CD63)  
            
        if "aige" in reports[i].filename.lower(): 
            try:
                aige_info = info[2]
            except:
                aige_info = []
            reports[i].setQualityMessages(aige_info] + info_cellQ4) 
            if reports[i].red >= 5.0: 
                reports[i].setResponder("aIgE Responder") 
            else: 
                reports[i].setResponder("aIgE Non-Responder")

        if "fmlp" in reports[i].filename.lower():
            try:
                fmpl_info = info[1]
            except:
                fmpl_info = []
            reports[i].setQualityMessages(fmpl_info + info_cellQ4) 
            if reports[i].red >= 5.0: 
                reports[i].setResponder("fMLP Responder") 
            else: 
                reports[i].setResponder("fMLP Non-Responder")
        
        finalReport = Reporting(reports)
        finalReport = finalReport.constructReport()

        print("\n -- This is the final report: \n")
        print(finalReport)

        ### save report to .xls
        if condition:
            excel_file = os.path.join(pathToOutput, f'AutoBat_{bat_name}_{donor_name}_{panel_name}_{condition}_{chosen_z1}_{chosen_y1}_{chosen_z2}.xlsx')
        else:
            excel_file = os.path.join(pathToOutput, f'AutoBat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.xlsx')
        df_excel = finalReport
        df_excel['Version'] = analysis_type_version
        #df_excel.drop(df[df['filename'] == '0'].index, inplace = True)
    
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df_excel.to_excel(writer, sheet_name='Sheet1')

        writer.save()
        
        # Save Thresholds to the Database
        thresholds_instance = models.AnalysisThresholds(
                                        X_Threshold = float(SSCA),
                                        Y_Threshold = float(FCR),
                                        Z2_1_Threshold = float(CD63),
            )
        thresholds_instance.analysisMarker_id_id = int(analysisMarker_id)
        thresholds_instance.save()
        # Save DF to the Database
        for index, row in finalReport.iterrows():
            file_name = index
            file_id = get_object_or_404(models.ExperimentFiles.objects.filter(file_name__icontains=file_name, analysis_id=analysis_id).values_list('file_id', flat=True))
            file_name = get_object_or_404(models.ExperimentFiles.objects.filter(file_name__icontains=file_name, analysis_id=analysis_id).values_list('file_name', flat=True))
            debrisPerc = row['debrisPerc']
            firstDoubPerc = row['firstDoubPerc']
            secDoubPerc = row['secDoubPerc']
            redQ4 = float(row['redQ4'])
            result = row['result']
            blackQ2 = row['blackQ2']
            blackQ3 = row['blackQ3']
            blackQ4 = row['blackQ4']
            zmeanQ4 = row['zmeanQ4']
            Z1_minQ4 = row['Z1_minQ4']
            Z1_maxQ4 = row['Z1_maxQ4']
            msi_YQ4 = row['msi_YQ4']
            cellQ3 = row['cellQ3']
            cellQ4 = row['cellQ4']
            responder = row['responder']
            cellTotal = row['cellTotal']
            qualityMessages = row['qualityMessages']
            plot_symbol = row['plot_symbol']
            plot_name = f'{file_name[:-4].lower()}.pdf'
            plot_path=os.path.join(pathToOutput, plot_name)
            if plot_symbol == 'unclear':
                add_symbol(plot_path, plot_path, error=True, checked = False, solved=False)
            if manual_check:
                if plot_symbol == 'ok':
                    add_symbol(plot_path, plot_path, error=True, checked = True, solved=True)
                else:
                    add_symbol(plot_path, plot_path, error=True, checked = True, solved=False)
           
            if ', []' in str(qualityMessages):
                qualityMessages = str(qualityMessages).replace(', []','')

            if qualityMessages != 'empty':
                quality_messages.append(qualityMessages)

            results_instance = models.AnalysisResults(
                                        debrisPerc = debrisPerc,
                                        firstDoubPerc = firstDoubPerc,
                                        secDoubPerc = secDoubPerc,
                                        redQ4 = redQ4,
                                        result = result,
                                        blackQ2 = blackQ2,
                                        blackQ3 = blackQ3,
                                        blackQ4 = blackQ4,
                                        zmeanQ4 = zmeanQ4,
                                        Z1_minQ4 = Z1_minQ4,
                                        Z1_maxQ4 = Z1_maxQ4,
                                        msi_YQ4 = msi_YQ4,
                                        cellQ3 = cellQ3,
                                        cellQ4 = cellQ4,
                                        cellTotal = cellTotal,
                                        qualityMessages = qualityMessages,
                                        plot_symbol=plot_symbol,
                                        responder = responder,
            )
            results_instance.file_id_id = int(file_id)
            results_instance.analysisMarker_id_id = int(analysisMarker_id)
            results_instance.user_id = user_id
            results_instance.save()
        # save the  info messages
        quality_messages = ', '.join(str(v) for v in quality_messages)
        models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_info_messages = quality_messages)
        # Save plots to database
        pdf_list = []
        for file in sample_obj:
            file_id = file[0]
            plot_name = file[2].lower()
            plot_name = f'{plot_name[:-4]}.pdf'
            plot_path=os.path.join(pathToOutput, plot_name)
            PDFresults_instance = models.FilesPlots(plot_path=plot_path)
            PDFresults_instance.analysisMarker_id_id = int(analysisMarker_id)
            PDFresults_instance.file_id_id = int(file_id)
            PDFresults_instance.save()
            pdf_list.append(plot_path)
    
        # Save Excel File's path to the Database
        EXCELresults_instance = models.AnalysisFiles(file_path=excel_file, file_type="Excel")
        EXCELresults_instance.analysisMarker_id_id = int(analysisMarker_id)
        EXCELresults_instance.save()


        # Create PDF File:
        if condition:
            pdf = f"AutoBat_{bat_name}_{donor_name}_{panel_name}_{condition}_{chosen_z1}_{chosen_y1}_{chosen_z2}.pdf"
        else:
            pdf = f"AutoBat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.pdf"
        pdf_path = os.path.join(pathToOutput, pdf)
        save_pdf(pdf_path, pdf_list, analysisMarker_id, 'AutoBat')
    except Exception:
        e = traceback.format_exc()
        models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Error", analysis_error=e)



@background(queue='autograt-queue-analysis', schedule=10)
def run_analysis_autograt_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, condition,
                        chosen_x, chosen_x_label, chosen_y1, chosen_y1_lable, chosen_z1, chosen_z1_lable, chosen_z2, chosen_z2_lable, device, outputPDFname, pathToData, pathToExports, 
                        pathToOutput, pathToGatingFunctions, rPath, analysis_type_version, user_id
                    ):
    start_time = Berlin_time()
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_start_time=start_time)
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="In Progress")

    sample_obj = models.ExperimentFiles.objects.values_list('file_id', 'file', 'file_name','allergen', 'control').filter(analysis_id = analysis_id)
    nrFiles = len(sample_obj)
    info = [None]*nrFiles
    reports = [None]*nrFiles
    algList = [None]*nrFiles
    files_list = []
    #usName = ''
    posFileName = ''
    posTwoFileName= ''
    unstainedFileName = ''
    #chosen_x_label = "Siglec-8"
    #chosen_z1 = "FSC-A"
    #chosen_z1_lable = "FSC_A"

    chosen_z2_filtered = [i for i in chosen_z2 if i is not None]
    chosen_z2_label_filtered = [i for i in chosen_z2_lable if i is not None]
    nr_zMarkers = len(chosen_z2_filtered)

    i = 0
    quality_messages = []
    #info_messages = ""
    try:
        for sample in sample_obj:
            file_id = sample[0]
            file_path = sample[1]
            file_name = sample[2]
            allergen = sample[3]
            algList[i] = allergen

            control = sample[4]
            if control == 'Primary Positive control':
                posFileName = file_name
            elif control == 'Secondary Positive control':
                posTwoFileName = file_name

            elif control == 'Negative control':
                usName = file_name

            elif control == 'Unstained':
                unstainedFileName = file_name

            if panel_name in ["bat-panel", "reduced-panel"]:
                baumgrassgater = BaumgrassGating(               
                                     
                                     file_path,            
                                     pathToGatingFunctions, 
                                     device, 
                                     pathToExports,
                                     report_Id = i)
                
                reports[i], info[i] = baumgrassgater.runbaumgrassgating()
                
                print(reports[i].getId())
                print(reports[i].getReport())
                files_list.append(pathToExports + file_name) # build filelist for triplots

                i += 1
            else:
                if condition:
                    pathToExports = (f'/home/abusr/autoBatWeb/auto-BAT-Web/media/FCS_fiels/{bat_name}/{donor_name}/{panel_name}/{condition}/')
                else:
                    pathToExports = (f'/home/abusr/autoBatWeb/auto-BAT-Web/media/FCS_fiels/{bat_name}/{donor_name}/{panel_name}/')
                files_list.append(pathToExports + file_name)

                try:
                    total_cells = get_object_or_404(models.MetaData.objects.filter(file_id=file_id, labels='tot').values_list('values', flat=True))
                except:
                    total_cells = 0
                
                reports[i] = Report(id = i) 
                reports[i].setZMarker("NA") # what if only one z_marker?       
                reports[i].setFilename(file_name)              
                reports[i].setCellTotal(total_cells)

            # percentages for distinct gating steps as measure for control - here all set to zero since no pregating is done               
                reports[i].setDebrisPerc(0)     
                reports[i].setFirstDoubPerc(0)               
                reports[i].setSecDoubPerc(0)

                print(reports[i].getId())
                print(reports[i].getReport())
                
                info[i]= ["For this panel no automatic pregating is done"]
                i += 1
            print(algList)
            print(info)
        
        # report STEP 2: Based on Reports per File create reports for each file AND each marker
        if nr_zMarkers == 1:
            reports[i].setZMarker(chosen_z2_label_filtered)
        
        if nr_zMarkers > 1:

        # new variables to reflect needed number of reports, etc
            grat_reports = [None]*(len(files_list)*nr_zMarkers)
            grat_info = [None]*(len(files_list)*nr_zMarkers)
            grat_algList = [None]*(len(files_list)*nr_zMarkers)
            
            count = 0
            
            for i in range(len(files_list)):
                for j in range(nr_zMarkers):
                    print("Creating reports for more than 1 z-Marker")
                    
                    print( "Counter: ", count)
                    grat_reports[count] = Report(id = count) 
                    grat_reports[count].setFilename(reports[i].filename) 
                    grat_reports[count].setZMarker(chosen_z2_label_filtered[j])
                    grat_reports[count].setCellTotal(reports[i].cellTotal)
                    grat_reports[count].setDebrisPerc(reports[i].debrisperc)            
                    grat_reports[count].setFirstDoubPerc(reports[i].firstdoubperc)
                    grat_reports[count].setSecDoubPerc(reports[i].secdoubperc)

                    grat_algList[count] = algList[i]
                    grat_info[count] = info[i]
                    
                    print(grat_reports[count].getId())
                    print(grat_reports[count].getReport())
                    
                    count = count + 1 

            reports = grat_reports
            info = grat_info
            algList = grat_algList
            
        
        autoworkflow = AutoBatWorkflow(files_list,
                                    pathToData,
                                    pathToExports,
                                    pathToOutput,
                                    outputPDFname,
                                    pathToGatingFunctions,
                                    device,
                                    chosen_x,   # Siglec-8
                                    chosen_y1,   # CD66b
                                    chosen_z1,
                                    chosen_z2,
                                    chosen_x_label,
                                    chosen_y1_lable,
                                    chosen_z1_lable,
                                    chosen_z2_lable,
                                    str(usName),
                                    str(posFileName),
                                    str(posTwoFileName),
                                    str(unstainedFileName),
                                    rPath,
                                    webapp="Yes")

        #results = autoworkflow.runAutoGRAT()
        df, Siglec, CD66, threshold_df = autoworkflow.runAutoGRAT()
        #df = results[0]
        ###################################################################
        # check out folder set as output folder for results
        #algList.insert(0, 'NA')
        #print(algList)
        #df.insert(0, 'ID', algList, True) # I somehow needed this row
        #print(df)
        #df = df.set_index('ID')
        print('##################################################')
        finalReport = Reporting(reports)
        finalReport = finalReport.constructReport()
        print(finalReport)
        print('##################################################')
        print(algList)
        #df = df.drop(['zMarker'], axis=1)
        #df = df.set_index('filename')
        print(df)
        
        for j in range(len(reports)):               
            reports[j].setRed(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["redQ4"]))                
            reports[j].setBlack(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["blackQ2"]))        
            reports[j].setBlackQ3(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["blackQ3"]))        
            reports[j].setBlackQ4(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["blackQ4"]))        
            reports[j].setZmean(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["zmeanQ4"]))
            reports[j].setZ1Min(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["Z1_min"]))
            reports[j].setZ1max(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["Z1_max"]))
            reports[j].setMsiY(float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["msi_Y"]))                                                                
            reports[j].cellQ3 = float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["cellQ3"])                                 
            reports[j].cellQ4 = float(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["cellQ4"]) 
            reports[j].setResult(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["result"].values[0]) 
            reports[j].setResponder(df[df['filename'].str.contains(reports[j].filename.lower(), regex=False) & df['zMarker'].str.contains(reports[j].zMarker)]["responder"].values[0]) 
            reports[j].setPlotSympol(None)
            if int(reports[j].cellTotal) < 100000:
                reports[j].setPlotSympol('unclear')           
            if reports[j].cellQ4 < 350:
                reports[j].setPlotSympol('unclear')
                print("\n The number of events in Q4 (basophils) is smaller than 350. This might result in problems with the analysis and the results must be handled with care. \n")
                info_cellQ4 = "The number of events in Q4 (basophils) is smaller than 350. This might result in problems with the analysis and the results must be handled with care."
            
            info[i].append(info_cellQ4)
            reports[j].setQualityMessages(info[i])
        ###==========================================================================================================================###
        # filling the quality messages column with the file specific error messages and
        # also applying the thresholds for responder/nonresponder in the controls

            #if reports[i].getId() == "us":               # bei der negativen Kontrolle kann ich auch die Thresholding Infos anfügen
                #reports[i].setQualityMessages(info[0])
                
                
            if "aige" in reports[j].filename.lower(): 
                if reports[j].red >= 5.0: 
                    reports[j].setResponder("aIgE Responder") 
                else: 
                    reports[j].setResponder("aIgE Non-Responder")

            if "fmlp" in reports[i].filename.lower():
                if reports[j].red >= 5.0: 
                    reports[j].setResponder("fMLP Responder") 
                else: 
                    reports[j].setResponder("fMLP Non-Responder")
        ###==========================================================================================================================###

        print(df)
        finalReport = Reporting(reports)
        finalReport = finalReport.constructReport()
        
        print("\n -- This is the final report: \n")
        print(finalReport)
        ###################################################################
        """
        """
        chosen_z2_1 = str(chosen_z2[0]) 
        chosen_z2_2 = str(chosen_z2[1])
        chosen_z2_3 = str(chosen_z2[2])
        chosen_z2_4 = str(chosen_z2[3])
        if condition:
            excel_file = os.path.join(pathToOutput, f'AutoGrat_{bat_name}_{donor_name}_{panel_name}_{condition}_{chosen_z1}_{chosen_y1}_{chosen_z2_1}_{chosen_z2_2}.xlsx')
        else:
            excel_file = os.path.join(pathToOutput, f'AutoGrat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2_1}_{chosen_z2_2}.xlsx')
        df_excel = df
        df_excel['Version'] = analysis_type_version
        df_excel.drop(df[df['filename'] == '0'].index, inplace = True)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df_excel.to_excel(writer, sheet_name='Sheet1')

        # Get the xlsxwriter workbook and worksheet objects.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        cell_format = workbook.add_format({'bg_color': 'yellow'})

        for r in range(0,len(df_excel.index)):
            if df_excel.iat[r,2] == "positiv":
                worksheet.set_row(r+1, None, cell_format)
        worksheet.autofit()
        writer.save()

        # Save Thresholds to the Database
        
        try:
            Z2_1_Threshold = float(threshold_df.loc[threshold_df['Channel'] == chosen_z2_1, 'Value'])
        except:
            Z2_1_Threshold = None
        try:
            Z2_2_Threshold = float(threshold_df.loc[threshold_df['Channel'] == chosen_z2_2, 'Value'])
        except:
            Z2_2_Threshold = None
        try:
            Z2_3_Threshold = float(threshold_df.loc[threshold_df['Channel'] == chosen_z2_3, 'Value'])
        except:
            Z2_3_Threshold = None
        try:
            Z2_4_Threshold = float(threshold_df.loc[threshold_df['Channel'] == chosen_z2_4, 'Value'])
        except:
            Z2_4_Threshold = None
        
        thresholds_instance = models.AnalysisThresholds(
                                        X_Threshold = float(Siglec),
                                        Y_Threshold = float(CD66),
                                        Z2_1_Threshold = Z2_1_Threshold,
                                        Z2_2_Threshold = Z2_2_Threshold,
                                        Z2_3_Threshold = Z2_3_Threshold,
                                        Z2_4_Threshold = Z2_4_Threshold
            )
        thresholds_instance.analysisMarker_id_id = int(analysisMarker_id)
        thresholds_instance.save()
        # Save DF to the Database
        
        
        # Save DF to the Database
        for index, row in finalReport.iterrows():
            file_name = index
            file_id = get_object_or_404(models.ExperimentFiles.objects.filter(file_name__icontains=file_name, analysis_id=analysis_id).values_list('file_id', flat=True))
            file_name = get_object_or_404(models.ExperimentFiles.objects.filter(file_name__icontains=file_name, analysis_id=analysis_id).values_list('file_name', flat=True))
            debrisPerc = row['debrisPerc']
            firstDoubPerc = row['firstDoubPerc']
            secDoubPerc = row['secDoubPerc']
            zMarker = row['zMarker']
            redQ4 = float(row['redQ4'])
            result = row['result']
            blackQ2 = row['blackQ2']
            blackQ3 = row['blackQ3']
            blackQ4 = row['blackQ4']
            zmeanQ4 = row['zmeanQ4']
            Z1_minQ4 = row['Z1_minQ4']
            Z1_maxQ4 = row['Z1_maxQ4']
            msi_YQ4 = row['msi_YQ4']
            cellQ3 = row['cellQ3']
            cellQ4 = row['cellQ4']
            responder = row['responder']
            cellTotal = row['cellTotal']
            qualityMessages = row['qualityMessages']
            plot_symbol = row['plot_symbol']
            z = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pns=zMarker).values_list('pnn', flat=True))
            plot_name = f'{file_name[:-4].lower()}_{z}.pdf'
            plot_path=os.path.join(pathToOutput, plot_name)
            if plot_symbol == 'unclear':
                add_symbol(plot_path, plot_path, error=True, checked = False, solved=False)
            if ', []' in str(qualityMessages):
                qualityMessages = str(qualityMessages).replace(', []','')

            if qualityMessages != 'empty':
                quality_messages.append(qualityMessages)

            results_instance = models.AnalysisResults(
                                        debrisPerc = debrisPerc,
                                        firstDoubPerc = firstDoubPerc,
                                        secDoubPerc = secDoubPerc,
                                        zMarker = zMarker
                                        redQ4 = redQ4,
                                        result = result,
                                        blackQ2 = blackQ2,
                                        blackQ3 = blackQ3,
                                        blackQ4 = blackQ4,
                                        zmeanQ4 = zmeanQ4,
                                        Z1_minQ4 = Z1_minQ4,
                                        Z1_maxQ4 = Z1_maxQ4,
                                        msi_YQ4 = msi_YQ4,
                                        cellQ3 = cellQ3,
                                        cellQ4 = cellQ4,
                                        cellTotal = cellTotal,
                                        qualityMessages = qualityMessages,
                                        plot_symbol=plot_symbol,
                                        responder = responder,
            )
            results_instance.file_id_id = int(file_id)
            results_instance.analysisMarker_id_id = int(analysisMarker_id)
            results_instance.user_id = user_id
            results_instance.save()
        # save the  info messages
        #models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_info_messages = info_messages)
        quality_messages = ', '.join(str(v) for v in quality_messages)
        models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_info_messages = quality_messages)
        # Save plots to database
        pdf_list_1 = []
        pdf_list_2 = []
        #chosen_z2.extend(('FSC-A', 'SSC-A'))
        for file in sample_obj:
            file_id = file[0]
            file_name = file[2].lower()
            control = file[4]
            for marker in chosen_z2:
                if marker:
                    if control == "Unstained":
                        plot_name = f'{file_name[:-4]}_histogram.pdf'
                    else:
                        plot_name = f'{file_name[:-4]}_{marker}.pdf'
                    plot_path=os.path.join(pathToOutput, plot_name)
                    PDFresults_instance = models.FilesPlots(plot_path=plot_path)
                    PDFresults_instance.file_id_id = int(file_id)
                    PDFresults_instance.analysisMarker_id_id = int(analysisMarker_id)
                    PDFresults_instance.save()
                    if control == "Unstained":
                        pdf_list_2.append(plot_path)
                    else:
                        pdf_list_1.append(plot_path)
    
        # Save Excel File's path to the Database
        EXCELresults_instance = models.AnalysisFiles(file_path=excel_file, file_type="Excel")
        EXCELresults_instance.analysisMarker_id_id = int(analysisMarker_id)
        EXCELresults_instance.save()


        # Create PDF File:
        pdf_list = []
        pdf_list.append(pdf_list_1)
        pdf_list.append(pdf_list_2)
        if condition:
            pdf = f"AutoGrat_{bat_name}_{donor_name}_{panel_name}_{condition}_{chosen_z1}_{chosen_y1}_{chosen_z2_1}_{chosen_z2_2}.pdf"
        else:
            pdf = f"AutoGrat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2_1}_{chosen_z2_2}.pdf"
        pdf_path = os.path.join(pathToOutput, pdf)
        save_pdf(pdf_path, pdf_list, analysisMarker_id, 'AutoGrat')

    except Exception:
        e = traceback.format_exc()
        models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Error", analysis_error=e)
