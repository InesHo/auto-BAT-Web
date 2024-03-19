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
        </ol>
    <li><a href="#senarios"> ➤  Common Use cases </a></li>
        <ol>
        <li><a href="#senario1"> ➤ Senario 1: Add New User </a></li>
        <li><a href="#senario2"> ➤ Senario 2: Delete Experemant Files </a></li>
        <li><a href="#senario3"> ➤ Senario 3: Applying AutoBatWorkFlow Updates </a></li>
        </ol>
    <li><a href="#Troubleshooting"> ➤ Troubleshooting </a></li>
    <li><a href="#To-Do"> ➤ To Do </a></li>
    <li><a href="#references"> ➤ References</a></li>

  </ol>
</details>

---
<h2 id="overview"> 📖 Overview</h2>
<p align="justify"> 
  AutoBatWeb is a web-based application developed to facilitate the storage, analysis, and visualization of the flow cytometry experimental files (fcs file format) using a friendly user interface and populating data into the database. Designed to meat the needs of our research group of having data-sets and their analysis results stored in a single database to retrieve and compare results.
</p>

---
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

---
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

---
<h2 id="installation"> ⚙️ Installations</h2>
<p align="justify"> 
  The following instructions works for Ubuntu 22.04 (for other operating systems reffer to the documentaion of each installation). 
</p>
<ol>
  <li><b>Install Anaconda:</b></li>
    <ul>
      <li><b>Download Anaconda:<pre><code>$ url https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh --output anaconda.sh</code></pre></b></li>
      <li><b>Install Anaconda:<pre><code>$ bash anaconda.sh</code></pre></b></li>
      <li><b>Reload bach profile<pre><code>$ source ~/.bashrc</code></pre></b></li>
    </ul>
  <li><b>Install apache2</b></li>
    <ul>
      <li><b><pre><code>$ sudo apt update</code></pre></b></li>
      <li><b><pre><code>$ sudo apt install apache2</code></pre></b></li>
    </ul>
  <li><b>Install Git</b></li>
    <ul>
      <li><b><pre><code>$ sudo apt update</code></pre></b></li>
      <li><b><pre><code>$ sudo apt install git</code></pre></b></li>
    </ul>
  <li><b>Install PostgreSql</b></li>
    <ul>
      <li><b><pre><code>$ sudo apt update</code></pre></b></li>
      <li><b><pre><code>$ sudo apt install postgresql postgresql-contrib</code></pre></b></li>
    </ul>
</ol>

---
<h2 id="setup"> ⚙️ Setting Up the Development Environment</h2>
<p align="justify"> 
  The following instructions works for Ubuntu 22.04 (for other operating systems reffer to the documentaion of each installation). 
</p>
<ol>
  <li><b>Create Database:</b></li>
    <ul>
      <li><b>open the database:<pre><code>$ sudo -i -u postgres </code></pre></b></li>
      <li><b><pre><code>$ psql</code></pre></b></li>
      <li><b>change the default user password:<pre><code>postgres=# ALTER USER postgres WITH PASSWORD 'YOR-NEW-PASSWOR';</code></pre></b></li>
      <li><b>create new user<pre><code>postgres=# CREATE USER baumgrass WITH PASSWORD 'YOR-NEW-PASSWOR';</code></pre></b></li>
      <li><b>create a new database<pre><code>postgres=# CREATE DATABASE autobatdb;</code></pre></b></li>
      <li><b>make the new user the owner of the database<pre><code>postgres=# ALTER DATABASE autobatdb OWNER TO baumgrass;</code></pre></b></li>
      <li><b>exit postgres<pre><code>postgres=# \q</code></pre></b></li>
    </ul>
  <li><b>Create Conda environment</b></li>
    <ul>
      <li><b><pre><code>$ conda create --name AutoBat</code></pre></b></li>
    </ul>
  <li><b>Activate Conda environment</b></li>
    <ul>
      <li><b><pre><code>$ conda activate AutoBat</code></pre></b></li>
    </ul>
  <li><b>Install R</b></li>
    <ul>
      <li><b><pre><code>$ conda install -c conda-forge r-base=3.6.3</code></pre></b></li>
    </ul>
  <li><b>Install Python</b></li>
    <ul>
      <li><b><pre><code>$ conda install python=3.8.5</code></pre></b></li>
    </ul>
  <li><b>Install R packages</b></li>
    <ul>
      <li><b><pre><code>$ R </code></pre></b></li>
      <li><b><pre><code>> install.packages("MASS")</code></pre></b></li>
      <li><b><pre><code>> install.packages("stringr")</code></pre></b></li>
      <li><b><pre><code>> if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")</code></pre></b></li>
      <li><b><pre><code>> BiocManager::install("flowCore")</code></pre></b></li>
      <li><b><pre><code>> install.packages("colorspace")</code></pre></b></li>
      <li><b><pre><code>> install.packages("extrafont")</code></pre></b></li>
      <li><b><pre><code>> library(extrafont)</code></pre></b></li>
      <li><b><pre><code>> font_install("fontcm")</code></pre></b></li>
      <li><b><pre><code>> loadfonts()</code></pre></b></li>
      <li><b><pre><code>> q()</code></pre></b></li>
    </ul>
</ol>

---
<h2 id="config"> ⚡️ Configurations</h2>

<p align="justify"> 
  For security reasons, we have stored sensitive information like SECRET_KEY and database credentials in a separate file. Also, we have stored the path to the AutoBatWorkFlow in the file to be easily changed every time you change the path.
  This file is called config.py and it is stored in the django project directory and ignored by git, so you nead to create it as it is not available in the github repository
</p>

<ol>
  <li><b>create a folder in the home directory:<pre><code>$ mkdir autoBatWeb</code></pre></b></li>
  <li><b><pre><code>$ cd autoBatWeb</code></pre></b></li>
  <li><b>clone Autobat repository<pre><code>$ git clone https://github.com/InesHo/auto-BAT.git</code></pre></b></li>
  <li><b>clone Autobat-Web repository<pre><code>$ git clone  https://github.com/InesHo/auto-BAT-Web.git</code></pre></b></li>
  <li><b>Navigate to the Autobat-Web project directory<pre><code>$ cd auto-BAT-Web</code></pre></b></li>
  <li><b>create config file<pre><code>$ vim config.py</code></pre></b></li>
  <li><b>add the following variables<pre><code>DATABASE_NAME = 'autobatdb'
USER = 'baumgrass'
PASSWORD = ... Find the password in the server or create your own
HOST = '127.0.0.1' # change the IP if the database stored in other server
PORT = '5432'
SECRET_KEY = ... # Find the key in the server or create your own
AUTOBAT_PATH = '/home/abusr/autoBatWeb/auto-BAT'
</code></pre></b></li>
  <li><b>install dependencies<pre><code>$ pip install -r requirements.txt</code></pre></b></li>
  <li><b>make Migrations<pre><code>$ python manage.py makemigrations</code></pre></b></li>
  <li><b>migrate<pre><code>$ python manage.py migrate</code></pre></b></li>
  <li><b>create Superuser to login<pre><code>$ python manage.py createsuperuser</code></pre></b></li>
  <li><b>run the application<pre><code>$ python manage.py runserver</code></pre></b></li>
</ol>

---
<h2 id="deployment"> 🖥️ Deployment</h2>

<p align="justify"> 
 In the previous step, the application will be running in the Django default port and will not be continually running as it is considered as a development mode, so we have used Apatche2 and mod_wsgi to deploy the application.
</p>
<ol>
  <li><b>In the settings.py change ALLOWED_HOSTS if you want to deploy in another server</b></li>
  <li><b>..</b></li>
</ol>

---
<h2 id="getting-started"> 🏁 Getting Started</h2>
<ul>
  <li>start the web-app<b></b></li>
  <li>stop the web-app<b></b></li>
  <li>start background tasks<b></b></li>
  <li>stop background tasks<b></b></li>
  <li>....<b></b></li>
</ul>

---
<h2 id="project-files-description"> 📂 Project Files Description</h2>
<ul>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
</ul>


---
<h2 id="functions"> 📜 Important Functions</h2>


<h3 id="function1"> 🔸 Function 1: experimentfile</h3>


<p></p>

---
<h3 id="function2"> 🔸 Function 2: run_analysis_autobat</h3>
<p></p>

---
<h3 id="function3"> 🔸 Function 3: run_analysis_autograt</h3>
<p></p>

---
<h3 id="function4"> 🔸 Function 4: re_analysis_all</h3>
<p></p>

---
<h3 id="function5"> 🔸 Function 5: run_analysis_autobat_task</h3>
<p></p>

---
<h3 id="function6"> 🔸 Function 6: run_analysis_autograt_task</h3>
<p></p>

---

<h2 id="senarios"> 👀 Examples of Common Senarios </h2>
<h3 id="senario1"> 🔸 Senarios 1: Add New User</h3>

<p></p>

---

<h3 id="senario2"> 🔸 Senarios 2: Delete Experemant Files </h3>
<p></p>

---

<h3 id="senario3"> 🔸 Senarios 2: Applying AutoBatWorkFlow Updates </h3>
<p></p>
---

<h2 id="Troubleshooting"> ⚠️ Troubleshooting</h2>
<ul>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
</ul>

---

<h2 id="To-Do"> 💡 To-Do</h2>
<ul>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
</ul>

---

<h2 id="references"> 📚 References</h2>
<ul>
  <li><b></b>https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/</li>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
  <li><b></b></li>
</ul>
