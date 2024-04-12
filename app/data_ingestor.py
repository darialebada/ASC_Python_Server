""" data_ingestor.py """
import csv

class DataIngestor:
    """ DataIngestor class - edit data from csv file """
    def __init__(self, csv_path: str):
        """  Read data from csv file and store it in a list of dictionaries """
        self.list_data = []
        with open(csv_path, mode = 'r', encoding='utf-8') as f:
            data = csv.DictReader(f)
            for row in data:
                # get only necessary data for tasks
                dict_data_ingestor = {"Location" : row['LocationDesc'],
                        "Question" : row['Question'],
                        "Data_Value" : row['Data_Value'],
                        "Stratification" : row['Stratification1'],
                        "Stratification_Category" : row['StratificationCategory1'],
                        "Total" : row['Total'],
                        "Age (years)" : row['Age(years)'],
                        "Education" : row['Education'], 
                        "Gender" : row['Gender'],
                        "Income" : row['Income'],
                        "Race/Ethnicity" : row['Race/Ethnicity']}
                self.list_data.append(dict_data_ingestor)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of' +
            'moderate-intensity aerobic physical activity or 75 minutes a' +
            'week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of' +
            'moderate-intensity aerobic physical activity or 75 minutes' +
            'a week of vigorous-intensity aerobic physical activity and' +
            'engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of' +
            'moderate-intensity aerobic physical activity or 150 minutes' +
            'a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on' +
            '2 or more days a week',
        ]
