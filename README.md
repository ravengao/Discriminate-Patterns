# Discriminate Patterns

This is a visualization system showing features and network to discriminate patterns of compounds and inner substructures based on medical data.

This system aims to present a matrix-based view to present different type of relationships and data feature presentation. For compound- structure view, For inner relationship exploration of compounds or structures, we use association rules to help understand and explore the network of patterns.

The data basically consists of one large table of compound and the presence and absence of substructures in each compound. Some compounds are active, others are not. The objective is to extract/visualize set of bits on which discriminate the actives from the inactives. As this file is very large, we usually compress it. So each column now corresponds to several substructures as shown in the second table. Then a value 1 means that at least one of the substructure is present, and a value of 0 means that none of the substructure is present in the fingerprint.

## 1. Selector

A heatmap of the number of patterns based on different parameters such as support (x-aixs, proportion of pattern existence in all), and aiScore (ratio of active / inactive the pattern locate in) Once you select the specific range, it will generate a list of patterns that satisfy the conditions. View 2 of parallel coordinate updated.

![alt tag](https://github.com/ravengao/Discriminate-Patterns/blob/master/img/dp-heatmap.png)

## 2. PCS (Parallel Coordinate + Scatterplots) and Network Tree

The dimensions of all patterns selected include: support, aiScore, active compound #, inactive compound # and number of elements in each pattern. Each 2 dimensions (parameter) will form scatter plot for further analysis. Interaction include brushing on both parallel coordinate and scatter plot. The it will generate another list of patterns selected on the up left corner. You can then click on one specific pattern to see more information. 

Tree network is a hierarchical network of selected pattern. You can choose confidence level to generate new patterns. (e.g.: pattern 134 will generate patterns like 1345, 1347, 1349) You can click on each node to either collapse or expand children nodes. Color of each node indicate the active vs inactive compound ratio. Size is the frequency of the pattern.

![alt tag](https://github.com/ravengao/Discriminate-Patterns/blob/master/img/02.png)
