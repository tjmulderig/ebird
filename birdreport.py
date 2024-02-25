import datetime
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

class birdreport():
    
    """
    Reads in provided JSON data on bird observations and generates reporting
    information such as number of unique species seen and number of birds observed.

    Methods:
        speciesObserved
        speciesCount
        plotObservations
        plotCount
    """

    def __init__(self, data, regionCode, back):

        self.back = back
        self.regionCode = regionCode
        self.df = pd.DataFrame(data)
        print("Generating birding report for data:")
        print(self.df.head())

        num_unique_species = len(self.df['speciesCode'].unique())
        num_unique_locations = len(self.df['locName'].unique())
        num_birds_total = self.df['howMany'].sum()
        pct_obs_reviewed = self.df['obsReviewed'].sum() / self.df['obsValid'].sum()
        highest_count_species = self.df.loc[
                                    self.df['howMany'] == self.df['howMany'].max(), 
                                    ['comName', 'howMany', 'locName', 'obsDt']
                                    ]
        print("------------------------------------------------------")
        print("Birdreport summary stats:")
        print("Number of unique species seen:", num_unique_species)
        print("Number of unique locations:", num_unique_locations)
        print("Total number of birds observed:", num_birds_total)
        print("Percentage of observations reviewed by birding experts:",
               "{:.0%}".format(pct_obs_reviewed))
        print("Largest amount seen of any species at one time: \n", highest_count_species)

    def speciesObserved(self):

        """
        Returns python list of all unqiue species seen in the observations.
        """
        species_obs = self.df['comName'].unique()
        
        return species_obs
    
    def speciesCount(self):

        """
        Sums across each common name (species) the howMany column to calculate
        total amount of each species seen across time range.

        Returns 
            Pandas Data Series of total counts per species indexed by
        'comName' column. 
        """
        species_count = self.df.groupby(['comName'])['howMany'].sum().sort_values(ascending=False)
        
        return species_count

    def plotObservations(self):       
        
        """
        Plots location of observations on map of New Jersey with county lines. 
        """
        if self.regionCode != 'US-NJ':
            raise Exception("Method currently works for NJ data only.") 
        
        mapfile = gpd.read_file('C:\\Users\\tjmul\\ebird\\shapefiles\\GU_CountyOrEquivalent.shp')
        crs = {'init': 'EPSG:4326'}
        
        geometry = [Point(xy) for xy in zip(self.df['lng'], self.df['lat'])]

        geodf = gpd.GeoDataFrame(self.df, crs = crs, geometry = geometry)

        fig, ax = plt.subplots(figsize = (10, 10))
        mapfile.to_crs(epsg=4326).plot(ax=ax, color='darkgrey')
        geodf.plot(ax=ax, alpha = 0.3, color='blue')
        
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        today_str = datetime.datetime.today().strftime('%Y-%m-%d')
        firstday = datetime.datetime.today() \
                    - datetime.timedelta(days=self.back)
        firstday_str = firstday.strftime('%Y-%m-%d')
        title = "Recent Bird Observations in New Jersey, " + firstday_str \
                + " to " + today_str
        ax.set_title(title)

        plt.show()

        return

    def plotCount(self):

        """
        Plots bar chart of number of observations on date. 
        """

        self.df['obsDt'] = pd.to_datetime(self.df['obsDt'], format='mixed')
        self.df['date'] = self.df['obsDt'].dt.date
        
        df_days = self.df.groupby(['date'])['howMany'].sum().sort_index()

        ax = df_days.plot.bar()

        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Birds")
        ax.set_title("Number of Birds Seen on Each Date")

        plt.show()

        return


