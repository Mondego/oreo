# Oreo
 Source code clones are categorized into four types of increasing difficulty of detection, ranging from purely textual (Type-1) to purely semantic (Type-4). Most clone detectors reported in the literature work well up to Type-3, which accounts for syntactic differences. In between Type-3 and Type-4, however, there lies a spectrum of clones that, although still exhibiting some syntactic similarities, are extremely hard to detect – the Twilight Zone. Most clone detectors reported in the literature fail to operate in this zone. Oreo is a novel approach to source code clone detection that not only detects Type-1 to Type-3 clones accurately, but is also capable of detecting harder-to-detect clones in the Twilight Zone. Oreo is built using a combination of machine learning, information retrieval, and software metrics. We evaluate the recall of Oreo on BigCloneBench, and perform manual evaluation for precision. Oreo has both high recall and precision. More importantly, it pushes the boundary in detection of clones with moderate to weak syntactic similarity in a scalable manner.

## Clone Oreo Repository
 Clone the Oreo repository, preferably the version which we have tagged as -Oreo_FSE. 
 The Oreo is under constant active development and therefore more recent versions might not be very stable. We will release more tags in future when we have more stable version.


## Generate Input for Oreo
 To be able to find method level clone pairs using Oreo, you will need to provide an input file on which Oreo will detect clone pairs.
 To generate this input file you can use a tool called `Metric Calculator`, which we provide with Oreo. The tool needs to know the path of the dataset for which this input file needs to be created. 
 We support dataset in various formats like `tgz`, `zip`, or usual `linux directory`. If the dataset is presented as a `zip` file, the Metric Claculator will go throught the zip will and all the subdirectories inside it looking for the .java files. It will then calculate metrics of the methods found in these files. And finally it will create an output file where each line corresponds to information about one method. This file then can be used as an input to Oreo.

 Before we go further, you will need to create a text file. To make things easier let's call this file file_with_dataset_path.txt. Metric Calculator reads this text file to get the absolute path of the datasets it need to process.
 Each line in this text file corresponds to a dataset. If you only have one dataset to process, you just need to have one line in this file.
 ```
 example:
 if the dataset is present at /home/user/vaibhav/java_dataset.zip
 then, the file_with_dataset_path.txt will contain just one line, which is  
 /home/user/vaibhav/java_dataset.zip  
 If you have more than one datasets, you can provide their paths in separat lines.  
```

 Follow the following steps to generate input
```
 In a terminal, go to the root folder of Oreo.
 Change directory to java-parser
 
 run ant command to create jar
 
 ant metric

 run jar with following command
 
 java -jar dist/metricCalculator.jar <file_with_dataset_path> <input_mode>
```
 input_mode is one of `zip`, `tgz`, or `dir`  
 file_with_dataset_path is the absolute path to the file which contains the absolute path to the dataset  

 When the process ends, an output file named mlcc_input.file will be created. This file can be now used as an input for Oreo.
 To find this file on the filesystem, look for a folder with a sufix `_metric_output`. This folder will be sibling to the directory which contains the `<file_with_dataset_path>` file. 
 I know this is confusin, in future, we will make it simpler.

## Setting Up Oreo

Before going futher, make sure you have Java 8 and Python3.6 installed.

 ```
 change directory to oreo/input/dataset/  
 Copy the above file (mlcc_input.file) to this location and rename the file to blocks.file. Make sure there is no other file present at this location.
 ```
 Oreo has two components, one which produces possible candidates 
 and other which consumes this candidates and predicts whether they are clone pairs or not. 
 To run Oreo, we need to tell Oreo where these candidates will be generated. 
 ```
 now change the directory to Oreo's root directory, that is to oreo/
 open the file sourcerercc.properties.
 ```
 (we reused a lot of code from SourcererCC to make Oreo, and hence the name sourcerercc.properties.)
 ```
 change the value of the property CANDIDATES_DIR to contain 
 the absolute path where you want the possible candidate clone pairs to be generated.
 
 Now open oreo/python_scripts/Predictor.py in an editor.
 In this file, you need to provide paths to 3 variables.
 

 self.candidates_dir. This path should be same as the path provided in sourcerercc.properties (CANDIDATES_DIR)
 
 self.output_dir. The absolute path to the directory where you want the clone pairs to be reported.
 
 self.modelfilename_type31. the absolute path to the trained model 
 which will be used by the Predictor. 
 
 This trained model can be downloaded from this link:
 
 https://drive.google.com/open?id=1TiKTWFn9T7XMdvFwl7lIzwxEqjoDvrbq
 
 ```
 ### Install dependencies.
 The best way to install dependencies is by creating a virtual evironment (venv) for Python.
 Create a virtual environment using following command 
 ```
 python3 -m venv /path/to/new/virtual/environment
 ```
 
 Start the virtual environment:
```
 source /path/to/new/virtual/environment/bin/activate
```
 Change to oreo/python_scripts/dependencies/ directory
 run following command to install the dependencies
 ```
 pip install -r dependencies.txt
```
 ## Running Oreo
 After settip up Oreo, follow the following steps to run it.
 
 from the root of Oreo run following command.
 
 `python controller.py 1`
 
 This will run the code to generate candidate pairs. 
 Now, open another terminal and change directory to oreo/python_scripts. and Run following command 
 
 `python runPredictor.sh`
 
 This will consume candidates and produce clone pairs in the output directory. 
