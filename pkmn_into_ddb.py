import os
import csv
import json
import boto3
import argparse


def create_dynamodb_resource(profile_name, region_name):
    """Creates a DynamoDB resource.

    Args:
        profile_name (str): The AWS profile name. Optional.
        region_name (str): The AWS region name. Required.

    Returns:
        dynamodb resource.
    """
    session_params = {'region_name': region_name}
    if profile_name:
        session_params['profile_name'] = profile_name
    session = boto3.Session(**session_params)
    return session.resource('dynamodb')


def convert_csv_to_json(csv_file_path, json_file_path):
    """Converts a CSV file to JSON.

    Args:
        csv_file_path (str): The file path to the CSV file.
        json_file_path (str): The file path to save the JSON data.
    """
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return data


def insert_data_into_dynamodb(data, table):
    """Inserts data into the DynamoDB table using 'ID' as the key.

    Args:
        data (list): List of dictionaries to insert into DynamoDB.
        table (dynamodb.Table): The DynamoDB table instance.
    """
    for item in data:
        if 'ID' in item:  # Ensure 'ID' exists in the item
            table.put_item(Item=item)


def process_directory(directory_path, table):
    """Processes a directory to convert all CSV files to JSON files
    and insert entries into a DynamoDB table.

    Args:
        directory_path (str): The directory containing CSV files.
        table (dynamodb.Table): The DynamoDB table instance.
    """
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(directory_path, file_name)
            json_file_path = os.path.join(directory_path, file_name.replace('.csv', '.json'))
            data = convert_csv_to_json(csv_file_path, json_file_path)
            insert_data_into_dynamodb(data, table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload Pokémon data to DynamoDB.')
    parser.add_argument('--profile', type=str, help='AWS profile name.')
    parser.add_argument('--table-name', type=str, required=True, help='DynamoDB table name. (Required)')
    parser.add_argument('--region', type=str, required=True, help='AWS region. (Required)')

    args = parser.parse_args()

    table_name = args.table_name
    directory = os.path.expanduser('~/Desktop/pkmn_stuff')

    dynamodb = create_dynamodb_resource(args.profile, args.region)
    table = dynamodb.Table(table_name)
    process_directory(directory, table)
