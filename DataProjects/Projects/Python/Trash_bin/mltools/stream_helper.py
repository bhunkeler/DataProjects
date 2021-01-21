import math
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

class Stream_Helper():

    @staticmethod
    def volume(percentage):
        '''
        calculate the volume of the tras to define what size of car will be rewuired to empty

        argument:
        ---------
        percentage - sum of filling_level of all trash_bins

        return:
        -------
        volume  - volume in Cubic meters 
        '''
        value = percentage * ((0.37**2) * math.pi * 0.55)

        return value.round(2) 

    @staticmethod
    def volume_garbage_given_level(pdf, level):
        '''
        Get the volume of trash bin (filling level > ) data for a given time window

        arguments:
        ----------
        df_sql - contains all trash bin information 
        time   - data and time (e.g. '2021-01-10 08:00:00')

        return:
        -------
        pdf - return a dataframe for given level threshold 
        '''        

        levels = pdf[pdf['filling_level'] > level]
        total_percentage = levels['filling_level'].sum()
        
        return Stream_Helper.volume(total_percentage / 100)

    @staticmethod
    def trash_bin_data_at_time(df_sql, time):
        '''
        Get the trash bin data for a given time window

        arguments:
        ----------
        df_sql - contains all trash bin information 
        time   - data and time (e.g. '2021-01-10 08:00:00')

        return:
        -------
        pdf - return a dataframe given the data of the requested hour
        '''
        
        # filling level - Filter for a window end time and convert to pandas
        df_sql_time = df_sql.withColumn("window", df_sql.window.end).where(df_sql.window.end == time)
        pdf = df_sql_time.toPandas()
        return pdf

    @staticmethod
    def max_filling_level(df_sql):
        '''
        Retrieve the max filling level of all trash bins.

        arguments:
        ----------
        df_sql - contains all trash bin information 

        return:
        -------
        max_level - return the information for the trash bin with the max filling level
        '''
        
        df = df_sql.toPandas()
        dd = df[df['filling_level'] > 0]
        dd[dd['filling_level'] == dd['filling_level'].max()]

        df_min_max = df_sql.toPandas()
        dd = df_min_max[df_min_max['filling_level'] > 0]
        max_level = dd[dd['filling_level'] == dd['filling_level'].max()]        

        return max_level        

    @staticmethod
    def IoT_hw_failure(pdf):
        '''
        Evaluate HW failures within an 1hour time window

        arguments:
        ----------
        pdf  - pandas dataframe containing IoT state in given window

        return:
        -------
        IoT state - returns the IoT state for locations where filure exists
        '''        

        return pdf[pdf['maintenance'] == True]

    @staticmethod
    def mean_filling_level(pdf):
        '''
        Calculate the mean filling level of all trashbins within an 1hour time window

        arguments:
        ----------
        pdf  - pandas dataframe containing location and filling level in given window

        return:
        -------
        mean_filling_level - average filling level of all trash bins in a given 1hour window
        '''

        # claculate average filling level 
        mean_filling_level = pdf['filling_level'].mean()

        return mean_filling_level.round(2)

    @staticmethod
    def plot_fill_level(df):
        '''
        Plot the filling levels for respective locations

        arguments:
        ----------
        df  - dataframe containing location and filling level

        return:
        -------
        plot
        '''

        blueish   = '#3891BC'
        redish    = '#E63323'
        yellowish = '#3891BC'    
        
        plt.figure()
        plt.subplots(ncols=1, figsize=(10, 6)) 
        sns.set_style('darkgrid')

        conditional_colors = np.where(df['maintenance'] == True, 'y', np.where(df['filling_level'] >= 50, redish, blueish))
        sns.barplot(x = 'city', y = 'filling_level', data = df, palette = conditional_colors)
        plt.xlabel('locations', fontsize = 14)
        plt.ylabel('filling level', fontsize = 14)
        plt.title('Filling Level of Trash bins', fontsize = 18)
        plt.xticks(rotation=80)
        plt.show()

    @staticmethod
    def stream_dashboard(df, avg, vol, maint, any = None):
        '''
        Create a dashboard from stream data reflecting plots for 6h of data. We also show 
        a IoT Component state, average filling level, trash bin volue of trash bins containing >50% of filling.

        arguments:
        ----------
        df  -     containing all the streamed data for 24h
        avg -     containing the precalculated average filling level in a given window (1h)
        vol -     total volume of garbage in a given hour (only trash bin filling > 50% ) 
        maint -   IoT component state, which requires maintenance

        return:
        -------
        dashboard - plot

        '''

        sns.set_style("darkgrid")
        blueish   = '#3891BC'
        redish    = '#E63323'
        yellowish = '#3891BC'    


        explode = (0, 0.1) 
        fig, ax = plt.subplots(figsize=(15, 8), ncols=3, nrows=3)

        left   =  0.125  # the left side of the subplots of the figure
        right  =  0.9    # the right side of the subplots of the figure
        bottom =  0.1    # the bottom of the subplots of the figure
        top    =  0.9    # the top of the subplots of the figure
        wspace =  0.7    # the amount of width reserved for blank space between subplots
        hspace =  0.7    # the amount of height reserved for white space between subplots

        # This function actually adjusts the sub plots using the above paramters
        plt.subplots_adjust(
        left    =  left, 
        bottom  =  bottom, 
        right   =  right, 
        top     =  top, 
        wspace  =  wspace, 
        hspace  =  hspace
        )

        # The amount of space above titles
        y_title_margin = 1.0

        plt.suptitle("Trash bin Dasboard", y = 1.0, fontsize=12)

        ax[0][0].set_title("2021-01-10 08:00", y = y_title_margin)
        ax[0][1].set_title("2021-01-10 09:00", y = y_title_margin)
        ax[0][2].set_title("2021-01-10 10:00", y = y_title_margin)

        ax[1][0].set_title("2021-01-10 11:00", y = y_title_margin)
        ax[1][1].set_title("2021-01-10 12:00", y = y_title_margin)
        ax[1][2].set_title("2021-01-10 13:00", y = y_title_margin)

        ax[0][0].set_xticklabels(df[0]['city'],Rotation=80, fontsize = 8)
        ax[0][1].set_xticklabels(df[1]['city'],Rotation=80, fontsize = 8)
        ax[0][2].set_xticklabels(df[2]['city'],Rotation=80, fontsize = 8)

        ax[1][0].set_xticklabels(df[3]['city'],Rotation=80, fontsize = 8)
        ax[1][1].set_xticklabels(df[4]['city'],Rotation=80, fontsize = 8)
        ax[1][2].set_xticklabels(df[5]['city'],Rotation=80, fontsize = 8)

        # conditional_colors = np.where(df[0]['maintenance'] == True, 'y', np.where(df[0]['filling_level'] >= 50, redish, blueish))
        # ax[0][0].bar('city', 'filling_level', data = df[0], palette = conditional_colors)
        
        ax[0][0].bar('city', 'filling_level', data = df[0])
        ax[0][1].bar('city', 'filling_level', data = df[1])
        ax[0][2].bar('city', 'filling_level', data = df[2])
    
        ax[1][0].bar('city', 'filling_level', data = df[3])
        ax[1][1].bar('city', 'filling_level', data = df[4])
        ax[1][2].bar('city', 'filling_level', data = df[5])

        ax[0][0].legend(['08:00', 2014, 2015])
        ax[0][1].legend(['09:00', 2019, 2011])
        ax[0][2].legend(['10:00', 2014, 2015])

        ax[1][0].legend(['11:00', 2014, 2015])
        ax[1][1].legend(['12:00', 2014, 2015])
        ax[1][2].legend(['13:00', 2014, 2015])

        # Set all labels on the row axis of subplots data
        # ax[0][0].set_xlabel("location")
        # ax[0][1].set_xlabel("location")
        # ax[0][2].set_xlabel("location")

        ax[1][0].set_xlabel("location")
        ax[1][1].set_xlabel("location")
        ax[1][2].set_xlabel("location")

        # Set all labels on the row axis of subplots data
        ax[0][0].set_ylabel("Filling_level")
        ax[0][1].set_ylabel("Filling_level")
        ax[0][2].set_ylabel("Filling_level")

        ax[1][0].set_ylabel("Filling_level")
        ax[1][1].set_ylabel("Filling_level")
        ax[1][2].set_ylabel("Filling_level")

        # ax[0][0].grid(b=True, linewidth=0.5, color=)
        ax[0][0].grid(color='gray', linestyle='-', linewidth=0.5)
        ax[0][0].axhline(y=50, color='red', linestyle='--', linewidth=1.5)
        ax[0][1].axhline(y=50, color='red', linestyle='--', linewidth=1.5)
        ax[0][2].axhline(y=50, color='red', linestyle='--', linewidth=1.5)
        ax[1][0].axhline(y=50, color='red', linestyle='--', linewidth=1.5)
        ax[1][1].axhline(y=50, color='red', linestyle='--', linewidth=1.5)
        ax[1][2].axhline(y=50, color='red', linestyle='--', linewidth=1.5)

        ax[2][0].axis("off")
        ax[2][1].axis("off")
        ax[2][2].axis("off")

        ax[2][0].text(0, 0.8, 'Volume: ', fontsize=12, fontweight='bold' )    
        ax[2][0].text(0, 0.7, '08:00 : ' + str(vol[0]) + ' $m^3$', fontsize=12)
        ax[2][0].text(0, 0.6, '09:00 : ' + str(vol[1]) + ' $m^3$', fontsize=12)
        ax[2][0].text(0, 0.5, '10:00 : ' + str(vol[2]) + ' $m^3$', fontsize=12)
        ax[2][0].text(0, 0.4, '11:00 : ' + str(vol[3]) + ' $m^3$', fontsize=12)
        ax[2][0].text(0, 0.3, '12:00 : ' + str(vol[4]) + ' $m^3$', fontsize=12)
        ax[2][0].text(0, 0.2, '13:00 : ' + str(vol[5]) + ' $m^3$', fontsize=12)
        
        ax[2][1].text(0, 0.8, 'Average Filling level: ', fontsize=12, fontweight='bold' )    
        ax[2][1].text(0, 0.7, '08:00 : ' + str(avg[0]) + ' %', fontsize=12)
        ax[2][1].text(0, 0.6, '09:00 : ' + str(avg[1]) + ' %', fontsize=12)
        ax[2][1].text(0, 0.5, '10:00 : ' + str(avg[2]) + ' %', fontsize=12)
        ax[2][1].text(0, 0.4, '11:00 : ' + str(avg[3]) + ' %', fontsize=12)
        ax[2][1].text(0, 0.3, '12:00 : ' + str(avg[4]) + ' %', fontsize=12)
        ax[2][1].text(0, 0.2, '13:00 : ' + str(avg[5]) + ' %', fontsize=12)

        hw_failure = Stream_Helper.check_hw_failure(maint)

        ax[2][2].text(0, 0.8, 'Maintenance: ', fontsize=12, fontweight='bold' )    
        ax[2][2].text(0, 0.7, '08:00 : ' + str(hw_failure[0]), fontsize=12) 
        ax[2][2].text(0, 0.6, '09:00 : ' + str(hw_failure[1]), fontsize=12)
        ax[2][2].text(0, 0.5, '10:00 : ' + str(hw_failure[2]), fontsize=12)
        ax[2][2].text(0, 0.4, '11:00 : ' + str(hw_failure[3]), fontsize=12)
        ax[2][2].text(0, 0.3, '12:00 : ' + str(hw_failure[4]), fontsize=12)
        ax[2][2].text(0, 0.2, '13:00 : ' + str(hw_failure[5]), fontsize=12)

        plt.show()

    @staticmethod
    def check_hw_failure(maintenance):
        '''
        Check for hardware failure of IoT components and returns a list of failed components

        arguments:
        ----------
        maintenance - list of IoT which need maintenance

        return:
        -------
        hw_failure  - list of location concatenated per (hour)
        '''

        hw_failure = []
        failure = ''

        for i in range(len(maintenance)):
            if maintenance[i] == []:
                hw_failure.append(failure)
            else:
                hw_failure.append(','.join(maintenance[i]))
        
        return hw_failure

    @staticmethod
    def time_calc():
        '''
        just an intermediate helper function to calc time 
        '''
        import time 

        seconds = 1610234100  # Initial time in seconds
        for i in range(0,24):
            local_time = time.ctime(seconds)
            print('Local time: {0} seconds: {1}'.format(local_time, seconds))	
            seconds += 3600


if __name__ == '__main__':
    import pandas as pd

    hw_failure = []
    failure = ''

    data = {'city':['Winterthur', 'Zurich', 'Bern', 'Luzern'],
        'filling_level':[20, 44, 56, 72], 'maintenance': [False, True, False, False]}

    mn0 = []
    mn1 = ['D', 'E', 'F']
    maint = [mn0, mn0, mn0, mn1, mn1, mn1]

    hw_failure = Stream_Helper.check_hw_failure(maint)  

    print(hw_failure[0])
    print(hw_failure[3])
    
    # Create DataFrame
    df1 = pd.DataFrame(data)
    df2 = pd.DataFrame(data)
    df3 = pd.DataFrame(data)
    df4 = pd.DataFrame(data)
    df5 = pd.DataFrame(data)
    df6 = pd.DataFrame(data)

    df = [df1, df2, df3, df4, df5, df6]
    avg = [23, 34, 45, 56, 67, 78]
    vol = [0.22, 0.34, 0.45, 0.48, 0.55, 0.58]
    maint = [mn0, mn0, mn0, mn1, mn1, mn1]
    any = 'any'

    Stream_Helper.stream_dashboard(df, avg, vol, maint)

    end = 'end'


