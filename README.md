# CUSTOMER CHURN ANALYSIS WITH AZURE SYNAPSE ANALYTICS


  ![image](https://github.com/user-attachments/assets/2fa004ac-faf4-4336-8cf2-def82e367561)




This repository provides a comprehensive and detailed documentation of data preparation steps taken, assumptions made, including a detailed record of any data quality issues encountered and how they were 
addressed, and solutions implemented all through the ETL process.

Link to dataset : https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction



### Steps Taken:

1. Made use of Wisdows subsystem for Linux as CLI. I created a virtual environment to manage dependencies for this project with the command 
   below and named it 'pr_venv'

   - Create venv : python3 -m venv pr_venv
   - Activate venv : source pr_venv/bin/activate

   I created a directory within my project folder (command mkdir load_adls_gen2) and named it 'load_adls_gen2' then created a python file inside 
   it (command touch main.py) that automates the loading of the customer_churn.csv dataset into my ADLS Gen2 container directory. The python 
   script in the 'main.py' performs couple of tasks which are listed below.

3. Installed azure datalake storage file using the command below, this serves as the service collection client for for Datalake Gen2 resources
   pip install azure-storage-file-datalake


   Provisioned the needed datalake resourses with the azure cli commands stated below after confirmation that the resource group 'Ayodeji-rg'had 
   initially been provisioned. 

  - az login --tenant ID (login to my subcription)
  - az group show --name Ayodeji-rg (Confirms that the resource group was created)
  - az storage account create --name churnstg2 --resource-group Ayodeji-rg --location uksouth --sku Standard_GRS --kind StorageV2 -hierarchical- 
    namespace true (creates the storage account with hierarchical namespace)
  - az storage account show --name churnstg2 --resource-group Ayodeji-rg (Confirms that storage account 'churnstg2' was created inside the 
    Ayodeji_rg)
  - az storage container create --account-name churnstg2 --name churncontstg (Creates container 'churncontstg' inside churnstg2)
  - az container show --name churncontstg --resource-group Ayodeji-rg (Confirms that 'churncontstg' was created within 'Ayodeji-rg')

   The storage account resources are ready to be loaded with the customer_churn.csv dataset.

3. The python script inside main.py file is use to create 'raw_churn' directory within the container directory and eventually use to automate 
   the data loading process into 'raw_churn'. The 'raw_churn' directory holds the raw data within the datalake. Also, I created another 
   directory within inside the container and mained it 'parquet_churn', this directoy will be use to store the clean data after it has been 
   tranformed and coverted to a parquet file in Synapse Analytics.
   
   Note: a SAS token was generated at the storage account level and incorporated into the main.py file so as to link the datalake storage 
   account to the python script and this made loading the dataset into the container directory possible.

   In order to automate the loading process, I ran the cli command 'python ./main.py'. The python script loads the data into the raw_churn 
   directory and also confirms that some of the resources it was programmed to create already exist within the storage account ( this is because 
   I have created this resources initially using az cli commands).

   Both the churn_raw and the parquet directries can in the image below within the storage container.

   ![image](https://github.com/user-attachments/assets/b28e106b-09a6-400a-9bcb-657a971308d0)


4. I created a new Synapse Analytics workspace to carry out all necessary data cleaning tasks, leveraging the platform’s builtin SQL 
   capabilities and Spark pools to address missing values, outliers, inconsistencies, and incorrect data types that may hinder the modeling 
   process.

   The synapse workspace was linked to the datalake container directories ( i.e raw_churn and parquet_churn) by creating a Linked Service at the 
   synapse workspace level that syncronizes the workspace with the datalake gen2 storage account.

   Leveraged the builtin SQL to check for duplicates and missing values while the data still seats in the ADLS Gene2 storage with the help of 
   OPENROWSET function. So, the outcome confirms that there are no duplicates and missing values in the data because the SELECT DISTINCT clause 
   output the same number of rows initually present in the dataset (i.e 10000) as seen in the image below.

   ![image](https://github.com/user-attachments/assets/108fd91f-5025-4f0e-9b74-d46305f21736)

   Again, leveraging the the Spark pool to further check for duplicates and missing values in the dataset, I create another Spark Notebook, 
   named it 'Notebook 1' and attached it to a spark pool which I created ( 'churnsparkpool' this serves as spark cluster for the compute engine) 
   and wrote in pyspark script to further check for missing values and duplicates in the data. The output also indicates that there are no  
   missing values and duplicated in the data.

5. Designed and implemented an ETL pipeline entirely within Azure Synapse using its integrated pipelines, ensuring that data flows seamlessly 
   from raw ingestion to cleaned and processed tables.
      
   Within Synapse analytics I created 'copy data' activity and set the properties of the source to point to the raw_churn directory within the 
   ADLS Gen 2 storage where the customer_churn.csv raw data is located. I gave this source the name 'ChurnCSV' and creates a new link service 
   which point to the part of 'customer_churn.csv' in the ADLS Gen 2 storage. I previewed the data to and could see that the data is properly 
   presented with the column header in the right state, this confirms that the confirm header property checkbox was checked.

   Also, I set the sink properties of the pipeline into a new dataset which is going to be the parquet file inside ADLS Gen 2. Named the sink 
   'ChurnParquet' and synchronize it to ADLS Gen 2 with the same link service use for the source. Then I open the dataset and set the name of 
   the parquet file to 'churn.parquet' .

   After setting the properties of both the source and the sink, I proceed to set the proper mapping between them the by clicking 'import 
   schema' button perform data type tranformation in the
   mapping. Initially the data types were all set to strings, so I changed the data types to match the corresponding column in the mapping.

   After the transformation has been correctly done, I went back to the pipeline and click on 'debug' botton. I ensured I tracked the process of 
   the debug until it was successful as seen in the image below


      ![image](https://github.com/user-attachments/assets/aeaf08ea-9c4c-40d3-b382-3dca680ed580)

   So you could confirm that 'churn.parquet' file has been written into the parquet_churn directory within the ADLS Gen2 Storage directory.


   After creating the pipeline, I created a new Lake Database ('ChurnDB') within Synapse analytics on the Data Icon, linked the lake database to 
   the pipeline I just created and with the link service and select the parquet file.
   Then I created a new table ('Churntable') Then ran I serveless query on this table as seen below.

      ![image](https://github.com/user-attachments/assets/fbded9bb-5342-42eb-a20a-df71d623f64f)



      ![image](https://github.com/user-attachments/assets/6ebef83b-ff6e-4af8-91ce-6357f4810d62)


6. I perform basic exploratory data analysis (EDA) using Synapse Notebooks to deliver summary statistics and visualizations that can give the 
   team a solid understanding of the data distribution and any potential anomalies. 

      ![image](https://github.com/user-attachments/assets/62b67b87-3ce6-4b0d-a362-607b6ee9563d)


      ![image](https://github.com/user-attachments/assets/c639c44c-d93c-4b3d-a67f-cb73e6a49b2c)



7. Finally, I using the URL of the serverless SQL server from the synapse workspace to connect Power BI in order to create a simple customer 
   churn dashboard to further give in-depth visualization of the churn and non-churn customers as show in the image below.

      ![image](https://github.com/user-attachments/assets/1de37d7e-c8ca-42a7-95d1-3395c578ffc0)




  


      





       





   




  

  












 
