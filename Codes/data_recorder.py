import pandas as pd


class DataRecorder:

    '''
    Definition
    __________

    Class to record analysis data


    Class Attributes
    ________________

    file_path : string
        Directory to store the csv file in


    Methods
    _______

    record(file_name, dict_data) : Stores the recorded data into a csv file of the specified name, in the specified directory

    '''

    def __init__(self, file_path):
        '''
        Definition
        __________

        Initializes the DataRecorder class


        Parameters
        __________

        file_path : string
            Directory to store the csv file in

        '''

        self.file_path = file_path

    def record(self, file_name, dict_data):
        '''
        Definition
        __________

        Stores the recorded data into a csv file of the specified name, in the specified directory


        Parameters
        __________

        file_name : string
            Name of the CSV file to store the recorded data in

        dict_data : dictionary
            Recorded data for analysis

        '''

        df = pd.DataFrame.from_dict(dict_data)
        df.to_csv(self.file_path + file_name, index=None)
