import os
from langchain_community.graphs import Neo4jGraph

def test_langchain_neo4j_connection():
    """
    Attempts to connect to Neo4j using langchain_neo4j.Neo4jGraph
    and verifies connectivity.
    Prints success or failure messages.
    """
    try:
        # Retrieve Neo4j credentials from environment variables
        NEO4J_URI="neo4j+s://e14248e5.databases.neo4j.io"
        NEO4J_USER="neo4j"
        NEO4J_PASSWORD="j_OfoqhHCpE1vq-qFEHfcyI0WkjIKcGktFmqGtnp0Oc"
        # Basic validation for environment variables
        if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
            print("\nERROR: Missing Neo4j environment variables.")
            print("Please ensure NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD are set.")
            return False
        print(f"Attempting to connect to Neo4j at: {NEO4J_URI}")
        print(f"Using username: {NEO4J_USER}")
        # Initialize Neo4jGraph. This internally uses the Neo4j Python driver
        # and attempts to establish connectivity upon instantiation or first use.
        graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USER, password=NEO4J_PASSWORD)
        # To explicitly test the connection, we can try to get the schema or run a simple query.
        # Getting the schema is a good way to verify the connection is active and authenticated.
        # This will raise an exception if the connection fails.
        schema = graph.get_schema
        print("\nSUCCESS: Successfully connected to Neo4j using langchain_neo4j.Neo4jGraph!")
        print(f"Graph schema retrieved (first 200 chars): {schema[:200]}...")
        return True
    except Exception as e:
        print(f"\nERROR: Failed to connect to Neo4j using langchain_neo4j.Neo4jGraph.")
        print(f"Details: {e}")
        print("Please check the following:")
        print("1. Neo4j URI, username, and password in your environment variables.")
        print("2. Neo4j database is running and accessible from your environment.")
        print("3. Network configurations (firewall, security groups, VPC settings).")
        print("4. The correct Neo4j driver version is compatible with langchain_neo4j.")
        return False

# --- Execute the connection test when the script is run ---
if __name__ == "__main__":
    test_langchain_neo4j_connection()