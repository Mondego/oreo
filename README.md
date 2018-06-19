# Oreo
Source code clones are categorized into four types of increasing difficulty of detection, ranging from purely textual (Type-1) to purely semantic (Type-4). Most clone detectors reported in the literature work well up to Type-3, which accounts for syntactic differences. In between Type-3 and Type-4, however, there lies a spectrum of clones that, although still exhibiting some syntactic similarities, are extremely hard to detect – the Twilight Zone. Most clone detectors reported in the literature fail to operate in this zone. We present Oreo, a novel approach to source code clone detection that not only detects Type-1 to Type-3 clones accurately, but is also capable of detecting harder-to-detect clones in the Twilight Zone. Oreo is built using a combination of machine learning, information retrieval, and software metrics. We evaluate the recall of Oreo on BigCloneBench, and perform manual evaluation for precision. Oreo has both high recall and precision. More importantly, it pushes the boundary in detection of clones with moderate to weak syntactic similarity in a scalable manner.


## Generate input for Oreo
To be able to find method level clone pairs using Oreo, you will need to provide an input file on which Oreo will detect clone pairs.
To generate this input file you can a tool which we provide with Oreo. 

 