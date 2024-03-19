<h1 align="center"> AutoBat Web Application </h1>

<h2 id="table-of-contents"> 📋 Table of Contents</h2>
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#overview"> ➤ Overview</a></li>
    <li><a href="#features"> ➤ Main Features</a></li>
    <li><a href="#technologies-used"> ➤ Technologies Used</a></li>
    <li><a href="#installation"> ➤ Installations</a></li>
    <li><a href="#setup"> ➤ Setting Up the Development Environment</a></li>
    <li><a href="#deployment"> ➤ Deployment</a></li>
    <li><a href="#config"> ➤ Configurations</a></li>
    <li><a href="#getting-started"> ➤ Getting Started</a></li>
    <li><a href="#project-files-description"> ➤ Project Files Description</a></li>
    <li><a href="#functions"> ➤ Important Functions</a></li>
        <ol>
        <li><a href="#function1"> ➤ Function 1: experimentfile </a></li>
        <li><a href="#function2"> ➤ Function 2: run_analysis_autobat </a></li>
        <li><a href="#function3"> ➤ Function 3: run_analysis_autograt </a></li>
        <li><a href="#function4"> ➤ Function 4: re_analysis_all </a></li>
        <li><a href="#function5"> ➤ Function 5: run_analysis_autobat_task </a></li>
        <li><a href="#function6"> ➤ Function 6: run_analysis_autograt_task </a></li>
        <li><a href="#function7"> ➤ Function 7: research_results </a></li>
        </ol>
    <li><a href="#senarios"> ➤  Common Use cases </a></li>
        <ol>
        <li><a href="#senario1"> ➤ Senario 1: Add New User </a></li>
        <li><a href="#senario2"> ➤ Senario 2: Delete Experemant Files </a></li>
        </ol>
    <li><a href="#Troubleshooting"> ➤ Troubleshooting </a></li>
    <li><a href="#To-Do"> ➤ To Do </a></li>
    <li><a href="#references"> ➤ References</a></li>

  </ol>
</details>

<br>
<h2 id="overview"> 📖 Overview</h2>
<p align="justify"> 
  AutoBatWeb is a web-based application developed to facilitate the storage, analysis, and visualization of the flow cytometry experimental files (fcs file format) using a friendly user interface and populating data into the database. Designed to meat the needs of our research group of having data-sets and their analysis results stored in a single database to retrieve and compare results.
</p>

<br>
<h2 id="features"> 🎯 Main Features</h2>
<ul>
  <li><b>User-friendly interface</b></li>
  <li><b>Secure login</b></li>
  <li><b>Upload FCS files</b></li>
  <li><b>Automatically extract and store Metadata and channels</b></li>
  <li><b>Background tasks to run the analysis of FCS files</b></li>
  <li><b>Export results as excel files</b></li>
  <li><b>Export visualization plots as pdf</b></li>
  <li><b>Generate Reports</b></li>

</ul>

<br>
<h2 id="technologies-used"> 🌐 Technologies Used</h2>
<ul>
  <li><b>Frontend:</b></li>
    <ul>
      <li><b>HTML </b></li>
      <li><b>Bootstrap</b></li>
    </ul>
  <li><b>Backend:</b></li>
    <ul>
      <li><b>Python</b></li>
      <li><b>Django</b></li>
    </ul>
  <li><b>Database:</b></li>
    <ul>
      <li><b>PostgreSQL</b></li>
    </ul>
  <li><b>Web server</b> </li>
    <ul>
      <li><b>Ubuntu 22.04</b></li>
      <li><b>apache2</b></li>
    </ul>
  <li><b>Additional Modules</b> </li>
    <ul>
      <li><b>django-background-tasks</b></li>
      <li><b>django-jazzmin</b></li>
      <li><b>mod_wsgi</b></li>
    </ul>
</ul>

<br>
<h2 id="installation"> ⚙️ Installations</h2>
<p align="justify"> 
  The following instructions works for Ubuntu 22.04 (for other operating systems reffer to the documentaion of each installation). 
</p>
<ol>
  <li><b>Install Anaconda:</b></li>
    <ul>
      <li><b>Download Anaconda:<pre><code>url https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh --output anaconda.sh</code></pre></b></li>
      <li><b>Install Anaconda:<pre><code>bash anaconda.sh</code></pre></b></li>
      <li><b>Reload bach profile<pre><code>source ~/.bashrc</code></pre></b></li>
    </ul>
  <li><b>Install apache2</b></li>
    <ul>
      <li><b><pre><code>sudo apt update</code></pre></b></li>
      <li><b><pre><code>sudo apt install apache2</code></pre></b></li>
      <li><b><pre><code>sudo apt-get install libapache2-mod-wsgi-py3</code></pre></b></li>
    </ul>
    
  <li><b>Install Git</b></li>
    <ul>
      <li><b><pre><code>sudo apt update</code></pre></b></li>
      <li><b><pre><code>sudo apt install git</code></pre></b></li>
    </ul>
  <li><b>Install PostgreSql</b></li>
    <ul>
      <li><b><pre><code>sudo apt update</code></pre></b></li>
      <li><b><pre><code>sudo apt install postgresql postgresql-contrib</code></pre></b></li>
    </ul>
</ol>

<br>
<h2 id="setup"> ⚙️ Setting up the environment</h2>
<p align="justify"> 
  The following instructions works for Ubuntu 22.04 (for other operating systems reffer to the documentaion of each installation). 
</p>
<ol>
  <li><b>Create Database:</b></li>
    <ul>
      <li><b>open the database:<pre><code>sudo -i -u postgres </code></pre></b></li>
      <li><b><pre><code>psql</code></pre></b></li>
      <li><b>change the default user password:<pre><code>ALTER USER postgres WITH PASSWORD 'YOR-NEW-PASSWOR';</code></pre></b></li>
      <li><b>create new user<pre><code>CREATE USER baumgrass WITH PASSWORD 'YOR-NEW-PASSWOR';</code></pre></b></li>
      <li><b>create a new database<pre><code>CREATE DATABASE autobatdb;</code></pre></b></li>
      <li><b>make the new user the owner of the database<pre><code>ALTER DATABASE autobatdb OWNER TO baumgrass;</code></pre></b></li>
      <li><b>exit postgres<pre><code>\q</code></pre></b></li>
    </ul>
  <li><b>Create Conda environment</b></li>
    <ul>
      <li><b><pre><code>conda create --name AutoBat</code></pre></b></li>
    </ul>
  <li><b>Activate Conda environment</b></li>
    <ul>
      <li><b><pre><code>conda activate AutoBat</code></pre></b></li>
    </ul>
  <li><b>Install R</b></li>
    <ul>
      <li><b><pre><code>conda install -c conda-forge r-base=3.6.3</code></pre></b></li>
    </ul>
  <li><b>Install Python</b></li>
    <ul>
      <li><b><pre><code>conda install python=3.8.5</code></pre></b></li>
    </ul>
  <li><b>Install R packages</b></li>
    <ul>
      <li><b><pre><code>R </code></pre></b></li>
      <li><b><pre><code>install.packages("MASS")</code></pre></b></li>
      <li><b><pre><code>install.packages("stringr")</code></pre></b></li>
      <li><b><pre><code>if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")</code></pre></b></li>
      <li><b><pre><code>BiocManager::install("flowCore")</code></pre></b></li>
      <li><b><pre><code>install.packages("colorspace")</code></pre></b></li>
      <li><b><pre><code>install.packages("extrafont")</code></pre></b></li>
      <li><b><pre><code>library(extrafont)</code></pre></b></li>
      <li><b><pre><code>font_install("fontcm")</code></pre></b></li>
      <li><b><pre><code>loadfonts()</code></pre></b></li>
      <li><b><pre><code>q()</code></pre></b></li>
    </ul>
</ol>

<br>
<h2 id="config"> ⚡️ Configurations</h2>

<p align="justify"> 
  For security reasons, we have stored sensitive information like SECRET_KEY and database credentials in a separate file. Also, we have stored the path to the AutoBatWorkFlow in the file to be easily changed every time you change the path.
  This file is called config.py and it is stored in the django project directory and ignored by git, so you nead to create it as it is not available in the github repository
</p>

<ol>
  <li><b>create a folder in the home directory:<pre><code>mkdir autoBatWeb</code></pre></b></li>
  <li><b><pre><code>cd autoBatWeb</code></pre></b></li>
  <li><b>clone Autobat repository<pre><code>git clone https://github.com/InesHo/auto-BAT.git</code></pre></b></li>
  <li><b>clone Autobat-Web repository<pre><code>git clone  https://github.com/InesHo/auto-BAT-Web.git</code></pre></b></li>
  <li><b>Navigate to the Autobat-Web project directory<pre><code>cd auto-BAT-Web</code></pre></b></li>
  <li><b>create config file<pre><code>vim config.py</code></pre></b></li>
  <li><b>add the following variables<pre><code>DATABASE_NAME = 'autobatdb'
USER = 'baumgrass'
PASSWORD = ... Find the password in the server or create your own
HOST = '127.0.0.1' # change the IP if the database stored in other server
PORT = '5432'
SECRET_KEY = ... # Find the key in the server or create your own
AUTOBAT_PATH = '/home/abusr/autoBatWeb/auto-BAT'
</code></pre></b></li>
  <li><b>install dependencies<pre><code>pip install -r requirements.txt</code></pre></b></li>
  <li><b>make Migrations<pre><code>python manage.py makemigrations</code></pre></b></li>
  <li><b>migrate<pre><code>python manage.py migrate</code></pre></b></li>
  <li><b>create Superuser to login<pre><code>python manage.py createsuperuser</code></pre></b></li>
  <li><b>run the application<pre><code>python manage.py runserver</code></pre></b></li>
</ol>

<br>
<h2 id="deployment"> 🖥️ Deployment</h2>

<p align="justify"> 
 In the previous step, the application will be running in the Django default port and will not be continually running as it is considered as a development mode, so we have used Apatche2 and mod_wsgi to deploy the application.
</p>
<ol>

  <li><b>In the settings.py change ALLOWED_HOSTS if you want to deploy in another server</b></li>
  <li><b><pre><code>cd /etc/apache2/sites-available/</code></pre></b></li>
  <li><b>create new file for autobat config by copying the default config<pre><code>sudo cp 000-default.conf autobat_web.conf</code></pre></b></li>
  <li><b>edit the file<pre><code>sudo vim autobat-web.conf</code></pre></b></li>
  <li><b>add the following to the end of the file - (make sure to change paths)
  <pre><code>

        LoadModule wsgi_module modules/mod_wsgi.so
        Alias /static /home/abusr/autoBatWeb/auto-BAT-Web/static
        <Directory /home/abusr/autoBatWeb/auto-BAT-Web/static>
                Require all granted
        </Directory>

        Alias /media /home/abusr/autoBatWeb/auto-BAT-Web/media
        <Directory /home/abusr/autoBatWeb/auto-BAT-Web/media>
                Require all granted
        </Directory>

        <Directory /home/abusr/autoBatWeb/auto-BAT-Web/autoBatWeb>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        WSGIScriptAlias / /home/abusr/autoBatWeb/auto-BAT-Web/autoBatWeb/wsgi.py
  </pre></code></b></li>
  <li><b>collectstatic (from Django project directory)<pre><code>python manage.py collectstatic</code></pre></b></li>
  <li><b>run the command in project directory (autoBatWeb)<pre><code>python auto-BAT-Web/manage.py runmodwsgi --setup-only --port=80 --user abusr  --access-log --server-name=autobat.drfz.de --server-root=AutoBat-Webserver-80</code></pre></b></li>
  <li><b>create file to start the app<pre><code>sudo vim /usr/bin/start_autobat </code></pre></b></li>
  <li><b>add the following (considering path)<pre><code>sudo /home/abusr/autoBatWeb/AutoBat-Webserver-80/apachectl start </code></pre></b></li>
  <li><b>create file to stop the app<pre><code>sudo vim /usr/bin/stop_autobat</code></pre></b></li>
  <li><b>add the following (considering path)<pre><code>sudo /home/abusr/autoBatWeb/AutoBat-Webserver-80/apachectl stop</code></pre></b></li>
  <li><b>create file to restart the app<pre><code>sudo vim /usr/bin/restart_autobat</code></pre></b></li>
  <li><b>add the following (considering path)<pre><code>sudo /home/abusr/autoBatWeb/AutoBat-Webserver-80/apachectl restart</code></pre></b></li>
</ol>

<br>
<h2 id="getting-started"> 🏁 Getting Started</h2>
<p align="justify"> 
 In the previous step, we have created executable scripts so we can simply start and stop the using the following commands:
</p>
<ul>
  <li><b>start the web-app<pre><code>start_autobat </code></pre></b></li>
  <li><b>stop the web-app<pre><code>stop_autobat </code></pre></b></li>
  <li><b>restart the web-app<pre><code>restart_autobat </code></pre></b></li>

</ul>
<p align="justify"> 
 The background tasks should be started separately and can only be run in the Django directory and the conda environment is activated.
</p>
<ul>
  <li><b>start background tasks<pre><code>nohup python manage.py process_tasks > tasks.log & </code></pre></b></li>
  <li><b>show if the background task is running <pre><code>ps aux | grep manage.py </code></pre></b></li>
  <img src="assets/img/show_background_tasks.png"/>
  <li><b>stop background tasks (needs pid from previous step)<pre><code>kill pid </code></pre></b></li>
</ul>

<br>
<h2 id="project-files-description"> 📂 Project Files Description</h2>
<ul>
  <li><b>functions.py: </b> Contains the functions we have created to support some functionalities like changing the metadata of the file and creating the pdf files for the plots visualization</li>
  <li><b>models.py: </b> Contains the tables used for storing data and defining their relations</li>
  <li><b>tasks.py: </b>Contains the functions that should run in the background like collecting metadata,channels data, marker means run AutoBat analysis and AutoGrat analusis</li>
  <li><b>views.py: </b>Contains data to be rendered on the templates</li>
</ul>

<br>
<h2 id="functions"> 📜 Important Functions</h2>
<h3 id="function1"> 🔸 Function 1: experimentfile</h3>
<p align="justify"> 
 This is a view class that is used to upload and process FCS files. Following are the points to the way it works:
</p>
<ul>
  <li><b> GET Method: </b></li>
  <ul>
    <li><b> Renders a form (ExperimentFilesForm) to upload experiment files</b></li>
  <li><b> Renders the 'files/add_files.html' template with the form </b></li>
  </ul>
  <li><b> POST Method: </b></li>
  <ul>
    <li><b>Handles the form submission</b></li>
    <li><b>Retrieves files from the request</b></li>
    <li><b>Validates the form data</b></li>
    <li><b>Extracts form data such as bat ID, donor ID, panel ID, and condition</b></li>
    <li><b>Creates a new analysis instance with the extracted data</b></li>
    <li><b>Saves the analysis ID for future reference</b></li>
    <li><b>Creates directories for storing uploaded files based on bat ID, donor ID, panel ID, and condition</b></li>
    <li><b> Iterates over each uploaded file:</b></li>
      <ul>
      <li><b>Saves the file to the appropriate directory</b></li>
      <li><b>Retrieves metadata from the uploaded file</b></li>
      <li><b>Extracts allergen information from the metadata</b></li>
      <li><b>Creates an instance of ExperimentFiles for each uploaded file, storing file details, allergen information, and control type</b></li>
      <li><b>Saves the file instance with the associated analysis ID and user ID</b></li>
      <li><b>Processes the uploaded files using the change_FCS_data function and runs it as a background tasks</b></li>
      </ul>
    <li><b>Extracts channel information from one of the uploaded files</b></li>
    <li><b>Creates instances of Channels for each channel in the uploaded files, storing channel pnn and pns</b></li>
    <li><b>Initiates the processing of uploaded files using the process_files function and runs it as a background tasks</b></li>
    <li><b>Renders the 'files/files_ready.html' template with the analysis ID when successful file processing</b></li>
    <li><b>Renders the 'files/files_error.html' template if there was an error</b></li>
  </ul>
</ul>

<br>
<h3 id="function2"> 🔸 Function 2: run_analysis_autobat</h3>
<p align="justify"> 

 This is a view function that is used to collect the required parameters and send them to the background tasks to analyze AutoBat. Following are the points to the way it works:
</p>
<ul>
  <li><b> POST request: </b></li>
  <ul> 
  <li><b>Retrieves necessary data from the request and the database (e.g., bat ID, donor ID, panel ID)</b></li>
  <li><b>Parses parameters from the request related to manual thresholds and chosen markers</b></li>
  <li><b>Checks if the analysis for the chosen markers has already been performed</b></li>
  <li><b>If not, creates an instance of AnalysisMarkers in the database to track the analysis</b></li>
  <li><b>Determines file paths for data, exports, and output based on the conditions</b></li>
  <li><b>Executes the run_analysis_autobat_task function with the provided parameters</b></li>
  <li><b>Renders the "analysis/analysis_ready.html" template upon successful execution</b></li>
  </ul>
<li><b> If Error: </b></li>
  <ul>
    <li><b>Renders the "analysis/analysis_error.html" template if the analysis for the chosen markers has already been performed</b></li>
    <li><b>Renders the "analysis/analysis_markers_error.html" template if no markers have been selected for analysis</b></li>
  </ul>
</ul>

<br>
<h3 id="function3"> 🔸 Function 3: run_analysis_autograt</h3>
<p align="justify"> 
 This is a view function that is used to collect the required parameters and send them to the background tasks to analyze AutoGrat. Following are the points to the way it runs:
 </p>
<ul>
  <li><b> POST request: </b></li>
  <ul> 
    <li><b> Retrieves necessary data from the request and the database (e.g., bat ID, donor ID, panel ID) </b></li>
    <li><b> Parses parameters from the request related to chosen markers (X, Y, Z2_1 to Z2_4) </b></li>
    <li><b> Prepares data for the analysis, including labels and conditions</b></li>
    <li><b> Checks if the selected markers for analysis have already been used</b></li>
    <li><b> If not, creates an instance of AnalysisMarkers in the database to track the analysis</b></li>
    <li><b> Determines file paths for data, exports, and output based on the conditions</b></li>
    <li><b> Executes the run_analysis_autograt_task function with the provided parameters</b></li>
    <li><b> Renders the "analysis/analysis_ready.html" template upon successful execution</b></li>
  </ul> 
  <li><b>If Error: </b></li>
    <ul> 
    <li><b>Renders the "analysis/analysis_error.html" template if the analysis for the chosen markers has already been performed</b></li>
    <li><b>Renders the "analysis/analysis_markers_error.html" template if no markers have been selected for analysis</b></li>
    </ul> 
  </ul> 


<br>
<h3 id="function4"> 🔸 Function 4: re_analysis_all</h3>
<p align="justify"> 
 This is a view function that is used to delete old analyses of the latest version and reanalyze them or analyze them with a new version by collecting required parameters and sending them to the background tasks to analyze AutoBat or AutoGrat. Following are the points to the way it runs:
</p>
<ul>
<li><b>Parses the analysis type from the request</b></li>
<li><b>If the analysis type is "AutoBat":</b></li>
  <ul>
  <li><b>Retrieves analysis markers data for AutoBat analysis from the database</b></li>
  <li><b>Iterates over each analysis marker and gathers necessary data for re-analysis</b></li>
  <li><b>Determines file paths for data, exports, and output based on conditions</b></li>
  <li><b>Checks the current version against the stored version</b></li>
  <li><b>If versions match:</b></li>
    <ul>
    <li><b>Deletes existing analysis data associated with the marker</b></li>
    <li><b>Updates analysis status to "Waiting" and clears any error or info messages</b></li>
    <li><b>Executes the run_analysis_autobat_task function with the provided parameters</b></li>
    </ul>
  <li><b>If versions don't match:</b></li>
    <ul>
    <li><b>Creates a new instance of analysis markers for re-analysis</b></li>
    <li><b>Executes the run_analysis_autobat_task function with the provided parameters</b></li>
    </ul>
  </ul>
<li><b>If the analysis type is "AutoGrat", the process is similar to "AutoBat" with adjustments for the analysis type:</b></li>
  <ul>
  <li><b>Retrieves analysis markers data for AutoGrat analysis from the database</b></li>
  <li><b>Iterates over each analysis marker and gathers necessary data for re-analysis</b></li>
  <li><b>Determines file paths for data, exports, and output based on conditions</b></li>
  <li><b>Checks the current version against the stored version</b></li>
    <li><b>If versions match:</b></li>
    <ul>
    <li><b>Deletes existing analysis data associated with the marker</b></li>
    <li><b>Updates analysis status to "Waiting" and clears any error or info messages</b></li>
    <li><b>Executes the run_analysis_autograt_task function with the provided parameters</b></li>
    </ul>
  <li><b>If versions don't match:</b></li>
    <ul>
    <li><b>Creates a new instance of analysis markers for re-analysis</b></li>
    <li><b>Executes the run_analysis_autograt_task function with the provided parameters</b></li>
    </ul>
  </ul>
<li><b>>Renders the "analysis/re_analysis_error.html" template if the analysis type is neither "AutoBat" nor "AutoGrat":</b></li>
<li><b>When successful re-analysis, it renders the "analysis/analysis_ready.html" template</b></li>
</ul>
  
<br>
<h3 id="function5"> 🔸 Function 5: run_analysis_autobat_task</h3>
<p align="justify">
 This is a task function that is used to recive parameters from the view function and send them to the AutoWorkFlow to analyze AutoBat in the background and then saves the data to the databas. Following are the points to the way it works:
</p>
<ul>
  <li><b>Sets start time for analysis and updates status to "In Progress"</b></li>
  <li><b>Retrieves information about experiment files related to the analysis</b></li>
  <li><b>Processes each sample file:</b></li>
  <ul>
    <li><b>If the panel is either "bat-panel" or "reduced-panel", performs gating using BaumgrassGating</b></li>
    <li><b>Otherwise, constructs a report with basic information due to no automatic pregating for the panel</b></li>
  </ul>
  <li><b>Executes an automated workflow (AutoBatWorkflow) to generate results.</b></li>
  <li><b>Processes the results and updates report information such as thresholds, percentages, and quality messages.</b></li>
  <li><b>Generates a final report.</b></li>
  <li><b>Saves the final report to an Excel file and stores it in the database.</b></li>
  <li><b>Saves analysis thresholds and results to the database.</b></li>
  <li><b>Saves quality messages and plots to the database.</b></li>
  <li><b>If there is an error: saves the analysis status as Error and stores the analysis error in the database</b></li>
</ul>

<br>
<h3 id="function6"> 🔸 Function 6: run_analysis_autograt_task</h3>
<p align="justify">
 This is a task function that is used to recive parameters from the view function and send them to the AutoWorkFlow to analyze AutoGrat in the background and then saves the data to the databas. Following are the points to the way it works:
</p>

<ul>
  <li><b>Updates the start time of the analysis and sets the status to "In Progress".</b></li>
  <li><b>Retrieves information about the files related to the analysis.</b></li>
  <li><b>Processes each sample file:</b></li>
  <ul>
    <li><b>If the panel is either "bat-panel" or "reduced-panel", performs gating using BaumgrassGating</b></li>
    <li><b>Otherwise, constructs a report with basic information due to no automatic pregating for the panel</b></li>
  </ul>
  <li><b>If there are multiple z-markers, creates separate reports for each combination of files and markers.</b></li>
  <li><b>Executes an automated workflow (AutoBatWorkflow) to generate results.</b></li>
  <li><b>Processes the results and updates report information such as thresholds, percentages, and quality messages.</b></li>
  <li><b>Generates a final report.</b></li>
  <li><b>Saves the final report to an Excel file and stores it in the database.</b></li>
  <li><b>Saves analysis thresholds and results to the database.</b></li>
  <li><b>Saves quality messages and plots to the database.</b></li>
  <li><b>If there is an error: saves the analysis status as Error and stores the analysis error in the database</b></li>
</ul>

<br>
<h3 id="function7"> 🔸 Function 7: research_results</h3>
<p align="justify"> 
 This is a view function that is used to retrive and filter data from the database based on the filters in the research questions interface. Following are the points to the way it works:
</p>
<ul>
  <li><b>Extracts data from the AnalysisResults model and related models</b></li>
  <li><b>Allows filtering of the extracted data based on various parameters from the request</b></li>
  <li><b>Generates an Excel file containing the filtered data</b></li>
  <li><b>Saves the Excel file in a specified directory to be downloaded from the research results page</b></li>
  <li><b>Saves a CSV file containing the IDs of associated files if the number of rows in the data is less than 500 to be used to retrive plots to download a pdf</b></li>
  <li><b>Renders a template (analysis/research_results.html) with the filtered analysis results, Excel file name, CSV file name (if less than 500 records), and the count of rows in the data</b></li>
</ul>

<br>
<h2 id="senarios"> 👀 Examples of Common Senarios </h2>
<h3 id="senario1"> 🔸 Senarios 1: Add New User</h3>
<ol>
  <li><b> Go to the Admin Panel </b></li>
  <img src="assets/img/add_user_1.png"/>
  <li><b> In the Authentication and Authorization click Users </b></li>
  <img src="assets/img/add_user_2.png"/>
  <li><b> Click Add user </b></li>
  <img src="assets/img/add_user_3.png"/>
  <li><b> Write the username and password and click save </b></li>
  <img src="assets/img/add_user_4.png"/>
</ol>

<br>

<h3 id="senario2"> 🔸 Senarios 2: Delete Experemant Files </h3>
<p align="justify"> 
  Make sure to follow the steps carefully, and delete the physical files exactly as we show in the following steps:
</p>
<ol>
  <li><b> Go to the Analysis page </b></li>
  <img src="assets/img/delete_files_1.png"/>
  <li><b> Show the files of the experiment you want to delete </b></li>
  <img src="assets/img/delete_files_2.png"/>
  <li><b> Memorize the analysis number at the end of the url </b></li>
  <img src="assets/img/delete_files_3.png"/>
  <li><b> Go to the Admin Panel </b></li>
  <img src="assets/img/delete_files_4.png"/>
  <li><b> Click on the Analysis model </b></li>
  <img src="assets/img/delete_files_5.png"/>
  <li><b> Click on the analysis number you memorize in the step 3 </b></li>
  <img src="assets/img/delete_files_6.png"/>
  <li><b> Click delete </b></li>
  <img src="assets/img/delete_files_7.png"/>
  <li><b> Go to the files directory in the operating system - for the mentioned example the directory is: <pre><code>cd media/FCS_files/BAT_207/DZWN1/platelet-panel/standard_BAT </code></pre></li>
  <li><b> List the files to do final check<pre><code>ls </code></pre></li>
  <img src="assets/img/delete_files_8.png"/>
  <li><b> Delete the files inside the folder <pre><code>rm *.fcs </code></pre></li>
</ol>

<br>
<h2 id="Troubleshooting"> ⚠️ Troubleshooting</h2>
<ul>
  <li><b>Sometimes after restarting the operating system in the server the web application cant run: This apache might be using the default port do we need to stop it and restart the app</b><pre><code>sudo /etc/init.d/apache2 stop </code></pre><pre><code>start_autobat</code></pre></li>

  <li><b>AutoBatWorkFlow updates are not applyed?</b> Make sure to cover the following stepes:</li>
  <ul>
    <li>Pull updates from GitHub</li>
    <li>If the new update requires another parameter, make sure to include it in the view functions run_analysis_autobat, run_analysis_autograt, reanalyze_all, run_analysis_autobat_tasks and run_analysis_autograt_tasks</li>
    <li>If the results are changing, then add the required field in the modal Analysis Results</li>
    <li>Upload files failed: make sure file names and allergen does not contain unknowen characters</li>
    <li>Restart the web app (see <a href="#getting-started"> Getting Started</a>)</li>
    <li>Restart Background tasks (see <a href="#getting-started"> Getting Started</a>)</li>
  </ul>

</ul>

<br>
<h2 id="To-Do"> 💡 To-Do</h2>
<ul>
  <li><b>The Django project is created with only one app, so it is recommended to divide it into multiple apps</b></li>
  <li><b>Add interfaces to allow users to delete and update records</b></li>
  <li><b>Inhance retriving data from the database by for example using select_related to reduce the number of quiries sent to the database and make more faster </b></li>
</ul>

<br>
<h2 id="references"> 📚 References</h2>
<ul>
  <li><a href="https://docs.djangoproject.com/en/3.2/"> Django Documentation </a></li>
  <li><a href="https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/"> Django modwsgi </a></li>
  <li><a href="https://www.postgresql.org/docs/current/tutorial-start.html"> postgresql Documentation </a></li>
  <li><a href="https://getbootstrap.com/docs/5.0/getting-started/introduction/"> Bootstrap Documentation </a></li>
</ul>
