import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename = "transformedSampleSets.csv"
data = pd.read_csv(filename)

# Column names and rows
print('Column names: ' + ', '.join(data.columns))
print("Number of rows: %d" % len(data))

# Get row by row index
def getRow(rowIndex):
    return data.iloc[rowIndex]

# Get column by column name
def getCol(colName):
    return data[colName]

# Get an entry by row index and column name
def getEntry(rowIndex, colName):
    return data.at[rowIndex, colName]

# Calculate percent change in antibody measurement for each patient of each vaccine type
def percentChangeAfter200Days(columnName):
    results = {}
    
    # Tranform 'Time' values to number
    data['Day'] = data['Time'].str.extract('(\d+)').astype(int)
    
    # Iterate through each different virus
    for virus in data['Virus'].unique():
        virusData = data[data['Virus'] == virus]
        virusResults = {}
        
        # Iterate through each subject for each virus
        for subject in virusData['Subject'].unique():
            subjectData = virusData[virusData['Subject'] == subject]
            
            # Day 0 and Day 200+ measurements
            day0Data = subjectData[subjectData['Time'] == 'Day0']
            dayOver200data = subjectData[subjectData['Day'] > 200].sort_values(by='Day').head(1)
            
            if not day0Data.empty and not dayOver200data.empty:
                day0measurement = day0Data[columnName].values[0]
                dayOver200measurement = dayOver200data[columnName].values[0]
                percentChange = ((dayOver200measurement - day0measurement) / day0measurement) * 100
                virusResults[subject] = percentChange
        
        results[virus] = virusResults
    
    return results

# Calculate mean, median, mode, and standard deviation of percent changes for each different virus
def calculateStatistics(columnName):
    percentChanges = percentChangeAfter200Days(columnName)
    statistics = {}
    
    for virus, subjects in percentChanges.items():
        percentChangeVals = list(subjects.values())
        
        # Used numpy and pandas for statistics calculations
        if percentChangeVals:
            mean = np.mean(percentChangeVals)
            median = np.median(percentChangeVals)
            mode = pd.Series(percentChangeVals).mode().iloc[0]
            stdDev = np.std(percentChangeVals)
            
            statistics[virus] = {
                'Mean': mean,
                'Median': median,
                'Mode': mode,
                'Standard Deviation': stdDev
            }
    
    return statistics

# Calculate log difference in antibody measurement for each patient of each vaccine type
def logDifferenceAfter200Days(columnName):
    results = {}
    
    # Needed 'Time' values as number
    data['Day'] = data['Time'].str.extract('(\d+)').astype(int)
    
    # Iterate through each subject for each virus
    for virus in data['Virus'].unique():
        virusData = data[data['Virus'] == virus]
        virusResults = {}
        
        for subject in virusData['Subject'].unique():
            subjectData = virusData[virusData['Subject'] == subject]
            
            # Day 0 and Day 200+ measurements
            day0Data = subjectData[subjectData['Time'] == 'Day0']
            dayOver200data = subjectData[subjectData['Day'] > 200].sort_values(by='Day').head(1)
            
            if not day0Data.empty and not dayOver200data.empty:
                day0measurement = day0Data[columnName].values[0]
                dayOver200measurement = dayOver200data[columnName].values[0]
                
                # To avoid log(0), introduced negligible constant (1e-9)
                if day0measurement > 0:
                    logRatio = np.log(dayOver200measurement + 1e-9) - np.log(day0measurement + 1e-9)
                else:
                    logRatio = np.nan
                
                virusResults[subject] = logRatio
        
        results[virus] = virusResults
    
    return results

# Calculate mean, median, mode, and standard deviation of log differences for each different virus
def calculateLogStatistics(columnName):
    logRatios = logDifferenceAfter200Days(columnName)
    statistics = {}
    
    for virus, subjects in logRatios.items():
        logRatioVals = [val for val in subjects.values() if not np.isnan(val)]
        
        # used numpy and pandas for statistics calculations
        if logRatioVals:
            mean = np.mean(logRatioVals)
            median = np.median(logRatioVals)
            mode = pd.Series(logRatioVals).mode().iloc[0]
            stdDev = np.std(logRatioVals)
            
            statistics[virus] = {
                'Mean': mean,
                'Median': median,
                'Mode': mode,
                'Standard Deviation': stdDev
            }
    
    return statistics


# Print results to check output in console
percentChanges = percentChangeAfter200Days('Measurement')

print("Percent change for each subject for each different virus: ")
for virus, subjects in percentChanges.items():
    print(f'Virus: {virus}')
    for subject, percent_change in subjects.items():
        print(f'  Subject: {subject}, Percent Change: {percent_change:.2f}%')

print()

statistics = calculateStatistics('Measurement')
logStatistics = calculateLogStatistics('Measurement')

print()
print ("Statistics for Percent Change: ")
print()

for virus, stats in statistics.items():
    print(f'Virus: {virus}')
    for stat_name, stat_value in stats.items():
        print(f'  {stat_name}: {stat_value:.2f}')

print()
print ("Statistics for Log Difference: ")
print()

for virus, stats in logStatistics.items():
    print(f'Virus: {virus}')
    for stat_name, stat_value in stats.items():
        print(f'  {stat_name}: {stat_value:.2f}')