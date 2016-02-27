# Table of Contents
1. [What is SourcererCC](#what-is-sourcerercc)
2. [How to use SourcererCC](#how-to-use-sourcerercc)
    1. [Download](#download)
    2. [Configuration](#configuration)
    3. [Tokenization](#step-1-tokenization)
    4. [Indexing](#step-2-indexing)
    5. [Clone Detection](#step-3-clone-detection)
3. [Build you own tokenizer](#build-your-own-tokenizer)
    1. [Files Generated by the Tokenizer](#files-generated-by-the-tokenizer)
    2. [Clone Granularity](#clone-granularity)
    3. [Example: Tokenizing a java method into SourcereCC understandable format](#example-tokenizing-a-java-method-into-sourcerecc-understandable-format)
    4. [Understanding parentid and blockid](#what-is-parentid-blockid-pair)
    5. [Tracking code-units from blockIds](#tracking-code-units-from-blockids)



## What is SourcererCC?
SourcererCC is [Sourcerer](http://sourcerer.ics.uci.edu/ "Sourcerer Project @ UCI")'s token-based code clone detector for very large code bases and Internet-scale project repositories. SourcererCC works at many levels of granularity, from block level to project level, depending on specific clone detection needs.

## How to use SourcererCC
SourcererCC works in three steps: 

1. Tokenization
2. Indexing
3. Clone detection

First, the source code is tokenized in a special way, producing one or more token files. These token files are then fed to an indexer in order to produce an inverted index. Finally, a pair-wise similarity search is performed using the inverted index in order to identify the code clones. We explain each of these steps below; but before that, here are the instructions for how to obtain, install and configure SourcererCC.

### Download 

Click [here](http://mondego.ics.uci.edu/projects/clonedetection/files/dist/tool.zip "SourcererCC tool") to download the zip containing executable jar of SourcererCC. Alternatively, you may also clone the SourcererCC project to your workstation and then run the following ant command to build the executable jar.

``` ant clean cdi ```
   
We recommend creating the following directory structure:
```

SourcererCC
├── clone-detector
    ├── LICENSE
    ├── README.md
    ├── dist
    │   └── indexbased.SearchManager.jar
    ├── input   
    │   ├── dataset
    │   └── query
    ├── sourcerer-cc.properties
├── tokenizers

```
### Configuration
The first step is to configure some necessary properties in the sourcerer-cc.properties file. Below are the properties that you must specify
```
DATASET_DIR_PATH=input/dataset
```
This is where the tokenizer's generated output file (tokens.file created by the tokenizer) should be kept. Do not put the headers.file in this folder. You may also have more than one file in this folder. SourcererCC will index all the files which are kept inside this folder. 
```
QUERY_DIR_PATH=input/query
```
This is where the query files should be kept. Query files are created exactly the way the dataset files are created. They have exactly same format. In case you want to find intra-dataset clones, we suggest you provide the location to the dataset folder, i.e., input/dataset. You may have multiple query files as well. SourcererCC will go thorugh each of these files one by one while querying the indexes. 

```
IS_STATUS_REPORTER_ON=true
```
While SourcererCC is running in search mode, it can print how many queries it has processed on the outstream. This could be turned off by setting IS_STATUS_REPORTER_ON=false
```
PRINT_STATUS_AFTER_EVERY_X_QUERIES_ARE_PROCESSED=250
```
You can configure after how many queries should SourcererCC print the status report on the outstream. The above setting would mean that SourcererCC will print the status report after every 250 queries are processed. 

Sweet, we are done with the configurations, so let's proceed to explaining how the whole thing works.

### Step 1: Tokenization

SourcererCC includes tokenizers for some programming languages, some of which work at file level while others work at method level and even block level. We explain here one of those tokenizers that works at method level for Java, C and C++. This tokenizer also supports block-level tokenization for Java only --  in the case of Java, a block is a code unit within curly braces `{}`. Alternative tokenizers exist, and many more can be developed by following the instructions in [Build you own tokenizer](#build-your-own-tokenizer)

**Make sure you have Java 8 installed.** 

Follow the following steps to tokenize a project.
 1. Download and install TXL from [Here](http://www.txl.ca "txl")
 2. To test if the txl is installed properly, enter the following command in the termial
 ```
 txl
 ```
 you should see an output similar to this:
 ```
  TXL v10.6d (27.8.15) (c) 1988-2015 Queen's University at Kingston
Usage:  txl [txloptions] [-o outputfile] inputfile [txlfile] [- progoptions]
(for more information use txl -help)

 ```
 If you don't get the above output, you need to reinstall TXL OR try reopening the terminal. 
 3. Click [Here](http://mondego.ics.uci.edu/projects/clonedetection/files/dist/tool.zip "SourcererCC tool") to download the zip containing executable jars of SourcererCC and InputBuilderClassic.jar.
 4. Unzip the tool.zip.
 5. Using Terminal, change directory to SourcererCC/clone-detector/parser/java. 
 6. Execute the following command:

```
java -jar InputBuilderClassic.jar /input/path/src/ /path/to/tokens.file /path/to/headers.file functions java 0 0 10 0 false false false 8
```

##### Explaining the parameters to the above command:
 1. Path to the folder containing source files. (will search recursively)
 2. Path where the tokenized output file should get generated. Make sure that the path you enter exists on the file system. The file will be created automatically by the InputBuilderClassic.jar. 
 3. Path where the bookkeeping files should get generated. This file contains the mapping of code unit ids and their path in the filesystem. 
 4. Granularity (functions or blocks (only for Java)). 
 5. Language of the source files. Choose one of *cpp*, *java*, or *c*
 6. minTokens: A code unit should have at least these many tokens to be considered for further processing. Setting the minTokens = 0 means no bottom limit
 7. maxTokens: A code snipper should have at most these many tokens to be considered for further processing. Setting the maxTokens = 0 means no upper limit
 8. minLines: A code unit should have at least these many lines to be considered for further processing. Setting the minLines = 0 means no bottom limit
 9. maxLines: A code unit should have at most these many lines to be considered for further processing. Setting the maxLines = 0 means no upper limit
 10. leave it as false
 11. leave it as false
 12. leave it as false 
 13. # of threads. Setting it to 8 would mean the tokenization will be carried out in parallel by 8 threads.

setting the minTokens/minLines = 0 means no bottom limit, setting maxTokens/maxLines = 0 means no upper limit.

### Step 2: Indexing


The next step is to index the dataset. Use the following command to create the index. We will explain the parameter to jar later.
```
java -jar dist/indexbased.SearchManager.jar index 8
```

### Step 3: Clone Detection

Finally, to detect clones, execute the following command
```
java -jar dist/indexbased.SearchManager.jar search 8
```

The jar expects two arguments:
action : index/search and,
similarity threshold : an integer between 1-10 (both inclusive)

The action “index” is to notify SourcererCC that we want to create fresh indexes of the dataset. The action “search” is to notify SourcererCC that we want to detect the clones. The second argument, similarity threshold, tells SourcererCC  to detect clones with a minimum similarity threshold. For example, a similarity threshold of 7 would mean we want to detect clone pairs that are 70% similar. 
Please note that the similarity threshold for both actions, index and search, should be same. That is, if you are using similarity threshold of 7 while indexing, then you should use the same similarity threshold while detecting clones. 

---

## Build your own tokenizer

In order for SourcererCC to be able to find source code clones, the first step is to tokenize the source files into the format used by SourcererCC. 

##### Files Generated by the Tokenizer
A tokenizer should generate at least two files:

1. Tokens file. This file is usually called tokens.file, but there is no restriction on the file name. In tokens.file, each code unit (block, method, file, or other) is represented in a line. There is no limit to the number of lines in tokens.file. Also, there is no limit to the number of such tokens.file files. You can either have one file with all of the tokenized code or multiple files with any number of tokenized code. Just make sure that you put all of these generated files into the *DATASET_DIR_PATH* directory (see Section [Configuring SourcererCC](#configuring-sourcerercc)). SourcererCC will index all files present inside this directory. 
2. Bookkeeping file. This file contains the mapping of code unit ids to their file system paths. Like tokens.file, you can name it whatever you want to. In this tutorial, this file is referenced to as headers.file. Please find more info about this file under the section "Tracking code-units from blockIds".

##### Clone Granularity
SourcererCC can find clones at different granularity levels. The granularity levels could be 
 1. file level, 
 2. function level (or method level), 
 3. block level, or 
 4. statement level. 

SourcererCC will find clones on the granularity level at which the source files of a project are tokenized. 

##### Example: Tokenizing a java method into SourcereCC format
In order to understand the tokenization required by SourcererCC, we present an example. This example is based on a java method, so it assumes method-level granularity.

##### Java Method 
``` 
     /**
     * Execute all nestedTasks.
     */
    public void execute() throws BuildException {
        if (fileset == null || fileset.getDir(getProject()) == null) {
            throw new BuildException("Fileset was not configured");
        }
        for (Enumeration e = nestedTasks.elements(); e.hasMoreElements();) {
            Task nestedTask = (Task) e.nextElement();
            nestedTask.perform();
        }
        nestedEcho.reconfigure();
        nestedEcho.perform();
    }
   ``` 
##### Tokenized output:
```
1,2@#@for@@::@@1,"Fileset@@::@@1,perform@@::@@2,was@@::@@1,configured"@@::@@1,throw@@::@@1,if@@::@@1,elements@@::@@1,null@@::@@2,nextElement@@::@@1,nestedTask@@::@@2,execute@@::@@1,e@@::@@3,nestedTasks@@::@@1,throws@@::@@1,getDir@@::@@1,void@@::@@1,Enumeration@@::@@1,nestedEcho@@::@@2,not@@::@@1,new@@::@@1,getProject@@::@@1,fileset@@::@@2,hasMoreElements@@::@@1,Task@@::@@2,public@@::@@1,reconfigure@@::@@1,BuildException@@::@@2
```

#### Explanation of the output:

In the tokens output file of a method-level granularity tokenizer, each method is represented in a line. In each line, 3 important delimiters are used, which should be applied in the following order:

 1. `@#@`  (this only occurs once)
 2. `,` 
 3. `@@::@@`

The first delimiter (`@#@`) separates the block identification part (`<parentId, blockId>`) from the block's tokens. 
In the above case, 1 is the parent id and 2 is the block id. We explain `<parentId, blockId>` in detail later. 

The remaining two delimiters apply to the tokens string. Of those, the comma (',') is used to separate the token entries.
For example, in the above case, we get the following
strings after splitting the token string on ',' (comma):
```
for@@::@@1
"Fileset@@::@@1
perform@@::@@2
…
```

The third delimiter applies to each token entry, and separates the token itself from the number of occurrences of that token in the block. For example, the token `perform@@::@@2` in the above example means that the term “perform” is present 2 times in the given method. 

#### What is `<parentId, blockId>` pair?

##### blockId:
A blockId is a unique id that identifies a code unit in the input of the tokenizer. A unit can be at any granularity level - file, method, block, or segment. For the above example “2” uniquely identifies the entire method. SourcererCC will report the clones using these blockIds. For example, if there are two duplicate methods with blockId 31 and 89, SourcererCC will report them as clones (31, 89) using their blockIds separated with a “,”. 
There are three requirement for these blockIds.

 1. they should be positive integers. (including Java long type)
 2. they should be unique
 3. they should be in increasing order. (In order to not compare two blocks more than once, SourcererCC only compares a block with those blocks that have higher blockIds)

##### parentId:

ParentId is used to tell SourcererCC that a line in the tokens file belongs to a group. SourcererCC does not compute clones between two lines that have the same parentIds. So, for example, in method-level granularity, all methods declared within a file might have the same parentId corresponding to the file.

To understand how parentId can be used, let’s consider a scenario. 
Suppose we have a repository of 10 java projects. We want to find file level clones but we do not want to find intra-project clones. A user would use a file level tokenizer to create the tokens file. Every line in this tokens file will represent a source file in the projects. As a consequence, every line in the tokens file will have a unique blockId. Because we are not interested in intra-project clones, the lines that come from same project should have the same parentId. This way, SourcererCC will only compute clones from the lines that have different parentIds.
In case users doesn’t want to create any groups whatsoever, they should specify the parentId in all lines as negative 1 (-1).

There are 2 requirements for the parentIds.
 1. they should be positive integers (including Java long type). In case a user does not want to create groups, specify -1 as parentId for all blocks. 
 2. each group should have a unique parentId. More than one line in the tokens file, however, can have the same parentId. 


#### Tracking code units from blockIds
SourcererCC reports clone pairs in the following format: blockId,blockId. In order to be able to track the code units of the clone pairs, the tokenizer should generate a bookkeeping file containing following information:
parentId, blockId, filesystem path to the file where the code unit exists, starting line number of the code unit, ending line number of the code unit. 




 
