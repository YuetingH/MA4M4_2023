# MA4M4 (22/23)
> Support Classes for MA4M4: Topics in Complexity Science at the University of Warwick

We provide guidance on how to use [Python packages](https://www.python.org/) via [Jupyter Notebook](https://jupyter.org/) to analyse networks. Please feel free to choose other programming languages, but we will help where we can in this case.

Instructions on how to install Python & Jupyter Notebook can be found online: [Windows](https://www.geeksforgeeks.org/how-to-install-jupyter-notebook-in-windows/) | [MacOS](https://www.geeksforgeeks.org/how-to-install-jupyter-notebook-on-macos/) | [Linux](https://www.geeksforgeeks.org/how-to-install-jupyter-notebook-in-linux/)

&nbsp;

## Support Class 1 (Week 3)
[SupportClass1.ipynb](https://github.com/YuetingH/MA4M4_2023/blob/main/Support_Class1/SupportClass1.ipynb): This notebook is to give you simple examples of the types of packages you can use to represent networks and compute their basic properties (e.g., [NetWorkX](https://networkx.org/), [Numpy](https://numpy.org/), [Pandas](https://pandas.pydata.org/)). 

After this class, you should be able to:
- import an empirical network from a website (e.g. [Konect](http://konect.cc/networks/)) into Jupyter Notebook
- compute some key network properites (e.g. degree, centrality, average distance)
- visualise a network and its corresponding adjacency matrix in a simple way
  
## Lab Class (Week 5 - 6)
[LabClass.ipynb](https://github.com/YuetingH/MA4M4_2023/blob/main/Lab_Class/LabClass.ipynb): This notebook provides a basic guidance to complete the tasks in [LabClass.pdf](https://github.com/YuetingH/MA4M4_2023/blob/main/Lab_Class/LabClass.pdf). Compared with the previous support class where we provide detailed programming code, our aim of this lab class is to give you an opportunity to practice coding. 

In this lab class, you will
- review some content covered in our last support class (e.g., network visualisation, centrality measures).
- further investigate structural properties of networks (e.g., Laplacian matrix)
- generate random graphs using the Erdös-Rényi model and Barabási–Albert model
- explore community structure using *modularity maximisation* [Optional]

## Support Class 2 - Seminar Session (Week 8)
[SupportClass2.ipynb](https://github.com/YuetingH/MA4M4_2023/blob/main/Support_Class2/SupportClass2.ipynb): This notebook provides coding examples of community detection on a specific dataset that consists of temporal undirected weighted networks. 

After this class, you should be able to:
- import an empirical network in a more general way, particularly for a temporal one
- perform modularity maximisation for community detection
- visualise relevant results and investigate robustness

## Support Class 3 - Seminar Session (Week 9)
[Network_Visualisation.ipynb](https://github.com/YuetingH/MA4M4_2023/blob/main/Support_Class2/Network_Visualisation.ipynb): This notebook serves as a documentation of coding resources related to network visualization. Additionally, we will give a presentation to provide further explanation. Slides are available [here](https://gamma.app/public/kjm9a9mdhzlcj7a).

After this class, you should be able to:
- create nice visualizations for small networks using NetworkX
- create nice visualizations for large networks using ForceAtlas2 (Node Layout) and Curved Edge (Edge Layout)
- produce Sankey Diagram to visualize the flow of community assignment over time
- have access to other network visualisation resources, such as software [Gephi](https://gephi.org/) & [Tulip](https://tulip.labri.fr/site/)

Please note that in order to run this Jupyter notebook successfully, you may need to install additional packages. Detailed instructions on how to do this can be found within the notebook itself.


