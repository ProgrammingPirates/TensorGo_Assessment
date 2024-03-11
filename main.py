import openai
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.environ.get('OPENAI_API_KEY', '')

def read_and_parse_csv(file_path):
    """
    Read and parse a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: Parsed DataFrame if successful, else None.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logger.error(f"Error reading the CSV file: {e}")
        return None

def perform_basic_statistical_analysis(data_frame):
    """
    Perform basic statistical analysis on the DataFrame.

    Parameters:
    - data_frame (pd.DataFrame): Input DataFrame.

    Returns:
    - None
    """
    if data_frame is not None:
        numeric_data = data_frame.select_dtypes(include=['number'])
        mean_values = numeric_data.mean()
        median_values = numeric_data.median()
        std_dev_values = numeric_data.std()
        correlation_coefficient = numeric_data.corr()

        logger.info("\nMean Values:\n%s", mean_values)
        logger.info("\nMedian Values:\n%s", median_values)
        logger.info("\nStandard Deviation Values:\n%s", std_dev_values)
        logger.info("\nCorrelation Coefficient:\n%s", correlation_coefficient)

def generate_plots(data_frame):
    """
    Generate histograms and scatter plot.

    Parameters:
    - data_frame (pd.DataFrame): Input DataFrame.

    Returns:
    - None
    """
    if data_frame is not None:
        # Histogram
        data_frame.hist(figsize=(10, 8), bins=20)
        plt.suptitle('Histograms of Numerical Columns')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.show()

        # Scatter Plot
        plt.scatter(data_frame['X'], data_frame['Y'])
        plt.title('Scatter Plot of X vs Y')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

def ask_gpt3_about_data_general(question, api_key):
    """
    Ask GPT-3 about the data using a given question.

    Parameters:
    - question (str): The question to ask GPT-3.
    - api_key (str): OpenAI API key.

    Returns:
    - str: GPT-3 response.
    """
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()


def configure_logger(log_level=logging.INFO):
    """
    Configure logger with the specified log level.

    Parameters:
    - log_level (int): Log level (e.g., logging.INFO, logging.DEBUG).

    Returns:
    - None
    """
    logging.basicConfig(level=log_level)

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
    - argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Perform statistical analysis on CSV files and generate plots.")
    parser.add_argument("csv_file_path", type=str, help="Path to the CSV file for analysis.")
    parser.add_argument("--save_plots", action="store_true", help="Save generated plots to files.")
    parser.add_argument("--plot_path", type=str, default="plots", help="Path to save plots if --save_plots is True.")
    parser.add_argument("--openai_api_key", type=str, help="OpenAI API key.")
    return parser.parse_args()

def create_plot_directory(plot_path):
    """
    Create a directory for saving plots if it does not exist.

    Parameters:
    - plot_path (str): Path to the plot directory.

    Returns:
    - None
    """
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

def main():
    args = parse_arguments()
    configure_logger()
    openai.api_key = args.openai_api_key or os.environ.get('OPENAI_API_KEY', '')
    data_frame = read_and_parse_csv(args.csv_file_path)
    if data_frame is not None:
        perform_basic_statistical_analysis(data_frame)
        create_plot_directory(args.plot_path)
        generate_plots(data_frame)
        questions = [
            "Can you provide general insights on the data?",
            "Describe any notable patterns in the dataset.",
            "Highlight any interesting observations in the data.",
        ]

        for question in questions:
            gpt3_response = ask_gpt3_about_data_general(question)
            logger.info("\nGPT-3 Response for '%s':\n%s", question, gpt3_response)

    else:
        logger.error("Failed to parse the CSV file.")

if __name__ == "__main__":
    main()
