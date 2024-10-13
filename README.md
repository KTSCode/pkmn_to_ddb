# Pokémon Data in DynamoDB
Josh, here are the instructions to setup and use the [Script](pkmn_into_ddb.py) to put the Pokémon data for all 9 generations into DynamoDB. Feel free to pull this repo and add to it. If you create a pull request, I can review it and help you with your ideas for the data.

## Setup:
1. **Install Homebrew**

   Homebrew is a package manager for macOS. If you don't have it installed, open Terminal and run:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install wget and Other Required Tools**

   Use Homebrew to install wget and any other essential tools, such as Python if it's not already installed:

   ```bash
   brew install wget
   # Install the AWS CLI if needed
   brew install awscli
   ```

3. **Install Python Requirements**

   Ensure you have a virtual environment set up and install the necessary Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the Pokémon Data Zip with wget**

   Use `wget` to download the Pokémon data zip file:

   ```bash
   wget https://github.com/lgreski/pokemonData/raw/refs/heads/master/PokemonData.zip -O ~/Desktop/pkmn_stuff/PokemonData.zip
   ```

5. **Unzip the Pokémon Data**

   Extract the contents of the zip file to your working directory:

   ```bash
   unzip PokemonData.zip
   ```

6. **Create the DynamoDB Table**

   Use the AWS CLI to create a DynamoDB table with `ID` as the primary key. The `--profile` flag is optional.

   First, set your table name and AWS region as environment variables:

   ```bash
   export TABLE_NAME=<YOUR_TABLE_NAME>
   export AWS_REGION=<YOUR_AWS_REGION>
   ```

   - Example:
     ```bash
     export TABLE_NAME=TestTable
     export AWS_REGION=us-east-1
     ```

   Then, run the following command:

   ```bash
   aws dynamodb create-table \
     --region $AWS_REGION \
     --table-name $TABLE_NAME \
     --attribute-definitions AttributeName=ID,AttributeType=S \
     --key-schema AttributeName=ID,KeyType=HASH \
     --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
   ```

7. **Run the Script to Put Data into DynamoDB**

   Execute the provided Python script to convert the CSV files and upload data to the DynamoDB table, passing the table name, region, and optionally the directory:

   ```bash
   python pkmn_into_ddb.py --table-name $TABLE_NAME --region $AWS_REGION
   ```

   To specify a different directory for CSV files, use the `--directory` argument:

   ```bash
   python pkmn_into_ddb.py --table-name $TABLE_NAME --region $AWS_REGION --directory <YOUR_DIRECTORY>
   ```

   Optionally, include a profile:

   ```bash
   python pkmn_into_ddb.py --table-name $TABLE_NAME --region $AWS_REGION --profile <YOUR_PROFILE>
   ```

### Notes:
- **AWS CLI Configuration**: Configure your AWS CLI if you wish to use profiles.
- **Data Verification**: Check the DynamoDB Console or use the AWS CLI to verify that data has been uploaded successfully.
