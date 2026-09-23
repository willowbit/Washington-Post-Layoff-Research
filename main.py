import getData, csv
import analyzeData

print("### Starting script! ###")

print("Retrieving data...")
people = getData.main()

print("Analyzing data...")
analyzeData.analyze(people)

print("Done! Look in results.txt for retrieved data.")