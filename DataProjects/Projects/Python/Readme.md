

**CAS Machine Intelligence - Big Data**

Author: Bruno Hunkeler  
Date:   02.01.2021

  **Trash bin project**

  Any city in the world has trash-bins, which fill up over time. Each of the trash bins needs to be emptied from time to time.   
  Each workforce in a city work on a certain schedule and therefore on predefined routes to empty trash-bins. The assumption is, 
  that a route always follows the same pattern. A person of the workforce will start it's route and approach trash-bins, which 
  have a filling level of 10%, 20% etc. Some of the trash-bins are approached and are almost empty. In order to reduce the effort 
  resp. time consumption an optimization should be considered.  

  The project idea at hand is to equip each and every trash-bin with an IoT component, which communicates with a central server. 
  The IoT component should be able to send a timestamp, location- and filling information (e.g. 10, 20, ..., 100%) etc., but also 
  hardware status information about the component itself. 

  The received information must be processed via big data. A threshold needs to be defined (filling level e.g. 50%), where a 
  trash-bin needs attention. The appliaction should monitor the filling levels and propose an optimale route (leeds to an optimization) 
  based on the `travelling salesman problem`. A simulated annealing optimization algorithm or an OR - Tools approach should be used 
  to resolve the optimal route of a Garbageman.  




