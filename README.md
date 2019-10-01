# InferAi

Identifying potential threats from source code analysis is a time consuming task, as issues are usually found in low-level bugs that are hard to manually detect. There are tools such as static analyzers that can be run on code to help find problems before code is deployed. However, these tools incur a cost by spending time learning to configure the tool, compiling the code, and building abstract syntax trees before analysis can be performed, thus are not scalable when it comes to thousands of projects, some that may not even compile. 

To tackle this problem of scale, This repo contains a machine learning based solution called InferAI, which aims to automate the process of detecting potential threats in source code by automatically identifying which lines of code may contribute to a type of threat. 

An end user can easily use this model by inputting arbitrary source code, and the model will produce a report on with threat scores based on vulnerabilities detected in the code giving the user a clue on where to focus on triaging efforts.

### Training model

TODO

### API

TODO

