from operations import *
from birdreport import *
from config import get_key

api_key = get_key()
regionCode = 'US-NJ'
days_back = 14

if __name__ == "__main__":
    
    data = operation.getData(api_key, regionCode, back=days_back)
    
    operation.storeData('doc', data)

    data = operation.retreiveData('doc')

    report = birdreport(data, regionCode, days_back)

    print(report.speciesObserved())

    print(report.speciesCount())
    
    report.plotObservations()

    report.plotCount()