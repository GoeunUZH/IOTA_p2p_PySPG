# IOTA_p2p_PySPG


## Running the Autopeering model with pyspg

pyspg is a python module to run experiments in parallel over a large range of parameters. The syntax to run an experiment:

`python3 iota_p2p.py --repeat=5 --workers=32 sim.spg`

- --workers=32 is setting 32 threads to work in parallel
- sim.spg is the .spg with the actual parameters range in use for the experiment


Three files are needed in order for this command to work:

1. iota_p2p.py which is a wrapper to run the model trought pyspg

2. iota_p2p.input which is a file which records the inputs parameters for the model and their default value

3. iota_p2p.stdout which is a file which records the expected outputs

4. sim.spg wherech actually defines the "experiment": it assigns the parameters ranges, using pyspg sintax (see [pyspg wiki](https://github.com/tessonec/PySPG/wiki/Tutorial%3A-A-crash-course))

5. sim_powerLawFloat.go is the Autopeering simulation from IOTA team golang


 ## Results intepretation

The output of the command in the previous section is a csv file, named sim.csv.

For exanple, if we run the command:

`python3 iota_p2p.py --repeat=2 --workers=32 sim.spg`

with a `sim.spg` like

```
@execute iota_p2p.py                                   
.R 2 10  
:rho 2.5  
.N 100 500 1000  
+zipfs 0.5 6 0.2
```

we would obtain a main.csv looking something like this

```
R,rho,zipfs,diameter
1,2,0.5,11.0
1,2,0.6,12.0
1,2,0.7,12.0
1,2,0.8,14.0
1,2,0.9,14.0
1,3,0.5,8.0
1,3,0.6,9.0
1,3,0.7,9.0
1,3,0.8,10.0
1,3,0.9,11.0
1,4,0.5,7.0
1,4,0.6,7.0
1,4,0.7,8.0
1,4,0.8,9.0
1,4,0.9,9.0
1,5,0.5,6.0
1,5,0.6,7.0
1,5,0.7,7.0
1,5,0.8,8.0
1,5,0.9,8.0
2,2,0.5,11.0
2,2,0.6,12.0
2,2,0.7,12.0
2,2,0.8,14.0
2,2,0.9,14.0
2,3,0.5,8.0
2,3,0.6,9.0
2,3,0.7,9.0
2,3,0.8,10.0
2,3,0.9,11.0
2,4,0.5,7.0
2,4,0.6,7.0
2,4,0.7,7.0
2,4,0.8,9.0
2,4,0.9,9.0
2,5,0.5,6.0
2,5,0.6,7.0
2,5,0.7,7.0
2,5,0.8,8.0
2,5,0.9,8.0
...
```

`R`, `rho`, `zipfs`, `R` are parameters:
- `R` is the neighbor bound of each node in 
- `rho` is the the ratio determining the length of the rank to consider
- `r` is the minimum number of nodes' identities to return for both lower and upper sets
