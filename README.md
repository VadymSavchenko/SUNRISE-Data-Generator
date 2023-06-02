# SUNRISE-Data-Generator
A set of scripts to generate test data for Commercetools

## Preparation
1. Clone this repository
2. Clone the [sunrise-data](https://github.com/commercetools/commercetools-sunrise-data.git) repository
3. Do `npm install` in the sunrise-data repository
4. In Merchant Center, go to Developer settings, create a new API client and copy it as a .env file
5. Put the .env file into this project's root folder
6. Inside this repo, in the `config.py`, change `SUNRISE_PATH` to the path of the sunrise-data repository

## Data Generation
1. Open values.py and change the values to your liking. Make sure that:
   1. `possible_values.categories` are filled, and you have a folder for each category inside the `shop_images` folder
   2. `shop_images` folder contains images for each category. The more images, the better.
   3. `description.en` and `name.en` are dictionaries with category names as keys
2. Run the run.py script
