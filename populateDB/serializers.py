from django.shortcuts import get_object_or_404
from rest_framework import serializers
from . import models



class ResultsSerializers(serializers.ModelSerializer):
    bat_name = serializers.SerializerMethodField()
    donor_name = serializers.SerializerMethodField()
    panel_name = serializers.SerializerMethodField()
    analysis_id = serializers.SerializerMethodField()
    date_of_measurement = serializers.SerializerMethodField()
    analysis_type = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    allergen = serializers.SerializerMethodField()
    control =serializers.SerializerMethodField()
    clinicalClass_name = serializers.SerializerMethodField()
    ofc_class = serializers.SerializerMethodField()
    wheat_flour = serializers.SerializerMethodField()
    gluten = serializers.SerializerMethodField()
    gliadin = serializers.SerializerMethodField()
    tri_a_19 = serializers.SerializerMethodField()
    tri_a_14 = serializers.SerializerMethodField()
    class Meta:
        model = models.AnalysisResults
        fields = ('id', 'bat_name', 'donor_name', 'panel_name', 'analysis_type', 'analysis_id',
                'date_of_measurement', 'file_name', 'allergen', 'control',
                'clinicalClass_name', 'ofc_class', 'wheat_flour', 'gluten', 'gliadin', 'tri_a_19', 'tri_a_14',
                'redQ4', 'result', 'blackQ2', 'blackQ3', 'blackQ4', 'zmeanQ4', 'z1_min', 'z1_max', 'msi_Y', 'cellQ4', 'responder')

    def get_bat_name(self, obj):
        bat_name = obj['analysisMarker_id__analysis_id__bat_id__bat_name']
        if bat_name:
            return bat_name
        else:
            return None
    def get_donor_name(self, obj):
        donor_name = obj['analysisMarker_id__analysis_id__donor_id__donor_abbr']
        if donor_name:
            return donor_name
        else:
            return None
    def get_panel_name(self, obj):
        panel_name = obj['analysisMarker_id__analysis_id__panel_id__panel_name']
        if panel_name:
            return panel_name
        else:
            return None
    def get_analysis_type(self, obj):
        analysis_type = obj['analysisMarker_id__analysis_type']
        if analysis_type:
            return analysis_type
        else:
            return None

    def get_analysis_id(self, obj):
        analysis_id = obj['analysisMarker_id__analysis_id']
        if analysis_id:
            return analysis_id
        else:
            return None
    def get_date_of_measurement(self, obj):
        date_of_measurement = obj['analysisMarker_id__analysis_id__bat_id__date_of_measurement']
        if date_of_measurement:
            return date_of_measurement
        else:
            return None
    def get_file_name(self, obj):
        file_name = obj['file_id__file_name']
        if file_name:
            return file_name
        else:
            return None
    def get_allergen(self, obj):
        allergen = obj['file_id__allergen']
        if allergen:
            return allergen
        else:
            return None
    def get_control(self, obj):
        control = obj['file_id__control']
        if control:
            return control
        else:
            return None
    def get_clinicalClass_name(self, obj):
        clinicalClass_name = obj['analysisMarker_id__analysis_id__donor_id__donorclass_clinical__donor_clinicalClass_id__clinicalClass_name']
        if clinicalClass_name:
            return clinicalClass_name
        else:
            return None
    def get_ofc_class(self, obj):
        ofc_class = obj['analysisMarker_id__analysis_id__donor_id__donorclass_ofc__donor_ofc']
        if ofc_class:
            return ofc_class
        else:
            return None
    def get_wheat_flour(self, obj):
        wheat_flour = obj['analysisMarker_id__analysis_id__donor_id__donorclass_sige__wheat_flour']
        if wheat_flour:
            return wheat_flour
        else:
            return None
    def get_gluten(self, obj):
        gluten = obj['analysisMarker_id__analysis_id__donor_id__donorclass_sige__gluten']
        if gluten:
            return gluten
        else:
            return None
    def get_gliadin(self, obj):
        gliadin = obj['analysisMarker_id__analysis_id__donor_id__donorclass_sige__gliadin']
        if gliadin:
            return gliadin
        else:
            return None
    def get_tri_a_19(self, obj):
        tri_a_19 = obj['analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_19']
        if tri_a_19:
            return tri_a_19
        else:
            return None
    def get_tri_a_14(self, obj):
        tri_a_14 = obj['analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_14']
        if tri_a_14:
            return tri_a_14
        else:
            return None
