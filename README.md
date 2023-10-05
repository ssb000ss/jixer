# Console Application for Information Retrieval Using Various Search Engines

This console application provides an interface for performing search queries using different search engines. Users can select search engines, input queries, and save search results to files.

## Getting Started

To get started with the application, follow these steps:

### Prerequisites

Before you begin, make sure you have the following components installed on your computer:

- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)

### Installation

1. Clone the repository to your computer:

   ```bash
   git clone https://github.com/ssb000ss/jixer.git
   ```

2. Navigate to the project directory:

   ```bash
   cd jixer
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Create a `.env` file in the project's root folder and add the following environment variables:

   ```
   SHODAN_API_KEY=your_Shodan_key
   NETLAS_API_KEY=your_Netlas_key
   FOFA_API_KEY=your_Fofa_key
   FOFA_EMAIL=your_Fofa_email
   ZOOMEYE_API_KEY=your_Zoomeye_key
   ```

   Replace `your_Shodan_key`, `your_Netlas_key`, `your_Fofa_key`, `your_Fofa_email`, and `your_Zoomeye_key` with your actual API keys.

2. Run the application:

   ```bash
   python jixer_CLI.py
   ```

3. Follow the application's instructions to choose a search engine, input a query, and save the results.

## Development

If you want to make changes to the application, you'll need a development environment with Python. It's recommended to use a virtual environment:

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

3. Install development dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Make the necessary changes and run tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.