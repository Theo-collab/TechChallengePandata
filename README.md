# TechChallengePandata

# Software Architecture
![alt text](https://datatc2020.obs.ap-southeast-1.myhuaweicloud.com:443/dashboard_pictures/Bildschirmfoto%202020-07-05%20um%2021.55.41.png?AccessKeyId=BPQB2WGQ68ATVBCXSOK3&Expires=1594046858&Signature=Y2f2xDndW3jbvcIe%2FOwrwkszMk4%3D&x-obs-security-token=gQpjbi1ub3J0aC00jFU8rh5jAAmktwrVoGDAUlj-VJVdfboEG8I4j-H5rZqBWHP6OS63GD4CFJBN7Hy0EJHZUXh4YoW3xqa5uwMb1Mq06Pj89P_o4MPwgDmwzzP-F0KPZBPiXPd09TjZagN06S1IzwLsYv-GlA2_xp097238aeb8j7GRu3niVNpVzEz4JtktIxX0aZ15EKoohLvMksjrDYwvTfa7jZGk23qX6lnudiOOlr-_tKELnamCx9c4cXW3KY1bckuezxHglhOUD-hr9D93ZvN7DuE2yaAMAOsHdJRo_yvZZMQ7nzuvLtS_A2KvEnTw9xh88bymXw-cpGs8Iglz0_piMtz1Si5IYeGszUE6ky2AYx_rskVKWQ6hXN2PwlDgafua7TI76kxKRC1TdXdVAQKYYkvH4JqeuZjUhAPAhUEOJX6WUk1xJbEiuMW6X3WX8EUG8PcnJKNbI01RIj6KIQ8Q-o5RhiMLxo9vf-7uf3vyiFu8GIRLbl9ojoEuejbm_b93or5PF8lV2iSAVG8hjmvg1sZsq5Uf5zNWyW3rOUwWlGzMvHLwV-cGBFrcPx8BYTtEfFdaQmAbUWw03JnnnPkNROxicSlcN5A7PJJ1ptkkGfKzM_67OPV8NlWEG2939DvbMbNgZd4kC3-1DTQKtNsuwH8C9cI80O1xT9a7drw6YmkFLG8Wfn3N7feOmV-_KR221IFXWHP_DRCVbBT-jj5tX2hKRJ-hrEvMwf1LVbC3ebGHO86GEry3w6KEDlh-fUUpapKYx81CNrE_SGS1O2a-6lMecgT7syojIRcXcxlQYkKt-rIb3q6NEA1QBMeILxi94hJaTBjF4QsYneyhGnH2i7TMijDYa3eHGpfGOhPPgWO1UOrGyhIpHO0OJqo6oJGwxs_t8lX3Pw%3D%3D)
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
