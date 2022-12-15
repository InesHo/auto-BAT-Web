from background_task import background
from logging import getLogger
from Data import Data
from . import models
from .functions import image_grid, Berlin_time
import os
import sys
from PIL import Image
import pandas as pd
import math
import config
sys.path.insert(0, os.path.join(config.AUTOBAT_PATH, 'autoBat'))
from BaumgrassGating import BaumgrassGating
#from AutoBatWorkflow import AutoBatWorkflow
import flowkit as fk

logger = getLogger(__name__)


       
@background(queue='autoBat-queue', schedule=10)
def save_pdf(pdf_path, img_list, analysisMarker_id):
        
    image_grid(img_list, pdf_path)

    # Save pdf plot to database
    PDFresults_instance = models.AnalysisFiles(file_path=pdf_path, file_type="PDF", analysisMarker_id = analysisMarker_id)
    PDFresults_instance.save()
    
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Ready")
    end_time = Berlin_time()
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_end_time=end_time)

@background(queue='autoBat-queue', schedule=10)
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
                                    file_id = file_id,
                                    )
        
            meta_obj.save()

        pnnLabels = filename.pnn_labels
        xform = fk.transforms.LogicleTransform('asinh', param_t=1024, param_w=0.5, param_m=4.5, param_a=0)
        filename.apply_transform(xform)
        content = filename.as_dataframe(source='xform', col_names=pnnLabels)
        raw_fcs_val = content.to_dict()
        for label in pnnLabels:
            labels = f"{label}_mean"
            values = math.ceil((sum(raw_fcs_val[label].values())) / len(raw_fcs_val[label]) * 100) / 100
            mean_obj = models.MeanRawData(
                                    labels = labels,
                                    values = values,
                                    file_id = file_id,
                                    )
            mean_obj.save()

@background(queue='autoBat-queue', schedule=10)
def run_analysis_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name,
                        chosen_z1, chosen_y1, chosen_z2, device, outputPDFname, pathToData, pathToExports, 
                        pathToOutput, pathToGatingFunctions, rPath
                    ):

    start_time = Berlin_time()
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_start_time=start_time)
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="In Progress")

    sample_obj = models.ExperimentFiles.objects.values_list('file_id', 'file', 'file_name','allergen', 'control').filter(analysis_id = analysis_id)
    nrFiles = len(sample_obj)
    reports = [None]*nrFiles
    algList = [None]*nrFiles
    files_list = []
    usName = ''
    posFileName = ''
    posTwoFileName= ''

    i = 0
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
        
        baumgrassgater = BaumgrassGating(allergen,               
                                chosen_z1,
                                file_path,            
                                pathToGatingFunctions, 
                                device, 
                                pathToExports)

        reports[i] = baumgrassgater.runbaumgrassgating()
        files_list.append(pathToExports + file_name)               
        i += 1
    autoworkflow = AutoBatWorkflow(files_list,
                                    pathToData,
                                    pathToExports,
                                    pathToOutput,
                                    outputPDFname, 
                                    pathToGatingFunctions,
                                    device,
                                    chosen_z1,
                                    chosen_y1,
                                    chosen_z2, 
                                    str(usName),
                                    str(posFileName),
                                    str(posTwoFileName),
                                    rPath,
                                    webapp="Yes")
    
    
    
    df = autoworkflow.runCD32thresholding()

    excel_file = os.path.join(pathToOutput, f'AutoBat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.xlsx')
    writer = pd.ExcelWriter(excel_file)
    df.to_excel(writer)
    writer.save()   
    
    # Save Excel File's path to the Database
    EXCELresults_instance = models.AnalysisFiles(file_path=excel_file, file_type="Excel", analysisMarker_id = analysisMarker_id)
    EXCELresults_instance.save()
   
    # Save DF to the Database
    for index, row in df.iterrows():
        redQ4 = row['redQ4']
        result = row['result']
        blackQ2 = row['blackQ2']
        blackQ3 = row['blackQ3']
        blackQ4 = row['blackQ4']
        zmeanQ4 = row['zmeanQ4']
        CD63min = row['CD63min']
        CD63max = row['CD63max']
        msiCCR3 = row['msiCCR3']
        cellQ4 = row['cellQ4']
        responder = row['responder']
        results_instance = models.AnalysisResults(
                                        redQ4 = redQ4,
                                        result = result,
                                        blackQ2 = blackQ2,
                                        blackQ3 = blackQ3,
                                        blackQ4 = blackQ4,
                                        zmeanQ4 = zmeanQ4,
                                        CD63min = CD63min,
                                        CD63max = CD63max,
                                        msiCCR3 = msiCCR3,
                                        cellQ4 = cellQ4,
                                        responder = responder,
                                        analysisMarker_id = analysisMarker_id
        )
        results_instance.save()
    # Save plots to database
    img_list = []
    for file in sample_obj:
        file_id = file[0]
        plot_name = file[2].lower()
        plot_name = f'{ plot_name[:-4]}.png'
        plot_path=os.path.join(pathToOutput, plot_name)
        PNGresults_instance = models.FilesPlots(plot_path=plot_path, file_id=file_id)
        PNGresults_instance.save()
        img_list.append(plot_path)
    
    # Create PDF File:
    pdf = f"Autogated_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.pdf"
    pdf_path = os.path.join(pathToOutput, pdf)
    save_pdf(pdf_path, img_list, analysisMarker_id)

