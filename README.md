# Lobus Challenge
Completed by Sean Yun

## Objective
As stated in the challenge specifications, given a scenario where someone has to complete a sequence of tasks in a multi-story building where the elevator is not free to ride, minimize the total cost of riding the elevator while completing at least one task on each floor that is visited.

## Dependencies
### Environment setup
This solution uses Python 3.7. Various Python modules are utilized, including numpy, pandas, Beautiful Soup, Selenium, and luigi. Furthermore, the easiest way to set up the appropriate environment is through Anaconda, where one can set up a virtual environment, from which all the necessary packages can be installed with the following command:
- `conda install pandas bs4 selenium luigi`

## Execution
To create the two datasets for the challenge, we need to run the lot_pipeline.py script, which contains a luigi ETL pipeline that pulls the necessary information for each lot in an auction:
`python pipeline/lot_pipeline.py`

The two datasets will be in the data folder.  To find similar objects based on a specified threshold, we can run the following command:

`python auction_data_analysis.py <length> <width> <threshold>`

The `main()` function in `auction_data_analysis.py` takes in three command line arguments, the first two being the dimensions of the piece of art being a a point of comparison and the last being the threshold.  There are three parts to the output:
1. List of similar objects for the Nov. 17 auction
2. List of similar objects for the Mar. 18 auction
3. The average value of lots sold for both auctions grouped by artists who appear in both auctions.

For example, for a piece of art that is 55 cm by 59 cm and a threshold of 10 cm, run:
``` sh
$ python auction_data_analysis.py 55 59 10
Similar pieces from the first auction: 
                                                        dim_0  dim_1  price_value
artist              title                                                       
Maurice de Vlaminck Eglise sous la neige                46.5   55.1        87500
                    Village au bord de la rivière       54.0   65.1       100000
Henri Lebasque      Mère et enfant                      46.0   56.9        65000
Henri Le Sidaner    Barques blanches au clair de lune   58.0   69.0        81250

Similar pieces from the second auction: 
                                                    dim_0  dim_1  price_value
artist              title                                                   
Maurice de Vlaminck Paysage de neige                54.0   65.0        93750
                    La ferme                        54.0   65.0        47500
Henri Le Sidaner    Sur les dunes, Etaples          46.5   61.0        22500
Henri Lebasque      Trois baigneuses sur la plage   46.0   55.3        32500

Average values by artist: 
                      price_value_1117  price_value_0318
artist                                                 
Henri Le Sidaner                81250           22500.0
Henri Lebasque                  65000           32500.0
Maurice de Vlaminck             93750           70625.0
```

## Rationale behind technical choices
Below are some details about the reasoning behind my technical choices

### Luigi pipeline
Luigi provides an elegant way to define ETL pipelines by modeling different tasks as a directed graph where each task is a node and each edge is defined as required tasks that need to be completed before running a specified task.

For each task, an `output` file needs to be defined since luigi checks if that `output` file exists if a specific task is a dependency for another one.  This is nice because if the pipeline is run multiple times, certain tasks don't need to be restarted everytime if their `output` file already exists: for example, when scraping the page for a specific auction, once we got the lot URLs for the first time (the `PullLotURLsFromSale` task), if we needed to run the pipeline again for any reason, we didn't have to hit the web server again as long as the `output` file for the `PullLotURLsFromSale` task is still there.

Although there were only three tasks for this pipeline we defined, should I want to define more tasks, I can easily add it to the pipeline and then add the necessary dependencies for the other tasks.

### Selenium and Beautiful Soup
In order to scrape the necessary information, Beautiful Soup was used as our primary web scraper.

When trying to get all the lots for a specific sale, I noticed that a specific link (Load all) needed to be clicked in order to get every lot in that auction.  Therefore, I decided to use Selenium, which is tradionally used for front-end testing, to be able to click that 'Load all' link, which would then allow me to get the necessary HTML to get every lot link.

## Next Steps
Next steps to improve the current solution revolve around debugging the pipeline and refactoring the code base.

### Debugging data extraction
My main issue when extracting the data was the `LotDetails` section of the HTML docs for each lot since all the details were in one block rather than being in different paragraphs with a specific id.  Therefore, I had to play around with conditional statements to handle different edge cases (for example, if the lot details were missing medium info or if they had two lines describing the signature).  Unfortunately, I did not have enough time to handle everyone of the these cases, so the extract lot information is not perfect for a few lots.  Therefore, my first next step would involve debugging this and perhaps defining a few expected words for each piece of lot information that can then be used to find the information correctly rather than hardcoding the indices in the `LotData` class.

## Not using Selenium

After finishing my web scraping implementation for auction pages using Selenium, I realized that there was a tag ('?pg=all') that can be append to the url, which would then get the auction page with all the lots already loaded without having to click the 'Load all' link, therefore making Selenium unnecessary.  Unfortunately, when I tried to use urllib to get the lot urls, BeautifulSoup couldn't find the expected id that identified the container with all the lots.  Therefore, as a next step, with more time, I would try to figure out a way to use the '?pg=all' tag so that we can remove Selenium as a dependency.