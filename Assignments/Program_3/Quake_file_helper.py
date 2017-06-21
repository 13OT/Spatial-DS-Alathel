import glob
import json


class FileHelper(object):
    """
        This class helps read the earthquake data. by reading a series of json files

     Attributes:
        get_data: Returns a dictionary of earth quakes coordinates with year as key
     Usage:
        data = fh.get_data([2017]) #pass year in as list, get data for that year
        data = fh.get_data([2015,2016,2017]) #pass years in as list, get data for those years
    """

    def __init__(self):

        self.files = glob.glob('quake-????.json')

    def get_data(self, years=[], min_mag=7):
        """
        Reads earth quake data, given a list of year(s), from json files on the computer that match query parameter,
        saves the data if magnitude is bigger than 7
        Args:
            list
        Returns:
            Dictionary: data[year] = [(x,y),...,]
        example:

            Quakes = get_data(years)

            Quakes in now a dictionary of earth quakes locations with year as key
        """
        data = {}
        mag_data = {}

        for file in self.files:
            fyear = file.split('-')
            fyear = fyear[1].split('.')
            fyear = int(fyear[0])

            if fyear in years:
                f = open(file, 'r')
                json_data = json.load(f)
                keep = []

                for quake in json_data['features']:

                    if quake["properties"]["mag"] >= min_mag:
                        keep.append(tuple(
                            (quake['geometry']['coordinates'][0], quake['geometry']['coordinates'][1])))

                data[fyear] = keep
                f.close()

        return data


if __name__ == '__main__':
    pass
