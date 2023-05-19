# Master-thesis
Here is my master thesis program. It calculates reliability based on provided matrix. It was done according to the requirements set on the tesis.
After opening the program you will be asked to choose a file with a matrix that need to be calculated. It should look like this:
5
1,2
1,3
1,4
2,3
4,5
Where the first row is number of vertices, and all the other ones specify the edges (eg. there is an egde between first and second vertice)
You can then check if the matrix you provided is correct. For the above matrix it would look like this:
[[1,1,0,0,0]
[1,0,1,0,0]
[1,0,0,1,0]
[0,1,1,0,0]
[0,0,0,1,1]]
Where each row is an edge (first one is an egde between first and second vertice)
You will be prompted with two questions.
Which verticies should be connected? (eg. 2,3,5)
What should be the name of the results file?
After submitting the file with chosen name will be generated (in the results folder) and inside it there will be an equation generated by the program using factioring alghoritm. 
For the above example the solution will look like this:

R3*R5*(R1*R2+F1*R2*R4+R1*F2*R4)

R3 means the probability of edge 3 working correctly after specified time, and F2 means the probability of edge 2 not working correctly after specified time