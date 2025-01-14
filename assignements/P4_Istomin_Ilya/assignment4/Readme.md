# Logistics Platform
This platform is designed to provide an efficient solution for route and schedule planning, vehicle assignment, and integration of multiple packages with different constraints and synchronization requirements.

## Installation
 1. Set up a Python virtual environment:
 ```code
 python3 -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```
2. Install dependencies:
```code 
pip install -r requirements.txt
```
3. Install and set up Neo4j

## Setup

1. **Create a configuration file**: Create a **config.py** file in the root directory with the following content:
```code
class Config:
    user = "your_neo4j_username"
    password = "your_neo4j_password"
```

2. **Add your graph data**: Update the nodes and edges data in the utils.py file inside logistics folder to include your desired graph (cities, warehouses, connections, and transport types).
### Important note 
You can use my data or change with your own values but please save the **type and structure** of data providen.


## Usage

1. **Run the demo script**: To execute the full demonstration of the platform, run:
```code
python run_demo.py
```
2. **Explore via Jupyter Notebook**: To run the demo in an interactive environment:
```
jupyter notebook
```
Open the **demo.ipynb** notebook and execute the cells step by step. 

### Important Note
If you change structure of graph you may need to change values in py file and ipynb file



# System Overview
## GraphManager
**GraphManager** is the foundational layer for handling graph data and interactions with the Neo4j database. Key features:
- Initializes the graph by creating nodes and relationships.
- Calculates time and cost for transport modes and distances.
- Provides methods to retrieve information about nodes and edges.
- Resets the graph for a clean slate before setting up.

## RouteManager
**RouteManager** handlesroute-related logic:
- Finds the cheapest and fastest routes between nodes.
- Combines route data into delivery options (Same_day, One_day, Economy).
- Provides formatted route outputs with detailed information about loading, unloading, and travel times.

## FleetManager
**FleetManager** manages transport vehicles:
- Assigns vehicle IDs for given transport modes and routes.
- Reuses vehicles for identical routes to optimize transport usage.
- Centralizes vehicle assignment logic for all packages.

## PackageManager
**PackageManager** orchestrates package handling:
- Registers packages with specified delivery types and start times.
- Applies delays to synchronize departures when possible.
- Assigns vehicles to packages sharing the same initial segment.
- Creates a comprehensive delivery schedule, including timing for all segments, delays, and vehicle assignments.



# Example Workflow
1. Set up the graph: The run_demo.py script initializes the graph, creating nodes and relationships between cities with transport types and associated costs/times.

2. Generate routes: Use RouteManager to query routes between cities, finding the cheapest, fastest, or most suitable delivery options.

2. Register packages: Register multiple packages with PackageManager, specifying delivery types and desired start times.

3. Assign vehicles: PackageManager ensures packages with close departure times share vehicles for the initial segment when possible.

4. Create schedules: Generate the final delivery schedule, including all details for each segment, vehicle assignments, and applied delays.