var send_data = {}
$(document).ready(function () {
    // reset all parameters on page load
    resetFilters();
    // bring all the data without any filters
    getAPIData();
    // get all countries from database via 
    // AJAX call into bat_name select options
    getBat_names();
    // get all varities from database via 
    // AJAX call into variert select options
    getPanel_names();
    getFile_controls();
    getFile_controls_compare();
    getClinical_classes();
    getResponders();
    getOFC_classes();
    getOFC_classesExercise();
    getAnalysis_results();
    getAnalysis_type();
    // on selecting the bat_name option
    $('#bat_names').on('change', function () {
        // update the selected bat_name
 	if(this.value == "all")
            send_data['bat_name'] = "";
        else
            send_data['bat_name'] = this.value;
        getAPIData();
    });

    // on filtering the donor_name input
    $('#donor_names').on('input', function () {
        // get the api data of updated donor_name
        if(this.value == "all")
            send_data['donor_name'] = "";
        else
            send_data['donor_name'] = this.value;
        getAPIData();
    });


    // on on selecting the panel_name option
    $('#panel_names').on('change', function () {
        // get the api data of updated panel_name
        if(this.value == "all")
            send_data['panel_name'] = "";
        else
            send_data['panel_name'] = this.value;
        getAPIData();
    });

    // on on selecting the analysis_type option
    $('#analysis_type').on('change', function () {
        // get the api data of updated panel_name
        if(this.value == "all")
            send_data['analysis_type'] = "";
        else
            send_data['analysis_type'] = this.value;
        getAPIData();
    });


    // on filtering the marker_name input
    $('#marker_names').on('input', function () {
        // get the api data of updated marker_name
        if(this.value == "all")
            send_data['marker_name'] = "";
        else
            send_data['marker_name'] = this.value;
        getAPIData();
    });
    // on filtering the date_min input
    $('#date_min').on('change', function () {
        // get the api data of updated date_min
        if(this.value == "all")
            send_data['date_min'] = "";
        else
            send_data['date_min'] = this.value;
        getAPIData();
    });
    // on filtering the file date_max input
    $('#date_max').on('change', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['date_max'] = "";
        else
            send_data['date_max'] = this.value;
        getAPIData();
    });
    // on filtering the file allergens input
    $('#allergens').on('input', function () {
        // get the api data of updated file allergens
        if(this.value == "all")
            send_data['allergens'] = "";
        else
            send_data['allergens'] = this.value;
        getAPIData();
    });

    // on filtering the file control input
    $('#file_controls').on('change', function () {
        // get the api data of updated file controls
        if(this.value == "all")
            send_data['file_controls'] = "";
        else
            send_data['file_controls'] = this.value;
        getAPIData();
    });
    // on filtering the file OFC_classes input
    $('#OFC_classes').on('change', function () {
        // get the api data of updated file OFC_classes
        if(this.value == "all")
            send_data['OFC_classes'] = "";
        else
            send_data['OFC_classes'] = this.value;
        getAPIData();
    });
    // on filtering the file clinical_classes input
    $('#clinical_classes').on('change', function () {
        // get the api data of updated file controls
        if(this.value == "all")
            send_data['clinical_classes'] = "";
        else
            send_data['clinical_classes'] = this.value;
        getAPIData();
    });
    // on filtering the file results input
    $('#analysis_results').on('change', function () {
        // get the api data of updated file results
        if(this.value == "all")
            send_data['analysis_results'] = "";
        else
            send_data['analysis_results'] = this.value;
        getAPIData();
    });
    // on filtering the file responders input
    $('#responders').on('input', function () {
        // get the api data of updated file responders
        if(this.value == "all")
            send_data['responders'] = "";
        else
            send_data['responders'] = this.value;
        getAPIData();
    });
    // on filtering the redQ4_min input
    $('#redQ4_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['redQ4_min'] = "";
        else
            send_data['redQ4_min'] = this.value;
        getAPIData();
    });
    // on filtering the file redQ4_max input
    $('#redQ4_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['redQ4_max'] = "";
        else
            send_data['redQ4_max'] = this.value;
        getAPIData();
    });
    // on filtering the blackQ2_min input
    $('#blackQ2_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['blackQ2_min'] = "";
        else
            send_data['blackQ2_min'] = this.value;
        getAPIData();
    });
    // on filtering the file blackQ2_max input
    $('#blackQ2_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['blackQ2_max'] = "";
        else
            send_data['blackQ2_max'] = this.value;
        getAPIData();
    });

    // on filtering the blackQ3_min input
    $('#blackQ3_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['blackQ3_min'] = "";
        else
            send_data['blackQ3_min'] = this.value;
        getAPIData();
    });
    // on filtering the file blackQ3_max input
    $('#blackQ3_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['blackQ3_max'] = "";
        else
            send_data['blackQ3_max'] = this.value;
        getAPIData();
    });

    // on filtering the blackQ4_min input
    $('#blackQ4_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['blackQ4_min'] = "";
        else
            send_data['blackQ4_min'] = this.value;
        getAPIData();
    });
    // on filtering the file blackQ4_max input
    $('#blackQ4_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['blackQ4_max'] = "";
        else
            send_data['blackQ4_max'] = this.value;
        getAPIData();
    });
    // on filtering the zmeanQ4_min input
    $('#zmeanQ4_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['zmeanQ4_min'] = "";
        else
            send_data['zmeanQ4_min'] = this.value;
        getAPIData();
    });
    // on filtering the file zmeanQ4_max input
    $('#zmeanQ4_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['zmeanQ4_max'] = "";
        else
            send_data['zmeanQ4_max'] = this.value;
        getAPIData();
    });
    // on filtering the CD63min_min input
    $('#z1_min_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['z1_min_min'] = "";
        else
            send_data['z1_min_min'] = this.value;
        getAPIData();
    });
    // on filtering the file CD63min_max input
    $('#z1_min_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['z1_min_max'] = "";
        else
            send_data['z1_min_max'] = this.value;
        getAPIData();
    });

    // on filtering the CD63max_min input
    $('#z1_max_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['z1_max_min'] = "";
        else
            send_data['z1_max_min'] = this.value;
        getAPIData();
    });
    // on filtering the file CD63max_max input
    $('#z1_max_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['z1_max_max'] = "";
        else
            send_data['z1_max_max'] = this.value;
        getAPIData();
    });

    // on filtering the msiCCR3_min input
    $('#msi_Y_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['msi_Y_min'] = "";
        else
            send_data['msi_Y_min'] = this.value;
        getAPIData();
    });
    // on filtering the file msiCCR3_max input
    $('#msi_Y_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['msi_Y_max'] = "";
        else
            send_data['msi_Y_max'] = this.value;
        getAPIData();
    });
    // on filtering the cellQ4_min input
    $('#cellQ4_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['cellQ4_min'] = "";
        else
            send_data['cellQ4_min'] = this.value;
        getAPIData();
    });
    // on filtering the file cellQ4_max input
    $('#cellQ4_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['cellQ4_max'] = "";
        else
            send_data['cellQ4_max'] = this.value;
        getAPIData();
    });
    // on filtering the wheatFlour_min input
    $('#wheatFlour_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['wheatFlour_min'] = "";
        else
            send_data['wheatFlour_min'] = this.value;
        getAPIData();
    });
    // on filtering the file wheatFlour_max input
    $('#wheatFlour_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['wheatFlour_max'] = "";
        else
            send_data['wheatFlour_max'] = this.value;
        getAPIData();
    });

    // on filtering the gluten_min input
    $('#gluten_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['gluten_min'] = "";
        else
            send_data['gluten_min'] = this.value;
        getAPIData();
    });
    // on filtering the file gluten_max input
    $('#gluten_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['gluten_max'] = "";
        else
            send_data['gluten_max'] = this.value;
        getAPIData();
    });
    // on filtering the gliadin_min input
    $('#gliadin_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['gliadin_min'] = "";
        else
            send_data['gliadin_min'] = this.value;
        getAPIData();
    });
    // on filtering the file gliadin_max input
    $('#gliadin_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['gliadin_max'] = "";
        else
            send_data['gliadin_max'] = this.value;
        getAPIData();
    });
    // on filtering the tri_a_19_min input
    $('#tri_a_19_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['tri_a_19_min'] = "";
        else
            send_data['tri_a_19_min'] = this.value;
        getAPIData();
    });
    // on filtering the file tri_a_19_max input
    $('#tri_a_19_max').on('input', function () {
        // get the api data of updated file date_max
        if(this.value == "all")
            send_data['tri_a_19_max'] = "";
        else
            send_data['tri_a_19_max'] = this.value;
        getAPIData();
    });
    // on filtering the tri_a_14_min input
    $('#tri_a_14_min').on('input', function () {
        // get the api data of updated redQ4_min
        if(this.value == "all")
            send_data['tri_a_14_min'] = "";
        else
            send_data['tri_a_14_min'] = this.value;
        getAPIData();
    });
    // on filtering the file tri_a_14_max input
    $('#tri_a_14_max').on('input', function () {
        if(this.value == "all")
            send_data['tri_a_14_max'] = "";
        else
            send_data['tri_a_14_max'] = this.value;
        getAPIData();
    });
    // show only average results for each sample
    $('#AVR_sample').on('change', function () {
        if (this.checked)
            send_data['AVR_sample'] = this.value;
        else
            send_data['AVR_sample'] = "";
        getAPIData();
    });
    // show only average results for each donor
    $('#AVR_donor').on('change', function () {
        if (this.checked)
            send_data['AVR_donor'] = this.value;
        else
            send_data['AVR_donor'] = "";
        getAPIData();
    });

    // sort the data
    $('#sort_by').on('change', function () {
        send_data['sort_by'] = this.value;
        getAPIData();
    });

    // display the results after reseting the filters
    $("#reset_filters").click(function(){
        resetFilters();
        getAPIData();
    })
})



/**
    Function that resets all the filters   
**/
function resetFilters() {
    $("#bat_names").val("all");
    $("#donor_names").val("");
    $("#panel_names").val("all");
    $("#analysis_type").val("all");
    
    $("#OFC_classesExercise").val("all");
    $("#marker_names").val("");
    $("#date_min").val("");
    $("#date_max").val("");
    $("#allergens").val("");
    $("#compare_allergen").val("");
    $("#file_controls").val("all");
    $("#compare_file_controls").val("all");
    $("#OFC_classes").val("all");
    $("#clinical_classes").val("all");
    $("#analysis_results").val("all");
    $("#responders").val("all");
    $("#zmarker").val("");
    $("#redQ4_min").val("");
    $("#redQ4_max").val("");
    $("#blackQ2_min").val("");
    $("#blackQ2_max").val("");
    $("#blackQ3_min").val("");
    $("#blackQ3_max").val("");
    $("#blackQ4_min").val("");
    $("#blackQ4_max").val("");
    $("#zmeanQ4_min").val("");
    $("#zmeanQ4_max").val("");
    $("#Z1_minQ4_min").val("");
    $("#Z1_minQ4_max").val("");
    $("#Z1_maxQ4_min").val("");
    $("#Z1_maxQ4_max").val("");
    $("#msi_YQ4_min").val("");
    $("#msi_YQ4_max").val("");
    $("#cellQ4_min").val("");
    $("#cellQ4_max").val("");
    $("#gIgEmin_min").val("");
    $("#gIgEmin_max").val("");
    $("#wheatFlour_min").val("");
    $("#wheatFlour_max").val("");
    $("#gluten_min").val("");
    $("#gluten_max").val("");
    $("#gliadin_min").val("");
    $("#gliadin_max").val("");
    $("#tri_a_19_min").val("");
    $("#tri_a_19_max").val("");
    $("#tri_a_14_min").val("");
    $("#tri_a_14_max").val("");
    $("#Tryptase_min").val("");
    $("#Tryptase_max").val("");
    $("#Histamine_min").val("");
    $("#Histamine_max").val("");
    $("#NaCl_min").val("");
    $("#NaCl_max").val("");
    $("#wheatFlourSPT_min").val("");
    $("#wheatFlourSPT_max").val("");
    $("#glutenSPT_min").val("");
    $("#glutenSPT_max").val("");
    $("#birch_min").val("");
    $("#birch_max").val("");
    $("#mugworth_min").val("");
    $("#mugworth_max").val("");
    $("#timothy_min").val("");
    $("#timothy_max").val("");
    $("#house_dust_mite_min").val("");
    $("#house_dust_mite_max").val("");
    $("#cat_min").val("");
    $("#cat_max").val("");
    $("#AVR_sample").prop('checked',false);
    $("#AVR_donor").prop('checked',false);
    $("#sort_by").val("none");

    send_data['bat_name'] = '';
    send_data['donor_name'] = '';
    send_data['panel_name'] = '';
    send_data['analysis_type'] = '';
    send_data['marker_name'] = '';
    send_data['date_min'] = '';
    send_data['date_max'] = '';
    send_data['allergens'] = '';
    send_data['compare_allergen'] = '';
    send_data['compare_file_controls'] = '';
    send_data['file_controls'] = '';
    send_data['OFC_classes'] = '';
    send_data['clinical_classes'] = '';
    send_data['analysis_results'] = '';
    send_data['responders'] = '';
    send_data['zmarker'] = '';
    send_data['redQ4_min'] = '';
    send_data['redQ4_max'] = '';
    send_data['blackQ2_min'] = '';
    send_data['blackQ2_max'] = '';
    send_data['blackQ3_min'] = '';
    send_data['blackQ3_max'] = '';
    send_data['blackQ4_min'] = '';
    send_data['blackQ4_max'] = '';
    send_data['zmeanQ4_min'] = '';
    send_data['zmeanQ4_max'] = '';
    send_data['z1_min_min'] = '';
    send_data['z1_min_max'] = '';
    send_data['z1_max_min'] = '';
    send_data['z1_max_max'] = '';
    send_data['msi_Y_min'] = '';
    send_data['msi_Y_max'] = '';
    send_data['cellQ4_min'] = '';
    send_data['cellQ4_max'] = '';
    send_data['wheatFlour_min'] = '';
    send_data['wheatFlour_max'] = '';
    send_data['gluten_min'] = '';
    send_data['gluten_max'] = '';
    send_data['gliadin_min'] = '';
    send_data['gliadin_max'] = '';
    send_data['tri_a_19_min'] = '';
    send_data['tri_a_19_max'] = '';
    send_data['tri_a_14_min'] = '';
    send_data['tri_a_14_max'] = '';
    send_data['AVR_sample'] = '';
    send_data['AVR_donor'] = '';
    send_data["sort_by"] = '',
    send_data['format'] = 'json';
}

/**.
    Utility function to showcase the api data 
    we got from backend to the table content
**/
function putTableData(result) {
    // creating table row for each result and
    // pushing to the html cntent of table body of results table
    let row;
    if(result["results"].length > 0){
        $("#no_results").hide();
        $("#list_data").show();
        $("#list_results").html("");  
        $.each(result["results"], function (a, b) {
            row = "<tr> <td>" + b.bat_name + "</td>" +
                "<td>" + b.donor_name + "</td>" +
		"<td>" + b.panel_name + "</td>" +
		"<td>" + b.date_of_measurement + "</td>" +
		"<td>" + b.analysis_type + "</td>" +
		"<td>" + b.file_name + "</td>" +
		"<td>" + b.allergen + "</td>" +
		"<td>" + b.control + "</td>" +
		"<td>" + b.clinicalClass_name + "</td>" +
		"<td>" + b.ofc_class + "</td>" +
                "<td>" + b.wheat_flour + "</td>" +
		"<td>" + b.redQ4.toFixed(2) + "</td>" + 
    		"<td>" + b.result + "</td>" + 
    		"<td>" + b.blackQ2.toFixed(2)+ "</td>" +
    		"<td>" + b.blackQ3.toFixed(2) + "</td>" + 
    		"<td>" + b.blackQ4.toFixed(2) + "</td>" +
    		"<td>" + b.zmeanQ4.toFixed(2) + "</td>" + 
    		"<td>" + b.z1_min.toFixed(2) + "</td>" +
    		"<td>" + b.z1_max.toFixed(2) + "</td>" + 
    		"<td>" + b.msi_Y.toFixed(2) + "</td>" + 
    		"<td>" + b.cellQ4 + "</td>" +
    		"<td>" + b.responder + "</td>" + 
            $("#list_results").append(row);   
        });
    }
    else{
        // if no result found for the given filter, then display no result
        $("#no_results h5").html("No results found");
        $("#list_data").hide();
        $("#no_results").show();
    }
    // setting previous and next page url for the given result
    let prev_url = result["previous"];
    let next_url = result["next"];
    // disabling-enabling button depending on existence of next/prev page. 
    if (prev_url === null) {
        $("#previous").addClass("disabled");
        $("#previous").prop('disabled', true);
    } else {
        $("#previous").removeClass("disabled");
        $("#previous").prop('disabled', false);
    }
    if (next_url === null) {
        $("#next").addClass("disabled");
        $("#next").prop('disabled', true);
    } else {
        $("#next").removeClass("disabled");
        $("#next").prop('disabled', false);
    }
    // setting the url
    $("#previous").attr("url", result["previous"]);
    $("#next").attr("url", result["next"]);
    // displaying result count
    $("#result-count span").html(result["count"]);
}

function getAPIData() {
    let url = $('#list_data').attr("url")
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
    });
}

$("#next").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})

$("#previous").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})

function getBat_names() {
    let url = $("#bat_names").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            bat_names_option = "<option value='all' selected>BAT Name</option>";
            $.each(result["bat_name"], function (a, b) {
                bat_names_option += "<option>" + b + "</option>"
            });
            $("#bat_names").html(bat_names_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getPanel_names() {
    let url = $("#panel_names").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                panel_name_options = "<option value='all' selected>Panel Name</option>";
                $.each(result["panel_name"], function (a, b) {
                        panel_name_options += "<option>" + b + "</option>"
                });
                $("#panel_names").html(panel_name_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}


function getFile_controls() {
    let url = $("#file_controls").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                fileControls_options = "<option value='all' selected>File Controls</option>";
                $.each(result["file_control"], function (a, b) {
                        fileControls_options += "<option>" + b + "</option>"
                });
                $("#file_controls").html(fileControls_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}


function getFile_controls_compare() {
    let url = $("#compare_file_controls").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                fileControls_options = "<option value='all' selected>File Controls</option>";
                $.each(result["file_control"], function (a, b) {
                        fileControls_options += "<option>" + b + "</option>"
                });
                $("#compare_file_controls").html(fileControls_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}



function getClinical_classes() {
    let url = $("#clinical_classes").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                clinical_classes_options = "<option value='all' selected>Clinical Classification</option>";
                $.each(result["clinicalClass_name"], function (a, b) {
                        clinical_classes_options += "<option>" + b + "</option>"
                });
                $("#clinical_classes").html(clinical_classes_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}

function getResponders() {
    let url = $("#responders").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                responders_options = "<option value='all' selected>Responders</option>";
                $.each(result["responder"], function (a, b) {
                        responders_options += "<option>" + b + "</option>"
                });
                $("#responders").html(responders_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}

function getOFC_classes() {
    let url = $("#OFC_classes").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                OFC_classes_options = ["<option value='all' selected>OFC Classification</option>",
					"<option value='negative'>negative</option>",
					"<option value='positive'>positive</option>"]; 

                $("#OFC_classes").html(OFC_classes_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}
function getOFC_classesExercise() {
    let url = $("#OFC_classesExercise").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                OFC_classesExercise_options = ["<option value='all' selected>OFC Class - Exercise</option>",
                                        "<option value='negative'>negative</option>",
                                        "<option value='positive'>positive</option>"];

                $("#OFC_classesExercise").html(OFC_classesExercise_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}

function getAnalysis_results() {
    let url = $("#analysis_results").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                analysis_results_options = ["<option value='all' selected>Results</option>",
                                        "<option value='negativ'>negativ</option>",
                                        "<option value='positiv'>positiv</option>"]; 

                $("#analysis_results").html(analysis_results_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}

function getAnalysis_type() {
    let url = $("#analysis_type").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
                analysis_type_options = ["<option value='all' selected>Analysis Type</option>",
                                        "<option value='AutoBat'>AutoBat</option>",
                                        "<option value='AutoGrat'>AutoGrat</option>"];

                $("#analysis_type").html(analysis_type_options)
        },
        error: function(response){
                        console.log(response)
        }
  });
}
