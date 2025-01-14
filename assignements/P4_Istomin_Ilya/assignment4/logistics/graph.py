from neo4j import GraphDatabase
import neo4j.exceptions

class GraphManager:
    def __init__(self, uri, user, password, transport_params, nodes, edges):
        """
        Initializes the GraphManager with connection details, transport parameters, nodes, and edges.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.transport_params = transport_params  # Transport parameters
        self.nodes = nodes  # Graph nodes
        self.edges = edges  # Graph edges

    def close(self):
        """Closes the connection to Neo4j."""
        self.driver.close()

    def reset_graph(self):
        """Completely deletes all data, indexes, and constraints from the graph."""
        with self.driver.session() as session:
            # Delete all nodes and relationships
            session.run("MATCH (n) DETACH DELETE n")
            print("All nodes and relationships have been deleted.")

            # Remove indexes
            try:
                indexes = session.run("SHOW INDEXES YIELD name RETURN name")
                for record in indexes:
                    session.run(f"DROP INDEX `{record['name']}`")
                print("All indexes have been deleted.")
            except neo4j.exceptions.ClientError:
                print("Failed to retrieve or delete indexes. This may be due to Neo4j version limitations.")

            # Remove constraints
            try:
                constraints = session.run("SHOW CONSTRAINTS YIELD name RETURN name")
                for record in constraints:
                    session.run(f"DROP CONSTRAINT `{record['name']}`")
                print("All constraints have been deleted.")
            except neo4j.exceptions.ClientError:
                print("Failed to retrieve or delete constraints. This may be due to Neo4j version limitations.")

    def setup_graph(self):
        """Initializes the graph by creating nodes and relationships."""
        with self.driver.session() as session:
            # Create nodes
            for node in self.nodes:
                session.run("""
                    CREATE (n:City {id: $id, type: $type, name: $name, color: $color})
                """, id=node['id'], type=node['type'], name=node['name'], color=node['color'])
            print("Nodes created.")

            # Create relationships
            for edge in self.edges:
                for transport in self.transport_params.keys():  # Iterate through transport options
                    if transport in edge['transports']:
                        total_time, total_cost = self.calculate_time_and_cost(transport, edge['distance'])

                        # Create relationships for the transport type
                        session.run(f"""
                            MATCH (a:City {{id: $from_node}}), (b:City {{id: $to_node}})
                            CREATE (a)-[:{transport} {{
                                distance: $distance, total_time: $total_time, total_cost: $total_cost
                            }}]->(b)
                        """, from_node=edge['from'], to_node=edge['to'], distance=edge['distance'],
                                total_time=total_time, total_cost=total_cost)

                        # Create reverse relationships
                        session.run(f"""
                            MATCH (a:City {{id: $to_node}}), (b:City {{id: $from_node}})
                            CREATE (a)-[:{transport} {{
                                distance: $distance, total_time: $total_time, total_cost: $total_cost
                            }}]->(b)
                        """, from_node=edge['from'], to_node=edge['to'], distance=edge['distance'],
                                total_time=total_time, total_cost=total_cost)
            print("Relationships created.")

    def calculate_time_and_cost(self, transport, distance):
        """Calculates the total time and cost for a transport mode over a given distance."""
        params = self.transport_params[transport]
        total_time = (distance / 100) * params['time_per_100km'] 
        total_cost = (distance / 100) * params['cost_per_100km']
        return total_time, total_cost

    def get_node_info(self, node_id):
        """Retrieves information about a specific node."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n {id: $node_id})
                RETURN n
            """, node_id=node_id)
            node = result.single()
            if node:
                return node["n"]
            return None

    def get_edge_info(self, from_node, to_node, transport_type):
        """Retrieves relationship information between two nodes for a specific transport type."""
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH (a:City {{id: $from_node}})-[r:{transport_type}]->(b:City {{id: $to_node}})
                RETURN r
            """, from_node=from_node, to_node=to_node)
            edge = result.single()
            if edge:
                return edge["r"]
            return None
