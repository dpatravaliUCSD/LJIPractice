# using pandas and numpy for transformation
import pandas as pd
import numpy as np

filename = "sampleSets.csv"
data = pd.read_csv(filename)

# print the field names
print('Fields: ' + ', '.join(data.columns))

# transform last column
measurements = data.columns[-1]
data[measurements] = pd.to_numeric(data[measurements], errors='coerce')
data[measurements] = np.log2(data[measurements] / 5)

# new file witih transformed data
output_filename = "transformedSampleSets.csv"
data.to_csv(output_filename, index=False)
print("New file:", output_filename)