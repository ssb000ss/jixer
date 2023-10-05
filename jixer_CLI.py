import logging
import os
import dotenv

from engine import ShodanClient, NetlasClient, FofaClient, ZoomeyeClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# Function to initialize settings and search engines
def init_settings():
    dotenv.load_dotenv('.env')
    engines = {
        'shodan': ShodanClient(os.environ.get('SHODAN_API_KEY')),
        'netlas': NetlasClient(os.environ.get('NETLAS_API_KEY')),
        'fofa': FofaClient(api_key=os.environ.get('FOFA_API_KEY'), email=os.environ.get('FOFA_EMAIL')),
        'zoomeye': ZoomeyeClient(os.environ.get('ZOOMEYE_API_KEY')),
    }
    return engines


# Function to display the search engine selection menu
def show_engine_menu(engines):
    count = 1
    for key in engines.keys():
        print(f'{count}) - {key}')
        count += 1


# Function to perform search and save results
def perform_search(engine, query):
    count = engine.count(query)
    if count:
        logger.info(f"Running the {engine} engine with the query: {query}")
        servers = engine.search(query, count)
        if engine.save_results(query, servers):
            logger.info("Results have been successfully saved.")
        else:
            logger.error("An error occurred while saving the results.")
    else:
        logger.error("Please check the correctness of the query!")


# Main function
def main():
    engines = init_settings()

    while True:
        show_engine_menu(engines)
        print("Select an engine for search or enter 'exit'")
        engine_key = input("> ").strip()

        if engine_key == "exit":
            break

        if engine_key.isdigit() and 0 < int(engine_key) <= len(engines):
            engine = list(engines.values())[int(engine_key) - 1]
            print(f"Enter a valid query for the {engine} engine")
            query = input("> ")
            perform_search(engine, query)
        else:
            logger.error(f"Input error. Enter a number from 1 to {len(engines)}")


if __name__ == '__main__':
    main()
