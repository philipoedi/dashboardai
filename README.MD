# DashboardAI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

DashboardAI is an experimental project that demonstrates the potential of combining natural language processing with data visualization. It allows users to interact with their data through natural language queries, generating both SQL queries and visualizations automatically using OpenAI's API.

⚠️ **Note:** This project uses OpenAI's deprecated Completion API. While it served as an interesting proof of concept, modern solutions like ChatGPT's Code Interpreter now provide more robust alternatives. As such, this project is no longer actively maintained.

## Features

- Upload CSV and Excel files for analysis
- Natural language to SQL query conversion
- Automatic visualization generation based on natural language descriptions
- Interactive data tables with sorting and filtering capabilities
- Real-time graph updates based on user queries

## Technology Stack

- Python 3.9
- Dash & Plotly for visualization
- OpenAI API (text-davinci-003 model)
- SQLite for in-memory database operations
- Pandas for data manipulation

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/dashboardai.git
cd dashboardai
```

2. Install dependencies:

```bash
uv pip install -r requirements.txt
```


3. Create a `.env` file in the root directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```


## Usage

1. Start the application:

```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:8050`
3. Upload your data file (CSV or Excel)
4. Use natural language to query your data or create visualizations

## Example Queries

- "Show me a scatter plot of income vs debt"
- "What is the average income grouped by year?"
- "Create a bar chart showing sales by region"

## Testing

Run the test suite using pytest:

```bash
pytest
```

2. Open your browser and navigate to `http://localhost:8050`
3. Upload your data file (CSV or Excel)
4. Use natural language to query your data or create visualizations

## Example Queries

- "Show me a scatter plot of income vs debt"
- "What is the average income grouped by year?"
- "Create a bar chart showing sales by region"

## Testing

Run the test suite using pytest:

## Project Structure

- `app.py`: Main application file
- `dashboardai/`: Core package directory
  - `api.py`: OpenAI API integration
  - `data.py`: Data handling and database operations
  - `visualizations.py`: Visualization components
- `test/`: Test suite directory

## Limitations

- Uses deprecated OpenAI Completion API
- Limited to basic SQL queries and visualizations
- No support for complex data transformations

## Future Considerations

While this project served as an interesting exploration of AI-powered data visualization, modern solutions like ChatGPT's Code Interpreter provide more sophisticated capabilities. As such, this project will remain as a demonstration piece rather than receiving further development.

## Contributing

While this project is no longer actively maintained, you're welcome to fork it and adapt it for your needs. If you do make improvements, please consider sharing them with the community.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the API that made this experiment possible
- Plotly and Dash teams for their excellent visualization libraries
- The open-source community for various dependencies used in this project
