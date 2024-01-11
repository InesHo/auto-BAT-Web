from background_task import background
from logging import getLogger
from . import models
from .functions import pdf_grid, image_grid, Berlin_time
import os
import sys
from PIL import Image
import pandas as pd
import math
import config
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
    
    if analysis_type == "autograt":
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
def run_analysis_autobat_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name,
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
                pathToExports = (f'/home/abusr/autoBatWeb/auto-BAT-Web/media/FCS_fiels/{bat_name}/{donor_name}/{panel_name}/')
                files_list.append(pathToExports + file_name)

                reports[i] = Report(id = file_name.lower())
                total_cells = get_object_or_404(models.MetaData.objects.filter(file_id=file_id, labels='tot').values_list('values', flat=True))
                reports[i].setCellTotal(total_cells)
                reports[i].setDebrisPerc(0) 
                reports[i].setFirstDoubPerc(0)
                reports[i].setSecDoubPerc(0)
                info[i]= ["For this panel no automatic pregating is done"]
                i += 1
            
            else:
                baumgrassgater = BaumgrassGating(chosen_z1,
                                file_path,            
                                pathToGatingFunctions, 
                                device, 
                                pathToExports)

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
        else:
            df, SSCA, FCR, CD63, info_bg = autoworkflow.runCD32thresholding()
        quality_messages.append(info_bg)
        print("\n -- This is the dataframe from first part of reporting: \n")
        print(df)
        #results = autoworkflow.runCD32thresholding()
        # check out folder set as output folder for results
        df = df.set_index('filename')
        info_cellQ4 = []

        for i in range(len(reports)):
            #reports[i].setFileName(df.loc[reports[i].getId(),"filename"])
            reports[i].setRed(df.loc[reports[i].getId().lower(),"redQ4"])
            reports[i].setBlack(df.loc[reports[i].getId().lower(),"blackQ2"])
            reports[i].setBlackQ3(df.loc[reports[i].getId().lower(),"blackQ3"])
            reports[i].setBlackQ4(df.loc[reports[i].getId().lower(),"blackQ4"])
            reports[i].setZmean(df.loc[reports[i].getId().lower(),"zmeanQ4"])
            reports[i].setZ1Min(df.loc[reports[i].getId().lower(),"Z1_min"])
            reports[i].setZ1max(df.loc[reports[i].getId().lower(),"Z1_max"])
            reports[i].setMsiY(df.loc[reports[i].getId().lower(),"msi_Y"])
            reports[i].cellQ3 = df.loc[reports[i].getId().lower(),"cellQ3"]
            reports[i].cellQ4 = df.loc[reports[i].getId().lower(),"cellQ4"]
            reports[i].setResult(df.loc[reports[i].getId().lower(),"result"])
            reports[i].setResponder(df.loc[reports[i].getId().lower(),"responder"])
            if reports[i].cellQ4  < 350:
                print("\n The number of events in Q4 (basophils) is smaller than 350. This might result in problems with the analysis and the results must be handled with care. \n")
                info_cellQ4 = "The number of events in Q4 (basophils) is smaller than 350. This might result in problems with the analysis and the results must be handled with care."



        ###==========================================================================================================================###
        # filling the quality messages column with the file specific error messages and
        # also applying the thresholds for responder/nonresponder in the controls

            if reports[i].getId() == "us":               # bei der negativen Kontrolle kann ich auch die Thresholding Infos anfügen
                info[i].extend((info_bg, info_cellQ4))
                #reports[i].setQualityMessages(info[i])
            else:
                info[i].append(info_cellQ4)

            if "aIgE" in reports[i].getId():
                #reports[i].setQualityMessages(info[i])
                if reports[i].red >= 5.0:
                    reports[i].setResponder("aIgE Responder")
                else:
                    reports[i].setResponder("aIgE Non-Responder")

            if "fMLP" in reports[i].getId():
                #reports[i].setQualityMessages(info[i])
                if reports[i].red >= 5.0:
                    reports[i].setResponder("fMLP Responder")
                else:
                    reports[i].setResponder("fMLP Non-Responder")
            reports[i].setQualityMessages(info[i])
            """
            if "us" in reports[i].getId().lower():               # bei der negativen Kontrolle kann ich auch die Thresholding Infos anfügen
                reports[i].setQualityMessages(info[0] + info_bg + info_cellQ4)
                reports[i].setYThreshold(FCR)
                reports[i].setZ1Threshold(CD63)

            if "aige" in reports[i].getId().lower():
                reports[i].setQualityMessages(info[2] + info_cellQ4)
                if reports[i].red >= 5.0:
                    reports[i].setResponder("aIgE Responder")
                else:
                    reports[i].setResponder("aIgE Non-Responder")

            if "fmlp" in reports[i].getId().lower():
                reports[i].setQualityMessages(info[1] + info_cellQ4)
                if reports[i].red >= 5.0:
                    reports[i].setResponder("fMLP Responder")
                else:
                    reports[i].setResponder("fMLP Non-Responder")
            """
        finalReport = Reporting(reports)
        finalReport = finalReport.constructReport()

        print("\n -- This is the final report: \n")
        print(finalReport)

        ### save report to .xls
        excel_file = os.path.join(pathToOutput, f'AutoBat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.xlsx')
        df_excel = finalReport
        df_excel['Version'] = analysis_type_version
        #df_excel.drop(df[df['filename'] == '0'].index, inplace = True)
    
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df_excel.to_excel(writer, sheet_name='Sheet1')

        """
        # Get the xlsxwriter workbook and worksheet objects.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        cell_format = workbook.add_format({'bg_color': 'yellow'})

        for r in range(0,len(df_excel.index)):
            if df_excel.iat[r,2] == "positiv":
                worksheet.set_row(r+1, None, cell_format) 

        worksheet.autofit()
        """
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
        pdf = f"AutoBat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.pdf"
        pdf_path = os.path.join(pathToOutput, pdf)
        
        save_pdf(pdf_path, pdf_list, analysisMarker_id, 'autobat')
    except Exception:
        e = traceback.format_exc()
        models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Error", analysis_error=e)



@background(queue='autograt-queue-analysis', schedule=10)
def run_analysis_autograt_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name,
                        chosen_x, chosen_x_label, chosen_y1, chosen_y1_lable, chosen_z1, chosen_z1_lable, chosen_z2, chosen_z2_lable, device, outputPDFname, pathToData, pathToExports, 
                        pathToOutput, pathToGatingFunctions, rPath, analysis_type_version, user_id
                    ):
    start_time = Berlin_time()
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_start_time=start_time)
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="In Progress")

    sample_obj = models.ExperimentFiles.objects.values_list('file_id', 'file', 'file_name','allergen', 'control').filter(analysis_id = analysis_id)
    nrFiles = len(sample_obj)
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

    i = 0
    info_messages = ""
    try:
        for sample in sample_obj:
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

            if panel_name in ['full-panel', 'grat-panel']:
                pathToExports = (f'/home/abusr/autoBatWeb/auto-BAT-Web/media/FCS_fiels/{bat_name}/{donor_name}/{panel_name}/')
                files_list.append(pathToExports + file_name)
            else:
                baumgrassgater = BaumgrassGating(chosen_x,
                                file_path,
                                pathToGatingFunctions,
                                device,
                                pathToExports)

                reports[i] = baumgrassgater.runbaumgrassgating()
                files_list.append(pathToExports + file_name)
                info_messages = str(reports[i][1])
                i += 1
        print(usName)
        print(pathToExports)
        print(pathToOutput)
        print(files_list)
        print(pathToData)
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
        """
        for row in df.index:
            df['responder'][row] = 'NA'
            if "aige" in df['filename'][row]:
                if df['redQ4'][row] >= 5.0:
                    df['responder'][row] = "aIgE Responder"
                elif df['redQ4'][row] < 5.0:
                    df['responder'][row] = "aIgE None_Responder"
            elif "fmlp" in df['filename'][row]:
                if df['redQ4'][row] >= 5.0:
                    df['responder'][row] = "fMLP Responder"
                elif df['redQ4'][row] < 5.0:
                    df['responder'][row] = "fMLP None_Responder"
        """
        chosen_z2_1 = str(chosen_z2[0]) 
        chosen_z2_2 = str(chosen_z2[1])
        chosen_z2_3 = str(chosen_z2[2])
        chosen_z2_4 = str(chosen_z2[3])
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
        print(df)
        for index, row in df.iterrows():
            file_name = row['filename']
            file_id = get_object_or_404(models.ExperimentFiles.objects.filter(file_name__icontains=file_name, analysis_id=analysis_id).values_list('file_id', flat=True))
            print(file_id)
            zMarker = row['zMarker']
            redQ4 = float(row['redQ4'])
            result = row['result']
            blackQ2 = row['blackQ2']
            blackQ3 = row['blackQ3']
            blackQ4 = row['blackQ4']
            zmeanQ4 = row['zmeanQ4']
            Z1_minQ4 = row['Z1_min']
            Z1_maxQ4 = row['Z1_max']
            msi_YQ4 = row['msi_Y']
            cellQ3 = row['cellQ3']
            cellQ4 = row['cellQ4']
            responder = row['responder']

            results_instance = models.AnalysisResults(
                                        zMarker = zMarker,
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
                                        responder = responder,
            )
            results_instance.file_id_id = int(file_id)
            results_instance.analysisMarker_id_id = int(analysisMarker_id)
            results_instance.user_id = user_id
            results_instance.save()

        # save the  info messages
        models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_info_messages = info_messages)
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
        pdf = f"AutoGrat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2_1}_{chosen_z2_2}.pdf"
        pdf_path = os.path.join(pathToOutput, pdf)
        save_pdf(pdf_path, pdf_list, analysisMarker_id, 'autograt')
    except Exception:
        e = traceback.format_exc()
        models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Error", analysis_error=e)
