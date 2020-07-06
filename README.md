# TechChallengePandata

# Software Architecture
The Pandata backend is fully running in the HUAWEI Cloud Service World. An Ubuntu 18.04 server is executing a shell script for GET request to several APIs. These data responses are saved on the Elastic Cloud Server. This server has some integrated pre-processing and a parallel file system with an object storage bucket in the cloud mounted over OBSFS. The data bucket in the Object Storage Service has a file structure with an input and an output folder. The raw data from the different sources is stored in the input folder. Several processing Notebooks access this input folder and process the data. Different Pandata functions such as Panda score happen in the notebooks. The processed data is stored into the output folder. To stay inside the HUAWEI universe, we used Data Lake Visualization to create a dashboard to visualize all our information. Alternatively, Qlik Sense accesses the processed data output to give another dynamic Dashboard visualization.

# Components
1)	Elastic Cloud Server

An Elastic Cloud Server is a computational unit that can be used to run jobs on the HUAWEI cloud. There is a physical machine executing the implemented Shell script written for a Bourne-again shell. The Cron-Deamon is used to schedule this script daily. This cloud server is the bases of our up to date data.

2)	Object Storage Service

Object Storage Service is a stable, secure, efficient, and easy-to-use cloud storage service that is scalable and compatible. On Object Storage Service we can store all our files, and we can also build the parallel file system which can directly link to the Elastic Cloud Server. Object Storage Service is the bases of our file storage.

3)	Model Arts

ModelArts is a one-stop development platform for AI developers. On ModelArts we can import data and files in Objective Storage Service, then use jupyter notebooks to process the data, and finally output the processed data to our use place. ModelArts is the bases of our data processing.

4)	Data Lake Visualization

Data Lake Visualization is the data visualization platfrom of the Huawei Cloud, which we can connect different data sources with.  It offers direct communication with the buckets that are stored in Object Storage Service and impressive visuals for an effective user interaction. Dashboard can be easily published which is an advantage over the other dashboard platforms.

5)	Qlik Sense

Qlik Sense is a data analytics platform that offers a dashboard, which can be used for data visualization. We used Rest APIs to connect csv files that are stored in Huawei's Object Storage Service, with our Dashboard. Our implementation includes an interactive interaction for the users, as it enables them to search the destination. This search function works like a query for our database to get the respective results to communicate with the users. This produt is the bases of our data visualization step.
