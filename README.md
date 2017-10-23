# Discriminate Patterns

This is a visualization system showing features and network to discriminate patterns of compounds and inner substructures based on medical data.

This system aims to present a matrix-based view to present different type of relationships and data feature presentation. For compound- structure view, For inner relationship exploration of compounds or structures, we use association rules to help understand and explore the network of patterns.

The data basically consists of one large table of compound and the presence and absence of substructures in each compound. Some compounds are active, others are not. The objective is to extract/visualize set of bits on which discriminate the actives from the inactives. As this file is very large, we usually compress it. So each column now corresponds to several substructures as shown in the second table. Then a value 1 means that at least one of the substructure is present, and a value of 0 means that none of the substructure is present in the fingerprint.

## Selector

![alt tag](https://github.com/ravengao/Discriminate-Patterns/blob/master/img/dp-heatmap.png)

## PCS (Parallel Coordinate + Scatterplots) and Network Tree

![alt tag](https://github.com/ravengao/Discriminate-Patterns/blob/master/img/02.png)
