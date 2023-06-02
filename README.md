# SUNRISE-Data-Generator
A set of scripts to generate test data for Commercetools

## Preparation
1. Clone this repository
2. Run `pip install -r requirements.txt`
3. Clone the [sunrise-data](https://github.com/commercetools/commercetools-sunrise-data.git) repository
4. Run `npm install` inside the sunrise-data repository
5. In Merchant Center, go to Developer settings, create a new API client and copy it as an .env file
6. Put the .env file into this project's root folder
7. Inside this repo, in the `config.py`, change `SUNRISE_PATH` to the path of the sunrise-data repository

## Data Generation
1. Open values.py and change the values to your liking. Make sure that:
   1. `possible_values.categories` are filled, and you have a folder for each category inside the `shop_images` folder
      1. Categories can have one level of subcategories. Parent categories are created automatically, based on the categories in `values.py`
   2. `shop_images` folder contains images for each category. The more images, the better.
      1. Just use category keys as folder names. Do not include parent category keys in the folder names.
   3. `description.en` and `name.en` are dictionaries with category names as keys
2. Run the `run.py` script
   1. You will be prompted to replace the `.env` file if it already exists in the sunrise-data repository.
   2. Check your project key when prompted and press Enter
   3. Choose whether to run cleanups or not. This will clean everything that this script can create.